import re
import colorama
from colorama import Fore, Back, Style

# Key:
# 0 - blank
# 1 - blue
# 2 - red
# 3 - circle

BLANK = 0
BLUE = 1
RED = 2
DOT = 3
INITIAL_STATE = [[3, 1, 1, 0], [0, 2, 1, 0], [0, 2, 1, 0], [0, 2, 2, 3]]

def printBoard(board):
    print(Style.RESET_ALL, end="")
    for i in board:
        for j in i:
            if j == 0:
                print("*", end=" ")
                print(Style.RESET_ALL, end="")
            elif j == 1:
                print(Fore.BLUE + "█", end=" ")
                print(Style.RESET_ALL, end="")
            elif j == 2:
                print(Fore.RED + "█", end=" ")
                print(Style.RESET_ALL, end="")
            elif j == 3:
                print("█", end=" ")
                print(Style.RESET_ALL, end="")
        print("")

def applyMove(board, move, agent):
    #resetting current agent position in board
    neutral = (-1, -1)
    for i in range(0, 4):
        for j in range(0, 4):
            if(board[i][j] == agent):
                board[i][j] = 0

    #1 2 E 4 3 1 1
    xMove = int(move[0]) - 1
    yMove = int(move[2]) - 1
    orientation = move[4]
    lCoords = [(xMove, yMove)]

    if(orientation == 'E'):
        lCoords.extend([(xMove, yMove + 1), (xMove + 1, yMove), (xMove + 2, yMove)])
    elif(orientation == 'S'):
        lCoords.extend([(xMove + 1, yMove), (xMove, yMove + 1), (xMove, yMove + 2)])
    elif(orientation == 'W'):
        lCoords.extend([(xMove, yMove - 1), (xMove - 1, yMove), (xMove - 2, yMove)])
    elif(orientation == 'N'):
        lCoords.extend([(xMove - 1, yMove), (xMove, yMove - 1), (xMove, yMove - 2)])

    for coord in lCoords:
        board[coord[0]][coord[1]] = agent
    
    if(len(move) > 5):
        board[neutral[0]][neutral[1]] = 0
        dotInit = (int(move[6]) - 1, int(move[8]) - 1)
        dotFinal = (int(move[10]) - 1, int(move[12]) - 1)
        board[dotInit[0]][dotInit[1]] = 0
        board[dotFinal[0]][dotFinal[1]] = 3

def playGame():
    board = INITIAL_STATE.copy()
    move = ""
    agent = 1
    while(move != "quit"):
        print("Board:")
        printBoard(board)
        print("")

        move = input("Enter move: ")
        if(move == "quit"): break

        if(isValidMove(board, agent, move)):
            applyMove(board, move, agent)
            if(agent == 1): agent = 2
            else: agent = 1
        else:
            print("Invalid move. Try again.")

def invalidCoordinate(coord, gameState, agent):
    i = coord[0], j = coord[1]
    return i < 0 or i > 3 or j < 0 or j > 3 or (gameState[i][j] != BLANK and gameState[i][j] != agent)

def evaluateAction(gameState, nextGameState):
    #getSuccessors
    return 0

def getAction(gameState):
    def minimax():
        return 0
    def maxValue():
        return 0
    def minValue():
        return 0
    
    
    bestScore = float('-inf') # min init val
    bestAction = None
    legalActions = getLegalActions(gameState)
    for action in legalActions:
        successor = gameState.generateSuccessor(0, action) 
        score = minimax(1, 0, successor)  
        if score > bestScore: 
            bestScore = score
            bestAction = action
    return bestAction

def getLegalDotPos(gameState):
    # getting valid actions for dot piece
    validDotPositions = []
    dot1 = (-1, -1)
    dot2 = (-1, -2)

    # find dot1 and save, find dot2 and save
    foundDot1 = False
    for i in gameState:
       for j in gameState[i]:
           if(gameState[i][j] == DOT and (not foundDot1)):
               dot1 = (i, j)
               foundDot1 = True
           elif(gameState[i][j] == DOT and (not foundDot1)):
               dot2 = (i, j)

    # finding valid dot 1 pos
    for i in gameState:
       for j in gameState[i]:
           if(gameState[i][j] == BLANK or (i, j) == dot1):
              validDotPositions.append(((i, j), dot2))

    # finding valid dot 2 pos
    for i in gameState:
       for j in gameState[i]:
           if(gameState[i][j] == BLANK or (i, j) == dot2):
              validDotPositions.append(dot1, (i, j))

    return validDotPositions

