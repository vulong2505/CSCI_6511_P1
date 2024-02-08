from n_puzzle import *
from a_star import *


def load_file(file_path):
    puzzle_data = []

    with open(file_path, 'r') as file:
        for line in file.readlines():
            puzzle_data.append(list(map(int, line.split('\t'))))

    blank_row, blank_col = find_blank_tile(puzzle_data)

    return NPuzzle(size=len(puzzle_data), state=puzzle_data, blank_row=blank_row, blank_col=blank_col)


def print_solution_path(solution_path):
    if solution_path is None:
        print("No solution found.")
        return
    else:
        print(f"Solution path found in {len(solution_path) - 1} steps:")
        for step_number, path in enumerate(solution_path):
            print(f"Step {step_number}:")
            print(path)
            print()


def find_blank_tile(puzzle):
    for i, row in enumerate(puzzle):
        if 0 in row:
            blank_row = i
            blank_col = row.index(0)

    return blank_row, blank_col


if __name__ == "__main__":
    unsolved_puzzle = load_file("n-puzzle.txt") # Edit file name as needed
    soln_path = A_star_search(unsolved_puzzle)
    print_solution_path(soln_path)