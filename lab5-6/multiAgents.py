# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        foodList = newFood.asList()
        # get manhattanDistance to nearest food
        nearestFoodDistance = min(manhattanDistance(newPos, food) for food in foodList) if foodList else 0
        foodReward = 1.0 / (nearestFoodDistance + 1)

        # get manhattanDistance to nearest ghost
        ghostDistances = [manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates]
        ghostPenalty = 3.5 / (min(ghostDistances) + 1)
        return successorGameState.getScore() + foodReward - ghostPenalty

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        def minimax(agentIndex, depth, state):
            # If we reach a terminal state or the maximum depth, evaluate the state
            if depth == self.depth: return self.evaluationFunction(state)
            #numAgents = state.getNumAgents()

            if agentIndex == 0: #Pacman - maxmimizing
                return maxValue(agentIndex, depth, state)
            else: #Ghost - minimizing
                return minValue(agentIndex, depth, state)
        
        def maxValue(agentIndex, depth, state): # Pacman
            legalActions = state.getLegalActions(agentIndex)
            if not legalActions: return self.evaluationFunction(state)

            # Find the best action's value by maximizing over possible successors
            bestScore = float('-inf') # min init val
            for action in legalActions:
                successor = state.generateSuccessor(agentIndex, action)
                # maximize score of agents(ghost - min) at next depth
                bestScore = max(bestScore, minimax(1, depth, successor))
            return bestScore

        def minValue(agentIndex, depth, state): # Ghost
            legalActions = state.getLegalActions(agentIndex)
            if not legalActions: return self.evaluationFunction(state)

            bestScore = float('inf')
            #nextAgent = (agentIndex + 1) % state.getNumAgents()
            nextAgent = agentIndex
            if(agentIndex == state.getNumAgents() - 1): nextAgent = 0
            else: nextAgent = nextAgent + 1

            for action in legalActions:
                successor = state.generateSuccessor(agentIndex, action)
                if nextAgent == 0: # minimize score of agent at next depth (pacman)
                    bestScore = min(bestScore, minimax(0, depth + 1, successor))
                else:  # minimize score of next ghosts
                    bestScore = min(bestScore, minimax(nextAgent, depth, successor))
            return bestScore
        
        # get legal actions of Pacman (first agent - max)
        bestScore = float('-inf') # min init val
        bestAction = None
        legalActions = gameState.getLegalActions(0)
        for action in legalActions:
            successor = gameState.generateSuccessor(0, action) # get pacman successor state
            score = minimax(1, 0, successor)  # next agent is the first ghost
            if score > bestScore: # maximize score and track of max score action
                bestScore = score
                bestAction = action
        return bestAction
        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def AB(gameState,agent,depth,a,b):
            result = []
            # Reached max depth #
            if depth == self.depth or not gameState.getLegalActions(agent):
                return self.evaluationFunction(gameState),0

            # all ghosts have finised one round: increase depth #
            if agent == gameState.getNumAgents() - 1: depth += 1

            if agent == gameState.getNumAgents() - 1:
                nextAgent = self.index
            else:
                nextAgent = agent + 1

            # For every successor find minmax value #
            for action in gameState.getLegalActions(agent):
                if not result: # First move
                    nextValue = AB(gameState.generateSuccessor(agent,action),nextAgent,depth,a,b)
                    result.append(nextValue[0])
                    result.append(action)

                    #set alpha if max agent, beta if min agent
                    if agent == self.index: a = max(result[0],a)
                    else: b = min(result[0],b)
                else:
                    #checks to prune: result > beta if max agent, result < agent if min agent
                    if result[0] > b and agent == self.index: return result
                    if result[0] < a and agent != self.index: return result

                    previousValue = result[0] # Keep previous value
                    nextValue = AB(gameState.generateSuccessor(agent,action),nextAgent,depth,a,b)

                    if agent == self.index: #max agent
                        if nextValue[0] > previousValue:
                            result[0] = nextValue[0]
                            result[1] = action
                            a = max(result[0],a)
                    elif nextValue[0] < previousValue: #min agent
                        result[0] = nextValue[0]
                        result[1] = action
                        b = min(result[0],b)
            return result
        return AB(gameState,self.index,0,-float("inf"),float("inf"))[1]
        #util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectimax(agentIndex, depth, state):
            if depth == self.depth or not state.getLegalActions(agentIndex):
                return self.evaluationFunction(state) # evaluate state if max depth or terminal state

            if agentIndex == 0:  # Pacman (maximizing)
                return maxValue(agentIndex, depth, state)
            else:  # Ghosts (chance nodes)
                return expValue(agentIndex, depth, state)

        def maxValue(agentIndex, depth, state):  # Pacman's maximizing turn
            legalActions = state.getLegalActions(agentIndex)
            if not legalActions: return self.evaluationFunction(state)

            bestScore = float('-inf')
            for action in legalActions:
                successor = state.generateSuccessor(agentIndex, action)
                bestScore = max(bestScore, expectimax(1, depth, successor))

            return bestScore

        def expValue(agentIndex, depth, state):  # Ghosts' chance nodes
            legalActions = state.getLegalActions(agentIndex)
            if not legalActions: return self.evaluationFunction(state)

            numActions = len(legalActions)
            totalScore = 0
            nextAgent = (agentIndex + 1) % state.getNumAgents()

            for action in legalActions:
                successor = state.generateSuccessor(agentIndex, action)
                if nextAgent == 0:  # If the next agent is Pacman, increase the depth
                    totalScore += expectimax(nextAgent, depth + 1, successor)
                else:  # Other ghosts' turns
                    totalScore += expectimax(nextAgent, depth, successor)
            return totalScore / numActions  # Return the average (expected value)

        # Pacman (agent 0) starts by maximizing
        bestScore = float('-inf')
        bestAction = None
        legalActions = gameState.getLegalActions(0)

        for action in legalActions:
            successor = gameState.generateSuccessor(0, action)
            currScore = expectimax(1, 0, successor)  # Next agent is the first ghost
            if currScore > bestScore:  # Maximize score for Pacman
                bestScore = currScore
                bestAction = action

        return bestAction
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION:
      FoodReward - min manh. dist. to food (encourages to go to food)
      GhostPenalty - cumulative of penalty for each ghost (encourages/discourages going to ghosts)
        Penalty - Negative if ghost not scared, Positive if ghost is scared
      CapsuleReward - min manh. dist. to capsule (encourages to go to capsule)
      Final Heuristic: current score + foodReward - ghostPenalty + capsuleReward
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newGhostStates = currentGameState.getGhostStates()
    newCapsules = currentGameState.getCapsules()
    foodList = currentGameState.getFood().asList()

    # get manhattanDistance to nearest food
    nearestFoodDistance = min(manhattanDistance(newPos, food) for food in foodList) if foodList else 0
    foodReward = 1.0 / (nearestFoodDistance + 1)

    # avoid all ghosts unless scared, otherwise go towards them
    ghostPenalty = 0
    for ghost in newGhostStates:
        ghostDist = manhattanDistance(newPos, ghost.getPosition())
        if ghost.scaredTimer > 0:  # Ghost is scared, Pacman should chase it
            ghostPenalty -= 2.0 / (ghostDist + 1)
        else:  # Ghost is active, avoid it
            ghostPenalty += 2.8 / (ghostDist + 1)

    #always go towards capsules when ghosts are not scared
    nearestCapsuleDistance = min(manhattanDistance(newPos, cap) for cap in newCapsules) if newCapsules else 0
    capsuleReward = 2.0 / (nearestCapsuleDistance + 1) if newCapsules else 0
    
    return currentGameState.getScore() + foodReward + capsuleReward - ghostPenalty
    #util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

