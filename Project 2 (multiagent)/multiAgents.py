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

        min_dist = -1
        for i in range(len(newFood[:])):
            for q in range(len(newFood[0])):
            
                if newFood[i][q]:
                    foodPos = tuple((i,q))
                    dist = util.manhattanDistance(newPos,foodPos)
                    if (dist < min_dist) or (min_dist == -1):
                        min_dist = dist

                           
        min_g_dist = -1
        for ghost in newGhostStates:
            gPos = ghost.getPosition()
            g_dist = util.manhattanDistance(newPos, gPos)
            if (g_dist < min_g_dist) or (min_g_dist == -1):
                min_g_dist = g_dist

                
        if (currentGameState.getNumFood() > successorGameState.getNumFood()) and (min_g_dist > 2):
            heuristic = 100
        elif min_g_dist > 2:
            heuristic = 1.0/min_dist
        else:
            heuristic = (1.0/min_dist) + min_g_dist
           
        return heuristic
    
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
        def max_node(depth, state):
            
            if (depth ==0) or (state.isLose()) or (state.isWin()):
                return self.evaluationFunction(state), Directions.STOP         
           
            max_score = float('-inf')
            
            for action in state.getLegalActions(0):
                
                nex_state = state.generateSuccessor(0, action)
                score = min_node(1, depth, nex_state)
                
                if score > max_score:
                    max_score = score
                    best_action = action
            
            
            return max_score, best_action
         
        def min_node(agentIDX, depth, state):
            
            if (depth == 0) or (state.isLose()) or (state.isWin()):
                return self.evaluationFunction(state)
            
            min_score = float('inf')
            
            for action in state.getLegalActions(agentIDX):
                
                nex_state = state.generateSuccessor(agentIDX, action)
                
                if agentIDX == (gameState.getNumAgents() -1):
                    score, unnecessary_action = max_node(depth - 1, nex_state)
                else:                    
                    score = min_node(agentIDX + 1, depth, nex_state)
                

                if (score < min_score):
                    min_score = score
                            
            return min_score        
                
        max_score, best_action = max_node(self.depth, gameState)
        
        return best_action 

                

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        def max_node(alpha, beta, depth, state):
            
            if (depth ==0) or (state.isLose()) or (state.isWin()):
                return self.evaluationFunction(state), Directions.STOP         
           
            max_score = float('-inf')
            
            for action in state.getLegalActions(0):
                
                nex_state = state.generateSuccessor(0, action)
                score = min_node(alpha, beta, 1, depth, nex_state)
                
                if score > max_score:
                    max_score = score
                    best_action = action
                    
                if max_score >=  beta:
                    return max_score, best_action
                if max_score > alpha:
                    alpha = max_score
            
            return max_score, best_action
         
        def min_node(alpha, beta, agentIDX, depth, state):
            
            if (depth == 0) or (state.isLose()) or (state.isWin()):
                return self.evaluationFunction(state)
            
            min_score = float('inf')
            
            for action in state.getLegalActions(agentIDX):
                
                nex_state = state.generateSuccessor(agentIDX, action)
                
                if agentIDX == (gameState.getNumAgents() -1):
                    score, unnecessary_action = max_node(alpha, beta, depth - 1, nex_state)
                else:                    
                    score = min_node(alpha, beta, agentIDX + 1, depth, nex_state)
                
                if (score < min_score):
                    min_score = score

                if min_score <= alpha:
                    return min_score
                if min_score < beta:
                    beta = min_score
                            
            return min_score        
        init_alpha = float('-inf')
        init_beta = float('inf')
        max_score, best_action = max_node(init_alpha, init_beta, self.depth, gameState)
        
        return best_action 

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
        
        def max_node(depth, state):
            
            if (depth ==0) or (state.isLose()) or (state.isWin()):
                return self.evaluationFunction(state), Directions.STOP         
           
            max_score = float('-inf')
            
            for action in state.getLegalActions(0):
                
                nex_state = state.generateSuccessor(0, action)
                score = min_node(1, depth, nex_state)
                
                if score > max_score:
                    max_score = score
                    best_action = action
            
            
            return max_score, best_action
         
        def min_node(agentIDX, depth, state):
            #should be exp node but it's basically the same
            #just didn't want to spend the time renaming everything.
            if (depth == 0) or (state.isLose()) or (state.isWin()):
                return self.evaluationFunction(state)
            
            score = 0
            num_act = float(len(state.getLegalActions(agentIDX))) 
            
            for action in state.getLegalActions(agentIDX):
                
                nex_state = state.generateSuccessor(agentIDX, action)
                
                if agentIDX == (gameState.getNumAgents() -1):
                    new_score, unnecessary_action = max_node(depth - 1, nex_state)
                    score += new_score/num_act
                else:                    
                    score += min_node(agentIDX + 1, depth, nex_state)/num_act
                        
                          
            return score

        max_score, best_action = max_node(self.depth, gameState)

        
        return best_action

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    
    #Setting up the weights to multiply the features
    #full marks with -2, -1, -1, -1, 1, -1 
    tot_f_w = -2  #should be negative, we want less pellets-> more negative than food 
    food_w = -1 #should be negative, we want smaller distance
    ghost_w = -1 #should be negative since we want larger distance (and this value is inverse)
    scared_w = -1  #should be positive since we want smaller distance (and this value is inverse)
    score_w = 1 #gonna keep this at 1 and adjust everything else to them
    power_pellet_w = -1 #should be negative, we want less, but less negative than food

    #extracting information from currentGameState
    pac_pos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    power_pellets = currentGameState.getCapsules()     
    ###################################
    #######CALCULATING FEATURES########
    ###################################

    #total food left:
    tot_food = currentGameState.getNumFood()
    
    #minimum distance to a food pellet:
    food_dist = float('inf')
    for i in range(len(newFood[:])):
        for q in range(len(newFood[0])):
            if newFood[i][q]:
                food_pos= tuple((i,q))
                f_dist = util.manhattanDistance(pac_pos, food_pos)
                if f_dist < food_dist:
                    food_dist = f_dist
    #edge case
    if food_dist == float('inf'):
        food_dist = 0
                        
    #minimum distance to a ghost and min dist to a scared ghost:             
    ghost_dist = float('inf')
    for ghost in newGhostStates:
        ghost_pos = ghost.getPosition()
        g_dist = util.manhattanDistance(pac_pos, ghost_pos)
        if g_dist < ghost_dist:
            ghost_dist = g_dist
    #edge case when distance to ghost is 0        
    if ghost_dist == 0:
        ghost_dist = 0.1
            
           
    #minimum distance to a scared ghost:        
    scared_g_dist = float('inf')
    for ghost in newGhostStates:
        if ghost.scaredTimer > 0:
            scared_pos = ghost.getPosition()
            scared_dist = util.manhattanDistance(pac_pos, scared_pos)
            if scared_dist < scared_g_dist:
                scared_g_dist = scared_dist
    #edge case for when distance to scared ghost is 0            
    if scared_g_dist == 0:
        scared_g_dist = 0.1

    #base score of current game state:
    score = scoreEvaluationFunction(currentGameState)

    #minimum distance to power pellet
    pow_p_dist = float('inf')
    for power_p in power_pellets:
        power_dist = util.manhattanDistance(pac_pos, power_p)
        if power_dist < pow_p_dist:
            pow_p_dist = power_dist
    #edge case
    if pow_p_dist == float('inf'):
        pow_p_dist = 0
    
    #calculate herustic with weights:
    heuristic = (score_w*score) + (tot_f_w*tot_food) + (food_w*food_dist) + (ghost_w*(1.0/ghost_dist)) + (scared_w*(1.0/scared_g_dist))

    return heuristic

# Abbreviation
better = betterEvaluationFunction

