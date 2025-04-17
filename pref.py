class PrefGameState:
	def __init__(self, bule=30, refe=1):
		self.player_hands = [[], [], []]  # Player hands, hidden to other players, indexed by player

		# In general
		self.phase = "bidding"  # bidding, trick-taking or game-over
		self.scores = [(0, -bule, 0), (0, -bule, 0), (0, -bule,
													  0)]  # Scores of each player, indexed by player, with bule in the middle and corresponding soups on each side
		self.shuffled = 2  # The player who shuffled the cards
		self.refe_left = [refe, refe, refe]  # Number of refas left for each player, indexed by player
		self.refe_active = [False, False, False]  # If True, the player has a refa active
		self.players_in_game = [0, 1, 2]  # Player queue

		# Bidding
		self.bids = [(1, False), (1, False), (1, False)]  # Bids made by each player, indexed by player
		self.talon = []  # 2 talon cards, hidden at first but revealed once the bidding is over
		self.bid_first = None  # The player who made the first bid, who can call "bija"

		# Countering
		self.declarer = None  # The player who wins the bidding
		self.game = None  # The game being played (2=spades, 3=clubs, 4=hearts, 5=diamonds, 6=battle, 7=sans)
		self.igra = False  # If True, the game is worth +1 and is played without the talon
		self.counter = None  # The player who countered the declarer, if any

		# Trick taking
		self.played_cards = [[], [], []]  # Cards each player has played, indexed by player and then by turn
		self.current_trick = []  # Cards played in the current trick
		self.trick_winners = []  # Trick winners, indexed by trick

	# Bidding
	bidding_options = ["bid", "game-on", "pass"]

	def get_current_bidding_options(self, player):
		"""Returns the current bidding options for the player"""
		# First check if the player is the only one left
		if len(self.players_in_game) == 1:
			assert self.players_in_game[0] == player
			# Now, if it's still the first round, it means he can choose either option, and it's the last turn in the bidding phase
			if self.bids[player] == (1, False):
				return ["game-on", "pass", "bid"]
			# Otherwise, it's already over and he won the bid
			else:
				return []
		options = []
		# A player can call "game-on" if it's the first round (which means they did neither pass nor bid nor call "game-on" yet)
		if self.bids[player] == (1, False):
			options.append("game-on")
		# A player can pass if they have not passed already, and if (igra is called and it's the first round or if igra is not called)
		if self.bids[player][0] > 0 and (all([not bid[1] for bid in self.bids]) or (any([bid[1] for bid in self.bids]) and self.bids[player] == (1, False))):
			options.append("pass")
		# A player can bid if no one said "game-on" yet and there is a larger value to bid
		max_bid = self.get_max_bid()
		if all([not bid[1] for bid in self.bids]) and not (
				self.bid_first == player and self.bids[player][0] == 7 or self.bid_first != player and max_bid == 7):
			options.append("bid")

		return options

	def do_move(self, player: int, move):
		# Executes the move
		if move == "bid":
			self.bid(player)
		elif move == "game-on":
			self.igraj(player)
		elif move == "pass":
			self.dalje(player)
		else:
			raise ValueError("Invalid move")

	def get_max_bid(self):
		# Returns the maximum bid of the players
		return max([bid[0] for bid in self.bids])

	def bid(self, player: int):
		if self.bid_first == player:
			self.bids[player] = (self.get_max_bid(), self.bids[player][1])
		else:
			self.bids[player] = (self.get_max_bid() + 1, self.bids[player][1])
		if self.bid_first is None:
			self.bid_first = player
		self.players_in_game.pop(0)
		self.players_in_game.append(player)

	def igraj(self, player: int):
		self.bids[player] = (self.bids[player][0], True)
		self.players_in_game.pop(0)
		self.players_in_game.append(player)

	def dalje(self, player: int):
		self.bids[player] = (0, False)
		if self.bid_first == player:
			if self.bids[(player + 1) % 3][0] > 1:
				self.bid_first = (player + 1) % 3
			else:
				if self.bids[(player + 2) % 3][0] > 1:
					self.bid_first = (player + 2) % 3
		self.players_in_game.pop(0)

	def check_and_return_bidding_result(self):
		if sum([bid[0] for bid in self.bids]) == 0:
			return True, "refe"
		elif len(self.players_in_game) == 1 and self.bids[self.players_in_game[0]][0] > 1:
			return "no-igra-zovi"
		elif all([bid[0] != 1 or bid[1] is True for bid in self.bids]) and any([bid[1] for bid in self.bids]):
			return True, "game-on"
		else:
			return False, None

	def igra_bid(self, player: int, bid: int):
		self.bids[player] = (bid, True)
		self.players_in_game.pop(0)
		self.players_in_game.append(player)

	def igra_pass(self, player: int):
		self.bids[player] = (0, True)
		self.players_in_game.pop(0)
