import re
import colorama
import time
import copy
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
EMPTY_STATE = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
INITIAL_STATE = [[3, 2, 2, 0], [0, 1, 2, 0], [0, 1, 2, 0], [0, 1, 1, 3]]
OG_INITIAL_STATE = [[3, 1, 1, 0], [0, 2, 1, 0], [0, 2, 1, 0], [0, 2, 2, 3]]
repeatedStates = []
evaluatedStatesMax = []
evaluatedEvalsMax = []
evaluatedStatesMin = []
evaluatedEvalsMin = []

def menu():
    print(Style.RESET_ALL + "-------------------------------")
    print(Fore.GREEN + "Welcome to L Game!")
    print(Fore.RED + "   1. Player v Player")
    print("   2. Player v CPU, Player Starts")
    print("   3. Player v CPU, CPU Starts")
    print("   4. CPU v CPU")
    print("   5. Change initial state")
    print("   6. Reset initial state")
    print("   7. Quit")
    print(Style.RESET_ALL)
    choice = ""

    while(choice != "6"):
        repeatedStates = []
        choice = input("Enter a number to choose your game mode: ")
        if choice == "1" or choice.upper() == "PVP":
            playGamePVP()
            time.sleep(1)
            print("\nGoing back to menu...", end="")
            time.sleep(1.5)
            break
        elif choice == "2" or choice.upper() == "PVC1":
            playGamePVC(1)
            time.sleep(1)
            print("\nGoing back to menu...", end="")
            time.sleep(1.5)
            break
        elif choice == "3" or choice.upper() == "PVC2":
            playGamePVC(2)
            time.sleep(1)
            print("\nGoing back to menu...", end="")
            time.sleep(1.5)
            break
        elif choice == "4" or choice.upper() == "CVC":
            playGameCVC()
            time.sleep(1)
            print("\nGoing back to menu...", end="")
            time.sleep(1.5)
            break
        elif choice == "5" or choice.upper() == "CIS":
            INITIAL_STATE = changeInitialState()
            print("\nNew initial state:")
            printBoard(INITIAL_STATE)
            time.sleep(1)
            print("\nGoing back to menu...", end="")
            time.sleep(1.5)
            break
        elif choice == "6" or choice.upper() == "RIS":
            INITIAL_STATE = copy.deepcopy(OG_INITIAL_STATE)
            print("\nReset initial state:")
            printBoard(INITIAL_STATE)
            time.sleep(1)
            print("\nGoing back to menu...", end="")
            time.sleep(1.5)
            break
        elif choice == "7" or choice.upper() == "QUIT" or choice.upper() == "Q":
            return 0
        else:
            print("Please enter a valid game mode.\n")
    print("\n")
    menu()

def isValidInitialState(initState):
    # 3 1 W 1 1 4 4 2 4 E (L that moves first, the two neutral pieces, L that moves second).
    if(len(initState) == 19):
        pattern = r"^\d \d [A-Za-z] \d \d \d \d \d \d [A-Za-z]$"
        if not re.match(pattern, initState):
            print("Incorrect formatting.")
            return False
        
        nums = [0, 2, 6, 8, 10, 12, 14, 16]
        for i in nums:
            if(int(initState[i]) not in range(1, 5)):
                print("One or more numbers not in range.")
                return False

        validDirections = ['E', 'S', 'W', 'N']
        if(initState[4] not in validDirections or initState[18] not in validDirections):
            print("Invalid direction.")
            return False
        
        # check validity of L coords
        lCoords1 = generateLCoords(int(initState[0]) - 1, int(initState[2]) - 1, initState[4])
        lCoords2 = generateLCoords(int(initState[14]) - 1, int(initState[16]) - 1, initState[18])

        # check coords bounds
        for c in lCoords1:
            if(c[0] < 0 or c[1] < 0 or c[0] > 3 or c[1] > 3):
                print("One or more coordinates in first L out of bounds.")
                return False
        for c in lCoords2:
            if(c[0] < 0 or c[1] < 0 or c[0] > 3 or c[1] > 3):
                print("One or more coordinates in second L out of bounds.")
                return False
        
        # check if L's are intersecting anywhere
        for c1 in lCoords1:
            for c2 in lCoords2:
                if(c1[0] == c2[0] and c1[1] == c2[1]):
                    print("L's are overalapping.")
                    return False
        
        dot1 = (int(initState[6]) - 1, int(initState[8]) - 1)
        dot2 = (int(initState[10]) - 1, int(initState[12]) - 1)
        # check neutral piece bounds
        if(dot1[0] < 0 or dot1[1] < 0 or dot1[0] > 3 or dot1[1] > 3):
            print("Neutral piece 1 coordinates are out of bounds.")
            return False
        if(dot2[0] < 0 or dot2[1] < 0 or dot2[0] > 3 or dot2[1] > 3):
            print("Neutral piece 1 coordinates are out of bounds.")
            return False

        # check if neutral pieces overlay Ls anywhere
        if(dot1 in lCoords1 or dot1 in lCoords2):
            print("Nuetral piece 1 placed over one of the Ls.")
            return False
        if(dot2 in lCoords1 or dot2 in lCoords2):
            print("Nuetral piece 2 placed over one of the Ls.")
            return False
    else:
        print("Incorrect Format - not the correct length.")
        return False
    return True # all good

