class Dealer(object):
	def __init__(self):
		self.hand = []


	def draw(self, deck):
		self.hand.append(deck.draw())


	def show_hand(self, start=False):
		print("\n** Dealer's Hand **")
		if start == False:
			for card in self.hand:
				card.show()
		elif start == True:
			print('Card Not Visible')
			self.hand[1].show()


	def show_total(self, start=False):
		ace_indices = []
		total = 0
		index = 0
		for card in self.hand:
			total += card.val
			if card.val == 11:
				ace_indices.append(index)
			index += 1

		if start == True:
			print('** Dealer shows {} **'.format(self.hand[1].val))
			return total 

		while (total > 21) and (len(ace_indices) > 0):
			ace_index = ace_indices.pop()
			total -= 10

		if total <= 21:
			print('** Dealer has {} **'.format(total))
		elif total > 21:
			print('** Dealer has {}. Dealer busts **'.format(total))
		return total 


	def discard(self, location):
		while self.hand:
			location.append(self.hand.pop())