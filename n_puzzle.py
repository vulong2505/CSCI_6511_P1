import random
import copy


class NPuzzle:
    def __init__(self, size, state=None, parent=None, blank_row=None, blank_col=None, last_direction=None):
        self.size = size
        self.parent = parent  # might deprecate it since it's not working
        self.distance_from_root = 0 if parent is None else parent.distance_from_root + 1
        self.last_direction = None
        self.successors = []

        if state is None:
          self.state_matrix = [[(i * size) + j + 1 for j in range(size)] for i in range(size)]
          self.state_matrix[size - 1][size - 1] = 0  # Blank tile
          self.blank_row = size - 1
          self.blank_col = size - 1
        else:
          self.state_matrix = state
          self.blank_row = blank_row
          self.blank_col = blank_col
          self.last_direction = last_direction

    def __str__(self):
        return '\n'.join([' '.join(['{:2}'.format(item) if item != 0 else '  ' for item in row]) for row in self.state_matrix])

    def __eq__(self, other):
        return isinstance(other, NPuzzle) and self.state_matrix == other.state_matrix

    def __hash__(self):
        return hash(tuple(map(tuple, self.state_matrix)))

    def move_possible(self, direction):
        if direction == 'UP':
            return self.blank_row > 0
        elif direction == 'DOWN':
            return self.blank_row < self.size - 1
        elif direction == 'LEFT':
            return self.blank_col > 0
        elif direction == 'RIGHT':
            return self.blank_col < self.size - 1


    def move_blank(self, direction):
        if not self.move_possible(direction):
            return None

        new_puzzle = copy.deepcopy(self)

        if direction == 'UP':
            target_row, target_col = self.blank_row - 1, self.blank_col
        elif direction == 'DOWN':
            target_row, target_col = self.blank_row + 1, self.blank_col
        elif direction == 'LEFT':
            target_row, target_col = self.blank_row, self.blank_col - 1
        else:  # 'RIGHT'
            target_row, target_col = self.blank_row, self.blank_col + 1

        # Swap the blank with the target tile
        new_puzzle.state_matrix[self.blank_row][self.blank_col], new_puzzle.state_matrix[target_row][target_col] = \
            new_puzzle.state_matrix[target_row][target_col], new_puzzle.state_matrix[self.blank_row][self.blank_col]

        return NPuzzle(self.size, state=new_puzzle.state_matrix, parent=self, blank_row=target_row, blank_col=target_col, last_direction = direction)


    def is_goal_state(self):
        counter = 1
        for row in range(self.size):
            for col in range(self.size):
                if row == self.size - 1 and col == self.size - 1:
                    continue  # Skip the blank tile check
                if self.state_matrix[row][col] != counter:
                    return False
                counter += 1
        return True


    def generate_successors(self):
        directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        for direction in directions:
            successor = self.move_blank(direction)
            if successor:
                self.successors.append(successor)
                successor.distance_from_root = self.distance_from_root + 1
        return self.successors

    def reset(self):
      self.distance_from_root = 0
      self.parent = None
      self.last_direction = None


class NPuzzleGenerator:
    def generate(size, target_move_count):
        npuzzle = NPuzzle(size)
        move_count = 0
        previous_direction = None

        while move_count < target_move_count:
            current_direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
            if NPuzzleGenerator.get_opposite_direction(current_direction) == previous_direction:
                continue
            successor = npuzzle.move_blank(current_direction)
            if successor:
                npuzzle = successor
                move_count += 1
                previous_direction = current_direction

        npuzzle.reset()
        return npuzzle


    def get_opposite_direction(direction):
        opposites = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        return opposites[direction]