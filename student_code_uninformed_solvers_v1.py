
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def genChildren(self):
        poss_moves = self.gm.getMovables()
        for move in poss_moves:
            self.gm.makeMove(move)
            child_state = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)
            if child_state not in self.visited:
                child_state.parent = self.currentState
                self.currentState.children.append(child_state)
            self.gm.reverseMove(move)

    def visitChild(self):
        curr_state = self.currentState
        while curr_state.nextChildToVisit < len(curr_state.children):
            child_state = curr_state.children[curr_state.nextChildToVisit]
            curr_state.nextChildToVisit += 1
            if child_state not in self.visited:
                self.visited[child_state] = True
                self.gm.makeMove(child_state.requiredMovable)
                self.currentState = child_state
                return True
        return False

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if self.currentState.state == self.victoryCondition:
            return True
        while True:
            if not self.currentState.children:
                self.genChildren()
            if self.visitChild():
                return False
            if self.currentState.parent:
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent
            else:
                return True


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def genChildrenAtDepth(self, depth):
        self.currentState.nextChildToVisit = GameState.FIRST_CHILD_INDEX
        if depth == self.currentState.depth:
            poss_moves = self.gm.getMovables()
            for move in poss_moves:
                self.gm.makeMove(move)
                child_state = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)
                if child_state not in self.visited:
                    child_state.parent = self.currentState
                    self.currentState.children.append(child_state)
                self.gm.reverseMove(move)
            if self.currentState.children:
                return True
            else:
                return False
        elif depth > self.currentState.depth:
            curr_state = self.currentState
            atLeastOneChild = False
            for child in curr_state.children:
                self.gm.makeMove(child.requiredMovable)
                self.currentState = child
                if self.genChildrenAtDepth(depth):
                    atLeastOneChild = True
                self.gm.reverseMove(child.requiredMovable)
                self.currentState = self.currentState.parent
            return atLeastOneChild

    def visitNodeAtDepth(self, depth):
        if depth == self.currentState.depth + 1:
            curr_state = self.currentState
            while curr_state.nextChildToVisit < len(curr_state.children):
                child_state = curr_state.children[curr_state.nextChildToVisit]
                curr_state.nextChildToVisit += 1
                if child_state not in self.visited:
                    self.visited[child_state] = True
                    self.gm.makeMove(child_state.requiredMovable)
                    self.currentState = child_state
                    return True
        elif depth > self.currentState.depth + 1:
            curr_state = self.currentState
            while curr_state.nextChildToVisit < len(curr_state.children):
                child_state = curr_state.children[curr_state.nextChildToVisit]
                curr_state.nextChildToVisit += 1
                self.gm.makeMove(child_state.requiredMovable)
                self.currentState = child_state
                if self.visitNodeAtDepth(depth):
                    return True
                self.gm.reverseMove(child_state.requiredMovable)
                self.currentState = self.currentState.parent
        if self.currentState.parent:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            return self.visitNodeAtDepth(depth)
        if self.genChildrenAtDepth(depth):
            return self.visitNodeAtDepth(depth + 1)
        else:
            return False


    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if self.currentState.state == self.victoryCondition:
            return True
        return not self.visitNodeAtDepth(self.currentState.depth)
