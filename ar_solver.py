from collections import deque
import copy
import os
import glob
import random


class gameInstruction :
    def __init__(self, moveindex1):
        self.moveOptions = []
        self.moveOptions.append(moveindex1)
    
    def addMove(self,moveIndex) :
        self.moveOptions.append(moveIndex)

class game :
    def __init__(self, movelist, movecount, score):
        self.score = score
        self.movecount = movecount
        self.movelist = movelist

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
        self.moveIndex =-1
    def __str__(self):
        return f"MyObject(Col: {self.col}, Row: {self.row}, Size: {self.size}, Color: {self.color})"
    def setMoveIndex(self, index) :
        self.moveIndex=index
    

def hash_2d_array(arr_2d):
  tuple_of_tuples = tuple(tuple(row) for row in arr_2d)
  return hash(tuple_of_tuples)


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
        
        if (len(currentMoveList) == 0) :
            gameHasLegalMoves = False
            break

        

        bestMove = None
        maxScore = -1
        bestIndex = -1

        # HEURISTIC: Find the move that gives the highest immediate score
        for index, move in enumerate(currentMoveList):
            currentScore = (move.size - 1) ** 2
            
            if currentScore > maxScore:
                maxScore = currentScore
                bestMove = move
                bestIndex = index
            # Tie-breaker: If scores are equal, still use random to explore slightly
            elif currentScore == maxScore and random.randint(0, 1) == 0:
                 bestMove = move
                 bestIndex = index

        # Set the move index for tracking
        if bestMove is not None:
            bestMove.setMoveIndex(bestIndex)
        else:
            # Fallback if somehow currentMoveList was legal but empty (shouldn't happen)
            bestMove = currentMoveList[0] 
            bestMove.setMoveIndex(0)

        
        
        outputMoveList.append(bestMove)
        outputScore += (bestMove.size - 1) ** 2
        outputMoveCount += 1

        countAndRemove(GameMatrix, bestMove.col, bestMove.row,bestMove.color, cols, rows)
        adjustBoard(GameMatrix, rows, cols)
    return outputMoveList, outputMoveCount, outputScore

def runGameLoopWithPastKnowledge(GameMatrix, rows, cols, memoryMap) :
    gameHasLegalMoves = True
    currentMoveList = []
    outputMoveList = []
    outputScore = 0
    outputMoveCount = 0
    while gameHasLegalMoves:
        currentMoveList = searchForNextMove(GameMatrix, rows, cols)
        
        if (len(currentMoveList) == 0) :
            gameHasLegalMoves = False
            break

        bestMove = None
        boardHash = hash_2d_array(GameMatrix)
        if (memoryMap.get(boardHash) is not None and random.randint(0,1) == 0) :
            rememberedMoves = memoryMap.get(boardHash).moveOptions
            if (len(rememberedMoves) > 1) :
                indexNum = random.randint(0, len(rememberedMoves) - 1)
                bestMove = currentMoveList[rememberedMoves[indexNum]]
                bestMove.setMoveIndex(rememberedMoves[indexNum])
            else :
                bestMove = currentMoveList[0]
                bestMove.setMoveIndex(0)
        else :
            # HEURISTIC: Find the move that gives the highest immediate score (Explore)
            maxScore = -1
            bestIndex = -1

            for index, move in enumerate(currentMoveList):
                currentScore = (move.size - 1) ** 2
                
                if currentScore > maxScore:
                    maxScore = currentScore
                    bestMove = move
                    bestIndex = index
                # Tie-breaker: If scores are equal, still use random to explore slightly
                elif currentScore == maxScore and random.randint(0, 1) == 0:
                     bestMove = move
                     bestIndex = index

            # Set the move index for tracking
            if bestMove is not None:
                bestMove.setMoveIndex(bestIndex)
            else:
                bestMove = currentMoveList[0] 
                bestMove.setMoveIndex(0)


        
        
        outputMoveList.append(bestMove)
        outputScore += (bestMove.size - 1) ** 2
        outputMoveCount += 1

        countAndRemove(GameMatrix, bestMove.col, bestMove.row,bestMove.color, cols, rows)
        adjustBoard(GameMatrix, rows, cols)
    return outputMoveList, outputMoveCount, outputScore

def rememberGame(moveMap, gameToRemember, gameMatrix, cols, rows) :
    simMatrix = copy.deepcopy(gameMatrix)
    for move in gameToRemember.movelist :
        serializedSimMatrix = hash_2d_array(simMatrix)
        if moveMap.get(serializedSimMatrix) is not None :
            moveMap.get(serializedSimMatrix).addMove(move.moveIndex)
        else :
            moveMap[serializedSimMatrix] = gameInstruction(move.moveIndex)
        countAndRemove(simMatrix, move.col,move.row,move.color,cols,rows)
        adjustBoard(simMatrix,rows,cols)

def findBestGame(numberOfGuesses,mainIterCount,iterationCountPerGeneration,generationCount,filename) :
    gameList = []
    #initial RUN (Fully Random)
    gameMatrix, cols, rows = loadGameBoard(filename)
    for i in range(mainIterCount) :
        print("Main iter :: " + str(i))
        simMatrix = copy.deepcopy(gameMatrix)
        movelist, movecount, score = runGameLoop(simMatrix,rows,cols)
        gameList.append(game( movelist,movecount,score))

    gameList = sorted(gameList, key=lambda game: (-game.score))
    

    #Run with Bias toward strong answers
    for i in range(generationCount) :
        print("Current Gen :: " + str(i))
        gameMemoryMap = {}
        for top5GameIndex in range(numberOfGuesses) :
            rememberGame(gameMemoryMap, gameList[top5GameIndex],gameMatrix, cols, rows)
        
        for gameNumber in range(iterationCountPerGeneration) :
            simMatrix = copy.deepcopy(gameMatrix)
            movelist, movecount, score = runGameLoopWithPastKnowledge(simMatrix,rows,cols, gameMemoryMap)
            gameList.append(game( movelist,movecount,score))
        gameList = sorted(gameList, key=lambda game: (-game.score))


    # 1. Get just the base filename (e.g., 'input_group1062.txt')
    base_name = os.path.basename(filename)
    # 2. Construct the new filename to save in the 'outputs' directory
    outputName = os.path.join("outputs", "VERSION2_" + base_name)
    movelist = gameList[0].movelist
    movecount = gameList[0].movecount
    score = gameList[0].score
    writeOutputToFile(outputName, movelist, movecount, score)
    

if __name__ == "__main__" :
    runAllFiles = int(input("Do You want to run a specific file or the cases 1/0:: "))
    generationCount = 5
    iterationCount = 100
    guessCount = 10
    genIterCount = 200 
    if (runAllFiles == 1) :
        file_name = input("enter file name:: ")
        findBestGame(guessCount,iterationCount,genIterCount,generationCount,file_name)
    else :
        file_list = glob.glob(os.path.join("inputs", "*"))
        for file_name in file_list :
            print(file_name)
            findBestGame(guessCount,iterationCount, genIterCount,generationCount,file_name)
            
    