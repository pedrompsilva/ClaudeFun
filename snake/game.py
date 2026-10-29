"""Snake game rules, kept free of any UI code so they can be tested on their own."""

import random

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    def __init__(self, name, body, direction):
        self.name = name
        self.body = list(body)          # head first
        self.direction = direction
        self.pending = []               # queued turns, applied one per step
        self.alive = True
        self.score = 0

    @property
    def head(self):
        return self.body[0]

    def turn(self, direction):
        """Queue a turn. Reversing onto yourself is ignored."""
        last = self.pending[-1] if self.pending else self.direction
        if direction == last or direction == (-last[0], -last[1]):
            return
        if len(self.pending) < 2:       # lets quick taps like up-then-left work
            self.pending.append(direction)


class Game:
    def __init__(self, players=1, width=30, height=20, rng=None):
        if players not in (1, 2):
            raise ValueError("players must be 1 or 2")
        self.width = width
        self.height = height
        self.rng = rng or random.Random()
        mid = height // 2
        if players == 1:
            self.snakes = [Snake("Player", [(5, mid), (4, mid), (3, mid)], RIGHT)]
        else:
            self.snakes = [
                Snake("Green", [(5, mid - 3), (4, mid - 3), (3, mid - 3)], RIGHT),
                Snake("Blue", [(width - 6, mid + 3), (width - 5, mid + 3),
                               (width - 4, mid + 3)], LEFT),
            ]
        self.food = None
        self.over = False
        self.place_food()

    def place_food(self):
        taken = {cell for s in self.snakes for cell in s.body}
        free = [(x, y) for x in range(self.width) for y in range(self.height)
                if (x, y) not in taken]
        if not free:                     # board full: nothing left to eat
            self.food = None
            self.over = True
            return
        self.food = self.rng.choice(free)

    def step(self):
        """Advance the game by one tick."""
        if self.over:
            return
        alive = [s for s in self.snakes if s.alive]

        for s in alive:
            if s.pending:
                s.direction = s.pending.pop(0)

        new_heads = {}
        grows = {}
        for s in alive:
            dx, dy = s.direction
            new_heads[s] = (s.head[0] + dx, s.head[1] + dy)
            grows[s] = new_heads[s] == self.food

        # Cells occupied after the move. A tail that moves away this tick is free.
        occupied = set()
        for s in alive:
            occupied.update(s.body if grows[s] else s.body[:-1])

        dead = set()
        for s in alive:
            x, y = new_heads[s]
            if not (0 <= x < self.width and 0 <= y < self.height):
                dead.add(s)
            elif (x, y) in occupied:
                dead.add(s)
            elif any(o is not s and new_heads[o] == (x, y) for o in alive):
                dead.add(s)              # head-on collision: both lose

        ate = False
        for s in alive:
            if s in dead:
                s.alive = False
                continue
            s.body.insert(0, new_heads[s])
            if grows[s]:
                s.score += 1
                ate = True
            else:
                s.body.pop()

        if any(not s.alive for s in self.snakes):
            self.over = True
        elif ate:
            self.place_food()

    def winner(self):
        """In a 2-player game, the surviving snake, or None for a draw."""
        if not self.over or len(self.snakes) == 1:
            return None
        alive = [s for s in self.snakes if s.alive]
        if len(alive) == 1:
            return alive[0]
        return max(self.snakes, key=lambda s: s.score) if \
            self.snakes[0].score != self.snakes[1].score else None
