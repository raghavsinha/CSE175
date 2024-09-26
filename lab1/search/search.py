# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class Node:
    def __init__(self, state, action, parent, cost):
        self.state = state
        self.action = action
        self.parent = parent
        self.cost = cost
    
class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    
    # create stack and push first node
    # recurse until no nodes in stack:
    #   if top node is visited, pop
    #   if not, mark top node on stack as visited and push all its neighbors

    # you can also do this with a dictionary of tuples where each tuple contains the state and the action and parent
    # or you can use a dictionary of actions where each state is mapped to a list of actions for how to get there
    rootState = problem.getStartState()
    rootNode = Node(rootState, None, None)
    visited = {'0'}
    visitedStates = {'0'}
    stack = util.Stack()
    stack.push(rootNode)
    actions = list()

    while(not stack.isEmpty()):
        top = stack.list[-1]
        if(problem.isGoalState(top.state)):
            curr = top
            while(curr.state != rootState):
                actions.append(curr.action)
                curr = curr.parent
            actions.reverse()
            break
        else:
            if(top in visited):
                stack.pop()
            else:
                visited.add(top)
                visitedStates.add(top.state)
                print top.state
                succs = problem.getSuccessors(top.state)
                for s in succs:
                    action, nextState = s[1], s[0]
                    if(nextState not in visitedStates):
                        nextNode = Node(nextState, action, top)
                        stack.push(nextNode)
    return actions
    #util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    rootState = problem.getStartState()
    rootNode = Node(rootState, None, None)
    visited = {'0'}
    visitedStates = {'0'}
    queue = util.Queue()
    queue.push(rootNode)
    actions = list()

    while(not queue.isEmpty()):
        front = queue.list[-1]
        if(problem.isGoalState(front.state)):
            curr = front
            while(curr.state != rootState):
                actions.append(curr.action)
                curr = curr.parent
            actions.reverse()
            break
        else:
            if(front in visited):
                queue.pop()
            else:
                visited.add(front)
                visitedStates.add(front.state)
                succs = problem.getSuccessors(front.state)
                for s in succs:
                    action, nextState = s[1], s[0]
                    if(nextState not in visitedStates):
                        nextNode = Node(nextState, action, front)
                        queue.push(nextNode)
    return actions
    #util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    rootState = problem.getStartState()
    rootNode = Node(rootState, None, None, 0)
    visited = {rootState:rootNode}
    pq = util.PriorityQueue()
    pq.push(rootNode, 0)
    actions = list()

    while(not pq.isEmpty()):
        front = pq.pop()
        if(problem.isGoalState(front.state)):
            curr = front
            while(curr.state != rootState):
                actions.append(curr.action)
                curr = curr.parent
            actions.reverse()
            break
        else:
            print(visited.keys())
            visited[front.state] = front
            succs = problem.getSuccessors(front.state)
            for s in succs:
                action, nextState, cost = s[1], s[0], s[2]
                child = Node(nextState, action, front, front.cost + cost)
                if((nextState not in visited) or (cost < visited[nextState])):
                    visited[nextState] = child
                    pq.push(child, child.cost)
    return actions
    #util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    rootState = problem.getStartState()
    goalState = problem.goal
    rootNode = Node(rootState, None, None, 0)
    visited = {rootState:rootNode}
    pq = util.PriorityQueue()
    pq.push(rootNode, 0)
    actions = list()

    while(not pq.isEmpty()):
        front = pq.pop()
        if(problem.isGoalState(front.state)):
            curr = front
            while(curr.state != rootState):
                actions.append(curr.action)
                curr = curr.parent
            actions.reverse()
            break
        else:
            print(visited.keys())
            visited[front.state] = front
            succs = problem.getSuccessors(front.state)
            for s in succs:
                action, nextState, gCost = s[1], s[0], s[2]
                manhattanCost = gCost + util.manhattanDistance(nextState, goalState)
                if((nextState not in visited) or (manhattanCost < visited[nextState])):
                    child = Node(nextState, action, front, manhattanCost)
                    visited[nextState] = child
                    pq.push(child, child.cost)
    return actions
    #util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch