"""Tests for the game rules. Run with:  python -m unittest test_game.py"""

import random
import unittest

from game import DOWN, LEFT, RIGHT, UP, Game


def put_food(game, cell):
    game.food = cell


class OnePlayer(unittest.TestCase):
    def setUp(self):
        self.g = Game(1, 10, 10, rng=random.Random(1))
        self.s = self.g.snakes[0]
        put_food(self.g, (9, 9))         # out of the way

    def test_moves_forward(self):
        self.g.step()
        self.assertEqual(self.s.body, [(6, 5), (5, 5), (4, 5)])

    def test_cannot_reverse(self):
        self.s.turn(LEFT)
        self.g.step()
        self.assertEqual(self.s.head, (6, 5))

    def test_two_quick_turns_both_apply(self):
        self.s.turn(UP)
        self.s.turn(LEFT)
        self.g.step()
        self.g.step()
        self.assertEqual(self.s.body[:2], [(4, 4), (5, 4)])

    def test_eating_grows_and_scores(self):
        put_food(self.g, (6, 5))
        self.g.step()
        self.assertEqual(self.s.score, 1)
        self.assertEqual(len(self.s.body), 4)
        self.assertNotIn(self.g.food, self.s.body)

    def test_wall_ends_game(self):
        for _ in range(4):
            self.g.step()
        self.assertFalse(self.g.over)
        self.g.step()                    # head would be x = 10
        self.assertTrue(self.g.over)
        self.assertFalse(self.s.alive)

    def test_hitting_self_ends_game(self):
        self.s.body = [(5, 5), (4, 5), (4, 6), (5, 6), (6, 6), (6, 5)]
        self.s.direction = UP
        self.s.turn(LEFT)                # into (4, 5), part of the body
        self.g.step()
        self.assertTrue(self.g.over)

    def test_can_follow_own_tail(self):
        self.s.body = [(5, 5), (5, 6), (4, 6), (4, 5)]   # tail at (4, 5)
        self.s.direction = UP
        self.s.turn(LEFT)                # tail moves away as head arrives
        self.g.step()
        self.assertFalse(self.g.over)


class TwoPlayers(unittest.TestCase):
    def setUp(self):
        self.g = Game(2, 20, 10, rng=random.Random(2))
        self.a, self.b = self.g.snakes
        put_food(self.g, (0, 0))

    def test_start_positions_do_not_overlap(self):
        self.assertFalse(set(self.a.body) & set(self.b.body))

    def test_running_into_other_snake_loses(self):
        self.a.body = [(5, 4), (4, 4), (3, 4)]
        self.a.direction = RIGHT
        self.b.body = [(6, 6), (6, 5), (6, 4), (6, 3)]   # vertical wall at x=6
        self.b.direction = DOWN
        self.g.step()
        self.assertFalse(self.a.alive)
        self.assertTrue(self.b.alive)
        self.assertIs(self.g.winner(), self.b)

    def test_head_on_is_a_draw(self):
        self.a.body = [(5, 4), (4, 4), (3, 4)]
        self.a.direction = RIGHT
        self.b.body = [(7, 4), (8, 4), (9, 4)]
        self.b.direction = LEFT
        self.g.step()                    # both heads land on (6, 4)
        self.assertTrue(self.g.over)
        self.assertIsNone(self.g.winner())

    def test_long_random_game_stays_consistent(self):
        rng = random.Random(3)
        for _ in range(500):
            if self.g.over:
                break
            for s in self.g.snakes:
                s.turn(rng.choice([UP, DOWN, LEFT, RIGHT]))
            self.g.step()
            cells = [c for s in self.g.snakes for c in s.body]
            self.assertEqual(len(cells), len(set(cells)))
        self.assertTrue(self.g.over)


if __name__ == "__main__":
    unittest.main()
