# Q-Learning Chess Endgame Trainer

This repository contains a Q-learning agent that trains on chess positions (primarily endgame-style scenarios) and learns by playing against the Stockfish engine.

## What’s included

- **Tabular Q-Learning agent** with epsilon-greedy exploration, shared Q-table storage, and training metrics tracking.
- **Scenario/position generator** that constructs many randomized, legal-ish mini-positions (e.g., K+Q+P vs K+Q, K+2P vs K+P, etc.) to focus learning on smaller state spaces.
- **Reward shaping** that rewards checks, material gain/loss (via material scoring), and mildly encourages pushing the opposing king toward the edge.
- **Utilities** for material scoring, pretty-printing boards, and converting a board to a tensor representation (useful if extending to deep RL later).

## Repository structure

| File | Purpose |
| --- | --- |
| `agents_old.py` | Main Q-learning implementation (`QLearningChess`) and training loop vs Stockfish. |
| `get_board.py` | Generates randomized scenario boards (multiple endgame configurations). |
| `rewards.py` | Reward function used during learning updates. |
| `helper.py` | Material scoring, board printing, and board-to-tensor helper. |

## Setup

### Requirements

- Python 3.9+ (recommended)
- Stockfish installed locally (agent launches it via UCI).

### Python dependencies

Install core dependencies:
```bash
pip install python-chess numpy torch matplotlib colorama
```
The code also uses the standard library modules `os`, `pickle`, `copy`, and `random`.

### Stockfish path

By default, the agent expects Stockfish at `/usr/games/stockfish` (common on Linux installs), but this can be configured via the `stockfish_path` argument.

## Usage

### Train the agent

Minimal example (train as White vs Stockfish):
```python
from agents_old import QLearningChess

agent = QLearningChess(
    alpha=0.05,
    gamma=0.95,
    epsilon=1.0,
    load_existing=False,
    qtable_file="Q_table.pkl",
    stockfish_path="/usr/games/stockfish",
    train_as="white",
    stockfish_skill=0
)

agent.train(episodes=1000, custom_fens=None, verbose=False)
```
The training loop alternates the agent’s move and Stockfish’s response while updating Q-values.

### Train on scenario-generated positions (recommended)

`get_board.py` contains multiple scenario builders that assemble simplified boards for targeted learning.

A typical workflow is:
1. Generate a list of FENs/boards from scenario functions.
2. Pass them into `train(custom_fens=...)` so each episode starts from a random scenario position.

## Reward design (high level)

The reward function:
- Adds a bonus when the resulting position is check.
- Uses material score differences to reward winning captures (and penalize losing material), with sign handled based on which side is being trained.
- Adds a small shaping term for “edge closeness” of the opponent king (helps with mating-net style endgames).

## Notes / next steps

- The current approach uses a tabular Q-table keyed by a simplified FEN representation (without halfmove/fullmove counters) to reduce state variance.
- `helper.py` already includes a board-to-tensor conversion, which can be used to upgrade from tabular learning to a neural approximator.

## License

Add a license file (e.g., MIT) if you plan to publish this publicly.
