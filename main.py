""" Control the reinforcement algorithm
over multiple training episodes
"""
import time
from datetime import datetime

from learning import Learning
from model_objects import Car, Track



class Game_Episode:
	""" Control the game board and its elements"""
	
	def __init__(self, Learning, episode, timestamp, time_between_step, mode):
		""" Run an episode in mode test/train """
		self.Learning = Learning
		self.Q = self.Learning.retrieve_q_matrix()
		self.episode = episode
		self.timestamp = timestamp
		self.my_track = Track(self.timestamp, self.episode, mode)
		self.my_car = Car()
		self.my_way = self.my_track.retrieve_way()

		self.step = 0
		self.current_car_display = None
		self.new_pos_x = None
		self.new_pos_y = None
		self.old_pos_x = 2
		self.time_between_step = time_between_step

	def run_train_episode(self):
		""" Start a training episode:
		- Move the car along the track until an accident occurs.
		- The horizontal navigation is randomly chosen
		- Update the Q matrix
		"""

		while self.step < 9:
			self.step += 1
			
			self.new_pos_x, self.new_pos_y = self.my_car.retrieve_pos()
			evaluation = self.evaluate_position()
			self.Learning.update_q(self.new_pos_x, self.old_pos_x, self.episode)

			self.my_track.update_track(self.new_pos_x, self.new_pos_y, self.car_display)
			#time.sleep(self.time_between_step)
			if not evaluation:
				break
			self.my_car.random_step()
			self.my_car.drive()
			self.old_pos_x = self.new_pos_x

	def run_test_episode(self):
		""" Start a test episode:
		- Decide based on the values in the Q matrix
		on the best step to take
		- Move the car along the track
		"""

		while self.step < 9:
			self.step += 1
			
			self.new_pos_x, self.new_pos_y = self.my_car.retrieve_pos()
			evaluation = self.evaluate_position()

			self.my_track.update_track(self.new_pos_x, self.new_pos_y, self.car_display)
			time.sleep(self.time_between_step)
			if not evaluation:
				break
			self.my_car.smart_step(self.Q)
			self.my_car.drive()
			self.old_pos_x = self.new_pos_x

	def evaluate_position(self):
		""" Decide if this is a valid position based
		on the track composition
		"""

		if self.my_way[self.new_pos_y][self.new_pos_x] == 1:
			self.car_display = 8
			outcome = False
		else:
			self.car_display = 7
			outcome = True
		
		return outcome


class Game:
	""" Loop over multiple episodes to
	train the reinforcement model
	"""
	def __init__(self, total_episodes, time_training_step, time_testing_step):
		self.timestamp = datetime.now().strftime('%Y%m%d_%H_%M_%S')
		self.Learning = Learning(self.timestamp)
		self.total_episodes = total_episodes

	def train_model(self):
		""" Run the model a multiple number of times
		to fill the Q matrix
		"""
		for episode in range(self.total_episodes):
			Episode = Game_Episode(self.Learning, episode, self.timestamp, time_training_step, "train")
			Episode.run_train_episode()
		

	def test_prediction(self):
		""" Using the filled Q matrix, test the learned parameters """
		Episode = Game_Episode(self.Learning, self.total_episodes, self.timestamp, time_testing_step, "test")
		Episode.run_test_episode()


if __name__ == '__main__':
	# Define the number of episodes to train the model
	episodes_nr = 10
	# Define the time in seconds to wait between making each step
	time_training_step = 0
	time_testing_step = 1
	Game = Game(episodes_nr, time_training_step, time_testing_step)
	# Train the car on the track
	Game.train_model()
	# After training, test the track using the learned parameters
	Game.test_prediction()
