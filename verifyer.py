from collections import deque

class searchLocation :
    def __init__(self, col, row):
        self.col = col
        self.row = row


def loadGameBoard() :
    inputFile = open("input.txt")

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

    

def verifyOutput(outputFileName, GameMatrix, cols, rows) :
    currentScore = 0
    expectedScore = -1
    moveCount = 0
    expectedMoveCount = -1
    outputFile = open(outputFileName)
    lineList = outputFile.readlines()
    lineNumber = 0
    for line in lineList :
        if line == "\n" :
            continue
        if (lineNumber == 0) :
            expectedScore = int(line)
        elif (lineNumber == 1) :
            expectedMoveCount = int(line)
        else :
            color, count, row, col = map(int, line.split(" "))
            row -= 1
            col -= 1
            if (row < 0 or row >= rows or col < 0 or col >= cols) :
                print("Move out of Range")
                outputFile.close()
                return False
            wasValidMove = getMoveData(GameMatrix, col, row, color, count, rows, cols)
            if (not wasValidMove) :
                print("Move was Not Valid:: move "  + str(moveCount+1))
                outputFile.close()
                return False
            currentScore += (count - 1) ** 2
            moveCount += 1
            adjustBoard(GameMatrix,rows,cols)
        lineNumber += 1
    
    print("Made it to final Checks")
    print("Score:" + str(currentScore))
    print("Expected:" + str(expectedScore))
    print("MoveCount:" + str(moveCount))
    print("Expected:" + str(expectedMoveCount))
    outputFile.close()
    return (currentScore == expectedScore and moveCount == expectedMoveCount)
            
            
def testFunction(outputFileName) :
    GameMatrix, cols, rows = loadGameBoard()
    return (verifyOutput(outputFileName, GameMatrix, cols, rows))

if __name__ == "__main__" :
    GameMatrix, cols, rows = loadGameBoard()
    outputFileName = input()
    print(verifyOutput(outputFileName, GameMatrix, cols, rows))