from collections import deque
import numpy as np

goalState = ([1, 2, 3],
             [8, 0, 4],
             [7, 6, 5])

# initialState = ([2, 8, 3],
#                 [1, 6, 4],
#                 [7, 0, 5])

# 1 move initial state
initialState = ([1, 2, 3],
                [0, 8, 4],
                [7, 6, 5])

class EightPuzzle:
    def __init__(self, board):
        self.board = board
        self.bSize = 3
        self.goalState = (
            [1, 2, 3],
            [8, 0, 4],
            [7, 6, 5]
        )


    def isGoalState(self):
        return np.array_equal(self.board, self.goalState)

    def getPossibleMoves(self):
        possibleMoves = []
        pass

        return possibleMoves

    def validMove(self, newRow, newCol):
        return 0 <= newRow < self.bSize and 0 <= newCol < self.bSize

    def makeMove(self, newBoard):
        self.board = newBoard

    def printBoard(self):
        for i in range(self.bSize):
            print(" ----------------")
            for j in range(self.bSize):
                print(" | ", end="")
                print(self.board[i][j], end=" ")
                if j == self.bSize - 1:
                    print(" | ")
        print(" ----------------")
        
    def getBlankTilePosition(self):
        for i in range(self.bSize):
            for j in range(self.bSize):
                if self.board[i][j] == 0:
                    return (i, j)
                
    def getPossibleMoves(self):
        possibleMoves = []
        blankPos = self.getBlankTilePosition()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        for d in directions:
            newRow = blankPos[0] + d[0]
            newCol = blankPos[1] + d[1]
            if self.validMove(newRow, newCol):
                newBoard = np.array(self.board, copy=True)
                newBoard[blankPos[0]][blankPos[1]] = newBoard[newRow][newCol]
                newBoard[newRow][newCol] = 0
                possibleMoves.append(EightPuzzle(newBoard))

        return possibleMoves

    def AStarSearch(self):
        # Implement A* search algorithm
        possibleMoves = self.getPossibleMoves()
        for move in possibleMoves:
            if move.isGoalState():
                print("Found goal state:")
                move.printBoard()


TilePuzzle = EightPuzzle(initialState)
TilePuzzle.printBoard()
TilePuzzle.AStarSearch()
