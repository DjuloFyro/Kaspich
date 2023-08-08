class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state  # The game state associated with the node
        self.parent = parent  # Parent node
        self.children = []  # Child nodes
        self.visits = 0  # Number of times the node has been visited
        self.reward = 0  # Cumulative reward obtained from simulations
        
    def is_fully_expanded(self):
        """
        Check if all child states have been explored
        (i.e., if all legal moves from this state have corresponding child nodes)
        """
        return len(self.children) == len(self.state.legal_moves)
    
    def best_child(self, exploration_constant):
        # Choose the best child node based on the UCB1 formula (exploration vs. exploitation trade-off)
        # This involves finding the child node with the highest UCB1 value
        pass
    
    def expand(self):
        """
        Create a new child node corresponding to an unexplored legal move
        Update the game state according to the selected move
        """
        pass
    
    def simulate(self):
        """
        Simulate a game from the current state until a terminal state is reached
        Return the result of the simulation (e.g., +1 for win, -1 for loss, 0 for draw)
        """
        pass
    
    def backpropagate(self, reward):
        """
        Update the node's visits and reward statistics, and propagate the update up the tree
        """
        pass