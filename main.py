import random

from pref import PrefGameState


def main():
	state = PrefGameState()

	# Possible end states:
	# 1. All players passed -> refe
	# 2. All players passed except one who bid -> that player wins the bid
	# 3. One or more players called "game-on" -> Those players choose the game simultaneously and the highest one wins
	# Checks:
	# 1. sum([bid[0] for bid in state.bids]) == 0
	# 2. state.players_in_game == 1 and state.bids[state.players_in_game[0]][0] > 1
	# 3. all([bid[0] != 1 or bid[1] is True for bid in state.bids]) and any([bid[1] for bid in state.bids])

	while state.check_and_return_bidding_result()[0] is False:
		player = state.players_in_game[0]
		print(f"Player {player}'s turn")
		print(f"Current bids: {state.bids}")
		options = state.get_current_bidding_options(player)
		print(f"Player {player}'s options: {options}")
		i = random.randint(0, len(options) - 1)
		move = options[i]
		print(f"Player {player} chooses to {move}.")
		state.do_move(player, move)
		print()
	result = state.check_and_return_bidding_result()[1]
	if result == "game-on":
		# Kick all players who did not call "game-on"
		for player, (_, igra) in enumerate(state.bids):
			if igra is False:
				if player in state.players_in_game:
					state.players_in_game.remove(player)

		# Players who did call it do one bidding round of their own, the first one cannot pass though
		for i in range(len(state.players_in_game)):
			player = state.players_in_game[0]
			print(f"Player {player}'s turn")
			print(f"Current bids: {state.bids}")
			if i == 0:
				n = 1
			else:
				n = random.randint(0, 1)
				max_bid = state.get_max_bid()
				if max_bid == 5:
					n = 0
			if n == 0:
				print(f"Player {player} chooses to pass.")
				state.igra_pass(player)
			else:
				bid = random.randint(state.get_max_bid() + 1, 5)
				print(f"Player {player} chooses to bid {bid}.")
				state.igra_bid(player, bid)
			print()
	# If more than one player left, keep only the one with the highest bid
	max_bid = state.get_max_bid()
	for player in state.players_in_game:
		if state.bids[player][0] < max_bid:
			state.players_in_game.remove(player)
			state.bids.pop(player)
	declarer = state.players_in_game[0]
	print(f"Declarer is player {declarer} with bid {max_bid}.")




if __name__ == "__main__":
	main()