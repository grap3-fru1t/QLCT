import time
import sys
import random
import os

class Car:
	def __init__(self):
		""" The car can take positions -1,0,1 on the track,
		Every turn the car can move one position to the left or
		one position to the right
		"""
		self.pos = 0
		self.km = 0
		print("Starting game")
		self.start_turn()


	def start_turn(self):
		""" Compare the current position of the car
		with the position of other vehicles on the road (marked as 1).
		Also keep the track that the car stays on the road (does not leave the positions -1,0,1)
		"""
		while self.km < 9:
			self.current = my_track(self.km)
			self.km += 1
			print("My new position is {}".format(self.pos))
			if self.pos == -2 or self.pos == 2 or self.current[int(self.pos +1)] == 1:
				self.crash()
			else:
				self.choose_step()
				self.start_turn()
				time.sleep(1)
		else:
			print("You won!")
			sys.exit()

	def choose_step(self):
		""" Let us choose randomly a change of position """
		next_turn = random.randint(-1,1)
		self.pos += next_turn

	def crash(self):
		""" End the game if the car crashed into a wall or into another vehicle """
		if self.pos == 2 or self.pos == -2:
			print("Crashed into a wall. Restart game.")
		else:
			print("Crashed into a vehicle. Restart game.")
		sys.exit()


class Track:
	""" The track consists of # km. Each km can 
	contain vehicles on the way (marked as '1')
	"""
	def __init__(self):
		self.way = [[0,0,0], [0,0,0], [1,0,0], [0,0,0], [0,0,1], [0,0,0], [1,0,0], [0,0,0], [0,0,0]]
		self.width = 3
		self.show_track()

	def __call__(self, km):
		self.km = self.way[km]
		return(self.km)
		print(self.km)

	def show_track(self):
		for row in self.way:
			print(row)
		time.sleep(3)
		self.clear_screen()

	def clear_screen(self):
	    os.system('cls' if os.name=='nt' else 'clear')




if __name__ == '__main__':
	my_track = Track()
	Car()

