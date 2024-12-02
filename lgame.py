import re
import colorama
import time
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

def menu():
    print("Welcome to L Game! Choose your game mode: ")
    print("1. PVP")
    print("2. PVC")
    print("3. CVC")
    print("4. QUIT")
    choice = ""

    while(choice.upper() != "QUIT"):
        choice = input()
        if choice.upper() == "PVP":
            playGamePVP()
        elif choice.upper() == "PVC":
            playGamePVC()
        elif choice.upper() == "CVC":
            playGameCVC()
        elif choice.upper() == "QUIT":
            break
        else:
            print("Please enter a valid game mode: ")

def playGamePVC():
    print("You are Blue! CPU is Red!")
    board = INITIAL_STATE.copy()
    move = ""
    agent = 1
    while(move != "quit"):
        print("Board:")
        printBoard(board)
        print("")

        if(agent == 1):
            move = input("Enter move: ")
            if(move == "quit"): break

            if(isValidMove(board, agent, move)):
                applyMove(board, move, agent)
                agent = 2 if agent == 1 else 1 # flip agent
                possibleMoves = getSuccessors(board, agent)
                if(len(possibleMoves) == 0):
                    if(agent == 2):
                        print("CPU wins!")
                    else:
                        print("Player wins!")
                    break
            else:
                print("Invalid move. Try again.")
        else:
            board = getBestSuccessor(board, agent)
            possibleMoves = getSuccessors(board, agent)
            agent = 2 if agent == 1 else 1 # flip agent
            if(len(possibleMoves) == 0):
                if(agent == 2):
                    print("CPU wins!")
                else:
                    print("Player wins!")
                break

def playGameCVC():
    print("CPU 1 is Blue! CPU 2 is Red!")
    board = INITIAL_STATE.copy()
    agent = 1
    while(True):
        time.sleep(1) # pause for a sec
        print("Board:")
        printBoard(board)
        print("")
            
        board = getBestSuccessor(board, agent)
        agent = 2 if agent == 1 else 1 # flip agent
        possibleMoves = getSuccessors(board, agent)
        if(len(possibleMoves) == 0):
            if(agent == 2):
                print("CPU 2 wins!")
            else:
                print("CPU 1 wins!")
            break

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

def playGamePVP():
    board = INITIAL_STATE.copy()
    move = ""
    agent = 1
    while(move != " quit"):
        print("Board:")
        printBoard(board)
        print("")

        if(agent == 1):
            move = input("Enter blue player move: ")
            if(move == "quit"): break
        else:
            move = input("Enter red player move: ")  
            if(move == "quit"): break
        

        if(isValidMove(board, agent, move)):
            applyMove(board, move, agent)
            agent = 2 if agent == 1 else 1 # flip agent
            possibleMoves = getSuccessors(board, agent)
            if(len(possibleMoves) == 0):
                if(agent == 1):
                    print("Red Player wins!")
                else:
                    print("Blue Player wins!")
                break
        else:
            print("Invalid move. Try again.")

def invalidCoordinate(coord, gameState, agent):
    i = coord[0], j = coord[1]
    return i < 0 or i > 3 or j < 0 or j > 3 or (gameState[i][j] != BLANK and gameState[i][j] != agent)

def dotProximityToOpponent(dotPositions, opponentLCoords):
    score = 0
    for dot in dotPositions:
        for lCoord in opponentLCoords:
            distance = abs(dot[0] - lCoord[0]) + abs(dot[1] - lCoord[1])
            score -= distance  # The closer, the more restrictive
    return score

def evaluateAction(nextGameState, agent):
    # Define opponent agent
    nextAgent = 2 if agent == 1 else 1

    # Calculate the number of possible moves for both agents
    movesForCurrAgent = len(getSuccessors(nextGameState, agent))
    movesForOppAgent = len(getSuccessors(nextGameState, nextAgent))

    # Heuristic components
    weightCurr = 1
    weightOpp = 2

    # Central position control
    centralPos = [(1, 1), (1, 2), (2, 1), (2, 2)]
    centralControl = sum([0.5 for (x, y) in centralPos if nextGameState[x][y] == agent])

    # Super penalty or reward based on closeness to win/loss
    if movesForOppAgent <= 1:
        return float('inf')  # Winning move
    elif movesForCurrAgent <= 1:
        return float('-inf')  # Losing move

    # Final evaluation score
    return (weightCurr * movesForCurrAgent) - (weightOpp * movesForOppAgent) + centralControl

