from get_board import get_scenario_board
from rewards import reward_function
from helper import pretty_print_board

import chess
import random
import chess.engine
import numpy as np
import os
import pickle
from copy import deepcopy
import colorama
from colorama import Fore, Style
colorama.init(autoreset=True)

import matplotlib.pyplot as plt


class QLearningChess:
    def __init__(
        self,
        alpha=0.05,
        gamma=0.95,
        epsilon=1.0,
        epsilon_min=0.0,
        epsilon_decay_after_win=0.003,
        load_existing=False,
        qtable_file="Q_table.pkl",
        stockfish_path="/usr/games/stockfish",
        train_as="white",
        stockfish_skill=0
    ):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_initial = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay_after_win
        self.qtable_file = qtable_file
        self.train_as = train_as.lower()
        assert self.train_as in ["white", "black"], "train_as must be 'white' or 'black'"
        
        self.wins_before_decay = 0

        self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
        self.engine.configure({"Skill Level": stockfish_skill})
        print(f"🤖 Stockfish initialized (Skill={stockfish_skill})")

        # Create agents directory if it doesn't exist
        os.makedirs('agents', exist_ok=True)
        
        # Update qtable_file path to use agents folder
        if not qtable_file.startswith('agents/'):
            self.qtable_file = os.path.join('agents', qtable_file)
        else:
            self.qtable_file = qtable_file

        # Single shared Q-table used by both agents
        if load_existing and os.path.exists(self.qtable_file):
            print(f"🔁 Loading existing Q-table from {self.qtable_file}...")
            self.load(self.qtable_file)
        else:
            print("🆕 Starting new Q-table...")
            self.Q_table = {}

    def _simplify_state(self, board):
        """Use simplified FEN without halfmove/fullmove counters"""
        fen = board.fen()
        parts = fen.split(' ')
        return ' '.join(parts[:4])

    def _get_Q(self, state, action):
        return self.Q_table.get((state, action), 0.0)

    def _set_Q(self, state, action, value):
        self.Q_table[(state, action)] = value

    def _max_Q_value(self, board):
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return 0.0
        state = self._simplify_state(board)
        return max(self._get_Q(state, move.uci()) for move in legal_moves)

    def _epsilon_greedy_action(self, board):
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None
        if np.random.rand() < self.epsilon:
            return random.choice(legal_moves)
        state = self._simplify_state(board)
        q_values = [self._get_Q(state, move.uci()) for move in legal_moves]
        max_q = max(q_values)
        best_actions = [move for move, q in zip(legal_moves, q_values) if q == max_q]
        return random.choice(best_actions)

    def train(self, episodes=1000, custom_fens=None, verbose=False):
        if isinstance(custom_fens, str):
            custom_fens = [custom_fens]
        if not custom_fens:
            custom_fens = [chess.STARTING_FEN]

        # Convert Board objects to FEN strings if needed
        processed_fens = []
        for item in custom_fens:
            if isinstance(item, chess.Board):
                processed_fens.append(item.fen())
            elif isinstance(item, str):
                processed_fens.append(item)
            else:
                raise ValueError(f"Invalid type in custom_fens: {type(item)}")
        
        custom_fens = processed_fens

        print(f"\n🏁 Starting training for {episodes} episodes ({self.train_as.capitalize()} vs Stockfish)")
        print(f"   α={self.alpha}, γ={self.gamma}, ε={self.epsilon}\n")
        print(f"   Q-table size at start: {len(self.Q_table)} entries")

        wins, losses, draws = 0, 0, 0

        # Track metrics per episode
        self.episode_rewards = []
        self.episode_wins = []
        self.episode_losses = []
        self.episode_draws = []
        self.episode_lengths = []
        self.episode_epsilon = []  # NEW: Track epsilon decay
        self.episode_qtable_size = []  # NEW: Track Q-table growth

        for ep in range(1, episodes + 1):
            board = chess.Board(random.choice(custom_fens))
            done = False
            total_reward = 0
            moves_count = 0

            while not done and moves_count < 150:
                if (board.turn == chess.WHITE and self.train_as == "white") or \
                   (board.turn == chess.BLACK and self.train_as == "black"):

                    state = self._simplify_state(board)
                    action = self._epsilon_greedy_action(board)
                    if action is None:
                        break

                    # Execute agent's move
                    board.push(action)
                    moves_count += 1

                    if verbose and ep % 500 == 0:
                        print(Fore.CYAN + f"[Agent] {action.uci()}")

                    # Check if game over after agent's move
                    if board.is_game_over():
                        done = True
                        result = board.result()
                        
                        # Assign terminal reward based on result
                        if (result == "1-0" and self.train_as == "white") or \
                           (result == "0-1" and self.train_as == "black"):
                            terminal_reward = 100
                            wins += 1
                        elif result == "1/2-1/2":
                            terminal_reward = -20
                            draws += 1
                        else:
                            terminal_reward = -100
                            losses += 1
                        
                        self._set_Q(state, action.uci(), terminal_reward)
                        total_reward += terminal_reward
                        break

                    # Simulate opponent's move in copy
                    env_copy = deepcopy(board)
                    opp_result = self.engine.play(env_copy, chess.engine.Limit(depth=1))
                    opp_move = opp_result.move
                    
                    if opp_move is None:
                        maxQfuture = 0.0
                    else:
                        env_copy.push(opp_move)
                        
                        if env_copy.is_game_over():
                            result_copy = env_copy.result()
                            if (result_copy == "1-0" and self.train_as == "white") or \
                               (result_copy == "0-1" and self.train_as == "black"):
                                maxQfuture = 100
                            elif result_copy == "1/2-1/2":
                                maxQfuture = -20
                            else:
                                maxQfuture = -100
                        else:
                            maxQfuture = self._max_Q_value(env_copy)

                    # Intermediate reward
                    intermediate_reward = reward_function(board, action, board.turn)
                    total_reward += intermediate_reward

                    # Q-learning update
                    Qold = self._get_Q(state, action.uci())
                    Qnew = Qold + self.alpha * (intermediate_reward + self.gamma * maxQfuture - Qold)
                    self._set_Q(state, action.uci(), Qnew)

                    # Execute opponent's move on real board
                    if opp_move is not None:
                        board.push(opp_move)
                        moves_count += 1
                        if verbose and ep % 500 == 0:
                            print(Fore.LIGHTBLACK_EX + f"[Stockfish] {opp_move.uci()}")

                else:
                    # Stockfish moves first
                    result = self.engine.play(board, chess.engine.Limit(depth=1))
                    stockfish_move = result.move
                    if stockfish_move is None:
                        break
                    board.push(stockfish_move)
                    moves_count += 1
                    if verbose and ep % 500 == 0:
                        print(Fore.LIGHTBLACK_EX + f"[Stockfish] {stockfish_move.uci()}")

                # Check game over
                if board.is_game_over():
                    result = board.result()
                    done = True
                    if (result == "1-0" and self.train_as == "white") or \
                       (result == "0-1" and self.train_as == "black"):
                        wins += 1
                    elif result == "1/2-1/2":
                        draws += 1
                    else:
                        losses += 1
                    break

            # Track metrics per episode
            self.episode_rewards.append(total_reward)
            self.episode_wins.append(wins)
            self.episode_losses.append(losses)
            self.episode_draws.append(draws)
            self.episode_lengths.append(moves_count)
            self.episode_epsilon.append(self.epsilon)  # NEW
            self.episode_qtable_size.append(len(self.Q_table))  # NEW

            # Epsilon decay after first win
            if wins > self.wins_before_decay:
                if self.epsilon > self.epsilon_min:
                    self.epsilon -= self.epsilon_decay
                    self.epsilon = max(self.epsilon, self.epsilon_min)

            if ep % 100 == 0 or ep == episodes:
                avg_length = np.mean(self.episode_lengths[-100:]) if self.episode_lengths else 0
                win_rate = wins / ep if ep > 0 else 0
                print(Fore.YELLOW + f"Ep {ep}/{episodes} | ε={self.epsilon:.3f} | W={wins} L={losses} D={draws} | WR={win_rate:.1%} | AvgLen={avg_length:.1f}")

        self.last_stats = (wins, losses, draws)
        print(Fore.GREEN + f"✅ Training done. Wins={wins}, Losses={losses}, Draws={draws}")
        print(f"   Q-table size at end: {len(self.Q_table)} entries")
        self.save()

    def save(self):
        with open(self.qtable_file, "wb") as f:
            pickle.dump(self.Q_table, f)
        print(f"💾 Saved Q-table to {self.qtable_file} ({len(self.Q_table)} entries)")

    def load(self, qtable_file=None):
        qtable_file = qtable_file or self.qtable_file
        if os.path.exists(qtable_file):
            with open(qtable_file, "rb") as f:
                self.Q_table = pickle.load(f)
            print(f"✅ Loaded Q-table from {qtable_file} ({len(self.Q_table)} entries)")
        else:
            print(f"⚠️  File {qtable_file} not found, starting with empty Q-table")
            self.Q_table = {}

    def __del__(self):
        try:
            self.engine.quit()
        except:
            pass