def changeInitialState():
    initStateInput = ""
    initStateBoard = copy.deepcopy(EMPTY_STATE)
    while(initStateInput.upper() != "QUIT"):
        initStateInput = input("Enter a new initial state: ")
        if initStateInput.upper() != "QUIT" and initStateInput.upper() != "Q":
            if not isValidInitialState(initStateInput):
                print("Invalid initial state. Try again.\n")
                continue
            break
        else:
            quit()

    # get coords for each piece
    lCoords1 = generateLCoords(int(initStateInput[0]) - 1, int(initStateInput[2]) - 1, initStateInput[4])
    lCoords2 = generateLCoords(int(initStateInput[14]) - 1, int(initStateInput[16]) - 1, initStateInput[18])
    dot1 = (int(initStateInput[6]) - 1, int(initStateInput[8]) - 1)
    dot2 = (int(initStateInput[10]) - 1, int(initStateInput[12]) - 1)

    # applying coords to new initial state board
    for c in lCoords1:
        initStateBoard[c[0]][c[1]] = BLUE
    for c in lCoords2:
        initStateBoard[c[0]][c[1]] = RED
    initStateBoard[dot1[0]][dot1[1]] = DOT
    initStateBoard[dot2[0]][dot2[1]] = DOT
    return initStateBoard
        
def generateLCoords(x, y, direction):
    lCoords = [(x, y)]
    if(direction == 'E'):
        lCoords.extend([(x, y + 1), (x + 1, y), (x + 2, y)])
    elif(direction == 'S'):
        lCoords.extend([(x + 1, y), (x, y - 1), (x, y - 2)])
    elif(direction == 'W'):
        lCoords.extend([(x, y - 1), (x - 1, y), (x - 2, y)])
    elif(direction == 'N'):
        lCoords.extend([(x - 1, y), (x, y + 1), (x, y + 2)])
    return lCoords

def playGamePVP():
    board = copy.deepcopy(INITIAL_STATE)
    repeatedStates.append(copy.deepcopy(board))
    move = ""
    agent = 1
    while(move != " quit"):
        print("Current Board:")
        printBoard(board)
        print("")

        if(agent == 1):
            move = input("Enter blue player move, or \"hint\" for a suggested move: ")
            if(move == "quit"): break
        else:
            move = input("Enter red player move, or \"hint\" for a suggested move: ")  
            if(move == "quit"): break
        
        if(move.upper() == "HINT"):
            print("Suggested Move:")
            suggest = getBestSuccessor(board, agent)
            printBoard(suggest)
            print("\n")
        elif(isValidMove(board, agent, move)):
            applyMove(board, move, agent)
            repeatedStates.append(copy.deepcopy(board))
            agent = 2 if agent == 1 else 1 # flip agent
            possibleMoves = getSuccessors(board, agent)
            if(len(possibleMoves) == 0):
                if(agent == 1):
                    print("Red Player wins!")
                    return 0
                else:
                    print("Blue Player wins!")
                    return 0
                break
        else:
            print("Invalid move. Try again.")
    return 0

