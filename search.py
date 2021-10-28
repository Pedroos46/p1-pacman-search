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
    """
    """print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))"""

    "*** YOUR CODE HERE ***"
    """We initialize all the variables we need to implement the search algorithm"""
    expandedNodes = []
    frontier = util.Stack() #it will save triplets of type [state:tuple int, direction:string, cost:int)
    initial_state = problem.getStartState()
    frontier.push([initial_state, "", 0])  #it doesn't have a direction because is the initial state. The cost is 0.
    path_record = {} #Dict that saves the parent info of each child that has been visited
    path = [] #Actions to do from the inital state to the goal

    """ We check if the frontier is empty or not to proceed with the computations """
    while not frontier.isEmpty():
        """ Pop a node to the frontier and add it to the extended ones """
        node = frontier.pop()
        expandedNodes.append(node[0])
        """ Check if the state is the goal one"""
        if problem.isGoalState(node[0]):
            """it recovers the actions the pacman have to do from the initial state to the goal one."""
            child = node

            while child[0] is not initial_state:
                parent = path_record[child[0]]
                path.append(parent[1])
                child = parent

            path = path[::-1]
            path = path[1:]
            path.append(node[1])
            return path

        """ It retrieves the successors per node, checks if we have already expanded to that node and 
        if not, records the parent of the node and deletes the node from the frontier """
        succesorsArray = problem.getSuccessors(node[0])
        for n in succesorsArray:
            if n not in frontier.list and n[0] not in expandedNodes:
                frontier.push(n)
                path_record[n[0]] = node

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    expandedNodes = []
    frontier = util.Queue() #it will save triplets of type [state:tuple int, direction:string, cost:int)
    initial_state = problem.getStartState()
    path_record = {} #Dict that saves the parent info of each child that has been visited
    path = [] #Actions to do from the inital state to the goal
    frontier_state = []
    frontier.push([initial_state, "", 0])  #it doesn't have a direction because is the initial state. The cost is 0.
    frontier_state.append(initial_state)
    """ We check if the frontier is empty or not to proceed with the computations """

    while not frontier.isEmpty():
        """ Pop a node to the frontier and add it to the extended ones """
        node = frontier.pop()
        expandedNodes.append(node[0])
        """ Check if the state is the goal one"""
        if problem.isGoalState(node[0]):
            """it recovers the actions the pacman have to do from the initial state to the goal one."""
            child = node

            """Especific for q5"""
            tempChild = child[0]
            if isinstance(tempChild[0], tuple) and isinstance(tempChild[1], list):
                while tempChild[0] is not initial_state[0]:
                    parent = path_record[tempChild[0]]
                    path.append(tempChild[1])
                    child = parent

            else:
                """ q2 """
                while child[0] is not initial_state:
                    parent = path_record[child[0]]
                    path.append(parent[1])
                    child = parent


            path = path[::-1]
            path = path[1:]
            path.append(node[1])
            return path

        """ It retrieves the successors per node, checks if we have already expanded to that node and 
        if not, records the parent of the node and deletes the node from the frontier """
        succesorsArray = problem.getSuccessors(node[0])
        for n in succesorsArray:
            """Especific for q5"""
            tempn = n[0]
            if isinstance(tempn, tuple) and isinstance(tempn[1], list):
                if tempn[0] not in frontier_state and tempn[0] not in expandedNodes:
                    frontier.push(n)
                    frontier_state.append(tempn[0])
                    path_record[tempn[0]] = node

            else:
                """ q2 """
                if n[0] not in frontier_state and n[0] not in expandedNodes:
                    frontier.push(n)
                    frontier_state.append(n[0])
                    path_record[n[0]] = node


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    expandedNodes = []
    frontier = util.PriorityQueue()  # it will save triplets of type [state:tuple int, direction:string, cost:int)
    initial_state = problem.getStartState()
    path_record = {}  # Dict that saves the parent info of each child that has been visited
    path = []  # Actions to do from the inital state to the goal

    frontier.push([initial_state, "", 0], 0)  # it doesn't have a direction because is the initial state. The cost is 0.

    """ We check if the frontier is empty or not to proceed with the computations """
    while not frontier.isEmpty():
        """ Pop a node from the frontier  """
        node = frontier.pop()

        """ Check if the state is the goal one"""
        if problem.isGoalState(node[0]):
            """it backpropagates through the states to obtain the actions the pacman have to do from the initial state to the goal one."""
            child = node

            while child[0] is not initial_state:
                father = path_record[child[0]]
                path.append(father[1])
                child = father

            path = path[::-1] #we reverse the list to have the order from initial state to goal state
            path = path[1:]
            path.append(node[1])

            return path

        """ It retrieves the successors per node, checks if we have already expanded to that node and 
        if not, records the parent of the node as well as the cost from the parent to the node """

        "Check if the node it has not been expanded yet"
        if node[0] not in expandedNodes:
            expandedNodes.append(node[0])
            succesorsArray = problem.getSuccessors(node[0])

            for n in succesorsArray:
                """We backpropagate through the states to compute the total cost from the initial state to node "n" """
                fam_val = 0
                if n[0] not in expandedNodes:
                    """Checks if the node expanded is not the initial state """
                    if node[0] is not initial_state:
                        grandpa = path_record[node[0]]
                        fam_val = grandpa[2]
                        """Until we arrive to the initial node, we sum all costs it takes to go to the expanded node"""
                        while grandpa[0] != initial_state:
                            grandpa = path_record[grandpa[0]]
                            fam_val += grandpa[2]
                    """The total cost is the sum of the successor cost plus the family cost"""
                    total_cost = n[2]  + fam_val
                    frontier.update(n, total_cost) #we push it to the priority queue

                    """We add the successors as a new entry of the path record unless they where recorded before"""
                    if n[0] in path_record.keys():
                        """We compute the total family cost of the recorded path in order to compare it later with the new path we are checking """
                        father = path_record[n[0]]
                        fam_val2 = father[2]
                        if father[0] != initial_state:
                            grandpa2 = path_record[father[0]]
                            fam_val2 += grandpa2[2]
                            while grandpa2[0] != initial_state:
                                grandpa2 = path_record[grandpa2[0]]
                                fam_val2 += grandpa2[2]
                        """If the new path has a lower cost than the path recorded then we change the successor node's father"""
                        if fam_val2 > total_cost:
                            path_record[n[0]] = [node[0], node[1], n[2]]
                    else:
                        """If the succesor wasn't recorded before and it's not the initial state we create a new entry in the record"""
                        if n[0] is not initial_state:
                            path_record[n[0]] = [node[0], node[1], n[2]]

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """



    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    expandedNodes = []
    frontier = util.PriorityQueue()  # it will save triplets of type [state:tuple int, direction:string, cost:int)
    initial_state = problem.getStartState()
    path_record = {}  # Dict that saves the parent info of each child that has been visited
    path = []  # Actions to do from the inital state to the goal

    frontier.push([initial_state, "", 0], 0)  # it doesn't have a direction because is the initial state. The cost is 0.

    """ We check if the frontier is empty or not to proceed with the computations """
    while not frontier.isEmpty():
        """ Pop a node from the frontier  """
        node = frontier.pop()

        """ Check if the state is the goal one"""
        if problem.isGoalState(node[0]):
            """it backpropagates through the states to obtain the actions the pacman have to do from the initial state to the goal one."""
            child = node

            while child[0] is not initial_state:
                father = path_record[child[0]]
                path.append(father[1])
                child = father

            path = path[::-1]  # we reverse the list to have the order from initial state to goal state
            path = path[1:]
            path.append(node[1])

            return path

        """ It retrieves the successors per node, checks if we have already expanded to that node and 
        if not, records the parent of the node as well as the cost from the parent to the node """

        "Check if the node it has not been expanded yet"
        if node[0] not in expandedNodes:
            expandedNodes.append(node[0])
            succesorsArray = problem.getSuccessors(node[0])

            for n in succesorsArray:
                """We backpropagate through the states to compute the total cost from the initial state to node "n" """
                fam_val = 0
                if n[0] not in expandedNodes:
                    """Checks if the node expanded is not the initial state """
                    if node[0] is not initial_state:
                        grandpa = path_record[node[0]]
                        fam_val = grandpa[2]
                        """Until we arrive to the initial node, we sum all costs it takes to go to the expanded node"""
                        while grandpa[0] != initial_state:
                            grandpa = path_record[grandpa[0]]
                            fam_val += grandpa[2]
                    """The total cost is the sum of the successor cost plus the family cost"""
                    total_cost = n[2] + fam_val
                    frontier.update(n, total_cost + heuristic(n[0],problem))  # we push it to the priority queue

                    """We add the successors as a new entry of the path record unless they where recorded before"""
                    if n[0] in path_record.keys():
                        """We compute the total family cost of the recorded path in order to compare it later with the new path we are checking """
                        father = path_record[n[0]]
                        fam_val2 = father[2]
                        if father[0] != initial_state:
                            grandpa2 = path_record[father[0]]
                            fam_val2 += grandpa2[2]
                            while grandpa2[0] != initial_state:
                                grandpa2 = path_record[grandpa2[0]]
                                fam_val2 += grandpa2[2]
                        """If the new path has a lower cost than the path recorded then
                         we change the successor node's father"""
                        if fam_val2 > total_cost:
                            path_record[n[0]] = [node[0], node[1], n[2]]
                    else:
                        """If the succesor wasn't recorded before and it's not the 
                        initial state we create a new entry in the record"""
                        if n[0] is not initial_state:
                            path_record[n[0]] = [node[0], node[1], n[2]]

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