def getSuccessors(gameState, agent):
    # getting valid actions for l piece
    validLPositions = [] # get all valid starting positions
    for i in gameState:
        for j in gameState[i]:
            if(not invalidCoordinate((i,j), gameState, agent)):
                validLPositions.append((i, j))
    
    validOrientations = []
    for coord in validLPositions:
        i = coord[0], j = coord[1]
        allPossibleLs = [[(i, j), (i - 1, j), (i - 1, j + 1), (i - 1, j + 2)], [(i, j), (i - 1, j), (i - 1, j - 1), (i - 1, j - 2)],
                        [(i, j), (i + 1, j), (i + 1, j + 1), (i + 1, j + 2)], [(i, j), (i + 1, j), (i + 1, j - 1), (i + 1, j - 2)],
                        [(i, j), (i, j - 1), (i - 1, j - 1), (i - 2, j - 1)], [(i, j), (i, j - 1), (i + 1, j - 1), (i + 2, j - 1)],
                        [(i, j), (i, j + 1), (i - 1, j + 1), (i - 2, j + 1)], [(i, j), (i, j + 1), (i + 1, j + 1), (i + 2, j + 1)],
                        [(i, j), (i - 1, j), (i - 2, j), (i - 2, j + 1)], [(i, j), (i - 1, j), (i - 2, j), (i - 2, j - 1)],
                        [(i, j), (i + 1, j), (i + 2, j), (i + 2, j + 1)], [(i, j), (i + 1, j), (i + 2, j), (i + 2, j - 1)],
                        [(i, j), (i, j - 1), (i, j - 2), (i - 1, j - 2)], [(i, j), (i, j - 1), (i, j - 2), (i + 1, j - 2)],
                        [(i, j), (i, j + 1), (i, j + 2), (i - 1, j + 2)], [(i, j), (i, j + 1), (i, j + 2), (i + 1, j + 2)]]
        for orientation in allPossibleLs: # validating orientations
            valid = True
            for c in orientation: # validating coordinates in orientation
                if(invalidCoordinate(c, gameState, agent)):
                    valid = False
                    break
            if(valid):
                validOrientations.append(orientation)

    if(len(validOrientations) == 0):
        return []

    successorStates = []
    for o in validOrientations:
        nextGameState = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        nextGameState[o[0][0]][o[0][1]] = agent
        nextGameState[o[1][0]][o[1][1]] = agent
        nextGameState[o[2][0]][o[2][1]] = agent
        nextGameState[o[3][0]][o[3][1]] = agent
        successorStates.append(nextGameState) # no dot change

        validDotPositions = getLegalDotPos(nextGameState)
    return successorStates

def isValidMoveFormat(move):
    # Define the format using a regular expression
    pattern = r"^\d \d [A-Za-z] \d \d \d \d$"
    if not re.match(pattern, move):
        return False
    
    nums = [0, 2, 6, 8, 10, 12]
    for n in nums:
        if(int(move[n]) not in range(1, 5)):
            return False

    validOrientations = ['E', 'S', 'W', 'N']
    if(move[4] not in validOrientations):
        return False

    return True

def isValidMove(gameState, agent, move):
    if(isValidMoveFormat(move)):
        #if dot moved, len(move) == 13, otherwise len(move) = 5
        xMove = int(move[0]) - 1
        yMove = int(move[2]) - 1
        orientation = move[4]
        lCoords = [(xMove, yMove)]
        if(orientation == 'E'):
            lCoords.extend([(xMove, yMove + 1), (xMove + 1, yMove), (xMove + 2, yMove)])
        elif(orientation == 'S'):
            lCoords.extend([(xMove + 1, yMove), (xMove, yMove + 1), (xMove, yMove + 2)])
        elif(orientation == 'W'):
            lCoords.extend([(xMove, yMove - 1), (xMove - 1, yMove), (xMove - 2, yMove)])
        elif(orientation == 'N'):
            lCoords.extend([(xMove - 1, yMove), (xMove, yMove - 1), (xMove, yMove - 2)])

        legalLCoords = True
        for c in lCoords:
            if(c[0] < 0 or c[0] > 3 or c[1] < 0 or c[1] > 3):
                legalLCoords = False
                break
            if((gameState[c[0]][c[1]] != agent and gameState[c[0]][c[1]] != BLANK)):
                legalLCoords = False
                break

        if(not legalLCoords):
            return False

        if(len(move) > 5):
            dotInit = (int(move[6]) - 1, int(move[8]) - 1)
            dotFinal = (int(move[10]) - 1, int(move[12]) - 1)
            if(dotInit == dotFinal):
                return False
            if(gameState[dotInit[0]][dotInit[1]] != DOT):
                return False
            if(gameState[dotFinal[0]][dotFinal[1]] == DOT):
                return False
    else:
        return False
    
    return True

playGame()