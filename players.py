import random
import time
import pygame
import math
from copy import deepcopy
#this is the extra package to import
import sys
#from connect4 import *
MAX_INT = 2**64 - 1
#sys.setrecursionlimit(150000)
class connect4Player(object):
	def __init__(self, position, seed=0):
		self.position = position
		self.opponent = None
		self.seed = seed
		random.seed(seed)

	def play(self, env, move):
		move = [-1]

class human(connect4Player):

	def play(self, env, move):
		move[:] = [int(input('Select next move: '))]
		while True:
			if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
				break
			move[:] = [int(input('Index invalid. Select next move: '))]

class human2(connect4Player):

	def play(self, env, move):
		done = False
		while(not done):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					posx = event.pos[0]
					if self.position == 1:
						pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
					else: 
						pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))
					move[:] = [col]
					done = True

class randomAI(connect4Player):

	def play(self, env, move):
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		move[:] = [random.choice(indices)]

class stupidAI(connect4Player):

	def play(self, env, move):
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		if 3 in indices:
			move[:] = [3]
		elif 2 in indices:
			move[:] = [2]
		elif 1 in indices:
			move[:] = [1]
		elif 5 in indices:
			move[:] = [5]
		elif 6 in indices:
			move[:] = [6]
		else:
			move[:] = [0]

