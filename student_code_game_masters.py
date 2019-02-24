from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        pegs = []
        for i in range(1, 4):
            fact = parse_input('fact: (on ?disk peg' + str(i) + ')')
            xs = self.kb.kb_ask(fact)
            disks = []
            if xs:
                for bindings in xs.list_of_bindings:
                    disks.append(int(str(bindings[0].bound_to(Variable('?disk')))[4:]))
                disks.sort()
            pegs.append(tuple(disks))
        return tuple(pegs)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        terms = movable_statement.terms
        disk_to_move = str(terms[0])
        o_peg = str(terms[1])
        n_peg = str(terms[2])
        new_fact = parse_input('fact: (on ' + disk_to_move + ' ' + n_peg + ')')
        old_fact = parse_input('fact: (on ' + disk_to_move + ' ' + o_peg + ')')

        old_bot_bindings = self.kb.kb_ask(parse_input('fact: (onTopOf ' + disk_to_move + ' ?X)'))
        old_bot = str(old_bot_bindings.list_of_bindings[0][0].bound_to(Variable('?X')))
        if old_bot == 'base':
            fact1 = parse_input('fact: (isEmpty ' + o_peg + ')')    # if old peg will be empty
        else:
            fact1 = parse_input('fact: (onTopOf nothing ' + old_bot + ')')
        above_old_bot = parse_input('fact: (onTopOf ' + disk_to_move + ' ' + old_bot + ')')

        # if self.kb.kb_ask(parse_input('fact: (onTopOf ' + disk_to_move + ' base)')):
        #     self.kb.kb_retract(parse_input('fact: (onTopOf ' + disk_to_move + ' base)'))
        #     self.kb.kb_assert(parse_input('fact: (isEmpty ' + o_peg + ')'))
        # else:  # set new top for old peg
        #     o_peg_disks = self.kb.kb_ask(parse_input('fact: (onTopOf ' + disk_to_move + ' ?disk)'))
        #     for bindings in o_peg_disks.list_of_bindings:
        #         n_top = str(bindings[0].bound_to(Variable('?disk')))
        #         self.kb.kb_retract(parse_input('fact: (onTopOf ' + disk_to_move + ' ' + n_top + ')'))
        #         self.kb.kb_assert(parse_input('fact: (onTopOf nothing ' + n_top + ')'))

        # if target peg is empty
        n_peg_empty = parse_input('fact: (isEmpty ' + n_peg + ')')
        new_peg_empty = self.kb.kb_ask(n_peg_empty)
        if new_peg_empty:
            above_new_bot = parse_input('fact: (onTopOf ' + disk_to_move + ' base')
        else:  # if target peg has disks
            # find top disk on target peg
            all_tops = self.kb.kb_ask(parse_input('fact: (onTopOf nothing ?disk)'))
            for bindings in all_tops.list_of_bindings:
                top = str(bindings[0].bound_to(Variable('?disk')))
                if self.kb.kb_ask(parse_input('fact: (on ' + top + ' ' + n_peg + ')')):
                    fact2 = parse_input('fact: (onTopOf nothing ' + top + ')')
                    above_new_bot = parse_input('fact: (onTopOf ' + disk_to_move + ' ' + top + ')')
                    break

        self.kb.kb_retract(parse_input('fact: (onTopOf nothing ' + disk_to_move + ')'))
        self.kb.kb_retract(above_old_bot)
        self.kb.kb_retract(old_fact)
        if new_peg_empty:
            self.kb.kb_retract(n_peg_empty)
        else:
            self.kb.kb_retract(fact2)
        self.kb.kb_assert(new_fact)
        self.kb.kb_assert(above_new_bot)
        self.kb.kb_assert(fact1)
        self.kb.kb_assert(parse_input('fact: (onTopOf nothing ' + disk_to_move + ')'))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        posns = []
        posn = ['pos1', 'pos2', 'pos3']
        for y in posn:
            tiles = []
            for x in posn:
                fact = parse_input('fact: (pos ?tile ' + x + ' ' + y + ')')
                xs = self.kb.kb_ask(fact)
                if xs:
                    for bindings in xs.list_of_bindings:
                        space = str(bindings[0].bound_to(Variable('?tile')))
                        if space == 'empty':
                            tiles.append(-1)
                        else:
                            tiles.append(int(space[4:]))
            posns.append(tuple(tiles))
        return tuple(posns)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        terms = movable_statement.terms
        tile_to_move = str(terms[0])
        t_posx = str(terms[1])
        t_posy = str(terms[2])
        e_posx = str(terms[3])
        e_posy = str(terms[4])
        t_old_posn = parse_input('fact: (pos ' + tile_to_move + ' ' + t_posx + ' ' + t_posy + ')')
        t_new_posn = parse_input('fact: (pos ' + tile_to_move + ' ' + e_posx + ' ' + e_posy + ')')
        e_new_posn = parse_input('fact: (pos empty ' + t_posx + ' ' + t_posy + ')')
        e_old_posn = parse_input('fact: (pos empty ' + e_posx + ' ' + e_posy + ')')
        self.kb.kb_retract(e_old_posn)
        self.kb.kb_retract(t_old_posn)
        self.kb.kb_assert(t_new_posn)
        self.kb.kb_assert(e_new_posn)

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
