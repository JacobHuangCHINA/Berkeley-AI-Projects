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

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    
    stack = util.Stack()
    stacklist = set()
    path = {}
    
    stack.push(problem.getStartState())
    
    if problem.isGoalState(problem.getStartState()):
        return []
    
    while not stack.isEmpty():
        curNode = stack.pop()
        
        if not curNode == problem.getStartState():
           state = curNode[0]
        else:
           state = curNode
                
        if problem.isGoalState(state):
            return decode_path(curNode,path,problem)

        stacklist.add(state)
        
        for nexNode in problem.getSuccessors(state):
            if nexNode[0] in stacklist:
                continue
            
            stack.push(nexNode)
                                           
            if not nexNode in path:
                path[nexNode] = curNode

    return False                
        
def decode_path(curNode, path, problem):               
    #decode path into actions
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    n = Directions.NORTH
    e = Directions.EAST
    pathStack = util.Stack()
    actions = []
    while not curNode == problem.getStartState():
        
        pathStack.push(curNode) 
        curNode = path[curNode]
    

    while not pathStack.isEmpty():
        curNode = pathStack.pop()
        if curNode[1] == 'West':
            actions.append(w)
        elif curNode[1] == 'East':
            actions.append(e)
        elif curNode[1] == 'North':
            actions.append(n)
        elif curNode[1] == 'South':
            actions.append(s)
        else:
            actions.append(curNode[1])
    return actions        
            
    '''
    print problem.getStartState
    print "Is the start a goal", problem.isGoalState(problem.getStartState())
    print "start's successors:", problem.getSuccessors(problem.getStartState())
    '''
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    
    Q= util.PriorityQueue()
    path = {}
    #Set up cycle checking by making dictionary with Min costs for visited nodes:
    visited = {}
    expanded = set()
    start = problem.getStartState()
    visited[start] = 0
      
    if problem.isGoalState(start):
        return []

    
    Q.push(start,0)
      
    
    while not Q.isEmpty():
        
        curNode = Q.pop()
        if not curNode == problem.getStartState():
            state = curNode[0]
        else:
            state = curNode
        cost = visited[state]

        if state not in expanded:
                     
            if problem.isGoalState(state):
                return decode_path(curNode,path,problem)
            
            for nexNode in problem.getSuccessors(state):
                expanded.add(state)
                
                nexCost = cost + nexNode[2]
                #node[2] is always equal to 1 in breadth first
                #therefore, change this to nexNode[2] and you have the uniform cost search
                if nexNode[0] not in visited:
                    visited[nexNode[0]] = nexCost
                    Q.push(nexNode,nexCost)
                    path[nexNode] = curNode
                elif nexCost <=visited[nexNode[0]]:
                    visited[nexNode[0]] =nexCost
                    Q.push(nexNode,nexCost)
                    path[nexNode] = curNode
                   
    return False
    
        
    
def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    Q= util.PriorityQueue()
    path = {}
    #Set up cycle checking by making dictionary with Min costs for visited nodes:
    visited = {}
    expanded = set()
    start = problem.getStartState()
    visited[start] = 0
      
    if problem.isGoalState(start):
        return []
    
    Q.push(start,0)
    
    
    
    while not Q.isEmpty():
        
        curNode = Q.pop()
        if not curNode == problem.getStartState():
            state = curNode[0]
        else:
            state = curNode
        cost = visited[state]

        if state not in expanded:
                     
            if problem.isGoalState(state):
                return decode_path(curNode,path,problem)
            
            for nexNode in problem.getSuccessors(state):
                expanded.add(state)
                
                nexCost = cost + nexNode[2]
                #node[2] is always equal to 1 in breadth first
                #therefore, change this to nexNode[2] and you have the uniform cost search
                if nexNode[0] not in visited:
                    visited[nexNode[0]] = nexCost
                    Q.push(nexNode,nexCost)
                    path[nexNode] = curNode
                elif nexCost <=visited[nexNode[0]]:
                    visited[nexNode[0]] =nexCost
                    Q.push(nexNode,nexCost)
                    path[nexNode] = curNode
                   
    return False

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    #MOSTLY RIGHT BUT EXPANDING TOO MANY NODES + ONE OTHER CASE

    
    #basically the same, with cost of BFS and UCS as g, and heuristic as h to form f= g+h
    Q= util.PriorityQueue()
    path = {}
    #Set up cycle checking by making dictionary with Min costs for visited nodes:
    visited = {}
    expanded = set()
    start = problem.getStartState()
    
      
    if problem.isGoalState(start):
        return []

    HofN = heuristic(start,problem)
    visited[start] = HofN
    Q.push(start,HofN)#note GofN is 0 at starting node
    
      
    while not Q.isEmpty():
        
        curNode = Q.pop()
        if not curNode == problem.getStartState():
            state = curNode[0]
        else:
            state = curNode
        cost = visited[state]
        
        if state not in expanded:
                     
            if problem.isGoalState(state):
                return decode_path(curNode,path,problem)
            
            for nexNode in problem.getSuccessors(state):
                expanded.add(state)

                HofN = heuristic(nexNode[0],problem)
                GofN =  cost + nexNode[2] #(wait but that cost includes heuristic)
                #no actually we only save "travel" cost,or cost to get there from origin,
                #we don't compound all of the heuristics together
                
                nexCost = GofN + HofN
                if nexNode[0] not in visited:
                    visited[nexNode[0]] = GofN
                    Q.push(nexNode,nexCost)
                    path[nexNode] = curNode
                elif nexCost <=visited[nexNode[0]]:
                    visited[nexNode[0]] = GofN
                    Q.push(nexNode,nexCost)
                    path[nexNode] = curNode
                   
    return False

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
