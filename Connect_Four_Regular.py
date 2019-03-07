import time
import tkinter as tk
import math
import copy

# Static variables
height = 6
width = 7
board = [[0] * width for i in range(height)]
squareSize = 75
maxDepth = 3
pauseInSeconds = .6

class State:
    def __init__(self, boardState, depth, playerSymbol, opponentSymbol, moveMade):
        self.boardState = boardState
        self.depth = depth
        self.playerSymbol = playerSymbol
        self.opponentSymbol = opponentSymbol
        self.moveMade = moveMade


def miniMaxDecision(boardCopy, playerSymbol):
    move = None
    highest = -math.inf
    operators = generateSuccessors(boardCopy)
    for operator in operators:
        stateCopy = copy.deepcopy(boardCopy)
        stateCopy[operator[0]][operator[1]] = playerSymbol
        value = minValue(stateCopy, 0, -playerSymbol)
        if value >= highest:
            highest = value
            move = operator
    return move

def maxValue(boardState, currentDepth, playerSym):
    if currentDepth == maxDepth or gameOver(boardState, playerSym):
        return evaluate(boardState, playerSym, currentDepth)
    else:
        highest = -math.inf
        successors = generateSuccessors(boardState)
        for s in successors:
            stateCopy = copy.deepcopy(boardState)
            stateCopy[s[0]][s[1]] = playerSym
            current = minValue(stateCopy, currentDepth + 1, -playerSym)
            if current is not None and current >= highest:
                highest = current

        return highest

def minValue(boardState, currentDepth, playerSym):
    if currentDepth == maxDepth or gameOver(boardState, playerSym):
        return evaluate(boardState, playerSym, currentDepth)
    else:
        lowest = math.inf
        successors = generateSuccessors(boardState)
        for s in successors:
            stateCopy = copy.deepcopy(boardState)
            stateCopy[s[0]][s[1]] = playerSym
            current = maxValue(stateCopy, currentDepth + 1, -playerSym)
            if current is not None and current <= lowest:
                lowest = current

        return lowest

def evaluate(boardCopy, playerSym, depth):
    if gameOver(boardCopy, playerSym):
        return 1000 - depth
    if gameOver(boardCopy, -playerSym):
        return -1000 + depth


def playPiece(b, column, playerSym):
    for y in range(height):
        if b[y][column] == 0 and b[y + 1][column] != 0:
            b[y][column] = playerSym

def generateSuccessors(b):
    moves = []
    for x in range(width):
        if b[0][x] == 0:
            for y in range(height):
                if y == height - 1:
                    moves.append((y, x))
                    break
                else:
                    if b[y][x] == 0 and b[y + 1][x] != 0:
                        moves.append((y, x))
                        break
    return moves

def sameState(board1, board2):
    return board1 == board2

# TODO Fix the bug that grants red a win when it shouldn't.
#  Comparing strings will not work if players are using "1" and "-1" as tokens (ex: -1 1 1 1) win result in red win

def gameOver(boardToCheck, token):
    winningSeq = str(token) * 4
    #check rows
    for row in range(height):
        rowSeq = ""
        for col in range(width):
            rowSeq += str(boardToCheck[row][col])
        if winningSeq in rowSeq:
            print("win row", row)
            return True

    #check columns
    for col in range(width):
        colSeq = ""
        for row in range(height):
            colSeq += str(boardToCheck[row][col])
        if winningSeq in colSeq:
            print("win col", col)
            return True

    #check diagonals - down and right
    for row in range(height - 3):
        for col in range(width - 3):
            diagonalOffset = 0
            diagSeq = ""
            for diagonal in range(4):
                diagSeq += str(boardToCheck[row + diagonalOffset][col + diagonalOffset])
                diagonalOffset += 1
            if winningSeq in diagSeq:
                return True

    #check diagonals - up and right
    for row in range(height - 3, height):
        for col in range(width - 3):
            diagonalOffset = 0
            diagSeq = ""
            for diagonal in range(4):
                diagSeq += str(boardToCheck[row - diagonalOffset][col + diagonalOffset])
                diagonalOffset += 1
            if winningSeq in diagSeq:
                return True
    return False



def updateAndDrawGrid(w):
    w.delete("all")

    w.configure(background="black")

    for row in range(height):
        for col in range(width):
            entry = board[row][col]
            if entry == 1:
                w.create_oval(col * squareSize, row * squareSize, (col + 1) * squareSize, (row + 1) * squareSize,
                                   fill="red", outline="black")
            elif entry == -1:
                w.create_oval(col * squareSize, row * squareSize, (col + 1) * squareSize, (row + 1) * squareSize,
                                   fill="yellow", outline="black")
            else:
                w.create_oval(col * squareSize, row * squareSize, (col + 1) * squareSize, (row + 1) * squareSize,
                              fill="gray16", outline="black")
    w.pack()

if __name__ == "__main__":
    root = tk.Tk()
    window = tk.Canvas(root, width=width * squareSize, height=height * squareSize)
    totalTime = 0
    totalMoves = 0

    while True:
        updateAndDrawGrid(window)
        window.update()
        time.sleep(pauseInSeconds)


        print("Red is thinking...")
        bCopy = copy.deepcopy(board)
        startTime = time.time()
        redMove = miniMaxDecision(bCopy, 1)
        endTime = time.time()
        totalTime += endTime - startTime
        print("Red took " + str(endTime - startTime) + " seconds to decide on a move.")
        if redMove is not None:
            board[redMove[0]][redMove[1]] = 1
        else:
            print("Game over. No moves left")
            input()
            break
        totalMoves += 1

        updateAndDrawGrid(window)
        window.update()

        if gameOver(board, 1):
            print("RED WINS")
            input()
            break

        time.sleep(pauseInSeconds)

        print("Yellow is thinking...")
        bCopy = copy.deepcopy(board)
        startTime = time.time()
        yellowMove = miniMaxDecision(bCopy, -1)
        endTime = time.time()
        totalTime += endTime - startTime
        print("Yellow took " + str(endTime - startTime) + " seconds to decide on a move.")
        if yellowMove is not None:
            board[yellowMove[0]][yellowMove[1]] = -1
        else:
            print("Game over. No moves left")
            input()
            break

        # y = int(input())
        # x = int(input())
        # board[y][x] = -1
        totalMoves += 1

        updateAndDrawGrid(window)
        window.update()

        if gameOver(board, -1):
            input()
            break

    # avgTime = totalTime / totalMoves
    # print("Average time for AI to make a decision:", avgTime)
    print("Pieces played", totalMoves)