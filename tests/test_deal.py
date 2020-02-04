import unittest

from blackjack import Game
from player import Player
from carddeck import Card, Deck
import random as rand

class TestDeal(unittest.TestCase):
	def test_deal(self):
		rand.seed(7)
		game = Game()
		game.deal()
		result = game.dealer.hand[1].val == 3
		self.assertTrue(result)


if __name__ == "__main__":
	unittest.main()