#------------------------------------------------------------MinimaxAI----------------------------------------------------------------
class minimaxAI(connect4Player):

	count_arr = [[[0, 0, 0] for i in range(4)] for j in range(2)]
	eval_arr = [0, 0]
	switch = {1: 2, 2: 1}

	def update_count(self, env, player, c):
		r = env.topPosition[c] + 1
		# row count
		count = 0
		env.board[r, c] = 0
		for j in range(env.shape[1]):
			if env.board[r, j] == player:
				count += 1
			elif count >= 4:
				return
			elif count > 0:
				self.count_arr[player - 1][0][count - 1] -= 1
				count = 0
		if count >= 4:
			return
		elif count > 0:
			self.count_arr[player - 1][0][count - 1] -= 1
		env.board[r, c] = player
		count = 0
		for j in range(env.shape[1]):
			if env.board[r, j] == player:
				count += 1
			elif count >= 4:
				return
			elif count > 0:
				self.count_arr[player - 1][0][count - 1] += 1
				count = 0
		if count >= 4:
			return
		elif count > 0:
			self.count_arr[player - 1][0][count - 1] += 1

		# column count
		env.board[r, c] = 0
		count = 0
		for i in range(env.shape[0]):
			if env.board[i, c] == player:
				count += 1
			elif count >= 4:
				return
			elif count > 0:
				self.count_arr[player - 1][1][count - 1] -= 1
				count = 0
		if count >= 4:
			return
		elif count > 0:
			self.count_arr[player - 1][1][count - 1] -= 1
		env.board[r, c] = player
		count = 0
		for i in range(env.shape[0]):
			if env.board[i, c] == player:
				count += 1
			elif count >= 4:
				return
			elif count > 0:
				self.count_arr[player - 1][1][count - 1] += 1
				count = 0
		if count >= 4:
			return
		elif count > 0:
			# print("line 394:player: {}, count:{}".format(player, count))
			self.count_arr[player - 1][1][count - 1] += 1
		# negative diagonal
		min_row = r
		min_col = c
		while min_row > 0 and min_col > 0:
			min_row -= 1
			min_col -= 1
		d_row = min_row
		d_col = min_col
		count = 0
		env.board[r, c] = 0
		while d_row < env.shape[0] and d_col < env.shape[1]:
			if env.board[d_row][d_col] == player:
				count += 1
			elif count > 0:
				self.count_arr[player - 1][2][count - 1] -= 1
				count = 0
			d_row += 1
			d_col += 1
		if count >= 4:
			return
		elif count > 0:
			self.count_arr[player - 1][2][count - 1] -= 1

		d_row = min_row
		d_col = min_col
		count = 0
		env.board[r, c] = player
		while d_row < env.shape[0] and d_col < env.shape[1]:
			if env.board[d_row][d_col] == player:
				count += 1
			elif count >= 4:
				return
			elif count > 0:
				self.count_arr[player - 1][2][count - 1] += 1
				count = 0
			d_row += 1
			d_col += 1
		if count >= 4:
			return
		elif count > 0:
			self.count_arr[player - 1][2][count - 1] += 1
		min_row = r
		min_col = c
		while min_row < env.shape[0] - 1 and min_col > 0:
			min_row += 1
			min_col -= 1
		d_row = min_row
		d_col = min_col
		count = 0
		env.board[r, c] = 0
		while d_row >= 0 and d_col < env.shape[1]:
			if env.board[d_row][d_col] == player:
				count += 1
			elif count >= 4:
				return
			elif count > 0:
				self.count_arr[player - 1][3][count - 1] -= 1
				count = 0
			d_row -= 1
			d_col += 1
		if count >= 4:
			return
		elif count > 0:
			self.count_arr[player - 1][3][count - 1] -= 1
		d_row = min_row
		d_col = min_col
		count = 0
		env.board[r, c] = player
		while d_row >= 0 and d_col < env.shape[1]:
			if env.board[d_row][d_col] == player:
				count += 1
			elif count >= 4:
				return
			elif count > 0:
				self.count_arr[player - 1][3][count - 1] += 1
				count = 0
			d_row -= 1
			d_col += 1
		if count >= 4:
			return
		elif count > 0:
			self.count_arr[player - 1][3][count - 1] += 1

	def count_total(self, num_count, player):
		ret = 0
		for i in range(4):
			ret += self.count_arr[player-1][i][num_count-1]
		return ret

	def eval(self, env, player, c):
		#self.count_update(env, player, c)
		# print("eval state:\n{}".format(state))

		eval_value = 2 * self.count_total(1, player) + 25 * self.count_total(2, player) + 1000 * self.count_total(3, player)
		eval_value += self.weight_eval(env.board, player)
		# print("eval value:\n{}".format(eval_value))
		self.eval_arr[player-1] = eval_value
		return eval_value

	def weight_eval(self, state, mark):
		total_weight = 0
		# print("the length of sate is:{}".format(len(state)))
		weight = [[4, 20, 32, 72, 32, 20, 4] for i in range(len(state))]
		for i in range(len(state)):
			for j in range(len(state[0])):
				if state[i][j] == mark:
					total_weight += weight[i][j]
		return total_weight

	def Max(self, env, move, depth, player):
		#print("max depth :{}".format(depth))
		env.visualize = False

		if env.gameOver(move, self.opponent.position):
			return -100000
		if depth == 0:
			return -self.eval(env, self.opponent.position, move)
		value = -MAX_INT
		ori_count = deepcopy(self.count_arr)
		for c in range(env.shape[1]):
			r = env.topPosition[c]
			if r != -1:
				env.board[r][c] = player
				env.topPosition[c] -= 1
				self.update_count(env, player, c)
				#print("child in max is:\n{}".format(env.board))
				#print("count arr is {}".format(self.count_arr))
				max_val = self.Min(deepcopy(env), c, depth - 1, self.switch[player])
				value = max(value, max_val)

				#print("value in max is {}".format(max_val))
				self.count_arr = deepcopy(ori_count)
				env.board[r][c] = 0
				env.topPosition[c] += 1

		#print("max return :{}".format(value))
		return value

	def Min(self, env, move, depth, player):
		#env = deepcopy(env)
		env.visualize = False

		if env.gameOver(move, self.position):
			return 100000
		if depth == 0:
			return self.eval(env, self.position, move)
		value = MAX_INT
		ori_count = deepcopy(self.count_arr)

		for c in range(env.shape[1]):
			r = env.topPosition[c]
			if r != -1:
				env.board[r][c] = player
				env.topPosition[c] -= 1
				self.update_count(env, player, c)
				#print("child in min is:\n{}".format(env.board))
				#print("count arr is {}".format(self.count_arr))
				min_val = self.Max(deepcopy(env), c, depth - 1, self.switch[player])
				value = min(value, min_val)

				#print("value in min is {}".format(min_val))
				self.count_arr = deepcopy(ori_count)
				env.board[r][c] = 0
				env.topPosition[c] += 1
		#print("min return :{}".format(value))
		return value

	def minimax_decision(self, env, depth, player):
		#print("minimax depth :{}".format(depth))
		#env = deepcopy(env)
		env.visualize = False
		value = -MAX_INT
		decision_list = []
		ori_count = deepcopy(self.count_arr)
		for c in range(env.shape[1]):
			r = env.topPosition[c]
			if r != -1:
				env.board[r][c] = player
				env.topPosition[c] -= 1
				self.update_count(env, player, c)
				#print("child in minimax decision is:\n{}".format(env.board))
				#print("count arr is {}".format(self.count_arr))
				min_eval = self.Min(deepcopy(env), c, depth - 1, self.switch[player])
				decision_list.append((c, min_eval))
				value = max(value, min_eval)


				env.board[r][c] = 0
				env.topPosition[c] += 1
				self.count_arr=deepcopy(ori_count)
				# print("original_board:\n{}".format(state))
				#print("last evaluation value:{}".format(decision_list[-1][1]))

		move = []
		for i in range(len(decision_list)):
			if value == decision_list[i][1]:
				move.append(decision_list[i][0])
		#print("minimax value:{}".format(value))
		#print("minimax move:{}".format(move))
		return move

	def play(self, env, move):
		#print("--------------step start---------")
		#print("--------------step start---------")
		#print("--------------step start---------")
		#print("--------------max_int---------:{}".format(MAX_INT))
		if len(env.history[0]) > 0:
			last_1_col = env.history[0][-1]
			#print("last 1 column:{}".format(last_1_col))
			self.update_count(env, 1, last_1_col)
		if len(env.history[1]) > 0:
			last_2_col = env.history[1][-1]
			#print("last 2 column:{}".format(last_2_col))
			self.update_count(env, 2, last_2_col)
		move[:] = self.minimax_decision(deepcopy(env), 2, self.position)
		#print("move out of function:{}".format(move))
		# print("out of function")