def playGamePVC(agent):
    print("You are Blue! CPU is Red!")
    board = copy.deepcopy(INITIAL_STATE)
    repeatedStates.append(copy.deepcopy(board))
    move = ""
    while(move != "quit"):
        print("Board:")
        printBoard(board)
        print("")

        if(agent == 1):
            move = input("Enter blue player move, or \"hint\" for a suggested move: ")
            if(move == "quit"): break

            if(move.upper() == "HINT"):
                print("Suggested Move:")
                suggest = getBestSuccessor(board, agent)
                printBoard(suggest)
                print("\n")
            elif(isValidMove(board, agent, move)):
                applyMove(board, move, agent)
                repeatedStates.append(copy.deepcopy(board))
                agent = 2 if agent == 1 else 1 # flip agent
                possibleMoves = getSuccessors(board, agent)
                if(len(possibleMoves) == 0):
                    if(agent == 2):
                        print("Player wins!")
                        return 0
                    else:
                        print("CPU wins!")
                        return 0
                    break
            else:
                print("Invalid move. Try again.")
        else:
            print("CPU (Red) is moving...")
            board = getBestSuccessor(board, agent)
            repeatedStates.append(copy.deepcopy(board))
            possibleMoves = getSuccessors(board, agent)
            agent = 2 if agent == 1 else 1 # flip agent
            if(len(possibleMoves) == 0):
                if(agent == 2):
                    print("Player wins!")
                else:
                    print("CPU wins!")
                break

    return 0

def playGameCVC():
    print("CPU 1 is Blue! CPU 2 is Red!\n")
    board = copy.deepcopy(INITIAL_STATE)
    repeatedStates.append(copy.deepcopy(board))
    agent = 1
    print("Board:")
    printBoard(board)
    print("")
    while(True):
        if(agent == 1): print("CPU 1 (Blue) Is Moving...")
        else: print("CPU 2 (Red) Is Moving...")

        board = getBestSuccessor(board, agent)
        if(board == None):
            print("Board is Null")
        repeatedStates.append(copy.deepcopy(board))

        if(agent == 1):
            print("CPU 1 (Blue) Played:")
            printBoard(board)
            print("")
        else:
            print("CPU 2 (Red) Played:")
            printBoard(board)
            print("")

        agent = 2 if agent == 1 else 1 # flip agent
        possibleMoves = getSuccessors(board, agent)
        #print("Possible moves for agent", agent, "")

        if(len(possibleMoves) == 0):
            if(agent == 2): # red has no more moves
                print("CPU 2 (Blue) wins!")
                return 0
            else: # blue has no more moves
                print("CPU 1 (Red) wins!")
                return 0
            break
    return 0

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
    for i in range(0, 4):
        for j in range(0, 4):
            if(board[i][j] == agent):
                board[i][j] = 0

    #1 2 E 4 3 1 1
    xMove = int(move[2]) - 1
    yMove = int(move[0]) - 1

    orientation = move[4]
    lCoords = [(xMove, yMove)]

    if(orientation == 'E'):
        coords = [(xMove, yMove + 1), (xMove + 1, yMove), (xMove + 2, yMove)]
        coords1 = [(xMove, yMove + 1), (xMove - 1, yMove), (xMove - 2, yMove)]
        if(all(coordOutOfBounds(c) for c in coords)):
            lCoords.extend(coords)
        else:
            lCoords.extend(coords1)
    elif(orientation == 'S'):
        coords = [(xMove + 1, yMove), (xMove, yMove - 1), (xMove, yMove - 2)]
        coords1 = [(xMove + 1, yMove), (xMove, yMove + 1), (xMove, yMove + 2)]
        if(all(coordOutOfBounds(c) for c in coords)):
            lCoords.extend(coords)
        else:
            lCoords.extend(coords1)
    elif(orientation == 'W'):
        coords = [(xMove, yMove - 1), (xMove - 1, yMove), (xMove - 2, yMove)]
        coords1 = [(xMove, yMove - 1), (xMove + 1, yMove), (xMove + 2, yMove)]
        if(all(coordOutOfBounds(c) for c in coords)):
            lCoords.extend(coords)
        else:
            lCoords.extend(coords1)
    elif(orientation == 'N'):
        coords = [(xMove - 1, yMove), (xMove, yMove + 1), (xMove, yMove + 2)]
        coords1 = [(xMove - 1, yMove), (xMove, yMove - 1), (xMove, yMove - 2)]
        if(all(coordOutOfBounds(c) for c in coords)):
            lCoords.extend(coords)
        else:
            lCoords.extend(coords1)

    for coord in lCoords:
        board[coord[0]][coord[1]] = agent

    if(len(move) > 5):
        dotInit = (int(move[8]) - 1, int(move[6]) - 1)
        dotFinal = (int(move[12]) - 1, int(move[10]) - 1)
        board[dotInit[0]][dotInit[1]] = 0
        board[dotFinal[0]][dotFinal[1]] = 3

