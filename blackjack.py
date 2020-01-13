import random as rand 

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
		print("\n** Player's Hand **")
		for card in self.hand:
			card.show()


	def show_total(self):
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
			print('********Shuffling Cards*************')
			self.shuffle()
			return self.cards.pop()


class Game(object):
	def __init__(self):
		self.player = Player()
		self.dealer = Dealer()
		self.deck = Deck()
		self.discarded = self.deck.discarded


	def seed_player(self):
		input_check = False
		while input_check == False:
			print('Welcome to Blackjack. Please enter your starting money amount')
			money = input()
			try:
				money = float(money)
				self.player.money = money
				input_check = True
			except ValueError as e:
				print("Input error - Restarting Game...")


	def place_bet(self):
		input_check = False
		while input_check == False:
			print('Please enter your bet amount. You currently have ${}'.format(self.player.money))
			bet = input()

			try:
				bet = float(bet)
			except ValueError as e:
				print('You did not enter a valid bet amount')
				continue

			if self.player.money - bet < 0:
				print('You do not have that much money')
				continue
			else:
				print('Player bets ${}\n'.format(bet))
				input_check = True
				return bet 


	def deal(self):
		while len(self.dealer.hand) < 2:
			self.dealer.draw(self.deck)
			self.player.draw(self.deck)


	def discard_all(self):
		self.player.discard(self.discarded)
		self.dealer.discard(self.discarded)

		
	def play_hand(self):

		# Function to play hand and return the winner - Player, Dealer, Push, or Blackjack if player is dealt blackjack
		self.deal()
		self.dealer.show_hand(start=True)
		self.dealer.total = self.dealer.show_total(start=True)
		self.player.show_hand()
		self.player.total = self.player.show_total()

		if (self.player.total == 21) and (self.dealer.total == 21):
			self.discard_all()
			return 'push'
		elif self.player.total == 21:
			self.discard_all()
			return 'blackjack'
		elif self.dealer.total == 21:
			self.dealer.show_hand()
			self.dealer.show_total()
			self.discard_all()
			return 'dealer' 
		
		while self.player.total < 21:
			print('\nHit or Stand? - H/S')
			action = input()
			if action.lower() == 'h':
				self.player.draw(self.deck)
				self.dealer.show_hand(start=True)
				self.dealer.show_total(start=True)
				self.player.show_hand()
				self.player.total = self.player.show_total()

			elif action.lower() == 's':
				self.dealer.show_hand()
				self.dealer.show_total()
				break
			else:
				continue

		while (self.dealer.total < 17) and (self.player.total <= 21):
			self.dealer.draw(self.deck)
			self.dealer.show_hand()
			self.dealer.total = self.dealer.show_total()

		self.discard_all()

		if self.dealer.total == self.player.total:
			return 'push'
		elif (self.dealer.total <= 21) and (self.dealer.total > self.player.total):
			return 'dealer'
		elif (self.player.total <= 21) and (self.player.total > self.dealer.total):
			return 'player'
		elif self.player.total > 21:
			return 'dealer'
		elif self.dealer.total > 21:
			return 'player'


	def play_game(self):
		self.seed_player()
		while self.player.money >= 1:
			bet = self.place_bet()
			winner = self.play_hand()
			if winner == 'player':
				self.player.win_money(bet)
			elif winner == 'dealer':
				self.player.lose_money(bet)
			elif winner == 'blackjack':
				self.player.win_money(bet*1.5, blackjack=True)
			else:
				print("It's a push...")
				continue


def main():
	Game().play_game()


if __name__ == "__main__":
	main()

			


