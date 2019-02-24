import unittest, inspect
from multiprocessing.pool import ThreadPool
from multiprocessing.context import TimeoutError
from student_code_game_masters import *
from student_code_uninformed_solvers import *


class KBTest(unittest.TestCase):

    def setUp(self):
        self.pool = ThreadPool(processes=1)
        self.lastEndStep = 0

    def playXSteps(self, solver, plays):
        """
        Call the solver's solveOneStep for x times, and record the result game state

        Args:
             solver: solver of the game
             plays: list of lists; inner list consists of the number of steps (x) followed by the expected outcome
        """
        res = []
        for play in plays:
            x = play[0]
            while self.lastEndStep < x:
                solver.solveOneStep()
                self.lastEndStep += 1
            res.append(solver.gm.getGameState())
        return res

    def solve(self, solver):
        """
        Call the solver's solve function, which should solve the game.

        Args:
             solver: solver of the game
        """
        solver.solve()

    def runPlayXSteps(self, solver, plays, timeout=5):
        """
        Wrapper function; calls playXSteps(..) with a timeout

        Args:
             solver: solver of the game
             plays: list of lists; inner list consists of the number of steps (x) followed by the expected outcome
             timeout: time out in seconds. Default 5 seconds
        """
        try:
            results = self.pool.apply_async(self.playXSteps, [solver, plays]).get(timeout)
            for index, play in enumerate(plays):
                expected = play[1]
                self.assertEqual(results[index], expected)
        except TimeoutError:
            raise Exception("Timed out: %s" % inspect.stack()[1][3])

    def runSolve(self, solver, timeout=5):
        """
        Wrapper function; calls solve(..) with a timeout

        Args:
             solver: solver of the game
             timeout: time out in seconds. Default 5 seconds
        """
        try:
            self.pool.apply_async(self.solve, [solver,]).get(timeout)
            self.assertTrue(solver.gm.isWon())
        except TimeoutError:
            raise Exception("Timed out: %s" % inspect.stack()[1][3])

    ### Step 1. Hanoi, DFS
    ###    step 1A. testing file1
    ###    step 1B. testing file2
    ###    step 1C. testing file3
    ###    step 1D. testing file4
    ### Step 2. 8-puzzle, DFS
    ###    step 2A. testing file1
    ###    step 2B. testing file2
    ### Step 3. Hanoi, BFS
    ###    step 3A. testing file1
    ###    step 3B. testing file2
    ###    step 3C. testing file3
    ###    step 3D. testing file4
    ### Step 4. 8-puzzle, BFS
    ###    step 4A. testing file1
    ###    step 4B. testing file2
    ###
    ### Step 1. Hanoi, DFS
    ###    step 1A. testing file1

    def test01_3A_GM_Hanoi(self):
        th = TowerOfHanoiGame()
        th.read('hanoi_3_all_disks_on_peg_one.txt')

        movables = th.getMovables()
        self.assertEqual(th.getGameState(), ((1,2,3),(),()))
        required = [
            'fact: (movable disk1 peg1 peg2)',
            'fact: (movable disk1 peg1 peg3)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertTrue(th.isWon())

        # (1,2,3),(),()   ->  (2,3), (1,), ()
        th.makeMove(movables[0])
        self.assertEqual(th.getGameState(), ((2,3),(1,),()))
        required = [
            'fact: (movable disk1 peg2 peg1)',
            'fact: (movable disk1 peg2 peg3)',
            'fact: (movable disk2 peg1 peg3)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertTrue(th.isWon())

        th.reverseMove(movables[0])
        self.assertEqual(th.getGameState(), ((1,2,3),(),()))
        required = [
            'fact: (movable disk1 peg1 peg2)',
            'fact: (movable disk1 peg1 peg3)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertTrue(th.isWon())

        th.makeMove(movables[0])
        self.assertEqual(th.getGameState(), ((2,3),(1,),()))
        required = [
            'fact: (movable disk1 peg2 peg1)',
            'fact: (movable disk1 peg2 peg3)',
            'fact: (movable disk2 peg1 peg3)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertTrue(th.isWon())
        #print(((1,2,3),(),()), ((2,3),(1,),()), movables[0], th.isWon())

        # (2,3), (1,), () ->  (2,3), (), (1)
        movables = th.getMovables()
        th.makeMove(movables[1])
        self.assertEqual(th.getGameState(), ((2, 3), (), (1,)))
        required = [
            'fact: (movable disk1 peg3 peg1)',
            'fact: (movable disk1 peg3 peg2)',
            'fact: (movable disk2 peg1 peg2)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertTrue(th.isWon())
        #print(((2,3),(1,),()), ((2, 3), (), (1,)), movables[1], th.isWon())

        th.reverseMove(movables[1])
        self.assertEqual(th.getGameState(), ((2,3),(1,),()))
        required = [
            'fact: (movable disk1 peg2 peg1)',
            'fact: (movable disk1 peg2 peg3)',
            'fact: (movable disk2 peg1 peg3)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertTrue(th.isWon())
        #print(((1,2,3),(),()), ((2,3),(1,),()), movables[0], th.isWon())

        th.makeMove(movables[1])
        self.assertEqual(th.getGameState(), ((2, 3), (), (1,)))
        required = [
            'fact: (movable disk1 peg3 peg1)',
            'fact: (movable disk1 peg3 peg2)',
            'fact: (movable disk2 peg1 peg2)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertTrue(th.isWon())
        #print(((2,3),(1,),()), ((2, 3), (), (1,)), movables[1], th.isWon())

        # (2,3) () (1)     ->      (3) (2) (1)
        movables = th.getMovables()
        th.makeMove(movables[2])
        self.assertEqual(th.getGameState(), ((3,),(2,),(1,)))
        required = [
            'fact: (movable disk1 peg3 peg1)',
            'fact: (movable disk1 peg3 peg2)',
            'fact: (movable disk2 peg2 peg1)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        #print(((2, 3), (), (1,)), ((3,),(2,),(1,)), movables[2], th.isWon())
        self.assertTrue(th.isWon())

        th.reverseMove(movables[2])
        self.assertEqual(th.getGameState(), ((2, 3), (), (1,)))
        required = [
            'fact: (movable disk1 peg3 peg1)',
            'fact: (movable disk1 peg3 peg2)',
            'fact: (movable disk2 peg1 peg2)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertTrue(th.isWon())
        #print(((2,3),(1,),()), ((2, 3), (), (1,)), movables[1], th.isWon())

        movables = th.getMovables()
        th.makeMove(movables[2])
        self.assertEqual(th.getGameState(), ((3,),(2,),(1,)))
        required = [
            'fact: (movable disk1 peg3 peg1)',
            'fact: (movable disk1 peg3 peg2)',
            'fact: (movable disk2 peg2 peg1)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        #print(((2, 3), (), (1,)), ((3,),(2,),(1,)), movables[2], th.isWon())
        self.assertTrue(th.isWon())

        # (3) (2) (1) -> (1,3) (2) ()
        movables = th.getMovables()
        th.makeMove(movables[0])
        self.assertEqual(th.getGameState(), ((1,3,), (2,), ()))
        required = [
            'fact: (movable disk1 peg1 peg2)',
            'fact: (movable disk1 peg1 peg3)',
            'fact: (movable disk2 peg2 peg3)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertTrue(th.isWon())

        th.reverseMove(movables[0])
        self.assertEqual(th.getGameState(), ((3,),(2,),(1,)))
        required = [
            'fact: (movable disk1 peg3 peg1)',
            'fact: (movable disk1 peg3 peg2)',
            'fact: (movable disk2 peg2 peg1)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        #print(((2, 3), (), (1,)), ((3,),(2,),(1,)), movables[2], th.isWon())
        self.assertTrue(th.isWon())

        th.makeMove(movables[0])
        self.assertEqual(th.getGameState(), ((1,3,), (2,), ()))
        required = [
            'fact: (movable disk1 peg1 peg2)',
            'fact: (movable disk1 peg1 peg3)',
            'fact: (movable disk2 peg2 peg3)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertTrue(th.isWon())

        # (1,3) (2) () ->  (3) (1,2) ()
        movables = th.getMovables()
        th.makeMove(movables[0])
        self.assertEqual(th.getGameState(), ((3,), (1,2,), ()))
        required = [
            'fact: (movable disk1 peg2 peg1)',
            'fact: (movable disk1 peg2 peg3)',
            'fact: (movable disk3 peg1 peg3)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertTrue(th.isWon())

        th.reverseMove(movables[0])
        self.assertEqual(th.getGameState(), ((1,3,), (2,), ()))
        required = [
            'fact: (movable disk1 peg1 peg2)',
            'fact: (movable disk1 peg1 peg3)',
            'fact: (movable disk2 peg2 peg3)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertTrue(th.isWon())

        th.makeMove(movables[0])
        self.assertEqual(th.getGameState(), ((3,), (1,2,), ()))
        required = [
            'fact: (movable disk1 peg2 peg1)',
            'fact: (movable disk1 peg2 peg3)',
            'fact: (movable disk3 peg1 peg3)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertTrue(th.isWon())

        # (3) (1,2) () -> () (1,2) (3)
        movables = th.getMovables()
        th.makeMove(movables[2])
        self.assertEqual(th.getGameState(), ((), (1,2,), (3,)))
        required = [
            'fact: (movable disk1 peg2 peg1)',
            'fact: (movable disk1 peg2 peg3)',
            'fact: (movable disk3 peg3 peg1)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertTrue(th.isWon())

        th.reverseMove(movables[2])
        self.assertEqual(th.getGameState(), ((3,), (1,2,), ()))
        required = [
            'fact: (movable disk1 peg2 peg1)',
            'fact: (movable disk1 peg2 peg3)',
            'fact: (movable disk3 peg1 peg3)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertTrue(th.isWon())

        th.makeMove(movables[2])
        self.assertEqual(th.getGameState(), ((), (1,2,), (3,)))
        required = [
            'fact: (movable disk1 peg2 peg1)',
            'fact: (movable disk1 peg2 peg3)',
            'fact: (movable disk3 peg3 peg1)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertTrue(th.isWon())


    def test02_DFS_Hanoi(self):
        th = TowerOfHanoiGame()
        th.read('hanoi_3_all_disks_on_peg_one.txt')
        required = [
            'fact: (movable disk1 peg1 peg2)',
            'fact: (movable disk1 peg1 peg3)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertTrue(th.isWon())

        solver = SolverDFS(th,((),(),(1,2,3)))

        # self.playXSteps(solver, [
        self.runPlayXSteps(solver, [
            # [step, expected game state]
            [3, ((3,), (2,), (1,))],
            [13, ((1,), (), (2, 3))],
            [22, ((), (), (1, 2, 3))],
        ])


    def test03_DFS_Hanoi(self):
        th = TowerOfHanoiGame()
        th.read('hanoi_3_all_disks_on_peg_one.txt')
        required = [
            'fact: (movable disk1 peg1 peg2)',
            'fact: (movable disk1 peg1 peg3)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertTrue(th.isWon())

        required = [
            'fact: (movable disk1 peg3 peg1)',
            'fact: (movable disk1 peg3 peg2)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        solver = SolverDFS(th, ((),(),(1,2,3)))
        self.runSolve(solver)


    ###    step 1B. testing file2
    # start to work on 5 disks with all disks on peg1
    def test01A_GM_Hanoi(self):
        th = TowerOfHanoiGame()
        th.read('hanoi_5_all_disks_on_peg_one.txt')

        self.assertEqual(th.getGameState(), ((1,2,3,4,5),(),()))
        required = [
            'fact: (movable disk1 peg1 peg2)',
            'fact: (movable disk1 peg1 peg3)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertTrue(th.isWon())

        # (1,2,3,4,5) () () -> (2,3,4,5) (1) ()
        movables = th.getMovables()
        th.makeMove(movables[0])
        self.assertEqual(th.getGameState(), ((2,3,4,5),(1,),()))
        required = [
            'fact: (movable disk1 peg2 peg1)',
            'fact: (movable disk1 peg2 peg3)',
            'fact: (movable disk2 peg1 peg3)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertTrue(th.isWon())

        th.reverseMove(movables[0])
        self.assertEqual(th.getGameState(), ((1,2,3,4,5),(),()))
        required = [
            'fact: (movable disk1 peg1 peg2)',
            'fact: (movable disk1 peg1 peg3)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertTrue(th.isWon())


    def test03A_DFS_Hanoi(self):
        th = TowerOfHanoiGame()
        th.read('hanoi_5_all_disks_on_peg_one.txt')
        required = [
            'fact: (movable disk1 peg1 peg2)',
            'fact: (movable disk1 peg1 peg3)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertTrue(th.isWon())

        required = [
            'fact: (movable disk1 peg3 peg1)',
            'fact: (movable disk1 peg3 peg2)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')

        solver = SolverDFS(th, ((),(),(1,2,3,4,5)))
        self.runSolve(solver, 10)

    ###    step 1C. testing file3
    # work on 5 disks with smallest disk on peg3 and 2nd smallest on peg2
    def test01B_GM_Hanoi(self):
        th = TowerOfHanoiGame()
        th.read('hanoi_5_smallest_on_three_second_smallest_on_two.txt')

        self.assertEqual(th.getGameState(), ((3, 4, 5), (2,), (1,)))
        required = [
            'fact: (movable disk1 peg3 peg1)',
            'fact: (movable disk1 peg3 peg2)',
            'fact: (movable disk2 peg2 peg1)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertTrue(th.isWon())

        movables = th.getMovables()
        th.makeMove(movables[1])
        self.assertEqual(th.getGameState(), ((3, 4, 5), (1, 2), ()))
        required = [
            'fact: (movable disk1 peg2 peg1)',
            'fact: (movable disk1 peg2 peg3)',
            'fact: (movable disk3 peg1 peg3)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertTrue(th.isWon())

        th.reverseMove(movables[1])
        self.assertEqual(th.getGameState(), ((3, 4, 5), (2,), (1,)))
        required = [
            'fact: (movable disk1 peg3 peg1)',
            'fact: (movable disk1 peg3 peg2)',
            'fact: (movable disk2 peg2 peg1)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertTrue(th.isWon())

    def test01C_GM_Hanoi(self):
        th = TowerOfHanoiGame()
        th.read('hanoi_5_smallest_on_three_second_smallest_on_two.txt')

        movables = th.getMovables()
        self.assertEqual(th.getGameState(), ((3, 4, 5), (2,), (1,)))
        th.makeMove(movables[2])
        self.assertEqual(th.getGameState(), ((2, 3, 4, 5), (), (1,)))
        th.makeMove(movables[1])
        self.assertEqual(th.getGameState(), ((2, 3, 4, 5), (1,), ()))
        th.reverseMove(movables[1])
        self.assertEqual(th.getGameState(), ((2,3, 4, 5), (), (1,)))
        th.reverseMove(movables[2])
        self.assertEqual(th.getGameState(), ((3, 4, 5), (2,), (1,)))


    def test05A_DFS_Hanoi(self):
        th = TowerOfHanoiGame()
        th.read('hanoi_5_smallest_on_three_second_smallest_on_two.txt')

        required = [
            'fact: (movable disk1 peg3 peg1)',
            'fact: (movable disk1 peg3 peg2)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')

        solver = SolverDFS(th, ((),(),(1,2,3,4,5)))
        self.runSolve(solver, 10)

    ###    step 1D. testing file4
    # work on 5 disks with two smallest disks on peg3
    def test01D_GM_Hanoi(self):
        th = TowerOfHanoiGame()
        th.read('hanoi_5_two_smallest_on_peg_three.txt')

        movables = th.getMovables()
        self.assertEqual(th.getGameState(), ((3, 4, 5), (), (1,2)))
        th.makeMove(movables[1])
        self.assertEqual(th.getGameState(), ((3, 4, 5), (1,), (2,)))

        movables = th.getMovables()
        th.makeMove(movables[2])
        self.assertEqual(th.getGameState(), ((2, 3, 4, 5), (1,), ()))
        th.makeMove(movables[0])
        self.assertEqual(th.getGameState(), ((1,2,3, 4, 5), (), ()))
        th.reverseMove(movables[0])
        self.assertEqual(th.getGameState(), ((2, 3, 4, 5), (1,), ()))
        th.reverseMove(movables[2])
        self.assertEqual(th.getGameState(), ((3, 4, 5), (1,), (2,)))
        th.makeMove(movables[1])
        self.assertEqual(th.getGameState(), ((3, 4, 5), (), (1,2)))

    def test05B_DFS_Hanoi(self):
        th = TowerOfHanoiGame()
        th.read('hanoi_5_two_smallest_on_peg_three.txt')

        required = [
            'fact: (movable disk1 peg3 peg1)',
            'fact: (movable disk1 peg3 peg2)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')

        solver = SolverDFS(th, ((),(),(1,2,3,4,5)))
        self.runSolve(solver, 20)

    ### Step 2. 8-puzzle DFS
    ###    step 2A. testing file1

    def test06_GM_8Puzzle(self):
        p8 = Puzzle8Game()
        p8.read('puzzle8_top_right_empty.txt')

        self.assertEqual(p8.getGameState(), ((5,4,-1),(6,1,8),(7,3,2)))
        required = [
            'fact: (movable tile4 pos2 pos1 pos3 pos1)',
            'fact: (movable tile8 pos3 pos2 pos3 pos1)',
        ]
        p8.setWinningCondition(required, 'puzzle8_all_forbidden.txt')
        self.assertTrue(p8.isWon())

        movables = p8.getMovables()
        p8.makeMove(movables[0])
        self.assertEqual(p8.getGameState(), ((5,-1,4), (6,1,8), (7,3,2)))
        required = [
            'fact: (movable tile5 pos1 pos1 pos2 pos1)',
            'fact: (movable tile1 pos2 pos2 pos2 pos1)',
            'fact: (movable tile4 pos3 pos1 pos2 pos1)',
        ]
        p8.setWinningCondition(required, 'puzzle8_all_forbidden.txt')
        self.assertTrue(p8.isWon())

        p8.reverseMove(movables[0])
        self.assertEqual(p8.getGameState(), ((5,4,-1),(6,1,8),(7,3,2)))
        required = [
            'fact: (movable tile4 pos2 pos1 pos3 pos1)',
            'fact: (movable tile8 pos3 pos2 pos3 pos1)',
        ]
        p8.setWinningCondition(required, 'puzzle8_all_forbidden.txt')
        self.assertTrue(p8.isWon())

        p8.makeMove(movables[1])
        self.assertEqual(p8.getGameState(), ((5,4,8), (6,1,-1), (7,3,2)))
        required = [
            'fact: (movable tile8 pos3 pos1 pos3 pos2)',
            'fact: (movable tile1 pos2 pos2 pos3 pos2)',
            'fact: (movable tile2 pos3 pos3 pos3 pos2)',
        ]
        p8.setWinningCondition(required, 'puzzle8_all_forbidden.txt')
        self.assertTrue(p8.isWon())

        p8.reverseMove(movables[1])
        self.assertEqual(p8.getGameState(), ((5,4,-1),(6,1,8),(7,3,2)))
        required = [
            'fact: (movable tile4 pos2 pos1 pos3 pos1)',
            'fact: (movable tile8 pos3 pos2 pos3 pos1)',
        ]
        p8.setWinningCondition(required, 'puzzle8_all_forbidden.txt')
        self.assertTrue(p8.isWon())


    def test07_DFS_8Puzzle(self):
        p8 = Puzzle8Game()
        p8.read('puzzle8_top_right_empty.txt')
        required = [
            'fact: (movable tile6 pos3 pos2 pos3 pos3)',
            'fact: (movable tile8 pos2 pos3 pos3 pos3)',
        ]
        p8.setWinningCondition(required, 'puzzle8_all_forbidden.txt')
        self.assertFalse(p8.isWon())

        solver = SolverDFS(p8,((1,2,3),(4,5,6),(7,8,-1)))

        self.runPlayXSteps(solver, [
            # [step, expected game state]
            [9, ((5, 4, 3), (6, 1, -1), (7, 2, 8))],
            [17, ((5, -1, 4), (2, 1, 3), (6, 7, 8))],
            [34, ((5, 4, -1), (3, 2, 1), (6, 7, 8))],
        ])

    '''
    def test07A_DFS_8Puzzle(self):
        p8 = Puzzle8Game()
        p8.read('puzzle8_top_right_empty.txt')
        required = [
            'fact: (movable tile6 pos3 pos2 pos3 pos3)',
            'fact: (movable tile8 pos2 pos3 pos3 pos3)',
        ]
        p8.setWinningCondition(required, 'puzzle8_all_forbidden.txt')

        solver = SolverDFS(p8,((1,2,3),(4,5,6),(7,8,-1)))
        self.runSolve(solver, 40000)
    #     # self.runSolve(solver, 5)
    '''



    ###    step 2B. testing file2
    ### testing center empty flatfile

    def test06B_GM_8Puzzle(self):
        p8 = Puzzle8Game()
        p8.read('puzzle8_center_empty.txt')

        self.assertEqual(p8.getGameState(), ((1,2,3),(8,-1,4),(7,6,5)))
        required = [
            'fact: (movable tile2 pos2 pos1 pos2 pos2)',
            'fact: (movable tile4 pos3 pos2 pos2 pos2)',
            'fact: (movable tile6 pos2 pos3 pos2 pos2)',
            'fact: (movable tile8 pos1 pos2 pos2 pos2)',
        ]
        p8.setWinningCondition(required, 'puzzle8_all_forbidden.txt')
        self.assertTrue(p8.isWon())

        movables = p8.getMovables()
        p8.makeMove(movables[0])
        self.assertEqual(p8.getGameState(), ((1,-1,3),(8,2,4),(7,6,5)))
        required = [
            'fact: (movable tile1 pos1 pos1 pos2 pos1)',
            'fact: (movable tile3 pos3 pos1 pos2 pos1)',
            'fact: (movable tile2 pos2 pos2 pos2 pos1)',
        ]
        p8.setWinningCondition(required, 'puzzle8_all_forbidden.txt')
        self.assertTrue(p8.isWon())

        p8.reverseMove(movables[0])
        self.assertEqual(p8.getGameState(), ((1,2,3),(8,-1,4),(7,6,5)))
        required = [
            'fact: (movable tile2 pos2 pos1 pos2 pos2)',
            'fact: (movable tile4 pos3 pos2 pos2 pos2)',
            'fact: (movable tile6 pos2 pos3 pos2 pos2)',
            'fact: (movable tile8 pos1 pos2 pos2 pos2)',
        ]
        p8.setWinningCondition(required, 'puzzle8_all_forbidden.txt')
        self.assertTrue(p8.isWon())

        p8.makeMove(movables[1])
        self.assertEqual(p8.getGameState(), ((1,2,3), (8,4,-1), (7,6,5)))
        required = [
            'fact: (movable tile4 pos2 pos2 pos3 pos2)',
            'fact: (movable tile3 pos3 pos1 pos3 pos2)',
            'fact: (movable tile5 pos3 pos3 pos3 pos2)',
        ]
        p8.setWinningCondition(required, 'puzzle8_all_forbidden.txt')
        self.assertTrue(p8.isWon())

        p8.reverseMove(movables[1])
        self.assertEqual(p8.getGameState(), ((1,2,3),(8,-1,4),(7,6,5)))
        required = [
            'fact: (movable tile2 pos2 pos1 pos2 pos2)',
            'fact: (movable tile4 pos3 pos2 pos2 pos2)',
            'fact: (movable tile6 pos2 pos3 pos2 pos2)',
            'fact: (movable tile8 pos1 pos2 pos2 pos2)',
        ]
        p8.setWinningCondition(required, 'puzzle8_all_forbidden.txt')
        self.assertTrue(p8.isWon())

        p8.makeMove(movables[2])
        self.assertEqual(p8.getGameState(), ((1,2,3),(8,6,4),(7,-1,5)))
        required = [
            'fact: (movable tile7 pos1 pos3 pos2 pos3)',
            'fact: (movable tile5 pos3 pos3 pos2 pos3)',
            'fact: (movable tile6 pos2 pos2 pos2 pos3)',
        ]
        p8.setWinningCondition(required, 'puzzle8_all_forbidden.txt')
        self.assertTrue(p8.isWon())

        p8.reverseMove(movables[2])
        self.assertEqual(p8.getGameState(), ((1,2,3),(8,-1,4),(7,6,5)))
        required = [
            'fact: (movable tile2 pos2 pos1 pos2 pos2)',
            'fact: (movable tile4 pos3 pos2 pos2 pos2)',
            'fact: (movable tile6 pos2 pos3 pos2 pos2)',
            'fact: (movable tile8 pos1 pos2 pos2 pos2)',
        ]
        p8.setWinningCondition(required, 'puzzle8_all_forbidden.txt')
        self.assertTrue(p8.isWon())

        p8.makeMove(movables[3])
        self.assertEqual(p8.getGameState(), ((1,2,3), (-1,8,4), (7,6,5)))
        required = [
            'fact: (movable tile1 pos1 pos1 pos1 pos2)',
            'fact: (movable tile7 pos1 pos3 pos1 pos2)',
            'fact: (movable tile8 pos2 pos2 pos1 pos2)',
        ]
        p8.setWinningCondition(required, 'puzzle8_all_forbidden.txt')
        self.assertTrue(p8.isWon())

        p8.reverseMove(movables[3])
        self.assertEqual(p8.getGameState(), ((1,2,3),(8,-1,4),(7,6,5)))
        required = [
            'fact: (movable tile2 pos2 pos1 pos2 pos2)',
            'fact: (movable tile4 pos3 pos2 pos2 pos2)',
            'fact: (movable tile6 pos2 pos3 pos2 pos2)',
            'fact: (movable tile8 pos1 pos2 pos2 pos2)',
        ]
        p8.setWinningCondition(required, 'puzzle8_all_forbidden.txt')
        self.assertTrue(p8.isWon())

    '''
    def test07B_DFS_8Puzzle(self):
        p8 = Puzzle8Game()
        p8.read('puzzle8_center_empty.txt')
        required = [
            'fact: (movable tile6 pos3 pos2 pos3 pos3)',
            'fact: (movable tile8 pos2 pos3 pos3 pos3)',
        ]
        p8.setWinningCondition(required, 'puzzle8_all_forbidden.txt')

        solver = SolverDFS(p8,((1,2,3),(4,5,6),(7,8,-1)))
        self.runSolve(solver, 500000)
        # self.runSolve(solver, 5)
    '''

    ### Step 3 Hanoi BFS
    ###    step 3A. testing file1

    def test04_BFS_Hanoi(self):
        th = TowerOfHanoiGame()
        th.read('hanoi_3_all_disks_on_peg_one.txt')
        required = [
            'fact: (movable disk1 peg3 peg1)',
            'fact: (movable disk1 peg3 peg2)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertFalse(th.isWon())

        solver = SolverBFS(th,((),(),(1,2,3)))

        self.runPlayXSteps(solver, [
        #self.playXSteps(solver, [
            # [step, expected game state]
             [10, ((), (1, 2), (3,))],
            [11, ((1,), (3,), (2,))],
            [20, ((), (2, 3), (1,))],
        ])

    def test05_BFS_Hanoi(self):
        th = TowerOfHanoiGame()
        th.read('hanoi_3_all_disks_on_peg_one.txt')
        required = [
            'fact: (movable disk1 peg3 peg1)',
            'fact: (movable disk1 peg3 peg2)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertFalse(th.isWon())

        solver = SolverBFS(th, ((),(),(1,2,3)))
        #self.solve(solver)
        self.runSolve(solver, 20)


    #
    ###    step 3B. testing file2

    def test05B_BFS_Hanoi(self):
        th = TowerOfHanoiGame()
        th.read('hanoi_5_all_disks_on_peg_one.txt')

        self.assertEqual(th.getGameState(), ((1,2,3,4,5),(),()))
        required = [
            'fact: (movable disk1 peg3 peg1)',
            'fact: (movable disk1 peg3 peg2)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertFalse(th.isWon())

        solver = SolverBFS(th, ((),(),(1,2,3,4,5)))
        self.runSolve(solver,300)       # passed 94s on window


    ###    step 3C. testing file3

    def test05C_BFS_Hanoi(self):
        th = TowerOfHanoiGame()
        th.read('hanoi_5_smallest_on_three_second_smallest_on_two.txt')

        self.assertEqual(th.getGameState(), ((3, 4, 5), (2,), (1,)))
        required = [
            'fact: (movable disk1 peg3 peg1)',
            'fact: (movable disk1 peg3 peg2)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertFalse(th.isWon())

        solver = SolverBFS(th, ((),(),(1,2,3,4,5)))
        self.runSolve(solver,300)       # passed 54s on window


    ###    step 3D. testing file4

    def test05D_BFS_Hanoi(self):
        th = TowerOfHanoiGame()
        th.read('hanoi_5_two_smallest_on_peg_three.txt')

        self.assertEqual(th.getGameState(), ((3, 4, 5), (), (1,2)))
        required = [
            'fact: (movable disk1 peg3 peg1)',
            'fact: (movable disk1 peg3 peg2)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertFalse(th.isWon())

        solver = SolverBFS(th, ((),(),(1,2,3,4,5)))
        self.runSolve(solver,400)       # passed 125s on window


    ### Step 4. 8-puzzle BFS
    ###    step 4A. testing file1

    def test08A_BFS_8Puzzle(self):
        p8 = Puzzle8Game()
        p8.read('puzzle8_top_right_empty.txt')
        required = [
            'fact: (movable tile6 pos3 pos2 pos3 pos3)',
            'fact: (movable tile8 pos2 pos3 pos3 pos3)',
        ]
        p8.setWinningCondition(required, 'puzzle8_all_forbidden.txt')
        self.assertFalse(p8.isWon())

        solver = SolverBFS(p8,((1,2,3),(4,5,6),(7,8,-1)))

        self.runPlayXSteps(solver, [
            # [step, expected game state]
            [5, ((5, 4, 8), (6, -1, 1), (7, 3, 2))],
            [13, ((5, 4, 8), (-1, 6, 1), (7, 3, 2))],
            [21, ((6, 5, 4), (1, -1, 8), (7, 3, 2))],
        ])


    '''
    def test08B_BFS_8Puzzle(self):
        p8 = Puzzle8Game()
        p8.read('puzzle8_top_right_empty.txt')
        required = [
            'fact: (movable tile6 pos3 pos2 pos3 pos3)',
            'fact: (movable tile8 pos2 pos3 pos3 pos3)',
        ]
        p8.setWinningCondition(required, 'puzzle8_all_forbidden.txt')
        self.assertFalse(p8.isWon())

        solver = SolverBFS(p8,((1,2,3),(4,5,6),(7,8,-1)))

        self.runSolve(solver,40000)
    

    ###    step 4B. testing file2
    
    def test08D_BFS_8Puzzle(self):
        p8 = Puzzle8Game()
        p8.read('puzzle8_center_empty.txt')
        required = [
            'fact: (movable tile6 pos3 pos2 pos3 pos3)',
            'fact: (movable tile8 pos2 pos3 pos3 pos3)',
        ]
        p8.setWinningCondition(required, 'puzzle8_all_forbidden.txt')
        self.assertFalse(p8.isWon())

        solver = SolverBFS(p8,((1,2,3),(4,5,6),(7,8,-1)))

        self.runSolve(solver,400000)
    '''

if __name__ == '__main__':
    unittest.main()