#------------------------------------------------------------alphaBetaAI----------------------------------------------------------------
class alphaBetaAI(connect4Player):
	count_arr = [[[0, 0, 0] for i in range(4)] for j in range(2)]
	eval_arr = [0, 0]
	switch = {1: 2, 2: 1}

	def update_count(self, env, player, c):

		r = env.topPosition[c] + 1
		# row count
		count = 0
		env.board[r, c] = 0
		for j in range(env.shape[1]):
			if env.board[r, j] == player:
				count += 1
			elif count >= 4:
				return
			elif count > 0:
				self.count_arr[player - 1][0][count - 1] -= 1
				count = 0
		if count >= 4:
			return
		elif count > 0:
			self.count_arr[player - 1][0][count - 1] -= 1
		env.board[r, c] = player
		count = 0
		for j in range(env.shape[1]):
			if env.board[r, j] == player:
				count += 1
			elif count >= 4:
				return
			elif count > 0:
				self.count_arr[player - 1][0][count - 1] += 1
				count = 0
		if count >= 4:
			return
		elif count > 0:
			self.count_arr[player - 1][0][count - 1] += 1

		# column count
		env.board[r, c] = 0
		count = 0
		for i in range(env.shape[0]):
			if env.board[i, c] == player:
				count += 1
			elif count >= 4:
				return
			elif count > 0:
				self.count_arr[player - 1][1][count - 1] -= 1
				count = 0
		if count >= 4:
			return
		elif count > 0:
			self.count_arr[player - 1][1][count - 1] -= 1
		env.board[r, c] = player
		count = 0
		for i in range(env.shape[0]):
			if env.board[i, c] == player:
				count += 1
			elif count >= 4:
				return
			elif count > 0:
				self.count_arr[player - 1][1][count - 1] += 1
				count = 0
		if count >= 4:
			return
		elif count > 0:
			#print("line 394:player: {}, count:{}".format(player, count))
			self.count_arr[player - 1][1][count - 1] += 1
		# negative diagonal
		min_row = r
		min_col = c
		while min_row > 0 and min_col > 0:
			min_row -= 1
			min_col -= 1
		d_row = min_row
		d_col = min_col
		count = 0
		env.board[r, c] = 0
		while d_row < env.shape[0] and d_col < env.shape[1]:
			if env.board[d_row][d_col] == player:
				count += 1
			elif count > 0:
				self.count_arr[player - 1][2][count - 1] -= 1
				count = 0
			d_row += 1
			d_col += 1
		if count >= 4:
			return
		elif count > 0:
			self.count_arr[player - 1][2][count - 1] -= 1

		d_row = min_row
		d_col = min_col
		count = 0
		env.board[r, c] = player
		while d_row < env.shape[0] and d_col < env.shape[1]:
			if env.board[d_row][d_col] == player:
				count += 1
			elif count >= 4:
				return
			elif count > 0:
				self.count_arr[player - 1][2][count - 1] += 1
				count = 0
			d_row += 1
			d_col += 1
		if count >= 4:
			return
		elif count > 0:
			self.count_arr[player - 1][2][count - 1] += 1
		min_row = r
		min_col = c
		while min_row < env.shape[0] - 1 and min_col > 0:
			min_row += 1
			min_col -= 1
		d_row = min_row
		d_col = min_col
		count = 0
		env.board[r, c] = 0
		while d_row >= 0 and d_col < env.shape[1]:
			if env.board[d_row][d_col] == player:
				count += 1
			elif count >= 4:
				return
			elif count > 0:
				self.count_arr[player - 1][3][count - 1] -= 1
				count = 0
			d_row -= 1
			d_col += 1
		if count >= 4:
			return
		elif count > 0:
			self.count_arr[player - 1][3][count - 1] -= 1
		d_row = min_row
		d_col = min_col
		count = 0
		env.board[r, c] = player
		while d_row >= 0 and d_col < env.shape[1]:
			if env.board[d_row][d_col] == player:
				count += 1
			elif count >= 4:
				return
			elif count > 0:
				self.count_arr[player - 1][3][count - 1] += 1
				count = 0
			d_row -= 1
			d_col += 1
		if count >= 4:
			return
		elif count > 0:
			self.count_arr[player - 1][3][count - 1] += 1

	def count_total(self, num_count, player):
		ret = 0
		for i in range(4):
			ret += self.count_arr[player - 1][i][num_count - 1]
		return ret

	def eval(self, env, player, c):
		# self.count_update(env, player, c)
		# print("eval state:\n{}".format(state))

		eval_value = 2 * self.count_total(1, player) + 25 * self.count_total(2, player) + 1000 * self.count_total(3,
																												  player)
		eval_value += self.weight_eval(env.board, player)
		# print("eval value:\n{}".format(eval_value))
		self.eval_arr[player - 1] = eval_value
		return eval_value

	def weight_eval(self, state, mark):
		total_weight = 0
		# print("the length of sate is:{}".format(len(state)))
		weight = [[4, 20, 32, 72, 32, 20, 4] for i in range(len(state))]
		for i in range(len(state)):
			for j in range(len(state[0])):
				if state[i][j] == mark:
					total_weight += weight[i][j]
		return total_weight

	def Max(self, env, move, depth, player, alpha, beta):
		# print("max depth :{}".format(depth))
		#env.visualize = False

		if env.gameOver(move, self.switch[self.position]):
			return -100000
		if depth == 0:
			return -self.eval(env, self.opponent.position, move)
		value = -MAX_INT
		ori_count = deepcopy(self.count_arr)
		for c in range(env.shape[1]):
			r = env.topPosition[c]
			if r != -1:
				env.board[r][c] = player
				env.topPosition[c] -= 1
				self.update_count(env, player, c)
				# print("child in max is:\n{}".format(env.board))
				# print("count arr is {}".format(self.count_arr))
				max_val = self.Min(deepcopy(env), c, depth - 1, self.switch[player], alpha, beta)
				value = max(value, max_val)
				alpha = max(alpha, value)
				# print("value in max is {}".format(max_val))
				self.count_arr = deepcopy(ori_count)
				env.board[r][c] = 0
				env.topPosition[c] += 1
				if value >= beta:
					break
		# print("max return :{}".format(value))
		return value

	def Min(self, env, move, depth, player, alpha, beta):
		# env = deepcopy(env)
		#env.visualize = False

		if env.gameOver(move, self.position):
			return 100000
		if depth == 0:
			return self.eval(env, self.position, move)
		value = MAX_INT
		ori_count = deepcopy(self.count_arr)

		for c in range(env.shape[1]):
			r = env.topPosition[c]
			if r != -1:
				env.board[r][c] = player
				env.topPosition[c] -= 1
				self.update_count(env, player, c)
				# print("child in min is:\n{}".format(env.board))
				# print("count arr is {}".format(self.count_arr))
				min_val = self.Max(deepcopy(env), c, depth - 1, self.switch[player], alpha, beta)
				value = min(value, min_val)
				beta = min(beta, value)
				# print("value in min is {}".format(min_val))
				self.count_arr = deepcopy(ori_count)
				env.board[r][c] = 0
				env.topPosition[c] += 1
				if value <= alpha:
					break
		# print("min return :{}".format(value))
		return value

	def minimax_decision(self, env, depth, player, alpha, beta):
		# print("minimax depth :{}".format(depth))
		env = deepcopy(env)
		env.visualize = False
		value = -MAX_INT
		decision_list = []
		ori_count = deepcopy(self.count_arr)
		for c in range(env.shape[1]):
			r = env.topPosition[c]
			if r != -1:
				env.board[r][c] = player
				env.topPosition[c] -= 1
				self.update_count(env, player, c)
				# print("child in minimax decision is:\n{}".format(env.board))
				# print("count arr is {}".format(self.count_arr))
				min_eval = self.Min(deepcopy(env), c, depth - 1, self.switch[player], alpha, beta)
				decision_list.append((c, min_eval))
				value = max(value, min_eval)
				alpha = max(alpha, value)
				env.board[r][c] = 0
				env.topPosition[c] += 1
				self.count_arr = deepcopy(ori_count)
				if value >= beta:
					break
		# print("original_board:\n{}".format(state))
		# print("last evaluation value:{}".format(decision_list[-1][1]))

		move = []
		for i in range(len(decision_list)):
			if value == decision_list[i][1]:
				move.append(decision_list[i][0])
		# print("minimax value:{}".format(value))
		# print("minimax move:{}".format(move))
		return move

	def play(self, env, move):
		# print("--------------step start---------")
		# print("--------------step start---------")
		# print("--------------step start---------")
		# print("--------------max_int---------:{}".format(MAX_INT))
		#env.visualize = False
		if len(env.history[0]) > 0:
			last_1_col = env.history[0][-1]
			# print("last 1 column:{}".format(last_1_col))
			self.update_count(env, 1, last_1_col)
		if len(env.history[1]) > 0:
			last_2_col = env.history[1][-1]
			# print("last 2 column:{}".format(last_2_col))
			self.update_count(env, 2, last_2_col)
		move[:] = self.minimax_decision(deepcopy(env), 2, self.position, -MAX_INT, MAX_INT)
		#print("out of move:{}".format(move))



SQUARESIZE = 100
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)




