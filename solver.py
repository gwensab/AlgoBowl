from collections import deque
import copy
import os
import glob

class searchLocation :
    def __init__(self, col, row):
        self.col = col
        self.row = row

class locationScore :
    def __init__(self, col, row, size, color):
        self.col = col
        self.row = row
        self.size = size
        self.color = color
    def __str__(self):
        return f"MyObject(Col: {self.col}, Row: {self.row}, Size: {self.size}, Color: {self.color})"


def loadGameBoard(inputFileName) :
    inputFile = open(inputFileName)

    lineList = inputFile.readlines()
    rows = 0
    cols = 0
    linenum = -1
    for line in lineList :
        if line == "\n" :
            continue
        if linenum == -1 :
            rows, cols = map(int, line.split(" "))
            GameMatrix = [[0] * rows for _ in range(cols)]
            linenum = rows
        else :
            colnum = 0
            for char in line :
                if (char != '\n') :
                    GameMatrix[colnum][linenum] = int(char)
                    colnum+=1
        linenum-=1
    
    inputFile.close()
    
    return GameMatrix, cols, rows

def countAndRemove(GameMatrix, col, row, color, cols, rows) :
    size = 0
    checkQueue = deque()
    checkQueue.append(searchLocation(col,row))

    while len(checkQueue) > 0:
        currentPos = checkQueue.popleft()
        currentCol = currentPos.col
        currentRow = currentPos.row

        if (GameMatrix[currentCol][currentRow] == color) :
            GameMatrix[currentCol][currentRow] = 0
            size+= 1
            if (currentCol > 0) :
                checkQueue.append(searchLocation(currentCol -1, currentRow))
            if (currentCol < cols - 1) :
                checkQueue.append(searchLocation(currentCol + 1, currentRow))
            if (currentRow > 0) :
                checkQueue.append(searchLocation(currentCol, currentRow - 1))
            if (currentRow < rows - 1) :
                checkQueue.append(searchLocation(currentCol, currentRow + 1))
    return size

    

def getMoveData(GameMatrix, col, row, color, count, rows, cols) :
    if (GameMatrix[col][row] != color) :
        print("invalid color")
        return False
    movesize = countAndRemove(GameMatrix, col, row, color, cols, rows)
    if (movesize != count or movesize < 2) :
        print("invalid move size")
        return False
    return True
    
def adjustBoard(GameMatrix, rows, cols) :
    for column in GameMatrix :
        dropdown = 0
        for i in range(rows) :
            if (column[i] != 0):
                if (dropdown > 0) :
                    column[i - dropdown] = column[i]
                    column[i] = 0
            else :
                dropdown += 1
    for i in range(cols) :
        if (GameMatrix[i][0] == 0) :
            for z in range(i, cols) :
                if (GameMatrix[z][0] != 0) :
                    placeholder = GameMatrix[i]
                    GameMatrix[i] = GameMatrix[z]
                    GameMatrix[z] = placeholder
                    break

def searchForNextMove(GameMatrix, rows, cols) :
    matrix_copy = copy.deepcopy(GameMatrix)
    returnList = []
    for i in range(cols) :
        for z in range(rows) :
            if (matrix_copy[i][z] != 0) :
                color = matrix_copy[i][z]
                currentLocationScore = locationScore(i,z,countAndRemove(matrix_copy,i,z,matrix_copy[i][z],cols,rows), color)
                if (currentLocationScore.size > 1) :
                    returnList.append(currentLocationScore)
    return returnList

def writeOutputToFile(outputFileName, movelist, movecount, score) :
    f = open(outputFileName, 'w')

    f.write(str(score) + "\n")
    f.write(str(movecount) + "\n")

    for move in movelist :
        outputString = str(move.color) + " " + str(move.size) +  " " + str(move.row + 1) + " " + str(move.col + 1) + "\n"
        f.write(outputString)
    
    f.close()


def runGameLoop(GameMatrix, rows, cols) :
    gameHasLegalMoves = True
    currentMoveList = []
    outputMoveList = []
    outputScore = 0
    outputMoveCount = 0
    while gameHasLegalMoves:
        currentMoveList = searchForNextMove(GameMatrix, rows, cols)
        sortedMoveList = sorted(currentMoveList, key=lambda locationScore: (-locationScore.size, locationScore.row))
        
        if (len(currentMoveList) == 0) :
            gameHasLegalMoves = False
            break

        topMoveScore = (sortedMoveList[0].size - 1) ** 2
        bestMove = None

        if (len(sortedMoveList) > 1) :
            secondMoveScore = (sortedMoveList[1].size - 1) ** 2

            if (secondMoveScore > topMoveScore / 2 and sortedMoveList[0].row > sortedMoveList[1].row) :
                bestMove = sortedMoveList[1]
            else :
                bestMove = sortedMoveList[0]
        else :
            bestMove = sortedMoveList[0]

        
        
        outputMoveList.append(bestMove)
        outputScore += (bestMove.size - 1) ** 2
        outputMoveCount += 1

        countAndRemove(GameMatrix, bestMove.col, bestMove.row,bestMove.color, cols, rows)
        adjustBoard(GameMatrix, rows, cols)
    return outputMoveList, outputMoveCount, outputScore
    

    

if __name__ == "__main__" :
    
    file_list = glob.glob(os.path.join("inputs", "*"))
    for file_name in file_list :
        print(file_name)
        GameMatrix, cols, rows = loadGameBoard(file_name)
        outputName = "output2_" + file_name
        movelist, movecount, score = runGameLoop(GameMatrix, rows, cols)
        writeOutputToFile(outputName, movelist, movecount, score)
    