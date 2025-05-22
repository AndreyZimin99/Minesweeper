import random

from enum import Enum


class Command(Enum):
    OPEN = 'open'
    SHOW = 'show'
    EXIT = 'exit'


class Cell:
    def __init__(self):
        self.is_mine = False
        self.adjacent_mines = 0
        self.is_visible = False

    def reveal(self):
        self.is_visible = True


class GameField:
    def __init__(self, rows: int, cols: int, mines: int):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self.game_over = False
        self.first_opened = False

        if self.mines >= self.rows * self.cols:
            raise ValueError('Мин должно быть меньше чем ячеек!')

    def place_mines(self):
        mine_positions = set()
        while len(mine_positions) < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if (r, c) not in mine_positions:
                mine_positions.add((r, c))
                self.board[r][c].is_mine = True

    def calculate_adjacent_mines(self, r: int, c: int):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0:
                    continue
                if 0 <= r + i < self.rows and 0 <= c + j < self.cols:
                    if self.board[r + i][c + j].is_mine:
                        count += 1
        return count

    def reveal_cell(self, r: int, c: int):
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return

        cell = self.board[r][c]

        if cell.is_visible:
            return

        cell.reveal()
        cell.adjacent_mines = self.calculate_adjacent_mines(r, c)

        if cell.adjacent_mines == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (i != 0 or j != 0):
                        self.reveal_cell(r + i, c + j)

    def open_cell(self, x: int, y: int):
        if self.board[x][y].is_mine:
            print(f'В ячейке ({x}, {y}) мина! Вы проиграли!')
            self.game_over = True
            return

        if not self.first_opened:
            self._first_opened = True
            self.place_mines()

        self.reveal_cell(x, y)

    def show_board(self):
        print('Текущее состояние поля:')
        for row in self.board:
            row_display = []
            for cell in row:
                if cell.is_visible:
                    row_display.append(str(cell.adjacent_mines)
                                       if cell.adjacent_mines > 0 else ' ')
                else:
                    row_display.append('■')
            print(' '.join(row_display))
        print()


class ConsoleInterface:
    def __init__(self, game_field: GameField):
        self.game_field = game_field

    def start(self):
        while not self.game_field.game_over:
            command = input(
                'Введите одну из команд (open X Y / show / exit): '
            ).strip().lower()

            if command.startswith(Command.OPEN.value):
                try:
                    _, x, y = command.split()
                    x, y = int(x), int(y)
                    if (0 <= x < self.game_field.rows
                       and 0 <= y < self.game_field.cols):
                        self.game_field.open_cell(x, y)
                    else:
                        print('Координаты вне поля игры!')
                except ValueError:
                    print('Некоректный формат данных.'
                          'Числа должны быть целыми!')

            elif command == Command.SHOW.value:
                self.game_field.show_board()

            elif command == Command.EXIT.value:
                print('Выход из игры.')
                break

            else:
                print('Неизвестная команда. Используйте: "open X Y",'
                      '"show", или "exit".')


def main():
    print('Старт игры "Сапер"')
    while True:
        try:
            rows = int(input('Введите количество рядов: '))
            cols = int(input('Введите количество столбцов: '))
            cells = rows * cols
            mines = int(input('Введите количество мин: '))
            if mines >= cells:
                print('Мин должно быть меньше чем ячеек!')
                continue
        except ValueError:
            print('Некоректный формат данных. Числа должны быть целыми!')
        else:
            break

    game_field = GameField(rows, cols, mines)
    console_interface = ConsoleInterface(game_field)
    console_interface.start()


if __name__ == '__main__':
    main()
