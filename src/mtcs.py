import math
from board import *
from copy import deepcopy
import random
import time


EXPLORATION_FACTOR = 0.1

class MCTSNode:
    def __init__(self, move: Move, parent=None):
        self.move = move  # The move which led to this state
        self.parent = parent  # Parent node
        self.children = {}  # Child nodes
        self.N = 0  # Number total of game played
        self.Q = 0 # Number total of game won
    

    def add_children(self, children: dict) -> None:
        """Add children to a node

        Parameters:
            children(dict) : children to add to the current node
        """
        for child in children:
            self.children[str(child.move)] = child


    def uct(self, exploration_factor: float = EXPLORATION_FACTOR):
        """Compute the upper confidence bound applied on trees

        Parameters:
            exploration_factor(float) : factor to balance between exploration and exploitation
        """
        if self.N == 0:
            return 0 
        return self.Q / self.N + exploration_factor * math.sqrt(math.log(self.parent.N) / self.N)


class MTCS:
    def __init__(self, state: Board) -> None:
        self.root_state = deepcopy(state)
        self.root = MCTSNode(None, None)
        self.run_time = 0
        self.node_count = 0
        self.num_rollouts = 0
        pass
        
    def is_fully_expanded(self):
        """
        Check if all child states have been explored
        (i.e., if all legal moves from this state have corresponding child nodes)
        """
        return len(self.children) == len(self.state.legal_moves)
    
    def select(self):
        """
        Choose the best child node based on the UCB1 formula (exploration vs. exploitation trade-off)
        This involves finding the child node with the highest UCB1 value
        """
        node = self.root
        state = deepcopy(self.root_state)

        while len(node.children) != 0:
            children = node.children.values()
            max_value = max(children, key=lambda n : n.uct()).uct()
            max_nodes = [n for n in children if n.uct() == max_value]

            node = random.choice(max_nodes)

            state = state.apply_move(node.move)

            if node.N == 0:
                return node, state

        if self.expand(node, state):
            node = random.choice(list(node.children.values()))
            state = state.apply_move(node.move)
        
        return node, state
    
    def expand(self, parent: MCTSNode, state: Board) -> bool:
        """
        Create a new child node corresponding to an unexplored legal move
        Update the game state according to the selected move

        Parameters:
            parent(MTCSNode) : Parent of the current node
            state(Board) : State of the current board
        """
        if is_game_over(state):
            return False
    
        children = [MCTSNode(move, parent) for move in generate_legal_moves(state)]

        parent.add_children(children)

        return True
    
    def rollout(self, state: Board):
        """Simulate a game from the current state until a terminal state is reached

        Parameters:
            state: the current state of the board.

        Return:
            the result of the simulation (e.g., +1 for win, -1 for loss, 0 for draw)
        """
        while not is_game_over(state):
            state = state.apply_move(random.choice(list(generate_legal_moves(state))))
        
        return get_outcome(state)
    
    def backpropagate(self, node: MCTSNode, turn: int, outcome: int):
        """
        Update the node's visits and reward statistics, and propagate the update up the tree

        Parameters:
            node(MTCSNode) : Current node to begin backprop
            turn(int) : The turn color
            outcome(int) : the result of the simulation (e.g., +1 for win, -1 for loss, 0 for draw)
        """
        reward = 0 if outcome == turn else 1

        while node is not None:
            node.N += 1
            node.Q += reward
            node = node.parent

            if outcome == is_draw(self.root_state):
                reward = 0
            else:
                reward = 1 - reward

    

    def mtcs_search(self, time_limit: int):
        """
        Launch the monte carlo tree search (selection, expansion, simulation, backpropagation)

        Parameters:
            time_limit(int) : time limit to search in the tree
        """
        start_time = time.process_time()

        num_rollouts = 0

        while time.process_time() - start_time < time_limit:
            node, state = self.select()
            outcome = self.rollout(state=state)
            self.backpropagate(node, state.color_turn, outcome)
            num_rollouts +=1

        run_time = time.process_time() - start_time
        self.run_time = run_time
        self.num_rollouts = num_rollouts

    def choose_best_move(self) -> Move:
        """
        Choose the best move in the mtcs (choosing the node with the most total game played)

        Return:
            Move : the best move choosen
        """
        if is_game_over(self.root_state):
            return None
        
        max_value = max(self.root.children.values(), key=lambda n: n.N).N
        max_nodes = [node for node in self.root.children.values() if node.N == max_value]
        best_child = random.choice(max_nodes)

        return best_child.move
    
    def move(self, move: Move):
        if move in self.root.children:
            self.root_state = self.root_state.apply_move(move)
            self.root = self.root.children[str(move)]
            return
        
        self.root_state = self.root_state.apply_move(move)
        self.root = MCTSNode(None, None)

    def statistics(self) -> tuple:
        """
        Get statistics of the MTCS

        Return:
            Tuple : the number of rollout and the run_time
        """
        return self.num_rollouts, self.run_time