def plot_results(agent_white, agent_black, scenario_num):
    """Plot training results for both agents - ALL 12 PLOTS (6 original + 6 new)"""
    # Create images directory if it doesn't exist
    os.makedirs('images', exist_ok=True)
    
    fig = plt.figure(figsize=(20, 16))
    gs = fig.add_gridspec(4, 3, hspace=0.35, wspace=0.3)
    fig.suptitle(f'Training Results - Scenario {scenario_num}', fontsize=18, fontweight='bold')

    window = 100

    # ====== ROW 1: ORIGINAL PLOTS ======
    
    # Plot 1: Rewards (ORIGINAL - with raw + smoothed)
    ax1 = fig.add_subplot(gs[0, 0])
    if agent_white:
        ax1.plot(agent_white.episode_rewards, color='blue', alpha=0.3, label='White (raw)')
        if len(agent_white.episode_rewards) > window:
            moving_avg = np.convolve(agent_white.episode_rewards, np.ones(window)/window, mode='valid')
            ax1.plot(range(window-1, len(agent_white.episode_rewards)), moving_avg, color='blue', linewidth=2)
    
    if agent_black:
        ax1.plot(agent_black.episode_rewards, color='red', alpha=0.3, label='Black (raw)')
        if len(agent_black.episode_rewards) > window:
            moving_avg = np.convolve(agent_black.episode_rewards, np.ones(window)/window, mode='valid')
            ax1.plot(range(window-1, len(agent_black.episode_rewards)), moving_avg, color='red', linewidth=2)
    
    ax1.set_xlabel("Episodes", fontsize=10)
    ax1.set_ylabel("Total Reward", fontsize=10)
    ax1.set_title("Reward per Episode", fontsize=11, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Plot 2: Cumulative Wins (ORIGINAL)
    ax2 = fig.add_subplot(gs[0, 1])
    if agent_white:
        ax2.plot(agent_white.episode_wins, color='blue', linewidth=2, label='White')
    if agent_black:
        ax2.plot(agent_black.episode_wins, color='red', linewidth=2, label='Black')
    ax2.set_xlabel("Episodes", fontsize=10)
    ax2.set_ylabel("Cumulative Wins", fontsize=10)
    ax2.set_title("Wins Over Time", fontsize=11, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Plot 3: Cumulative Win Rate (ORIGINAL)
    ax3 = fig.add_subplot(gs[0, 2])
    if agent_white and len(agent_white.episode_wins) > 0:
        episodes_white = list(range(1, len(agent_white.episode_wins) + 1))
        win_rate_white = [w / e for w, e in zip(agent_white.episode_wins, episodes_white)]
        ax3.plot(win_rate_white, color='blue', linewidth=2, label='White')
    
    if agent_black and len(agent_black.episode_wins) > 0:
        episodes_black = list(range(1, len(agent_black.episode_wins) + 1))
        win_rate_black = [w / e for w, e in zip(agent_black.episode_wins, episodes_black)]
        ax3.plot(win_rate_black, color='red', linewidth=2, label='Black')
    
    ax3.set_xlabel("Episodes", fontsize=10)
    ax3.set_ylabel("Win Rate", fontsize=10)
    ax3.set_title("Win Rate Over Time (Cumulative)", fontsize=11, fontweight='bold')
    ax3.set_ylim([0, 1])
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # ====== ROW 2: ORIGINAL PLOTS (continued) ======

    # Plot 4: Episode Lengths (ORIGINAL - with raw + smoothed)
    ax4 = fig.add_subplot(gs[1, 0])
    if agent_white:
        ax4.plot(agent_white.episode_lengths, color='blue', alpha=0.3, label='White (raw)')
        if len(agent_white.episode_lengths) > window:
            moving_avg = np.convolve(agent_white.episode_lengths, np.ones(window)/window, mode='valid')
            ax4.plot(range(window-1, len(agent_white.episode_lengths)), moving_avg, color='blue', linewidth=2)
    
    if agent_black:
        ax4.plot(agent_black.episode_lengths, color='red', alpha=0.3, label='Black (raw)')
        if len(agent_black.episode_lengths) > window:
            moving_avg = np.convolve(agent_black.episode_lengths, np.ones(window)/window, mode='valid')
            ax4.plot(range(window-1, len(agent_black.episode_lengths)), moving_avg, color='red', linewidth=2)
    
    ax4.set_xlabel("Episodes", fontsize=10)
    ax4.set_ylabel("Moves per Episode", fontsize=10)
    ax4.set_title("Episode Length", fontsize=11, fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # Plot 5: Cumulative Draws (ORIGINAL)
    ax5 = fig.add_subplot(gs[1, 1])
    if agent_white:
        ax5.plot(agent_white.episode_draws, color='blue', linewidth=2, label='White')
    if agent_black:
        ax5.plot(agent_black.episode_draws, color='red', linewidth=2, label='Black')
    ax5.set_xlabel("Episodes", fontsize=10)
    ax5.set_ylabel("Cumulative Draws", fontsize=10)
    ax5.set_title("Draws Over Time", fontsize=11, fontweight='bold')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # Plot 6: Cumulative Draw Rate (ORIGINAL)
    ax6 = fig.add_subplot(gs[1, 2])
    if agent_white and len(agent_white.episode_draws) > 0:
        episodes_white = list(range(1, len(agent_white.episode_draws) + 1))
        draw_rate_white = [d / e for d, e in zip(agent_white.episode_draws, episodes_white)]
        ax6.plot(draw_rate_white, color='blue', linewidth=2, label='White')
    
    if agent_black and len(agent_black.episode_draws) > 0:
        episodes_black = list(range(1, len(agent_black.episode_draws) + 1))
        draw_rate_black = [d / e for d, e in zip(agent_black.episode_draws, episodes_black)]
        ax6.plot(draw_rate_black, color='red', linewidth=2, label='Black')
    
    ax6.set_xlabel("Episodes", fontsize=10)
    ax6.set_ylabel("Draw Rate", fontsize=10)
    ax6.set_title("Draw Rate Over Time (Cumulative)", fontsize=11, fontweight='bold')
    ax6.set_ylim([0, 1])
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    # ====== ROW 3: NEW PLOTS ======

    # Plot 7: Rolling Win Rate (NEW)
    ax7 = fig.add_subplot(gs[2, 0])
    
    def calculate_rolling_win_rate(wins_list, window=100):
        """Calculate win rate over rolling window"""
        rolling_rates = []
        for i in range(len(wins_list)):
            start_idx = max(0, i - window + 1)
            wins_in_window = wins_list[i] - (wins_list[start_idx-1] if start_idx > 0 else 0)
            episodes_in_window = min(i + 1, window)
            rolling_rates.append(wins_in_window / episodes_in_window if episodes_in_window > 0 else 0)
        return rolling_rates
    
    if agent_white and len(agent_white.episode_wins) > 0:
        rolling_wr = calculate_rolling_win_rate(agent_white.episode_wins, window)
        ax7.plot(rolling_wr, color='blue', linewidth=2, label='White')
    
    if agent_black and len(agent_black.episode_wins) > 0:
        rolling_wr = calculate_rolling_win_rate(agent_black.episode_wins, window)
        ax7.plot(rolling_wr, color='red', linewidth=2, label='Black')
    
    ax7.set_xlabel("Episodes", fontsize=10)
    ax7.set_ylabel("Win Rate", fontsize=10)
    ax7.set_title(f"Rolling Win Rate (last {window} eps)", fontsize=11, fontweight='bold')
    ax7.set_ylim([0, 1])
    ax7.legend()
    ax7.grid(True, alpha=0.3)

    # Plot 8: Rolling Loss Rate (NEW)
    ax8 = fig.add_subplot(gs[2, 1])
    
    def calculate_rolling_loss_rate(losses_list, window=100):
        """Calculate loss rate over rolling window"""
        rolling_rates = []
        for i in range(len(losses_list)):
            start_idx = max(0, i - window + 1)
            losses_in_window = losses_list[i] - (losses_list[start_idx-1] if start_idx > 0 else 0)
            episodes_in_window = min(i + 1, window)
            rolling_rates.append(losses_in_window / episodes_in_window if episodes_in_window > 0 else 0)
        return rolling_rates
    
    if agent_white and len(agent_white.episode_losses) > 0:
        rolling_lr = calculate_rolling_loss_rate(agent_white.episode_losses, window)
        ax8.plot(rolling_lr, color='blue', linewidth=2, label='White')
    
    if agent_black and len(agent_black.episode_losses) > 0:
        rolling_lr = calculate_rolling_loss_rate(agent_black.episode_losses, window)
        ax8.plot(rolling_lr, color='red', linewidth=2, label='Black')
    
    ax8.set_xlabel("Episodes", fontsize=10)
    ax8.set_ylabel("Loss Rate", fontsize=10)
    ax8.set_title(f"Rolling Loss Rate (last {window} eps)", fontsize=11, fontweight='bold')
    ax8.set_ylim([0, 1])
    ax8.legend()
    ax8.grid(True, alpha=0.3)

    # Plot 9: Rolling Draw Rate (NEW)
    ax9 = fig.add_subplot(gs[2, 2])
    
    def calculate_rolling_draw_rate(draws_list, window=100):
        """Calculate draw rate over rolling window"""
        rolling_rates = []
        for i in range(len(draws_list)):
            start_idx = max(0, i - window + 1)
            draws_in_window = draws_list[i] - (draws_list[start_idx-1] if start_idx > 0 else 0)
            episodes_in_window = min(i + 1, window)
            rolling_rates.append(draws_in_window / episodes_in_window if episodes_in_window > 0 else 0)
        return rolling_rates
    
    if agent_white and len(agent_white.episode_draws) > 0:
        rolling_dr = calculate_rolling_draw_rate(agent_white.episode_draws, window)
        ax9.plot(rolling_dr, color='blue', linewidth=2, label='White')
    
    if agent_black and len(agent_black.episode_draws) > 0:
        rolling_dr = calculate_rolling_draw_rate(agent_black.episode_draws, window)
        ax9.plot(rolling_dr, color='red', linewidth=2, label='Black')
    
    ax9.set_xlabel("Episodes", fontsize=10)
    ax9.set_ylabel("Draw Rate", fontsize=10)
    ax9.set_title(f"Rolling Draw Rate (last {window} eps)", fontsize=11, fontweight='bold')
    ax9.set_ylim([0, 1])
    ax9.legend()
    ax9.grid(True, alpha=0.3)

    # ====== ROW 4: NEW PLOTS (continued) ======

    # Plot 10: Epsilon Decay (NEW)
    ax10 = fig.add_subplot(gs[3, 0])
    if agent_white and len(agent_white.episode_epsilon) > 0:
        ax10.plot(agent_white.episode_epsilon, color='blue', linewidth=2, label='White')
    
    if agent_black and len(agent_black.episode_epsilon) > 0:
        ax10.plot(agent_black.episode_epsilon, color='red', linewidth=2, label='Black')
    
    ax10.set_xlabel("Episodes", fontsize=10)
    ax10.set_ylabel("Epsilon (ε)", fontsize=10)
    ax10.set_title("Exploration Rate (ε) Decay", fontsize=11, fontweight='bold')
    ax10.legend()
    ax10.grid(True, alpha=0.3)

    # Plot 11: Q-table Growth (NEW)
    ax11 = fig.add_subplot(gs[3, 1])
    if agent_white and len(agent_white.episode_qtable_size) > 0:
        ax11.plot(agent_white.episode_qtable_size, color='blue', linewidth=2, label='White')
    
    if agent_black and len(agent_black.episode_qtable_size) > 0:
        ax11.plot(agent_black.episode_qtable_size, color='red', linewidth=2, label='Black')
    
    ax11.set_xlabel("Episodes", fontsize=10)
    ax11.set_ylabel("Q-table Size (entries)", fontsize=10)
    ax11.set_title("Q-table Growth Over Time", fontsize=11, fontweight='bold')
    ax11.legend()
    ax11.grid(True, alpha=0.3)

    # Plot 12: Reward Variance (Convergence Indicator) (NEW)
    ax12 = fig.add_subplot(gs[3, 2])
    
    def calculate_rolling_variance(data, window=100):
        """Calculate rolling variance"""
        variances = []
        for i in range(len(data)):
            start_idx = max(0, i - window + 1)
            window_data = data[start_idx:i+1]
            variances.append(np.var(window_data) if len(window_data) > 1 else 0)
        return variances
    
    if agent_white and len(agent_white.episode_rewards) > window:
        reward_var = calculate_rolling_variance(agent_white.episode_rewards, window)
        ax12.plot(reward_var, color='blue', linewidth=2, label='White')
    
    if agent_black and len(agent_black.episode_rewards) > window:
        reward_var = calculate_rolling_variance(agent_black.episode_rewards, window)
        ax12.plot(reward_var, color='red', linewidth=2, label='Black')
    
    ax12.set_xlabel("Episodes", fontsize=10)
    ax12.set_ylabel("Reward Variance", fontsize=10)
    ax12.set_title(f"Reward Variance ({window}-ep window)", fontsize=11, fontweight='bold')
    ax12.legend()
    ax12.grid(True, alpha=0.3)

    plt.tight_layout()
    filename = f"images/training_results_scenario_{scenario_num}.png"
    plt.savefig(filename, dpi=150)
    print(f"\n📊 Plots saved to {filename}")
    plt.close()


def train_scenario(scenario_num, num_positions=50, episodes=5000):
    """Train both White and Black agents for a given scenario using shared Q-table"""
    print(f"\n{'='*60}")
    print(f"SCENARIO {scenario_num}")
    print(f"{'='*60}")
    
    # Generate training positions
    print(f"\n📋 Generating {num_positions} training positions for Scenario {scenario_num}...")
    custom_boards = get_scenario_board(scenario_num, num_positions)
    custom_scenarios = [board.fen() for board in custom_boards]
    print(f"✅ Generated {len(custom_scenarios)} positions\n")

    # Single Q-table file for this scenario (will be saved in agents folder)
    qtable_file = f"Q_table_scenario_{scenario_num}.pkl"

    # Delete old Q-table for this scenario to start fresh
    qtable_path = os.path.join('agents', qtable_file)
    if os.path.exists(qtable_path):
        os.remove(qtable_path)
        print(f"🗑️  Deleted old {qtable_path}")

    # Train White agent
    print("\n" + "="*60)
    print("🎯 TRAINING WHITE AGENT")
    print("="*60 + "\n")
    
    agent_white = QLearningChess(
        alpha=0.05,
        gamma=0.95,
        epsilon=1.0,
        epsilon_min=0.0,
        epsilon_decay_after_win=0.003,
        load_existing=False,
        qtable_file=qtable_file,
        stockfish_path="/usr/games/stockfish",
        train_as="white",
        stockfish_skill=0
    )
    agent_white.train(episodes=episodes, custom_fens=custom_scenarios, verbose=False)
    white_wins, white_losses, white_draws = agent_white.last_stats
    agent_white.engine.quit()

    # Train Black agent - LOADS THE SAME Q-TABLE that White just trained
    print("\n" + "="*60)
    print("🎯 TRAINING BLACK AGENT (using White's learned Q-table)")
    print("="*60 + "\n")
    
    agent_black = QLearningChess(
        alpha=0.05,
        gamma=0.95,
        epsilon=1.0,
        epsilon_min=0.0,
        epsilon_decay_after_win=0.003,
        load_existing=True,  # Load White's Q-table
        qtable_file=qtable_file,  # Same file!
        stockfish_path="/usr/games/stockfish",
        train_as="black",
        stockfish_skill=0
    )
    agent_black.train(episodes=episodes, custom_fens=custom_scenarios, verbose=False)
    black_wins, black_losses, black_draws = agent_black.last_stats
    agent_black.engine.quit()

    # Print combined summary
    print("\n" + "="*60)
    print(f"🏁 SCENARIO {scenario_num} - FINAL SUMMARY")
    print("="*60)
    print(f"\nWhite Agent:")
    print(f"  Wins:   {white_wins:4d} ({white_wins/(episodes)*100:.1f}%)")
    print(f"  Losses: {white_losses:4d} ({white_losses/(episodes)*100:.1f}%)")
    print(f"  Draws:  {white_draws:4d} ({white_draws/(episodes)*100:.1f}%)")
    
    print(f"\nBlack Agent:")
    print(f"  Wins:   {black_wins:4d} ({black_wins/(episodes)*100:.1f}%)")
    print(f"  Losses: {black_losses:4d} ({black_losses/(episodes)*100:.1f}%)")
    print(f"  Draws:  {black_draws:4d} ({black_draws/(episodes)*100:.1f}%)")
    
    print(f"\nTotal:")
    print(f"  Wins:   {white_wins + black_wins:4d}")
    print(f"  Losses: {white_losses + black_losses:4d}")
    print(f"  Draws:  {white_draws + black_draws:4d}")
    print("="*60 + "\n")

    # Plot results
    plot_results(agent_white, agent_black, scenario_num)

    return agent_white, agent_black


# Main execution
if __name__ == "__main__":
    scenarios = [4]  # King+Rook, King+Queen, King+Queen+Rook vs King
    
    for scenario_num in scenarios:
        train_scenario(scenario_num, num_positions=50, episodes=20000)
    
    print("\n" + "="*60)
    print("✅ ALL SCENARIOS COMPLETED")
    print("="*60)
