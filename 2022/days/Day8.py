from utils import AoCDay
from itertools import groupby

class Day8(AoCDay):
    # TODO: Rewrite using actual graphs for a real challenge
    def part1(self):
        grid = []
        for line in self.lines:
            grid.append([(int(c), False) for c in line.strip()])

        # Count the number of visible trees

        num_visible = 0

        for r in range(len(grid)):
            for c in range(len(grid[r])):
                # Check if this tree is visible from the left edge
                visible_from_left = True
                for i in range(c):
                    if grid[r][i][0] >= grid[r][c][0]:
                        visible_from_left = False
                        break
                # Check if this tree is visible from the top edge
                visible_from_top = True
                for i in range(r):
                    if grid[i][c][0] >= grid[r][c][0]:
                        visible_from_top = False
                        break

                # Check if this tree is visible from the right edge
                visible_from_right = True
                for i in range(len(grid[r])-1, c, -1):
                    if grid[r][i][0] >= grid[r][c][0]:
                        visible_from_right = False
                        break
                # Check if this tree is visible from the bottom edge
                visible_from_bottom = True
                for i in range(len(grid)-1, r, -1):
                    if grid[i][c][0] >= grid[r][c][0]:
                        visible_from_bottom = False
                        break
                # If this tree is visible from any edge, increment the count
                if visible_from_left or visible_from_top or visible_from_right or visible_from_bottom:
                    num_visible += 1
                    grid[r][c] = (grid[r][c][0], True)

        # Print the result
        self.p1 = num_visible
        # for r in grid:
        #     print(r)

    def part2(self):
        grid = []
        for line in self.lines:
            grid.append([int(c) for c in line.strip()])

        # Initialize the maximum scenic score to 0
        max_score = 0

        # Loop through each tree in the grid
        for r in range(len(grid)):
            for c in range(len(grid[r])):
                # Calculate the viewing distance in the up direction
                up_distance = 0
                for i in range(r-1, -1, -1):
                    up_distance += 1
                    if grid[i][c] >= grid[r][c]:
                        break
                # Calculate the viewing distance in the down direction
                down_distance = 0
                for i in range(r+1, len(grid)):
                    down_distance += 1
                    if grid[i][c] >= grid[r][c]:
                        break
                # Calculate the viewing distance in the left direction
                left_distance = 0
                for i in range(c-1, -1, -1):
                    left_distance += 1
                    if grid[r][i] >= grid[r][c]:
                        break
                # Calculate the viewing distance in the right direction
                right_distance = 0
                for i in range(c+1, len(grid[r])):
                    right_distance += 1
                    if grid[r][i] >= grid[r][c]:
                        break
                # Calculate the scenic score for this tree
                score = up_distance * down_distance * left_distance * right_distance
                # Update the maximum scenic score if necessary
                max_score = max(max_score, score)

        # Print the result
        self.p2 = max_score
