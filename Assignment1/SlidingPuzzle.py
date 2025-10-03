import heapq
import numpy as np

class SlidingTilePuzzle:
    def __init__(self, state, gVal=0, parent=None):
        self.state = tuple(state)
        self.gVal = gVal
        self.hVal = self.heuristicCost()
        self.fval = self.gVal + self.hVal
        self.parent = parent
        
    def __lt__(self, other):
        return self.fval < other.fval

    def isGoalState(self):
        # Create the current list of tiles with the blank removed
        tiles = [t for t in self.state if t != ' ']
        # Check that the first 3 tiles are 'W' and the last 3 tiles are 'B'
        return tiles[:3] == ['W', 'W', 'W'] and tiles[3:] == ['B', 'B', 'B']

    def printBoard(self, state):
        top =    "┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓"
        bottom = "┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛"
        print(top)
        print("┃", end="")
        for val in state:
            print(f" {val} ┃", end="")
        print()
        print(bottom)

    def heuristicCost(self):
        # Score tiles based on the number of misplaced tiles
        #   White tiles should have no black tiles to the left of them
        #   Black tiles should have no white tiles to the right of them

        cost = 0
        for i, tile in enumerate(self.state):
            # Count the number of black tiles to the left of the white tile
            if tile == 'W':
                for j in range(i):
                    if self.state[j] == 'B':
                        cost += 1
            # Count the number of white tiles to the right of the black tile
            elif tile == 'B':
                for j in range(i + 1, 7):
                    if self.state[j] == 'W':
                        cost += 1
        return cost

    def getMoves(self):
        blankPos = self.state.index(' ')
        possibleMoves = []

        for i, tile in enumerate(self.state):
            # Skip the blank tile
            if tile == ' ':
                continue

            distance = abs(i - blankPos)
            # Check if the move is valid (tiles can only jump up to 2 other tiles)
            if distance >= 4:
                continue
            # Update the g-value based on the distance of the move
            else:
                if distance == 1:
                    self.gVal += 1
                elif distance > 1:
                    self.gVal += distance - 1
                else:
                    continue

                # Create a deep copy of the current state
                newState = np.array(self.state, copy=True)
                # Swap the blank tile with the current tile
                newState[i], newState[blankPos] = newState[blankPos], newState[i]
                # Add the new possible move and updated g-value and that moves parent to the list
                possibleMoves.append(SlidingTilePuzzle(newState, self.gVal, self))

        return possibleMoves

    def aStarSolution(self):
        openList = []
        visited = set()
        # Add the initial state to the open list
        heapq.heappush(openList, (self.fval, self))
        while openList:
            # take the move with the lowest f-value from the open list
            _, current = heapq.heappop(openList)
            # Check if the current state is the goal state
            if current.isGoalState():
                path = []
                solutionCost = current.gVal
                # Backtrack to find the path
                while current:
                    path.append(current.state)
                    current = current.parent
                path.reverse()
                print("Solution found:")
                counter = 0
                # print the path
                for step in path:
                    if step == path[0]:
                        print("Initial State:")
                    else:
                        print(f"Step {counter}:")
                    self.printBoard(step)
                    counter += 1
                print(f"Solution found in {len(path) - 1} moves, at a cost of {solutionCost}.")
                return
            # Mark the current state as visited
            visited.add(current.state)

            # Get all possible moves from the current state with the cost of that move added to the g-value
            possibleMoves = current.getMoves()
            for move in possibleMoves:
                heapq.heappush(openList, (move.fval, move))
        print("No solution found.")
        return None


if __name__ == "__main__":
    # Initialise the board
    initialConfig = ['B', 'B', 'B', ' ', 'W', 'W', 'W']
    puzzle = SlidingTilePuzzle(initialConfig)
    solution = puzzle.aStarSolution()

