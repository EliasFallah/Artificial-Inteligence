from collections import deque
import heapq
import numpy as np

goalState = ([1, 2, 3],
             [8, 0, 4],
             [7, 6, 5])

initialState5 = ([2, 8, 3],
                 [1, 6, 4],
                 [7, 0, 5])

initialState18 = ([2, 1, 6],
                  [4, 0, 8],
                  [7, 5, 3])

initialState21 = ([5, 7, 2],
                  [0, 8, 6],
                  [4, 1, 3])


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

    def getBlankTile(self):
        for i in range(self.bSize):
            for j in range(self.bSize):
                if self.board[i][j] == 0:
                    return (i, j)
                
    def getMoves(self):
        possibleMoves = []
        blankPos = self.getBlankTile()
                       # Up,    Down,    Left,   Right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  

        for d in directions:
            newRow = blankPos[0] + d[0]
            newCol = blankPos[1] + d[1]
            if self.validMove(newRow, newCol):
                newBoard = np.array(self.board, copy=True)
                newBoard[blankPos[0]][blankPos[1]] = newBoard[newRow][newCol]
                newBoard[newRow][newCol] = 0
                possibleMoves.append(EightPuzzle(board=newBoard, parent=self, gVal=self.gVal + 1))
        return possibleMoves

    def getManhattanDistance(self):
        distance = 0
        state = np.array(self.board)
        goal = np.array(self.goalState)
        for num in range(1, 9):
            statePos = np.argwhere(state == num)
            goalPos = np.argwhere(goal == num)
            distance += np.abs(statePos[0][0] - goalPos[0][0]) + np.abs(statePos[0][1] - goalPos[0][1])
        return int(distance)

    def AStarSearch(self):
        openList = []
        closedList = []
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

TilePuzzle = EightPuzzle(initialState21)
TilePuzzle.AStarSearch()
