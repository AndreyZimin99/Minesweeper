import random


class Minesweeper:
    def __init__(self, rows: int, cols: int, mines: int):
        self._rows = rows
        self._cols = cols
        self._mines = mines
        self._board = [[' ' for _ in range(cols)] for _ in range(rows)]
        self._visible = [['■' for _ in range(cols)] for _ in range(rows)]
        self._mine_positions: set = set()
        self.game_over = False
        self._first_opened = False

        if self._mines >= self._rows * self._cols:
            raise ValueError('Мин должно быть меньше чем ячеек!')

    def place_mines(self):
        while len(self._mine_positions) < self._mines:
            r = random.randint(0, self._rows - 1)
            c = random.randint(0, self._cols - 1)
            if (r, c) not in self._mine_positions:
                self._mine_positions.add((r, c))
                self._board[r][c] = 'M'

    def count_adjacent_mines(self, r: int, c: int):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0:
                    continue
                if 0 <= r + i < self._rows and 0 <= c + j < self._cols:
                    if self._board[r + i][c + j] == 'M':
                        count += 1
        return count

    def reveal_cell(self, r: int, c: int):
        if self._visible[r][c] != '■':
            return

        adjacent_mines = self.count_adjacent_mines(r, c)
        self._visible[r][c] = str(adjacent_mines) if adjacent_mines > 0 else ' '

        if adjacent_mines == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if ((i != 0 or j != 0) and 0 <= r + i < self._rows and
                       0 <= c + j < self._cols):
                        self.reveal_cell(r + i, c + j)

    def open_cell(self, x: int, y: int):
        if (x, y) in self._mine_positions:
            print(f'В ячейке ({x}, {y}) мина! Вы проиграли!')
            self.game_over = True
            return

        if not self._first_opened:
            self._first_opened = True
            self.place_mines()

        self.reveal_cell(x, y)

    def show_board(self):
        print('Текущее состояние поля:')
        for row in self._visible:
            print(" ".join(row))
        print()


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

    game = Minesweeper(rows, cols, mines)

    while not game.game_over:
        command = input(
            'Введите одну из команд (open X Y / show / exit): '
            ).strip().lower()

        if command.startswith('open'):
            try:
                _, x, y = command.split()
                x, y = int(x), int(y)
                if 0 <= x < rows and 0 <= y < cols:
                    game.open_cell(x, y)
                else:
                    print('Координаты вне поля игры!')
            except ValueError:
                print('Некоректный формат данных. Числа должны быть целыми!')

        elif command == 'show':
            game.show_board()

        elif command == 'exit':
            print('Выход из игры.')
            break

        else:
            print('Неизвестнаяя команда. Используйте: "open X Y", '
                  '"show", или "exit".')


if __name__ == '__main__':
    main()
