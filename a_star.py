from queue import PriorityQueue
from collections import defaultdict
from itertools import count
from n_puzzle import *

import math


def A_star_search(start_puzzle):
  # f(n) Priority Queue
  open_set = PriorityQueue()

  # Tracking of previously visited states, i.e., where the current puzzle came from.
  closed_set = set()    # Used to keep track of states
  came_from = {}        # Used to backtrack and create the path

  # Default gScore is Inf
  gScore = defaultdict(lambda: math.inf)

  # Add initial tuple (f(n) heuristic of starting puzzle, starting puzzle) to the open set.
  unique_counter = count()  # Unique counter to serve as a tiebreaker in priority queue
  gScore[start_puzzle] = 0
  fScore_start = gScore[start_puzzle] + manhattan_heuristic(start_puzzle)
  open_set.put((fScore_start, next(unique_counter), start_puzzle))

  while not open_set.empty():
    current_fScore, _, current_puzzle = open_set.get()

    # Skip current_puzzle if already traversed
    if current_puzzle in closed_set:
        continue

    if current_puzzle.is_goal_state():
      return reconstruct_path(came_from, current_puzzle)

    closed_set.add(current_puzzle)

    for successor in current_puzzle.generate_successors():
      # Skip successor if already traversed
      if successor in closed_set:
        continue

      # g(n) is the backwards cost, distance from root; this is the gScore of the current puzzle, and cost of going to the next node is 1.
      tentative_gScore = gScore[current_puzzle] + 1

      if tentative_gScore < gScore[successor]:
        came_from[successor] = current_puzzle
        gScore[successor] = tentative_gScore
        fScore = tentative_gScore + manhattan_heuristic(successor)
        open_set.put((fScore, next(unique_counter), successor))

  # Open set empty and goal never reached
  return None


def manhattan_heuristic(current_puzzle):
  sum_distance = 0

  for i in range(current_puzzle.size):
    for j in range(current_puzzle.size):

      value = current_puzzle.state_matrix[i][j]

      # Skip blank
      if value == 0:
        continue

      # target_i is the row, target_j is the col
      target_i = (value - 1) // current_puzzle.size
      target_j = (value - 1) % current_puzzle.size

      # Add Manhattan distance from correct tile placement
      sum_distance += abs(i - target_i) + abs(j - target_j)

  return sum_distance


def reconstruct_path(came_from, current_puzzle):
    path = []

    while current_puzzle in came_from:
        path.append(current_puzzle)
        current_puzzle = came_from[current_puzzle]
    path.append(current_puzzle)  # Add the start state
    path.reverse()               # Since we added the path backwards, reverse the path such that it's start to goal.

    return path