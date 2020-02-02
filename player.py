# Create Player class
class Player(object):
	def __init__(self):
		self.hand = []
		self.money = 0


# Add card to player's hand
	def draw(self, deck):
		self.hand.append(deck.draw())


# Method for printing player's hand
	def show_hand(self):
		ace_indices = []
		total = 0
		index = 0
		for card in self.hand:
			total += card.val
			if card.val == 11:
				ace_indices.append(index)
			index += 1

		while (total > 21) and (len(ace_indices) > 0):
			ace_index = ace_indices.pop()
			total -= 10

		print("\n** Player's Hand **")
		for card in self.hand:
			card.show()

		if total <= 21:
			print('** Player has {} **'.format(total))
		elif total > 21:
			print('** Player has {}. Player busts **'.format(total))
		return total 


	def discard(self, location):
		while self.hand:
			location.append(self.hand.pop())


	def win_money(self, money, blackjack=False):
		self.money += money
		if blackjack == False:
			print('Player wins ${}'.format(money))
		else:
			print('Blackjack! Player wins ${}'.format(money))


	def lose_money(self, money):
		self.money -= money 
		print('\nDealer Wins. You lost ${}'.format(money))