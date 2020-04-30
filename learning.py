""" Define the learning algorithm """
import os
import numpy as np

class Learning:
	""" Define the modules to assess the
	automatic reinforcement
	"""
	def __init__(self, timestamp):
		""" R matrix 
		# Each row corresponds to one state (e.g. left right middle)
		# Each column corresponds to an action / next possible state: go left out (0) left (1), middle(2), right(3), right out(4)..
		"""
		log_name = "{timestamp}_Q_log.txt".format(timestamp=timestamp)
		self.log_path = os.path.join(os.getcwd(), "logs", log_name)
		#print(self.log)
		#				 0   1  2  3  4
		self.R = np.matrix([ [-1,-10,-10,-10,-1], # left outside track
						[-1,10,10,10,-1],    # left track
						[-1,10,10,10,-1],    # middle track
						[-1,10,10,10,-1],    # right track
						[-1,-10,-10,-10,-1]]) # right out track

		# initialize the Q matrix
		self.Q = np.matrix(np.zeros([5,5]))

		# Gamma learning parameter.
		self.gamma = 0.5

	def update_q(self, next_state, current_state, episode):
		""" Update the Q matrix """

		# Find the index of the maximum value in the current state row
		max_index = np.argmax(self.Q[next_state, ])

		# Find the corresponding maximum value
		max_value = self.Q[next_state, max_index]

		# Update the Q matrix
		self.Q[current_state, next_state] = self.R[current_state, next_state] + self.gamma * max_value
		
		# Log the updated Q matrix
		with open(self.log_path, 'a') as log:
			log.write("Logging Q matrix for episode {}:\n".format(episode))
			for row in self.Q:
				log.write("{}\n".format(str(row)))


	def retrieve_q_matrix(self):
		""" Retrieve the trained Q matrix """
		return self.Q
