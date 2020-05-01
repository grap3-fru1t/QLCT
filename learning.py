""" Define the learning algorithm """
import os
import numpy as np

class Learning:
	""" Define the modules to assess the
	automatic reinforcement
	"""
	def __init__(self, timestamp, track_dimensions):
		""" Initialize the learning process """
		log_q_name = "{timestamp}_Q_log.csv".format(timestamp=timestamp)
		self.log_q_path = os.path.join(os.getcwd(), "logs", log_q_name)
		
		# Array to save the learning parameters
		self.learning_parameters = []
		# Gamma learning parameter.
		self.gamma = 0.8
		self.track_dim = track_dimensions
		self.q_dim = self.track_dim[0] * self.track_dim[1]
		
		# initialize the Q matrix
		# Let the matrix be a square matrix of dimension [max_x*max_y, max_x*max_y]
		# e.g. for a topology of 2 columns and 5 rows:
		#					[row 0 col 0] [row 0 col 1] [row 1 col 0] .. [row 4 col 1]
		#		[row 0 col 0] [[0,           0,  		   0,       .., 	0]]
		#		[row 0 col 1] [[0,           0,  		   0,       .., 	0]]
		#		[row 1 col 0] [[0,           0,  		   0,       .., 	0]]
		# 		...			  [[0,           0,  		   0,       .., 	0]]
		#		[row 4 col 1] [[0,           0,  		   0,       .., 	0]]
		self.Q = np.matrix(np.zeros([self.q_dim, self.q_dim]))

		
	def update_q(self, next_st, current_st, reward, episode):
		""" Update the Q matrix """
		# Retrieve the correct matrix indexes
		next_state = next_st[1] * self.track_dim[1] + next_st[0]
		current_state = current_st[1] * self.track_dim[1] + current_st[0]

		# Find the index of the maximum value in the current state row
		max_index = np.argmax(self.Q[next_state, ])

		# Find the corresponding maximum value
		max_value = self.Q[next_state, max_index]

		# Update the Q matrix using the Bellmann equation
		self.Q[current_state, next_state] = self.Q[current_state, next_state] + self.gamma * (reward + max_value - self.Q[current_state, next_state])
		#self.Q = 
		self.Q = np.matrix(np.round(self.Q, 2))
		# Log the updated Q matrix
		with open(self.log_q_path, 'a') as log:
			log.write("Logging Q matrix for episode {}:\n".format(episode))
			log.write("Current state x y {}\n".format(current_st))
			log.write("Next state x y {}\n".format(next_st))
			log.write("{}\n".format(self.Q))

		return self.Q

	def save_numbers(self, episode):
		""" Save the important number for further processing later """
		current_sum = np.round(np.sum(self.Q), 2)
		current_square_sum = np.round(np.sum(self.Q**2), 2)
		self.learning_parameters.append([episode, current_sum, current_square_sum])
		

	def retrieve_l_parameters(self):
		""" Retrieve the trained parameters """
		return self.learning_parameters


	def retrieve_q_matrix(self):
		""" Retrieve the trained Q matrix """
		return self.Q
