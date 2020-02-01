import unittest

from blackjack import Player, Deck

class TestDraw(unittest.TestCase):
	def test_draw(self):
		p1 = Player()
		deck = Deck()
		p1.draw(deck)

		result = len(p1.hand)

		self.assertEqual(result, 1)


if __name__ == "__main__":
	unittest.main()



