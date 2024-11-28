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

def invalidCoordinate(coord, gameState, agent):
    i = coord[0], j = coord[1]
    return i < 0 or i > 3 or j < 0 or j > 3 or (gameState[i][j] != BLANK and gameState[i][j] != agent)

def evaluateAction(gameState, nextGameState):
    getSuccess


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
    dot1 = (-1, -1), dot2 = (-1, -2)

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
              validDotPositions.add(((i, j), dot2))

    # finding valid dot 2 pos
    for i in gameState:
       for j in gameState[i]:
           if(gameState[i][j] == BLANK or (i, j) == dot2):
              validDotPositions.add(dot1, (i, j))

    return validDotPositions

def getSuccessors(gameState, agent):
    # getting valid actions for l piece
    validLPositions = [] # get all valid starting positions
    for i in gameState:
        for j in gameState[i]:
            if(not invalidCoordinate((i,j), gameState, agent)):
                validLPositions.add((i, j))
    
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
                    valid = false
                    break
            if(valid):
                validOrientations.add(orientation)

    successorStates = []
    for o in validOrientations:
        nextGameState = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        nextGameState[o[0][0]][o[0][1]] = agent
        nextGameState[o[1][0]][o[1][1]] = agent
        nextGameState[o[2][0]][o[2][1]] = agent
        nextGameState[o[3][0]][o[3][1]] = agent
        successorStates.add(nextGameState) # no dot change

        validDotPositions = getLegalDotPos(nextGameState)
        
        for d in validDot1Positions: # moving dot 1
            nextGameState1 = nextGameState.copy()
            nextGameState1[d[0]][d[1]] = DOT
            successorStates.add(nextGameState1)
        for d in validDot2Positions: # moving dot 2
            nextGameState1 = nextGameState.copy()
            nextGameState1[d[0]][d[1]] = DOT
            successorStates.add(nextGameState1)

    return successorStates


def isValidMove(gameState, agent, move):
    #if dot moved, len(move) == 13, otherwise len(move) = 5
    xMove = move[0], yMove = move[2], orientation = move[4]
    lCoords = [(xMove, yMove)]
    if(orientation == 'E'):
        lCoords.add([(xMove, yMove + 1), (xMove - 1, yMove), (xMove - 2, yMove)])
    elif(orientation == 'S'):
        lCoords.add([(xMove + 1, yMove), (xMove, yMove + 1), (xMove, yMove + 2)])
    elif(orientation == 'W'):
        lCoords.add([(xMove, yMove - 1), (xMove + 1, yMove), (xMove + 2, yMove)])
    elif(orientation == 'N'):
        lCoords.add([(xMove - 1, yMove), (xMove, yMove - 1), (xMove, yMove - 2)])

    legalLCoords = True
    for c in lCoords:
        if(i < 0 or i > 3 or j < 0 or j > 3):
            legalLCoords = False
            break
        if((gameState[i][j] != agent and gameState[i][j] != BLANK)):
            legalLCoords = False
            break