from collections import deque
import heapq
import numpy as np

goalState = ([1, 2, 3],
             [8, 0, 4],
             [7, 6, 5])

initialStates = {
    "initialState1": ([2, 8, 3],
                      [1, 6, 4],
                      [7, 0, 5]),  # 5 moves

    "initialState2": ([2, 1, 6],
                      [4, 0, 8],
                      [7, 5, 3]),  # 18 moves

    "initialState3": ([5, 7, 2],
                      [0, 8, 6],
                      [4, 1, 3]),  # 21 moves

    "initialState4": ([0, 6, 5],
                      [4, 1, 7],
                      [3, 2, 8]),  # 26 moves

    "initialState5": ([0, 6, 5],
                      [4, 1, 8],
                      [3, 7, 2]),  # 26 moves

    "initialState6": ([6, 5, 7],
                      [4, 1, 0],
                      [3, 2, 8]),  # 27 moves

    "initialState7": ([6, 5, 7],
                      [4, 0, 1],
                      [3, 2, 8]),  # 28 moves

    "initialState8": ([6, 5, 7],
                      [4, 2, 1],
                      [3, 0, 8]),  # 29 moves

    "initialState9": ([5, 6, 7],
                      [0, 4, 8],
                      [3, 2, 1]),  # 29 moves

    "initialState10": ([6, 5, 7],
                       [4, 2, 1],
                       [3, 8, 0]),  # 30 moves

    "initialState11": ([0, 5, 7],
                       [6, 4, 1],
                       [3, 2, 8]),  # 30 moves

    "initialState12": ([5, 6, 7],
                       [4, 0, 8],
                       [3, 2, 1]),  # 30 moves

    "initialState13": ([2, 0, 4],
                       [1, 3, 5],
                       [7, 8, 6])  # 9 moves (not 47)
}


class EightPuzzle:
    def __init__(self, board, parent=None, gVal=0):
        self.board = board
        self.parent = parent
        self.bSize = 3
        self.goalState = (
            [1, 2, 3],
            [8, 0, 4],
            [7, 6, 5]
        )
        self.gVal = gVal
        self.hVal = self.getManhattanDistance()
        self.fVal = self.gVal + self.hVal
        
    def __gt__(self, other):
        return self.fVal > other.fVal

    def isGoalState(self):
        return np.array_equal(self.board, self.goalState)

    def validMove(self, row, col):
        return 0 <= row < self.bSize and 0 <= col < self.bSize

    def printBoard(self):
        top =    "┏━━━┳━━━┳━━━┓"
        middle = "┣━━━╋━━━╋━━━┫"
        bottom = "┗━━━┻━━━┻━━━┛"
        print(top)
        for i in range(self.bSize):
            print("┃", end="")
            for j in range(self.bSize):
                val = self.board[i][j]
                print(f" {val if val != 0 else ' '} ┃", end="")
            print()
            if i < self.bSize - 1:
                print(middle)
        print(bottom)
        print()

    # Get the current position of the blank tile
    def getBlankTile(self):
        for i in range(self.bSize):
            for j in range(self.bSize):
                if self.board[i][j] == 0:
                    return (i, j)

    # Return the possible moves from the current state
    def getMoves(self):
        possibleMoves = []
        blankPos = self.getBlankTile()
                       # Up,    Down,    Left,   Right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  

        # Iterate through the tiles in each cardinal direction of the blank tile
        for d in directions:
            newRow = blankPos[0] + d[0]
            newCol = blankPos[1] + d[1]
            # Check if the move is valid
            if self.validMove(newRow, newCol):
                # Create a deep copy of the current state
                newBoard = np.array(self.board, copy=True)
                # Swap the blank tile with the adjacent tile
                newBoard[blankPos[0]][blankPos[1]] = newBoard[newRow][newCol]
                newBoard[newRow][newCol] = 0
                # To the list of possible moves add the new state, its parent, and the g-value(increased by 1)
                possibleMoves.append(EightPuzzle(board=newBoard, parent=self, gVal=self.gVal + 1))
        return possibleMoves

    # Calculate the heuristic value of the current state using the Manhattan distance
    def getManhattanDistance(self):
        distance = 0
        # Create NumPy arrays of the board and goal state
        state = np.array(self.board)
        goal = np.array(self.goalState)
        # Iterate through all tiles on the board
        for num in range(1, 9):
            # Get the position of the current tile in the current and goal states
            statePos = np.argwhere(state == num)
            goalPos = np.argwhere(goal == num)
            # Calculate the Manhattan distance for the current tile
            distance += np.abs(statePos[0][0] - goalPos[0][0]) + np.abs(statePos[0][1] - goalPos[0][1])
        return int(distance)

    def AStarSearch(self):
        openList = []
        closedList = []
        # Add the initial state to the open list
        heapq.heappush(openList, (self.fVal, self))
        while openList:
            _, current = heapq.heappop(openList)
            if current.isGoalState():
                path = []
                while current:
                    path.append(current)
                    current = current.parent
                path.reverse()
                print("Solution found!")
                counter = 0
                for step in path:
                    if counter == 0:
                        print(f"Initial State:")
                    else:
                        print(f"Step {counter}:")
                    step.printBoard()
                    counter += 1
                print(f"Total moves: {len(path) - 1}")
                return

            closedList.append(tuple(map(tuple, current.board)))

            possibleMoves = current.getMoves()
            for move in possibleMoves:
                heapq.heappush(openList, (move.fVal, move))

        print("No solution found.")
        return

def printInitialState(state):
    top =    "┏━━━┳━━━┳━━━┓"
    middle = "┣━━━╋━━━╋━━━┫"
    bottom = "┗━━━┻━━━┻━━━┛"
    print(top)
    for i in range(3):
        print("┃", end="")
        for j in range(3):
            val = state[i][j]
            print(f" {val if val != 0 else ' '} ┃", end="")
        print()
        if i < 3 - 1:
            print(middle)
    print(bottom)
    print()

def selectInitialState():
    selection = ''
    # Print all initial states
    for name, state in initialStates.items():
        print(name)
        printInitialState(state)
    print("Select the initial state:")
    while not selection:
        selection = input()
        # Remove all non-numeric characters from user input
        selection = ''.join(filter(str.isdigit, selection))
        # Check if the selection is valid
        if int(selection) > 0 and int(selection) < len(initialStates):
            selectionNumber = 'initialState' + selection
        else:
            selection = ''
            print("Invalid selection. Please try again.")
    # Get the initial state from the dictionary
    initialState = initialStates.get(selectionNumber)
    return initialState

def __main__():

    initialState = selectInitialState()
    TilePuzzle = EightPuzzle(initialState)
    TilePuzzle.AStarSearch()

if __name__ == "__main__":
    __main__()

