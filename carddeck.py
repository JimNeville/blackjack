import random as rand

class Card(object):
	def __init__(self, val, suit):
		self.val = val
		self.suit = suit
		self.name = None
		self.alt_val = None


	def show(self):
		if self.name is None:
			print('{} of {}'.format(self.val, self.suit))
		else:
			print('{} of {}'.format(self.name, self.suit))


# Create Deck class
class Deck(object):
	def __init__(self):
		self.cards = []
		self.discarded = []
		self.build()
		self.shuffle()


# Build card deck
	def build(self):
		card_map = {11:'Jack', 12:'Queen', 13:'King'}

		for suit in ['Hearts', 'Diamonds', 'Spades', 'Clubs']:
			for value in range(2, 11): 
				self.cards.append(Card(value, suit))
			for i in range(11, 14):
				new_card = Card(10, suit)
				new_card.name = card_map[i]
				self.cards.append(new_card)
			ace = Card(11, suit)
			ace.alt_val = 1
			ace.name = 'Ace'
			self.cards.append(ace)


# Method to randomly shuffle the deck
	def shuffle(self):
		for i in range(len(self.cards) - 1, 0, -1):
			rand_int = rand.randint(0, i)
			self.cards[rand_int], self.cards[i] = self.cards[i], self.cards[rand_int]


# Method to draw card from remaining deck
	def draw(self):
		if len(self.cards) > 0:
			return self.cards.pop()
		else:
			for card in self.discarded:
				self.cards.append(card)
			print('******** Shuffling Cards ********')
			self.shuffle()
			return self.cards.pop()