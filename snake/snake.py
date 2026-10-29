"""Snake, for 1 or 2 players. Run with:  python snake.py"""

import tkinter as tk

from game import DOWN, LEFT, RIGHT, UP, Game

CELL = 24
COLS, ROWS = 30, 20
BAR = 36                                 # score bar height in pixels
TICK_MS = 110                            # lower = faster snake

BG = "#111418"
GRID = "#1a1f25"
TEXT = "#e8eaed"
FOOD = "#ff5d5d"
COLORS = [("#3ddc84", "#2a9d5c"), ("#4aa3ff", "#2f6fb0")]   # (head, body)

ARROWS = {"Up": UP, "Down": DOWN, "Left": LEFT, "Right": RIGHT}
WASD = {"w": UP, "s": DOWN, "a": LEFT, "d": RIGHT}


class App:
    def __init__(self, root):
        self.root = root
        root.title("Snake")
        root.resizable(False, False)
        self.canvas = tk.Canvas(root, width=COLS * CELL, height=ROWS * CELL + BAR,
                                bg=BG, highlightthickness=0)
        self.canvas.pack()
        root.bind("<KeyPress>", self.on_key)
        self.game = None
        self.players = 1
        self.state = "menu"              # menu | playing | paused | over
        self.after_id = None
        self.draw()

    # ---- flow -------------------------------------------------------------
    def start(self, players):
        self.players = players
        self.game = Game(players, COLS, ROWS)
        self.state = "playing"
        self.schedule()
        self.draw()

    def schedule(self):
        if self.after_id:
            self.root.after_cancel(self.after_id)
        self.after_id = self.root.after(TICK_MS, self.tick)

    def tick(self):
        self.after_id = None
        if self.state != "playing":
            return
        self.game.step()
        if self.game.over:
            self.state = "over"
        else:
            self.schedule()
        self.draw()

    # ---- input ------------------------------------------------------------
    def on_key(self, event):
        key = event.keysym
        low = key.lower()
        if key == "Escape":
            self.root.destroy()
            return

        if self.state == "menu":
            if key in ("1", "KP_1"):
                self.start(1)
            elif key in ("2", "KP_2"):
                self.start(2)
            return

        if self.state == "over":
            if low == "r":
                self.start(self.players)
            elif low == "m":
                self.state = "menu"
                self.draw()
            return

        if low in ("p", "space"):
            self.state = "paused" if self.state == "playing" else "playing"
            if self.state == "playing":
                self.schedule()
            self.draw()
            return

        if self.state != "playing":
            return
        snakes = self.game.snakes
        if self.players == 1:
            d = ARROWS.get(key) or WASD.get(low)
            if d:
                snakes[0].turn(d)
        else:
            if low in WASD:
                snakes[0].turn(WASD[low])
            elif key in ARROWS:
                snakes[1].turn(ARROWS[key])

    # ---- drawing ----------------------------------------------------------
    def cell(self, x, y, color, pad=1):
        x0, y0 = x * CELL + pad, BAR + y * CELL + pad
        self.canvas.create_rectangle(x0, y0, x0 + CELL - 2 * pad,
                                     y0 + CELL - 2 * pad, fill=color, width=0)

    def text(self, x, y, msg, size=14, color=TEXT, anchor="center"):
        self.canvas.create_text(x, y, text=msg, fill=color, anchor=anchor,
                                font=("Helvetica", size, "bold"))

    def draw(self):
        c = self.canvas
        c.delete("all")
        w, h = COLS * CELL, ROWS * CELL
        cx, cy = w // 2, BAR + h // 2

        if self.state == "menu":
            self.text(cx, cy - 90, "SNAKE", 40, COLORS[0][0])
            self.text(cx, cy - 20, "Press 1 for one player", 16)
            self.text(cx, cy + 10, "Press 2 for two players", 16)
            self.text(cx, cy + 70, "1 player: arrow keys or WASD", 11, "#9aa0a6")
            self.text(cx, cy + 92,
                      "2 players: Green = WASD, Blue = arrow keys", 11, "#9aa0a6")
            self.text(cx, cy + 114, "P or Space to pause, Esc to quit", 11, "#9aa0a6")
            return

        for x in range(0, w, CELL):      # faint grid
            c.create_line(x, BAR, x, BAR + h, fill=GRID)
        for y in range(BAR, BAR + h, CELL):
            c.create_line(0, y, w, y, fill=GRID)

        g = self.game
        if g.food:
            self.cell(*g.food, FOOD, pad=4)
        for i, s in enumerate(g.snakes):
            head, body = COLORS[i]
            for part in s.body[1:]:
                self.cell(*part, body)
            self.cell(*s.head, head if s.alive else "#777777")

        # score bar
        c.create_rectangle(0, 0, w, BAR, fill="#0b0d10", width=0)
        if self.players == 1:
            self.text(12, BAR // 2, f"Score: {g.snakes[0].score}", anchor="w")
        else:
            self.text(12, BAR // 2, f"Green: {g.snakes[0].score}",
                      color=COLORS[0][0], anchor="w")
            self.text(w - 12, BAR // 2, f"Blue: {g.snakes[1].score}",
                      color=COLORS[1][0], anchor="e")

        if self.state == "paused":
            self.text(cx, cy, "PAUSED", 28)
        elif self.state == "over":
            if self.players == 1:
                title = f"Game over - score {g.snakes[0].score}"
            else:
                win = g.winner()
                title = f"{win.name} wins!" if win else "It's a draw!"
            self.text(cx, cy - 20, title, 26)
            self.text(cx, cy + 20, "R to play again, M for menu, Esc to quit", 13)


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