def dotProximityToOpponent(dotPositions, opponentLCoords):
    score = 0
    for dot in dotPositions:
        for lCoord in opponentLCoords:
            distance = abs(dot[0] - lCoord[0]) + abs(dot[1] - lCoord[1])
            score -= distance  # The closer, the more restrictive
    return score

def isRepeatedState(gameState):
    for s in repeatedStates:
        if(compareStates(s, gameState)):
            return True

def evaluateAction(nextGameState, agent):
    #print("Evaluating:")
    #printBoard(nextGameState)
    # Define opponent agent
    nextAgent = 2 if agent == 1 else 1

    # Calculate the number of possible moves for both agents
    movesForCurrAgent = len(getSuccessors(nextGameState, agent))
    movesForOppAgent = len(getSuccessors(nextGameState, nextAgent))

    if(movesForCurrAgent == None or movesForOppAgent == None):
        print(movesForCurrAgent, movesForOppAgent)

    # Heuristic components
    weightCurr = 1.27
    weightOpp = 2.46

    # Central position control
    centralPos = [(1, 1), (1, 2), (2, 1), (2, 2)]
    centralControl = sum([1.5 for (x, y) in centralPos if nextGameState[x][y] == agent])
    oppCentralControl = sum([2.5 for (x, y) in centralPos if nextGameState[x][y] == nextAgent])

    superComp = 0
    # Super penalty or reward based on closeness to win/loss
    if movesForOppAgent <= 1:
        superComp = 150
    elif movesForCurrAgent <= 1:
        superComp = -150

    # Final evaluation score
    #print("Eval Score:", ((weightCurr * movesForCurrAgent) - (weightOpp * movesForOppAgent) + centralControl))
    return (weightCurr * movesForCurrAgent)/(weightOpp * movesForOppAgent) + centralControl/oppCentralControl + superComp

def evaluateAction1(nextGameState, agent):
    # Define opponent agent
    nextAgent = 2 if agent == 1 else 1

    # Calculate the number of possible moves for both agents
    movesForCurrAgent = len(getSuccessors(nextGameState, agent))
    movesForOppAgent = len(getSuccessors(nextGameState, nextAgent))

    # Heuristic components
    weightCurr = 1.5  # Increase weight for current agent's mobility to encourage proactive moves
    weightOpp = 1     # Maintain weight for opponent to balance defense

    # Central position control
    centralPos = [(1, 1), (1, 2), (2, 1), (2, 2)]
    centralControl = sum([1.0 for (x, y) in centralPos if nextGameState[x][y] == agent])  # Increase influence of central control

    # Peg proximity control
    pegProximity = 0
    pegPositions = [(x, y) for x in range(len(nextGameState)) for y in range(len(nextGameState[0])) if nextGameState[x][y] == DOT]
    for (x, y) in pegPositions:
        # Calculate Manhattan distance to agent's L-piece
        distances = [abs(x - lx) + abs(y - ly) for lx, ly in getCurrentLCoords(nextGameState, agent)]
        pegProximity += sum(distances)
    pegProximityWeight = -0.5  # Negative weight to encourage keeping distance from pegs

    # Super penalty or reward based on closeness to win/loss
    superComp = 0
    if movesForOppAgent == 0:
        return float('inf')  # Winning move
    elif movesForCurrAgent == 0:
        return float('-inf')  # Losing move
    elif movesForOppAgent <= 1:
        superComp = 200  # Increase reward for limiting opponent's moves to 1 or less
    elif movesForCurrAgent <= 1:
        superComp = -200  # Increase penalty for having 1 or fewer moves left

    # Cycle penalty
    cyclePenalty = 0
    if isRepeatedState(nextGameState):
        cyclePenalty = -100  # Penalize moves that result in repeated states to avoid cycles

    # Final evaluation score
    return (weightCurr * movesForCurrAgent) - (weightOpp * movesForOppAgent) + centralControl + superComp + (pegProximityWeight * pegProximity) + cyclePenalty

