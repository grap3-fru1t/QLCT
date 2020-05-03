""" Control the reinforcement algorithm
over multiple training episodes
"""
import os
import time
from datetime import datetime
import pickle
import matplotlib.pyplot as plt
import numpy as np
from learning import Learning
from model_objects import Agent, Track


class Game_Episode:
	""" Control the board and its elements.
	Execute one game instance = one episode.

	During the episode the object is trying
	semi-randomly to choose its path to reach the goal.
	"""

	def __init__(self, Learning, Track, episode, timestamp, time_between_step):
		""" Run an episode in mode test/train """
		
		self.episode = episode
		self.timestamp = timestamp
		self.my_track = Track
		# Call the instance to reset the track
		self.my_track(self.episode)
		self.my_way = self.my_track.retrieve_way()
		self.track_dimensions = self.my_way.shape
		self.my_agent = Agent(self.track_dimensions)
		
		self.Learning = Learning
		self.Q = self.Learning.retrieve_q_matrix()

		self.step = 0
		self.current_agent_display = None
		self.new_pos_x, self.new_pos_y = None, None
		self.old_pos_x, self.old_pos_y = 2, 0
		self.time_between_step = time_between_step
		self.episode_moves = []

	def run_train_episode(self):
		""" Execute one training episode
		- Make a move along the track
		- Update the track view
		- Update the Q matrix
		"""
		# The agent is allowed to crash twice
		self.life = 3
		while self.step < self.track_dimensions[0] and self.life > 0:
			self.step += 1
			
			self.new_pos_x, self.new_pos_y = self.my_agent.retrieve_pos()
			outcome, reward = self.evaluate_position()
			# Save the next move into the list
			self.episode_moves.append([self.new_pos_x, self.new_pos_y])
			# Update the Q learning matrix
			if self.step > 1:
				self.Q = self.Learning.update_q([self.new_pos_x, self.new_pos_y], [self.old_pos_x, self.old_pos_y], reward, self.episode)
			self.Learning.save_numbers(self.episode)
			self.my_track.update_track(self.new_pos_x, self.new_pos_y, self.agent_display)
			time.sleep(self.time_between_step)

			# Stop the current episode if an accident occurs
			if not outcome:
				break
			self.my_agent.random_step(self.Q)
			self.my_agent.drive()
			self.old_pos_x, self.old_pos_y = self.new_pos_x, self.new_pos_y
			
		return self.episode_moves

	def run_test_episode(self):
		""" Start a test episode:
		- Decide based on the values in the Q matrix
		on the best step to take
		- Move the agent along the track
		"""
		# The agent is allowed to crash twice
		self.life = 3
		while self.step < self.track_dimensions[0]:
			self.step += 1
			
			self.new_pos_x, self.new_pos_y = self.my_agent.retrieve_pos()
			outcome, reward = self.evaluate_position()
			# Save the next move into the list
			self.episode_moves.append([self.new_pos_x, self.new_pos_y])

			self.my_track.update_track(self.new_pos_x, self.new_pos_y, self.agent_display)
			time.sleep(self.time_between_step)

			# Stop the current episode if an accident occurs
			if not outcome:
				break
			self.my_agent.smart_step(self.Q)
			self.my_agent.drive()
			self.old_pos_x = self.new_pos_x
		return self.episode_moves

	def evaluate_position(self):
		""" Decide if this is a valid position based
		on the track composition
		"""
		# if the agent crashes against a wall or an abstacle, reward should be negative
		if self.my_way[self.new_pos_y, self.new_pos_x] == 1:
			self.agent_display = 8
			outcome = False
			reward = -1
		# If an obstacle is found, dmg is added to the car
		elif self.my_way[self.new_pos_y, self.new_pos_x] == 2:
			self.agent_display = 8
			outcome = True
			reward = 0
			self.life -= 1
		# if the agent doesn't crash, reinforce
		else:
			self.agent_display = 7
			outcome = True
			reward = 1
		return outcome, reward


class Game:
	""" Loop over multiple episodes to
	train the reinforcement model
	"""
	def __init__(self, total_episodes, time_training_step, time_testing_step):
		self.timestamp = datetime.now().strftime('%Y%m%d_%H_%M_%S')
		# Ínitialize a track instance
		self.Track = Track(self.timestamp)
		# Return the shape of the track
		self.way, self.dims = self.Track.retrieve_way(), self.Track.retrieve_way().shape
		# Initiate the Learning module using the dimensions of the track
		self.Learning = Learning(self.timestamp, self.dims)
		self.total_episodes = total_episodes
		# setup
		self.setup()


	def setup(self):
		""" Setup the logs """
		self.all_episodes_moves = []
		# setup the folders for the logs
		if not os.path.isdir(os.path.join(os.getcwd(), "logs")):
			os.path.mkdir(os.path.join(os.getcwd(), "logs"))
		# Prepare the logging
		log_num_name = "{timestamp}_log_numerics.csv".format(timestamp=self.timestamp)
		self.log_num_path = os.path.join(os.getcwd(), "logs", log_num_name)
		plot_name = "{timestamp}_plot.png".format(timestamp=self.timestamp)
		self.plot_path = os.path.join(os.getcwd(), "logs", plot_name)
		moves_name = "all_moves.obj".format(timestamp=self.timestamp)
		self.moves_path = os.path.join(os.getcwd(), "logs", moves_name)
		topology_name = "track_topology.npy".format(timestamp=self.timestamp)
		self.topology_path = os.path.join(os.getcwd(), "logs", topology_name)

		# Save the track condition
		np.save(self.topology_path, np.asarray(self.way))
		

	def train_model(self):
		""" Run the model a multiple number of times
		to fill the Q matrix
		"""
		for episode in range(self.total_episodes):
			Episode = Game_Episode(self.Learning, self.Track, episode, self.timestamp, time_training_step)
			episode_moves = Episode.run_train_episode()
			self.all_episodes_moves.append(episode_moves)

	def test_prediction(self):
		""" Using the filled Q matrix, test the learned parameters """
		for episode in range(self.total_episodes, self.total_episodes + 1):
			Episode = Game_Episode(self.Learning, self.Track, episode, self.timestamp, time_testing_step)
			episode_moves = Episode.run_test_episode()
			self.all_episodes_moves.append(episode_moves)

	def clean_up(self):
		""" Visualize the learning parameters.
		Save the parameters in a separate file
		"""
		
		# Save the moves for every episode to a file
		with open(self.moves_path, 'wb') as log:
			pickle.dump(self.all_episodes_moves, log)

		# Retrieve the learning parameters from each step performed
		parameters = np.round(np.array(self.Learning.retrieve_l_parameters()), 2)
		plt.plot(parameters[:, 0], parameters[:, 2], color='lightblue', linewidth=3)
		plt.title("Q Learning process")
		plt.xlabel("Episode")
		plt.ylabel("Sum of squared Q matrix elements")
		plt.savefig(self.plot_path)
		plt.show()
		# Save the learning parameters explicitly to a file
		with open(self.log_num_path, 'w') as log:
			log.write(str(parameters) + "\n")


if __name__ == '__main__':
	# Define the number of episodes to train the model
	episodes_nr = 150
	# Define the time in seconds to wait between making each step
	time_training_step = 0
	time_testing_step = 0
	Game = Game(episodes_nr, time_training_step, time_testing_step)
	# Train the agent on the track
	Game.train_model()
	# After training, test the track using the learned parameters
	Game.test_prediction()
	Game.clean_up()
	
