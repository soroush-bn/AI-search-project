import copy

from Board import Board
from Cell import Cell


class Find:
    def __init__(self, board: Board):
        self.board = board
        self.source = self.__find_source()
        self.goal = self.__find_goal()
        self.explored = []

    def __find_source(self):
        for row in range(self.board.m):
            for col in range(self.board.n):
                if self.__get_opt(row, col).lower() == 's':
                    return [row, col]

    def __find_goal(self):
        for row in range(self.board.m):
            for col in range(self.board.n):
                if self.__get_opt(row, col).lower() == 'g':
                    return [row, col]

    def __get_opt(self, row: int, col: int) -> str:
        return self.board.cells[row][col][0].lower()

    def __get_number(self, row: int, col: int) -> int:
        return int(self.board.cells[row][col][1:])

    def __successor(self, cell: Cell) -> list:
        cells = []
        if cell.row > 0:
            if self.__get_opt(cell.row - 1, cell.col) != 'w':
                c = Cell(cell.row - 1, cell.col, copy.deepcopy(cell.table), 0, 0, cell.path.copy())
                c.path.append(c)
                c.path_value, c.goal_value = self.__cal_opt(cell.path_value, cell.goal_value, c.row, c.col)
                if not self.explored.__contains__(c.__hash__()):
                    cells.append(c)

        if cell.col > 0:
            if self.__get_opt(cell.row, cell.col - 1) != 'w':
                c = Cell(cell.row, cell.col - 1, copy.deepcopy(cell.table), 0, 0, cell.path.copy())
                c.path.append(c)
                c.path_value, c.goal_value = self.__cal_opt(cell.path_value, cell.goal_value, c.row, c.col)
                if not self.explored.__contains__(c.__hash__()):
                    cells.append(c)

        if cell.row < self.board.m - 1:
            if self.__get_opt(cell.row + 1, cell.col) != 'w':
                c = Cell(cell.row + 1, cell.col, copy.deepcopy(cell.table), 0, 0, cell.path.copy())
                c.path.append(c)
                c.path_value, c.goal_value = self.__cal_opt(cell.path_value, cell.goal_value, c.row, c.col)
                if not self.explored.__contains__(c.__hash__()):
                    cells.append(c)

        if cell.col < self.board.n - 1:
            if self.__get_opt(cell.row, cell.col + 1) != 'w':
                c = Cell(cell.row, cell.col + 1, copy.deepcopy(cell.table), 0, 0, cell.path.copy())
                c.path.append(c)
                c.path_value, c.goal_value = self.__cal_opt(cell.path_value, cell.goal_value, c.row, c.col)
                if not self.explored.__contains__(c.__hash__()):
                    cells.append(c)

        return cells

    def __cal_opt(self, path_sum, goal_value, row, col):
        opt = self.__get_opt(row, col)

        if opt == '+':
            path_sum += self.__get_number(row, col)
        elif opt == '-':
            path_sum -= self.__get_number(row, col)
        elif opt == '*':
            path_sum *= self.__get_number(row, col)
        elif opt == '^':
            path_sum **= self.__get_number(row, col)
        elif opt == 'a':
            goal_value += self.__get_number(row, col)
        elif opt == 'b':
            goal_value -= self.__get_number(row, col)

        return path_sum, goal_value

    def __check_goal(self, cell: Cell) -> bool:
        if cell.path_value > cell.goal_value:
            self.__print_solution(cell)
            return True
        return False

    def bfs_search(self):
        queue = []

        queue.append(
            Cell(self.source[0], self.source[1], [[False for x in range(self.board.n)] for y in range(self.board.m)],
                 self.__get_number(self.source[0], self.source[1]),
                 self.__get_number(self.goal[0], self.goal[1]), []))

        queue[0].path.append(queue[0])

        while len(queue) > 0:
            cell = queue.pop(0)
            self.explored.append(cell.__hash__())
            neighbors = self.__successor(cell)

            for c in neighbors:
                if c.row == self.goal[0] and c.col == self.goal[1]:
                    if self.__check_goal(cell):
                        return
                else:
                    if not cell.table[c.row][c.col]:
                        queue.append(c)

        print('no solution!!!')

    def __print_solution(self, cell: Cell):
        print(len(cell.path))

        cell.path.pop(0)

        for p in cell.path:
            print(str(p.row + 1) + ' ' + str(p.col + 1))

        print(str(self.goal[0] + 1) + ' ' + str(self.goal[1] + 1))