def isStateInStates(state, stateList):
    for s in stateList:
        if(compareStates(s, state)):
            return True
    return False

def findStateInStates(state, stateList):
    for s in range(0, len(stateList)):
        if(compareStates(stateList[s], state)):
            return s
    return -1

def compareStates(state1, state2):
    for i in range(0, 4):
            for j in range(0, 4):
                if(state1[i][j] != state2[i][j]):
                    return False
    return True

def getBestSuccessor(gameState, agent):
    def minimax(board, depth, alpha, beta, mAgent, isMaxAgent):
        # if state is not in evaluated states, eval = -1
        if(isMaxAgent):
            locatedState = findStateInStates(board, evaluatedStatesMax)
            if(locatedState != -1):
                eval = evaluatedEvalsMax[locatedState]
                #print("Max: Found Match")
                return eval
            #else:
                #print("Depth:", depth, "| Max:", len(evaluatedEvalsMax), "| Min:", len(evaluatedEvalsMin))
        else:
            locatedState = findStateInStates(board, evaluatedStatesMin)
            if(locatedState != -1):
                eval = evaluatedEvalsMin[locatedState]
                return eval
            #selse:
                #print("Depth:", depth, "| Max:", len(evaluatedEvalsMax), "| Min:", len(evaluatedEvalsMin))
        
        successors = getSuccessors(board, mAgent)
        if depth == maxDepth or len(successors) == 0:
            eval = evaluateAction(board, mAgent)
            if(isMaxAgent):
                evaluatedStatesMax.append(board)
                evaluatedEvalsMax.append(eval)
            else:
                evaluatedStatesMin.append(board)
                evaluatedEvalsMin.append(eval)
            return eval

        elif isMaxAgent: # max agent
            return maxValue(board, depth, alpha, beta, mAgent)
        else: # min agent
            return minValue(board, depth, alpha, beta, mAgent)
     
    def maxValue(board, depth, alpha, beta, mAgent):
        #print("max, currDepth:", depth)
        maxEval = float('-inf')
        successors = getSuccessors(board, mAgent)
        nextAgent = 2 if mAgent == 1 else 1
        for successor in successors:
            # checking list
            eval = minimax(successor, depth + 1, alpha, beta, nextAgent, False)
            # saving into list
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        mAgent = nextAgent # flip agent
        return maxEval
    def minValue(board, depth, alpha, beta, mAgent):
        #print("min, currDepth:", depth)
        minEval = float('inf')
        successors = getSuccessors(board, minimaxAgent)
        nextAgent = 2 if mAgent == 1 else 1
        for successor in successors:
            eval = minimax(successor, depth + 1, alpha, beta, nextAgent, True)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        mAgent = nextAgent # flip agent
        return minEval
    
    maxDepth = 20
    bestScore = float('-inf') # min init val
    bestSuccessor = None
    successors = getSuccessors(gameState, agent)
    #print("Successors:", successors)
    #print("IS CURR STATE IN SUCCESSORS:", isStateInStates(gameState, successors))
    minimaxAgent = agent
    for successor in successors:
        score = minimax(successor, 1, float('-inf'), float('inf'), minimaxAgent, True)
        #print("Max:", len(evaluatedEvalsMax), "| Min:", len(evaluatedEvalsMin))
        #print("calculated score:", score)
        #print("IT STOPPEDDD!") 
        if score > bestScore: 
            bestScore = score
            bestSuccessor = successor
            #print("Best Successor updated:", bestSuccessor)
    #print("NEXT AND PREVIOUS THE SAME?:", compareStates(gameState, bestSuccessor))
    #print("Best Successor Eval: ", bestScore)
    #print("BEST SUCCESSOR FOUND:")
    #printBoard(bestSuccessor)
    #print(bestSuccessor)
    return bestSuccessor

