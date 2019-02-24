
import math
import itertools

class Node:
	def __init__(self, value=None):
		self.value = value
		self.left_child = None
		self.right_child = None


class RiddleSolver:
	def __init__(self, depth=None):
		self.depth = depth
		self.eligible_values = self.get_eligible_values()
		self.tree = self.build_tree()

	def get_eligible_values(self):
		# Define set of eligible values that node can take on
		num_nodes = self.depth * (self.depth + 1) / 2
		return [i + 1 for i in range(num_nodes)]

	def build_tree(self):
		# Basic error checking
		if type(self.depth) is not int or self.depth is None or self.depth <= 0:
			print('Invalid depth input')
			return None

		# Build list of required number of nodes
		nodes = [Node() for node in range(len(self.eligible_values))]

		# Assign children based on index of each node
		for index, node in enumerate(nodes):
			depth = self.get_depth_from_index(index)
			try:
				node.left_child = nodes[index + depth]
				node.right_child = nodes[index + depth + 1]
			except IndexError:
				continue
		return nodes

	def get_depth_from_index(self, index):
		i = 1
		while i * (i + 1) / 2 <= index:
			i += 1
		return i

	def get_node_value(self, node):
		# Base case - node value is already defined
		if node.value:
			return node.value

		# Base case - leaf node with undefined value
		if node.left_child is None or node.right_child is None:
			return None

		# Otherwise, bubble up difference of children
		left_child_val = self.get_node_value(node.left_child)
		right_child_val = self.get_node_value(node.right_child)
		if left_child_val is None or right_child_val is None:
			return None
		if left_child_val < right_child_val:
			return right_child_val - left_child_val
		return left_child_val - right_child_val

	def test_proposed_solution(self, initial_nodes, initial_values):
		# Set values for passed nodes
		for node, value in zip(initial_nodes, initial_values):
			node.value = value

		# Generate list of values
		values = []
		for node in self.tree:
			value = self.get_node_value(node)
			if value is None:
				return False
			values.append(value)

		# Test whether solution is valid
		return sorted(values) == sorted(self.eligible_values)

	def find_solutions(self):
		# Key insight is that lowest depth nodes are the only degrees of freedom

		# Get leaf nodes
		leaf_nodes = [node for node in self.tree if node.left_child is None and node.right_child is None]

		# Get total number of initial states by checking permutation search space
		total_permutations = math.factorial(len(self.eligible_values)) / \
			math.factorial(len(self.eligible_values) - len(leaf_nodes))

		solutions = []
		for index, combo in enumerate(itertools.permutations(self.eligible_values, len(leaf_nodes))):
			if index % 100000 == 0:
				print('{index} / {total}'.format(index=index, total=total_permutations))
			if self.test_proposed_solution(leaf_nodes, combo):
				solutions.append(combo)

		return solutions


if __name__ == '__main__':
	solver = RiddleSolver(6)
	solutions = solver.find_solutions()
	print(solutions)






