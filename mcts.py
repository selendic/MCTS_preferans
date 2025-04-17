class Node:
	def __init__(self, state, parent=None):
		self.state = state
		self.parent = parent
		self.children = []
		self.visits = 0
		self.value = 0
	def get_best_child(self):
		# TODO
		# Implement the logic to get the best child based on UCT or other criteria
		...
	def get_unexplored_move(self):
		# TODO
		# Implement the logic to get an unexplored move from the state
		...
	def rollout(self):
		state = self.state.clone()

		while not state.is_terminal():
			# Select a random move
			state = state.make_random_move()

		return state.evaluate()

def do_mcts(root: Node, iterations=1000):
	for _ in range(iterations):
		node = root

		# Selection
		while not node.state.is_terminal() and node.is_fully_expanded():
			node = node.get_best_child()

		# Expansion
		if not node.state.is_terminal():
			move = node.get_unexplored_move()
			new_state = node.state.apply_move(move)
			new_node = Node(new_state, parent=node)
			node.children.append(new_node)
			node = new_node

		# Simulation
		result = node.rollout()

		# Backpropagation
		while node is not None:
			node.visits += 1
			node.value += result
			node = node.parent