def getBestSuccessor(gameState, agent):
    def minimax(board, depth, alpha, beta, agent, isMaxAgent):
        #getSuccessors, heuristic, and evaluation
        if depth == maxDepth or getSuccessors(board, minimaxAgent) == []:
            return evaluateAction(board, minimaxAgent)
        elif isMaxAgent:
            maxValue(board, depth, alpha, beta, minimaxAgent)
        else:
            minValue(board, depth + 1, alpha, beta, minimaxAgent)
     
    def maxValue(board, depth, alpha, beta, minimaxAgent):
        maxEval = float('-inf')
        for successor in getSuccessors(gameState, minimaxAgent):
            eval = minimax(successor, depth + 1, alpha, beta, False)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        minimaxAgent = 2 if minimaxAgent == 1 else 1 # flip agent
        return maxEval
    def minValue(board, depth, alpha, beta, minimaxAgent):
        minEval = float('inf')
        for successor in getSuccessors(gameState, minimaxAgent):
            eval = minimax(successor, depth + 1, alpha, beta, True)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        minimaxAgent = 2 if minimaxAgent == 1 else 1 # flip agent
        return minEval
    
    maxDepth = 5
    bestScore = float('-inf') # min init val
    bestSuccessor = None
    successors = getSuccessors(gameState, agent)
    minimaxAgent = agent
    for successor in successors:
        score = minimax(successor, 1, float('-inf'), float('inf'), minimaxAgent, True)  
        if score > bestScore: 
            bestScore = score
            bestSuccessor = successor
    return bestSuccessor

# gets valid new dot positions given game state and current dot positions
def getLegalDotPos(nextGameState, dot1, dot2):
    # getting valid moves for dot piece
    validDotPositions = []

    # finding valid dot 1 pos not moving dot 2
    for i in range(0, 4):
       for j in range(0, 4):
           if(nextGameState[i][j] == BLANK): # only a valid move if blank spot
              validDotPositions.append(((i, j), dot2))

    # finding valid dot 2 pos not moving dot 1
    for i in range(0, 4):
       for j in range(0, 4):
           if(nextGameState[i][j] == BLANK): # only a valid move if blank spot
              validDotPositions.append(dot1, (i, j))

    return validDotPositions

# gets valid successor states for given agent and current game states
# Logic:
#     - calculates all valid L moves
#     - adds each L move without dot moves to successor list
#     - calculates new valid dot positions for each valid L move
#     - adds successor state with each new valid dot position 
def getSuccessors(gameState, agent):
    # getting valid actions for l piece
    validLPositions = [] # get all valid starting coords
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
            if(valid): validOrientations.append(orientation)

    if(len(validOrientations) == 0):
        return []

    successorStates = []
    # find all valid nuetral piece moves for each next orientation and create next game state
    for o in validOrientations:
        nextGameStateOldDots = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        dot1Init = None
        dot2Init = None
        for i in range(0, 4):
            for j in range(0, 4):
                # getting values for the starting points of each neutral piece
                if(dot1Init == None or dot2Init == None):
                    # if (i,j) is a dot...
                    if(gameState[i][j] == DOT):
                        # and we haven't found dot 1, then this is dot 1
                        if(dot1Init == None):
                            dot1Init = (i, j)
                        # and we have found dot 1, then this is dot 2
                        else:
                            dot2Init = (i, j)
                
                # moving everything from current to nextGameState except current agent
                if(gameState[i][j] != agent):
                    nextGameStateOldDots[i][j] = gameState[i][j]

        # place current orientation in nextGameState
        nextGameStateOldDots[o[0][0]][o[0][1]] = agent
        nextGameStateOldDots[o[1][0]][o[1][1]] = agent
        nextGameStateOldDots[o[2][0]][o[2][1]] = agent
        nextGameStateOldDots[o[3][0]][o[3][1]] = agent
        # add no dot change scenario to successorStates list
        successorStates.append(nextGameStateOldDots)

        # get valid dot positions for nextGameState
        validDotPositions = getLegalDotPos(nextGameStateOldDots, dot1Init, dot2Init)
        # reset neutral piece positions
        nextGameStateOldDots[dot1Init[0]][dot1Init[1]] = BLANK
        nextGameStateOldDots[dot2Init[0]][dot2Init[1]] = BLANK

        # place both dots in every valid position + add to successorStates list
        for d in validDotPositions:
            nextGameStateNewDots = nextGameStateOldDots.copy()
            nextGameStateNewDots[d[0][0]][d[0][1]] = DOT
            nextGameStateNewDots[d[1][0]][d[1][1]] = DOT
            successorStates.append(nextGameStateNewDots)

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

menu()