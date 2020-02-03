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

		
	def play_hand(self, bet):

		# Function to play hand and return the winner - Player, Dealer, Push, or Blackjack if player is dealt blackjack
		self.deal()
		self.dealer.total = self.dealer.show_hand(start=True)
		self.player.total = self.player.show_hand()

		if (self.player.total == 21) and (self.dealer.total == 21):
			os.system('clear')
			self.dealer.show_hand()
			self.player.show_hand()
			self.discard_all()
			return 'push', bet
		elif self.player.total == 21:
			self.discard_all()
			return 'blackjack', bet
		elif self.dealer.total == 21:
			os.system('clear')
			self.dealer.show_hand()
			self.player.show_hand()
			self.discard_all()
			return 'dealer', bet 
		
		while self.player.total < 21:
			if len(self.player.hand) < 3:
				print('\nHit, Stand or Double Down - H/S/D')
				action = input()

				if action.lower() == 'h':
					os.system('clear')
					self.player.draw(self.deck)
					self.dealer.show_hand(start=True)
					self.player.total = self.player.show_hand()

				elif action.lower() == 's':
					os.system('clear')
					self.dealer.show_hand()
					self.player.show_hand()
					time.sleep(1.5)
					break

				elif action.lower() == 'd':
					if self.player.money - (2*bet) >= 0:
						bet = 2*bet
						os.system('clear')
						self.player.draw(self.deck)
						self.dealer.show_hand(start=True)
						self.player.total = self.player.show_hand()
						time.sleep(1.5)
						break
					else:
						os.system('clear')
						self.dealer.show_hand(start=True)
						self.player.show_hand()
						print('\nYou do not have enough money to double down')
				elif action.lower() == 'q':
					exit()
				else:
					continue


			print('\nHit or Stand? - H/S')
			action = input()
			if action.lower() == 'h':
				os.system('clear')
				self.player.draw(self.deck)
				self.dealer.show_hand(start=True)
				self.player.total = self.player.show_hand()

			elif action.lower() == 's':
				os.system('clear')
				self.dealer.show_hand()
				self.player.show_hand()
				time.sleep(1.5)
				break
			elif action.lower() == 'q':
				exit()
			else:
				continue

		while (self.dealer.total < 17) and (self.player.total <= 21):
			os.system('clear')
			self.dealer.draw(self.deck)
			self.dealer.total = self.dealer.show_hand()
			self.player.show_hand()
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

			


