""" Let the car randomly navigate over the track.
The right choices/turns should be reinforced 
by the Q-Learning algorithm
"""
import time
import random
import os
from datetime import datetime

from learning import Learning

class Car:
	""" Moving object """
	def __init__(self):
		""" The car can take positions -1,0,1 on the track,
		Every turn the car can move one position to the left or
		one position to the right
		"""
		self.pos = 1
		self.km = 0

	def retrieve_pos(self):
		""" Get the coordinates """
		return self.pos, self.km

	def drive(self):
		""" Move one forward """
		self.km += 1

	def choose_step(self):
		""" Randomly move left or right """
		next_turn = random.randrange(-1,2)
		self.pos += next_turn


class Game:
	""" Control the game board and its elements"""
	def __init__(self):
		self.timestamp = datetime.now().strftime('%Y%m%d_%H_%M_%S')
		self.my_track = Track(self.timestamp)
		self.my_car = Car()
		self.my_way = self.my_track.retrieve_way()

		self.step = 0
		self.current_car_display = None
		self.new_pos_x = None
		self.new_pos_y = None
		self.old_pos_x = 0
		self.L = Learning(self.timestamp)
		print(self.L.R)

	def start_game(self):
		""" Start game """
		while self.step < 9:
			self.step += 1
			
			self.new_pos_x, self.new_pos_y = self.my_car.retrieve_pos()
			evaluation = self.evaluate_position()
			self.L.update_q(self.new_pos_x, self.old_pos_x)
			self.my_track.update_track(self.new_pos_x, self.new_pos_y, self.current_car_display)
			time.sleep(.5)
			if not evaluation:
				break
			self.my_car.choose_step()
			self.my_car.drive()
			self.old_pos_x = self.new_pos_x

	def evaluate_position(self):
		""" Decide if this is a valid position based
		on the track composition
		"""
		if self.new_pos_x == 3:
			self.new_pos_x = 2
			self.current_car_display = 8
			outcome = False
		elif self.new_pos_x == -1:
			self.new_pos_x = 0
			self.current_car_display = 8
			outcome = False
		elif self.my_way[self.new_pos_y][self.new_pos_x] == 1:
			self.current_car_display = 8
			outcome = False
		else:
			self.current_car_display = 7
			outcome = True
		
		return outcome


class Track:
	""" The track consists of # km. Each km can
	contain vehicles on the way (marked as '1')
	"""
	def __init__(self, timestamp):
		self.timestamp = timestamp
		self.initial_way = [[0, 0, 0], 
							[0, 0, 0], 
							[0, 0, 0], 
							[0, 0, 0], 
							[0, 0, 0], 
							[0, 0, 0], 
							[0, 0, 0], 
							[0, 0, 0], 
							[0, 0, 0]]
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
		with open("log_{}.txt".format(self.timestamp), 'a') as log:
			log.write(str("Logging Track:\n"))
			for row in self.way:
				print(row)
				log.write("{}\n".format(str(row)))


def clear_screen():
	""" Remove all console output """
	os.system('cls' if os.name == 'nt' else 'clear')



if __name__ == '__main__':
	Game = Game()
	Game.start_game()