# def minimax(agentIndex, depth, state, alpha, beta):
        #     # If we reach a terminal state or the maximum depth, evaluate the state
        #     if (not gameState.getLegalActions(agentIndex) or depth == self.depth):
        #         return self.evaluationFunction(state)
        #     if agentIndex == 0: #Pacman - maxmimizing
        #         return maxValue(agentIndex, depth, state, alpha, beta)
        #     else: #Ghost - minimizing
        #         return minValue(agentIndex, depth, state, alpha, beta)
        
        # def maxValue(agentIndex, depth, state, alpha, beta): # Pacman
        #     legalActions = state.getLegalActions(agentIndex)
        #     if not legalActions: return self.evaluationFunction(state)

        #     # Find the best action's value by maximizing over possible successors
        #     bestScore = float('-inf') # min init val
        #     for action in legalActions:
        #         if(alpha >= beta): break # prune
        #         successor = state.generateSuccessor(agentIndex, action)
        #         evaluation = minimax(1, depth, successor, alpha, beta)
        #         bestScore = max(bestScore, evaluation) # update best score for max in current subtree
        #         alpha = max(alpha, bestScore) # update alpha to max on current subtree
        #     return bestScore

        # def minValue(agentIndex, depth, state, alpha, beta): # Ghost
        #     legalActions = state.getLegalActions(agentIndex)
        #     if not legalActions: return self.evaluationFunction(state)

        #     bestScore = float('inf')
        #     nextAgent = agentIndex
        #     if(agentIndex == state.getNumAgents() - 1): nextAgent = 0
        #     else: nextAgent = nextAgent + 1

        #     for action in legalActions:
        #         if alpha >= beta: break #Prune
        #         successor = state.generateSuccessor(agentIndex, action)
        #         if nextAgent == 0:  # Back to Pacman
        #             evaluation = minimax(nextAgent, depth + 1, successor, alpha, beta)
        #         else:  # Other ghosts
        #             evaluation = minimax(nextAgent, depth, successor, alpha, beta)
                
        #         bestScore = min(bestScore, evaluation) # update best score for min in current subtree
        #         beta = min(beta, bestScore) # update beta to min on current subtree
        #     return bestScore
        
        # # get legal actions of Pacman (first agent - max)
        # bestScore = float('-inf') # min init val
        # bestAction = None
        # legalActions = gameState.getLegalActions(0)
        # for action in legalActions:
        #     successor = gameState.generateSuccessor(0, action) # get pacman successor state
        #     score = minimax(1, 0, successor, float('-inf'), float('inf'))  # next agent is the first ghost
        #     if score > bestScore: # maximize score and track of max score action
        #         bestScore = score
        #         bestAction = action
        # return bestAction