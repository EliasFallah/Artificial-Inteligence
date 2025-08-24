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
        tiles = [t for t in self.state if t != ' ']
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
        """
        Penalize tiles based on their position:
        - White tiles should be on the left (positions 0-2)
        - Black tiles should be on the right (positions 4-6)
        """
        cost = 0
        for i, tile in enumerate(self.state):
            if tile == 'W' and i > 2:
                cost += i - 2
            elif tile == 'B' and i < 3:
                cost += 3 - i
        return cost

    def getMoves(self):
        blankPos = self.state.index(' ')
        possibleMoves = []

        for i, tile in enumerate(self.state):
            if tile == ' ':
                continue

            distance = abs(i - blankPos)
            if distance >= 4:
                continue
            else:
                if distance == 1:
                    cost = 1
                elif distance > 1:
                    cost = distance - 1
                else:
                    continue

                newState = np.array(self.state, copy=True)
                newState[i], newState[blankPos] = newState[blankPos], newState[i]
                possibleMoves.append(SlidingTilePuzzle(newState, self.gVal + cost, self))

        return possibleMoves

    def aStarSolution(self):
        openList = []
        visited = set()
        heapq.heappush(openList, (self.fval, self))
        while openList:
            _, current = heapq.heappop(openList)
            if current.isGoalState():
                path = []
                while current:
                    path.append(current.state)
                    current = current.parent
                path.reverse()
                print("Solution found:")
                counter = 0
                for step in path:
                    if step == path[0]:
                        print("Initial State:")
                    else:
                        print(f"Step {counter}:")
                    self.printBoard(step)
                    counter += 1
                print(f"Total moves: {len(path) - 1}")
                return

            visited.add(current.state)
            
            possibleMoves = current.getMoves()
            for move in possibleMoves:
                heapq.heappush(openList, (move.fval, move))

        return None


if __name__ == "__main__":
    initialConfig = ['B', 'B', 'B', ' ', 'W', 'W', 'W']
    puzzle = SlidingTilePuzzle(initialConfig)
    solution = puzzle.aStarSolution()

    if solution:
        print(f"Solution found in {len(solution) - 1} moves:")
        for step in solution:
            puzzle.printBoard(step)
    else:
        print("No solution found.")