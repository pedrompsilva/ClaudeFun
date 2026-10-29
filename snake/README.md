# Snake

A basic snake game for 1 or 2 players, written in Python with tkinter, which is
part of the standard Python install. No extra packages needed.

## Play

```
cd snake
python snake.py
```

On the start screen press **1** for one player or **2** for two players.

| Mode | Controls |
|------|----------|
| 1 player | Arrow keys or WASD |
| 2 players | Green: WASD, Blue: arrow keys |

- **P** or **Space**: pause
- **R**: play again after a game ends
- **M**: back to the menu after a game ends
- **Esc**: quit

## Rules

- Eat the red food to grow and score a point.
- Hitting a wall, yourself or the other snake ends the game.
- In 2-player mode the surviving snake wins. If both crash on the same move,
  the higher score wins, and equal scores are a draw.

## Files

- `game.py`: the game rules, with no UI code
- `snake.py`: the window, drawing and keyboard controls
- `test_game.py`: tests for the rules (`python -m unittest test_game.py`)

To change the speed, edit `TICK_MS` near the top of `snake.py` (lower is faster).

On Linux, tkinter may need installing separately, for example
`sudo apt install python3-tk`. The python.org installers for Windows and macOS
include it.
