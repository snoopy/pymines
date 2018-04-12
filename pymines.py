"""A simple minesweeping game"""

import os
from random import randint
import sys


class Tile:
    """Tile has a display value and can have a mine"""

    def __init__(self, value):
        """Tile constructor"""

        self.value = value
        self.has_mine = False


class Board:
    """Board has a collection of tiles and provides methods
    to interact with them
    """

    def __init__(self, width, height, mines, closed_tile, open_tile):
        """Board constructor"""

        self.width = width
        self.height = height
        self.mines = mines
        self.closed_tile = closed_tile
        self.open_tile = open_tile
        self.tiles = []
        self.uncovered_tiles = 0

    def initialize(self):
        """Create the board with initial values and randomly place mines"""

        for _ in range(self.height):
            sublist = [Tile(self.closed_tile) for _ in range(self.width)]
            self.tiles.append(sublist)

        i = 0
        while i < self.mines:
            m, n = randint(0, self.height - 1), randint(0, self.width - 1)
            if not self.tiles[m][n].has_mine:
                self.tiles[m][n].has_mine = True
                i += 1

    def display(self):
        """Print the board along with coordinate indicators"""

        os.system('cls' if os.name == 'nt' else 'clear')

        print("  {}".format(" ".join(str(i) for i in range(0, self.width))))
        print("  {}".format("-" * (self.width * 2)))

        i = 0
        for col in range(len(self.tiles)):
            sys.stdout.write(str(i) + "|")
            for row in range(len(self.tiles[col])):
                print(self.tiles[col][row].value, end=" ")
            print("|" + str(i))
            i += 1

        print("  {}".format("-" * (self.width * 2)))
        print("  {}".format(" ".join(str(i) for i in range(0, self.width))))

    def count_mines(self, m, n):
        """Count the mines adjacent to the given tile"""

        mines = 0
        for y in range(m - 1, m + 2):
            for x in range(n - 1, n + 2):
                if (y < 0 or y >= self.height or x < 0 or x >= self.width):
                    continue

                if self.tiles[y][x].has_mine:
                        mines += 1

        return mines

    def check_tile(self, m, n):
        """Check tiles recursively"""

        if self.tiles[m][n].value != self.closed_tile:
            return

        self.uncovered_tiles += 1

        mines = self.count_mines(m, n)
        if mines > 0:
            self.tiles[m][n].value = mines
            return

        self.tiles[m][n].value = self.open_tile

        for y in range(m - 1, m + 2):
            for x in range(n - 1, n + 2):
                if x == n and y == m:
                    continue

                if y < 0 or y >= self.height or x < 0 or x >= self.width:
                    continue

                self.check_tile(y, x)

    def is_uncovered(self, goal):
        """Check if all tiles except for mines have been uncovered"""

        return self.uncovered_tiles == goal

    def tile_has_mine(self, m, n):
        """Determine if a user-picked tile contains a mine or not"""

        return self.tiles[m][n].has_mine


class Game:
    """Game provides the main loop and passes user input to board"""

    def __init__(self):
        """Game constructor"""

        width = 10
        height = 10
        mines = 10
        closed_tile = "~"
        open_tile = " "
        self.board = Board(width, height, mines, closed_tile, open_tile)
        self.goal = width * height - mines
        self.board.initialize()

    def play(self):
        """Play the game until a win/lose condition is encountered"""

        while True:
            self.board.display()

            try:
                m, n = self.get_input()
            except ValueError:
                # exit when non numeric input
                break
            except Exception as ex:
                input(ex)
                continue

            if self.board.tile_has_mine(m, n):
                print("Game Over")
                break

            self.board.check_tile(m, n)

            if self.board.is_uncovered(self.goal):
                print("You Won")
                break

    def get_input(self):
        """make sure the user enters 2 valid numbers or quit"""

        while True:
            position = input("\nEnter m n: ").split()
            if len(position) != 2:
                raise Exception("Invalid number of arguments")

            m, n = map(int, position)
            try:
                m = int(m)
                n = int(n)
            except ValueError:
                sys.exit(0)

            if m < 0 or m >= self.board.height or n < 0 or n > self.board.width:
                raise Exception("Invalid range")

            return m, n


def main(argv):
    game = Game()
    game.play()


if __name__ == "__main__":
    main(sys.argv)
