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
		self.pos_x = 0
		self.pos_y = 0
		self.status = None
		cls()
		while self.pos_y <= My_Track.max_y and self.status != 'crashed':
			self.drive_forward()
		
	def drive_forward(self):
		""" Drive one km forward, check the position and display the track to the screen """
		self.check_position()
		My_Track.show_track(self.pos_x, self.pos_y, self.status)
		self.choose_step()
		time.sleep(3)
		cls()

	def choose_step(self):
		""" Let us choose randomly a change of position """
		next_turn = random.randint(-1,1)
		self.pos_x += next_turn
		self.pos_y += 1

	def check_position(self):
		""" Check that the car didnt crash into the wall """
		if self.pos_x <= My_Track.max_x and self.pos_x >= My_Track.min_x:
			return
		else:
			self.status = 'crashed'
			My_Track.show_track(self.pos_x, self.pos_y, self.status)


class CarState:
	""" The state changes every km. Will contain information on the previous states """
	def __init__(self):


class Track:
	def __init__(self):
		self.min_x = -1
		self.max_x = 1
		self.min_y = 0
		self.max_y = 10

	def show_track(self, pos_x, pos_y, status):
		self.car_display = 'v'
		self.empty_display = '-'
		for i in range(0, self.max_y + 1):
			row_display = ''
			for j in range(-1, self.max_x + 1):
				if pos_y == i and pos_x == j:
					row_display = row_display + '|' + self.car_display
				elif status == 'crashed':
					row_display = '|x|x|x'
					status = None
					continue
				else:
					row_display = row_display + '|' + self.empty_display
			print(row_display + '|')


def cls():
	""" Clear the screen """
	os.system('cls' if os.name=='nt' else 'clear')

if __name__ == '__main__':
	My_Track = Track()
	Car()

