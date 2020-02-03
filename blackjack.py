from player import Player 
from dealer import Dealer 
from carddeck import Card, Deck
import os
import time

class Game(object):
	def __init__(self):
		self.player = Player()
		self.dealer = Dealer()
		self.deck = Deck()
		self.discarded = self.deck.discarded


	def seed_player(self):
		os.system('clear')
		input_check = False
		while input_check == False:
			print('Welcome to Blackjack. Please enter your starting money amount')
			money = input()

			if money == 'q':
				exit()

			try:
				money = float(money)
				self.player.money = money
				input_check = True
				os.system('clear')
			except ValueError as e:
				os.system('clear')
				print("Input error - Plese input a starting amount greater than 0")


	def place_bet(self):
		input_check = False
		while input_check == False:
			print('Please enter your bet amount. You currently have ${}'.format(self.player.money))
			bet = input()

			if bet == 'q':
				exit()

			try:
				bet = float(bet)
			except ValueError as e:
				os.system('clear')
				print('You did not enter a valid bet amount')
				continue

			if self.player.money - bet < 0:
				os.system('clear')
				print('You do not have that much money')
				continue
			else:
				os.system('clear')
				print('Player bets ${}'.format(bet))
				input_check = True
				return bet 


	def deal(self):
		while len(self.dealer.hand) < 2:
			self.dealer.draw(self.deck)
			self.player.draw(self.deck)


	def discard_all(self):
		self.player.discard(self.discarded)
		self.dealer.discard(self.discarded)


	def show_status(self, start=False, clear=True):
		if clear is True:
			os.system('clear')
		dealer_total = self.dealer.show_hand(start=start)
		player_total = self.player.show_hand()
		return dealer_total, player_total

		
	def play_hand(self, bet):

		# Function to play hand and return the winner - Player, Dealer, Push, or Blackjack if player is dealt blackjack
		self.deal()
		self.dealer.total, self.player.total = self.show_status(start=True, clear = False)

		if (self.player.total == 21) and (self.dealer.total == 21):
			self.show_status()
			self.discard_all()
			return 'push', bet
		elif self.player.total == 21:
			self.discard_all()
			return 'blackjack', bet
		elif self.dealer.total == 21:
			self.show_status()
			self.discard_all()
			return 'dealer', bet 
		
		while self.player.total < 21:
			if len(self.player.hand) < 3:
				print('\nHit, Stand or Double Down - H/S/D')
				action = input()

				if action.lower() == 'h':
					self.player.draw(self.deck)
					self.player.total = self.show_status(start=True)[1]

				elif action.lower() == 's':
					self.show_status()
					time.sleep(2)
					break

				elif action.lower() == 'd':
					if self.player.money - (2*bet) >= 0:
						bet = 2*bet
						self.player.draw(self.deck)
						self.player.total = self.show_status(start=True)[1]
						time.sleep(2)
						break
					else:
						self.show_status(start=True)
						print('\nYou do not have enough money to double down')
				elif action.lower() == 'q':
					exit()
				else:
					continue


			print('\nHit or Stand? - H/S')
			action = input()
			if action.lower() == 'h':
				self.player.draw(self.deck)
				self.player.total = self.show_status(start=True)[1]

			elif action.lower() == 's':
				self.show_status()
				time.sleep(2)
				break
			elif action.lower() == 'q':
				exit()
			else:
				continue

		while (self.dealer.total < 17) and (self.player.total <= 21):
			self.dealer.draw(self.deck)
			self.dealer.total = self.show_status()[0]
			time.sleep(2)

		self.discard_all()

		if self.dealer.total == self.player.total:
			return 'push', bet
		elif (self.dealer.total <= 21) and (self.dealer.total > self.player.total):
			return 'dealer', bet
		elif (self.player.total <= 21) and (self.player.total > self.dealer.total):
			return 'player', bet
		elif self.player.total > 21:
			return 'dealer', bet
		elif self.dealer.total > 21:
			return 'player', bet


	def play_game(self):
		self.seed_player()
		while self.player.money >= 1:
			bet = self.place_bet()
			winner, bet = self.play_hand(bet)
			if winner == 'player':
				self.player.win_money(bet)
			elif winner == 'dealer':
				self.player.lose_money(bet)
			elif winner == 'blackjack':
				self.player.win_money(bet*1.5, blackjack=True)
			else:
				print("\nIt's a push...\n")
				continue


def main():
	Game().play_game()


if __name__ == "__main__":
	main()

			


