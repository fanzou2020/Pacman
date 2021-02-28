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
import heapq

import util

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

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))

    open = util.Stack()  # store states in stack
    currPath = util.Stack()  # store path of expanded states
    visited = []

    open.push(problem.getStartState())
    currPath.push([])
    while not open.isEmpty():
        state = open.pop()
        path = currPath.pop()

        if state not in visited:
            visited.append(state)

            if problem.isGoalState(state):
                return path

            for nextState, action, cost in problem.getSuccessors(state):
                open.push(nextState)
                currPath.push(path + [action])


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    open = util.Queue()
    currPath = util.Queue()
    visited = []

    open.push(problem.getStartState())
    currPath.push([])
    while not open.isEmpty():
        state = open.pop()
        path = currPath.pop()

        if state not in visited:
            visited.append(state)

            if problem.isGoalState(state):
                return path

            for nextState, action, cost in problem.getSuccessors(state):
                open.push(nextState)
                currPath.push(path + [action])



def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    open = util.PriorityQueue() # key state, priority is cost
    currPath = dict()  # key is state, value is (path, cost)
    visited = []
    open.push(problem.getStartState(), 0)
    currPath[problem.getStartState()] = ([], 0)

    while not open.isEmpty():
        state = open.pop()
        path, cost = currPath[state]
        if state not in visited:
            visited.append(state)

            if problem.isGoalState(state):
                return path

            for nextState, action, nextCost in problem.getSuccessors(state):
                # relax process in Dijsktra
                open.update(nextState, cost+nextCost)
                if nextState not in currPath:
                    currPath[nextState] = (path + [action], cost + nextCost)
                else:
                    oldPath, oldCost = currPath[nextState]
                    if nextCost + cost < oldCost:
                        currPath[nextState] = (path + [action], cost + nextCost)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # # the key of pq should be the state node.
    # def updateByComparingState(pq, item, priority):
    #     for index, (p, c, i) in enumerate(pq.heap):
    #         if i[0] == item[0]:  # modification here
    #             if p <= priority:
    #                 break
    #             del pq.heap[index]
    #             pq.heap.append((priority, c, item))
    #             heapq.heapify(pq.heap)
    #             break
    #     else:
    #         pq.push(item, priority)
    #
    # open = util.PriorityQueue()
    # visited = []
    # startState = problem.getStartState()
    # startHeuristic = heuristic(startState, problem)
    # open.push((problem.getStartState(), [], 0), startHeuristic)
    #
    # while not open.isEmpty():
    #     state, actions, cost = open.pop()
    #     if state not in visited:
    #         visited.append(state)
    #
    #         if problem.isGoalState(state):
    #             return actions
    #
    #         for nextState, action, nextCost in problem.getSuccessors(state):
    #             newCostPlusHeuristic = cost + nextCost + heuristic(nextState, problem)
    #             updateByComparingState(open, (nextState, actions + [action], cost + nextCost), newCostPlusHeuristic)
    #

    open = util.PriorityQueue() # key is state, priority is cost+heuristic
    currPath = dict()  # key is state, value is (path, cost)
    visited = []
    startState = problem.getStartState()
    open.push(startState, heuristic(startState, problem))
    currPath[startState] = ([], 0)

    while not open.isEmpty():
        state = open.pop()
        path, cost = currPath[state]
        if state not in visited:
            visited.append(state)

            if problem.isGoalState(state):
                return path

            for nextState, action, nextCost in problem.getSuccessors(state):
                # relax process in Dijsktra
                newCostPlusHeuristic = cost + nextCost + heuristic(nextState, problem)
                open.update(nextState, newCostPlusHeuristic)
                if nextState not in currPath:
                    currPath[nextState] = (path + [action], cost + nextCost)
                else:
                    oldPath, oldCost = currPath[nextState]
                    if nextCost + cost < oldCost:
                        currPath[nextState] = (path + [action], cost + nextCost)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