#def generateMove(initState, finalState):
#    blueInitLCoords = getCurrentLCoords(initState, 1)
#    blueFinalLCoords = getCurrentLCoords(finalState, 1)
#    redInitLCoords = getCurrentLCoords(initState, 2)
#    redFinalLCoords = getCurrentLCoords(finalState, 2)
#
#    if(compareLCoords(blueInitLCoords, blueFinalLCoords)):
#        
#    else:
#
#
    # find neutral piece that changed
#    dotsInit = getDotCoords(initState)
#    dotsFinal = getDotCoords(finalState)
#
#    if(dotsInit == dotsFinal):

def invalidCoordinate(coord, gameState, agent):
    #print(f"Debug: coord={coord}, type={type(coord)}")  # Debugging line
    i = coord[0]
    j = coord[1]
    return i < 0 or i > 3 or j < 0 or j > 3 or (gameState[i][j] != BLANK and gameState[i][j] != agent)

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
              validDotPositions.append((dot1, (i, j)))

    return validDotPositions

def getDotCoords(gameState):
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
    return (dot1Init, dot2Init)

def getCurrentLCoords(gameState, agent):
    lCoords = []
    for i in range(0, 4):
        for j in range(0, 4):
            if(gameState[i][j] == agent):
                lCoords.append((i, j))
    return lCoords

def compareLCoords(lCoords1, lCoords2):
    for c1 in lCoords1:
        foundMatch = False
        for c2 in lCoords2:
            if(c1[0] == c2[0] and c1[1] == c2[1]):
                foundMatch = True
                break
        if(not foundMatch):
            return False
    return True

# gets valid successor states for given agent and current game state
# Logic:
#     - calculates all valid L moves
#     - adds each L move without dot moves to successor list
#     - calculates new valid dot positions for each valid L move
#     - adds successor state with each new valid dot position 
def getSuccessors(gameState, agent):
    #print("CURR:")
    #printBoard(gameState)
    #print("SUCCS:")
    #print("SUCCESSORS:")
    # getting valid actions for l piece
    validLPositions = [] # get all valid starting coords
    for i in range(0, 4):
        for j in range(0, 4):
            coord = (i, j)
            if(not invalidCoordinate(coord, gameState, agent)):
                validLPositions.append((i, j))

    currLCoords = getCurrentLCoords(gameState, agent)
    
    validOrientations = []
    for coord in validLPositions:
        i = coord[0]
        j = coord[1]
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
            if(valid and not compareLCoords(orientation, currLCoords)):
                validOrientations.append(orientation)
    
    if(len(validOrientations) == 0):
        return []

    validOrientations = [sorted(vO) for vO in validOrientations]
    validOrientations = [list(t) for t in {tuple(vO) for vO in validOrientations}]
    del validOrientations[0]

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
        #printBoard(nextGameStateOldDots)
        #print(nextGameStateOldDots)
        #print("")
        successorStates.append(copy.deepcopy(nextGameStateOldDots))

        # get valid dot positions for nextGameState
        validDotPositions = getLegalDotPos(nextGameStateOldDots, dot1Init, dot2Init)
        # reset neutral piece positions
        nextGameStateOldDots[dot1Init[0]][dot1Init[1]] = BLANK
        nextGameStateOldDots[dot2Init[0]][dot2Init[1]] = BLANK

        # place both dots in every valid position + add to successorStates list
        for d in validDotPositions:
            nextGameStateNewDots = copy.deepcopy(nextGameStateOldDots)
            nextGameStateNewDots[d[0][0]][d[0][1]] = DOT
            nextGameStateNewDots[d[1][0]][d[1][1]] = DOT
            #printBoard(nextGameStateNewDots)
            #print("")
            successorStates.append(nextGameStateNewDots)
    
    #print("Successors:", successorStates)

    for i in range(0, len(successorStates)):
        if(compareStates(successorStates[i], gameState)):
            successorStates.pop(i)
            break    

    return successorStates

def isValidMoveFormat(move):
    # Define the format using a regular expression
    if(len(move) == 13):
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
    elif(len(move) == 5):
        pattern = r"^\d \d [A-Za-z]$"
        if not re.match(pattern, move):
            return False
        
        nums = [0, 2]
        for n in nums:
            if(int(move[n]) not in range(1, 5)):
                return False

        validOrientations = ['E', 'S', 'W', 'N']
        if(move[4] not in validOrientations):
            return False
        return True
    else:
        return False

def coordOutOfBounds(coord):
    if(coord[0] > 3 or coord[1] > 3 or coord[0] < 0 or coord[1] < 0):
        return False
    return True

def isValidMove(gameState, agent, move):
    if(isValidMoveFormat(move)):
        #if dot moved, len(move) == 13, otherwise len(move) = 5
        xMove = int(move[2]) - 1
        yMove = int(move[0]) - 1

        orientation = move[4]
        lCoords = [(xMove, yMove)]
        if(orientation == 'E'):
            coords = [(xMove, yMove + 1), (xMove + 1, yMove), (xMove + 2, yMove)]
            coords1 = [(xMove, yMove + 1), (xMove - 1, yMove), (xMove - 2, yMove)]
            if(all(coordOutOfBounds(c) for c in coords)):
                lCoords.extend(coords)
            else:
                lCoords.extend(coords1)
        elif(orientation == 'S'):
            coords = [(xMove + 1, yMove), (xMove, yMove - 1), (xMove, yMove - 2)]
            coords1 = [(xMove + 1, yMove), (xMove, yMove + 1), (xMove, yMove + 2)]
            if(all(coordOutOfBounds(c) for c in coords)):
                lCoords.extend(coords)
            else:
                lCoords.extend(coords1)
        elif(orientation == 'W'):
            coords = [(xMove, yMove - 1), (xMove - 1, yMove), (xMove - 2, yMove)]
            coords1 = [(xMove, yMove - 1), (xMove + 1, yMove), (xMove + 2, yMove)]
            if(all(coordOutOfBounds(c) for c in coords)):
                lCoords.extend(coords)
            else:
                lCoords.extend(coords1)
        elif(orientation == 'N'):
            coords = [(xMove - 1, yMove), (xMove, yMove + 1), (xMove, yMove + 2)]
            coords1 = [(xMove - 1, yMove), (xMove, yMove - 1), (xMove, yMove - 2)]
            if(all(coordOutOfBounds(c) for c in coords)):
                lCoords.extend(coords)
            else:
                lCoords.extend(coords1)

        print(lCoords)

        for c in lCoords:
            if(invalidCoordinate((c[0], c[1]), gameState, agent)):
                return False
            
        currLCoords = getCurrentLCoords(gameState, agent)
        if(compareLCoords(currLCoords, lCoords)):
            print("Cannot move to same position. ", end="")
            return False

        if(len(move) > 5):
            dotInit = (int(move[8]) - 1, int(move[6]) - 1)
            dotFinal = (int(move[12]) - 1, int(move[10]) - 1)
            if(dotInit == dotFinal):
                return False
            if(gameState[dotInit[0]][dotInit[1]] != DOT):
                return False
            if(gameState[dotFinal[0]][dotFinal[1]] == DOT):
                return False
            for c in lCoords:
                if(c[0] == dotFinal[0] and c[1] == dotFinal[1]):
                    return False
    else:
        return False
    return True

menu()