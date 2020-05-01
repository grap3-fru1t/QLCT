""" Let the car randomly navigate over the track.
The right choices/turns should be reinforced 
by the Q-Learning algorithm
"""
import time
import random
import os
import numpy as np
from datetime import datetime

class Car:
	""" Moving object """
	def __init__(self, dim, Q=None):
		""" The car can take horizontal positions
		on the track.
		"""
		self.pos_x = 2
		self.pos_y = 0
		self.Q = Q
		self.dim_x = dim[1]

	def retrieve_pos(self):
		""" Get the coordinates """
		return self.pos_x, self.pos_y

	def drive(self):
		""" Change the vertical state:
		Move one  state forward """
		self.pos_y += 1

	def random_step(self):
		""" Change the horizontal state:
		Randomly move left or right """
		next_turn = random.randrange(-1,2)
		self.pos_x += next_turn

	def smart_step(self, Q):
		""" Change the horizontal state:
		Use the maximum value in the corresponding
		Q matrix row to decide on the next 
		horizontal action
		"""
		# Obtain the correct index for the current state
		q_row_index = self.pos_y * self.dim_x + self.pos_x
		q_row = Q[q_row_index, ]
		# Sort the indeces according to their values in descending order
		max_indeces = np.argsort(q_row)[::-1]
		# Loop over the sorted indeces to find the first 
		# allowed position with highest probability
		for index in max_indeces:
			# The difference between the new position and the old one should not exceed 1
			if abs(self.pos_x - index % self.dim_x) <= 1:
				self.pos_x = index % self.dim_x
				break

class Track:
	""" The track consists of # km. Each km can
	contain vehicles on the way (marked as '1')
	"""
	def __init__(self, timestamp):
		""" The Track will be initialised once 
		to obtain the track dimensions
		"""
		log_name = "{timestamp}_track_log.csv".format(timestamp=timestamp)
		self.log_path = os.path.join(os.getcwd(), "logs", log_name)
		self.initial_way = np.array([[1, 0, 0, 0, 1], 
									 [1, 1, 0, 0, 1], 
									 [1, 0, 1, 0, 1], 
									 [1, 1, 0, 0, 1], 
									 [1, 0, 0, 1, 1],
									 [1, 0, 1, 0, 1],
									 [1, 0, 0, 0, 1],
									 [1, 1, 0, 0, 1],
									 [1, 0, 1, 0, 1],
									 [1, 0, 0, 0, 1],
									 [1, 0, 0, 1, 1],
									 [1, 1, 0, 0, 1] 
									])
		self.way = self.initial_way

	def __call__(self, episode):
		""" The track will be resetted by a call in every new episode """
		self.episode = episode
		self.way = self.initial_way

	def retrieve_way(self):
		""" Return the track composition """
		return self.way

	def update_track(self, pos, km, display):
		""" Update the track to display the current position
		of the car
		"""
		self.way = self.initial_way
		old_value = self.way[km, pos]
		self.way[km, pos] = display
		self.show_track()
		# Delete the traces of the last step performed
		self.way[km, pos] = old_value

	def show_track(self):
		""" Display the track on a clean screen """
		clear_screen()
		with open(self.log_path, 'a') as log:
			log.write("Logging Track for episode {}:\n".format(self.episode))
			for row in self.way:
				print(row)
				log.write("{}\n".format(str(row)))


def clear_screen():
	""" Remove all console output """
	os.system('cls' if os.name == 'nt' else 'clear')
