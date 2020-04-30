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
	def __init__(self, Q=None):
		""" The car can take horizontal positions
		on the track.
		"""
		self.pos_x = 2
		self.pos_y = 0
		self.Q = Q

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
		max_index = np.argmax(Q[self.pos_x, ])
		self.pos_x = max_index

class Track:
	""" The track consists of # km. Each km can
	contain vehicles on the way (marked as '1')
	"""
	def __init__(self, timestamp, episode, mode):

		log_name = "{timestamp}_track_{mode}_log.txt".format(timestamp=timestamp, mode=mode)
		self.log_path = os.path.join(os.getcwd(), "logs", log_name)
		self.episode = episode
		self.initial_way = [[1, 0, 0, 0, 1], 
							[1, 0, 0, 0, 1], 
							[1, 0, 0, 0, 1], 
							[1, 0, 0, 0, 1], 
							[1, 0, 0, 0, 1], 
							[1, 0, 0, 0, 1], 
							[1, 0, 0, 0, 1], 
							[1, 0, 0, 0, 1], 
							[1, 0, 0, 0, 1]]
		self.way = self.initial_way
		clear_screen()

	def retrieve_way(self):
		""" Return the track composition """
		return self.way

	def update_track(self, pos, km, display):
		""" Update the track to display the current position
		of the car
		"""
		self.way = self.initial_way
		old_value = self.way[km][pos]
		self.way[km][pos] = display
		self.show_track()
		# Delete the traces of the last step performed
		self.way[km][pos] = old_value

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
