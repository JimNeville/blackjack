from player import Player 
from dealer import Dealer 
from carddeck import Card, Deck

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
		self.dealer.total = self.dealer.show_hand(start=True)
		self.player.total = self.player.show_hand()

		if (self.player.total == 21) and (self.dealer.total == 21):
			self.discard_all()
			return 'push'
		elif self.player.total == 21:
			self.discard_all()
			return 'blackjack'
		elif self.dealer.total == 21:
			self.dealer.show_hand()
			self.discard_all()
			return 'dealer' 
		
		while self.player.total < 21:
			print('\nHit or Stand? - H/S')
			action = input()
			if action.lower() == 'h':
				self.player.draw(self.deck)
				self.dealer.show_hand(start=True)
				self.player.total = self.player.show_hand()

			elif action.lower() == 's':
				self.dealer.show_hand()
				break
			else:
				continue

		while (self.dealer.total < 17) and (self.player.total <= 21):
			self.dealer.draw(self.deck)
			self.dealer.total = self.dealer.show_hand()

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

			


