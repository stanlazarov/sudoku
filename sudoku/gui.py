import sys
import pygame
import time
import copy
from sudoku.solver import solve
from pygame.constants import K_ESCAPE

class Sudoku(object):
    # board size variables
    node_height = 63
    node_width = 63
    node_margin = 3
    size = width, height = (node_width + node_margin) * 9 + node_margin, (node_height + node_margin) * 10 + node_margin
    line_width = 8

    # colors
    black = 0, 0, 0
    white = 255, 255, 255
    wrong_color = 240, 114, 105
    selected_rowcol_color = 193, 212, 230
    selected_color = 44, 129, 209

    # selected cell
    selected = 0

    # works but make it toggleable with a button or something like that
    check_for_mistakes = True

    def __init__(self, starting_board):
        pygame.init()

        # initialize the board and make solved board
        self.board = starting_board[:]
        self.solved = copy.deepcopy(self.board)
        solve(self.solved)

        # initialize fonts
        self.timer_font = pygame.font.Font(None, 35)
        self.numbers_font = pygame.font.Font(None, 40)

    def format_time(self, seconds):
        """A function formatting time from seconds to HH:MM:SS"""
        minutes = 0
        hours = 0
        if seconds >= 60:
            minutes += seconds // 60
            seconds %= 60
        if minutes >= 60:
            hours += minutes // 60
            minutes %= 60
        return "{:02d}:{:02d}:{:02d}".format(int(hours), int(minutes), int(seconds)) if hours > 0 else "{:02d}:{:02d}".format(int(minutes), int(seconds))

    def get_index_from_position(self, pos):
        """a function calculating the indices of the cell clicked from the pixel(x, y) position of the mouse click event"""
        x, y = pos
        return ((y - self.node_margin) // (self.node_height + self.node_margin), (x - self.node_margin) // (self.node_width + self.node_margin))

    def update_display(self, screen, start_time):
        """a function to visualize everything in the game window"""
        screen.fill(self.black)

        for row in range(9):
            for col in range(9):
                curr_color = self.white

                # make selected cell and its row and col different color
                if self.selected:
                    if self.selected == (row, col):
                        curr_color = self.selected_color
                    elif row == self.selected[0] or col == self.selected[1]:
                        curr_color = self.selected_rowcol_color

                # if checking for mistakes is on, make cell red if incorrect
                if self.check_for_mistakes and self.board[row][col] != self.solved[row][col] and self.board[row][col] > 0:
                    curr_color = self.wrong_color

                # draw square cells
                pygame.draw.rect(screen, curr_color, ((self.node_margin + self.node_width) * col + self.node_margin, (self.node_margin + self.node_height) * row + self.node_margin, self.node_width, self.node_height))

                # draw numbers
                if self.board[row][col] > 0:
                    curr_number = self.numbers_font.render(str(self.board[row][col]), 50, self.black)
                    screen.blit(curr_number, ((self.node_margin + self.node_width) * col + self.node_margin + 25, (self.node_margin + self.node_height) * row + self.node_margin + 20))

        # draw bolder lines for making 3x3 squares more visible
        pygame.draw.line(screen, self.black, ((self.node_width + self.node_margin) * 3, 0), ((self.node_width + self.node_margin) * 3, (self.node_height + self.node_margin) * 9), self.line_width)
        pygame.draw.line(screen, self.black, ((self.node_width + self.node_margin) * 6, 0), ((self.node_width + self.node_margin) * 6, (self.node_height + self.node_margin) * 9), self.line_width)
        pygame.draw.line(screen, self.black, (0, (self.node_height + self.node_margin) * 3), ((self.node_width + self.node_margin) * 9, (self.node_height + self.node_margin) * 3), self.line_width)
        pygame.draw.line(screen, self.black, (0, (self.node_height + self.node_margin) * 6), ((self.node_width + self.node_margin) * 9, (self.node_height + self.node_margin) * 6), self.line_width)

        # set timer
        timer = self.timer_font.render("Time: {}".format(self.format_time(time.time() - start_time)), 50, self.white)
        screen.blit(timer, (((self.node_width + self.node_margin) * 6 + self.node_margin * 10 - 5), (self.node_height + self.node_margin) * 9 + self.node_margin * 10 - 5))

        pygame.display.update()

    def handle_events(self):
        """a function to handle all the events"""
        for event in pygame.event.get():
            # quit game if close button is clicked
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # call other function that handles keyboard input
            if event.type == pygame.KEYDOWN:
                self.handle_number_event(pygame.key.get_pressed())
            # make clicked cell selected
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                xe, ye = self.get_index_from_position(pos)
                # check if mouse is clicked on a cell on the board
                if 0 <= xe <= 8 and 0 <= ye <= 8:
                    self.selected = xe, ye
                # this was for testing the get_pos() function
                #print("{} -> {}".format(str(pos), str(self.selected)))

    def handle_number_event(self, key):
        """a function to handle keyboard click events"""
        # quit game if escape is pressed
        if key[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        # check if there isnt any selected cell to input a number in
        if not self.selected: return
        # input the number in the board
        x, y = self.selected
        if key[pygame.K_1]:
            self.board[x][y] = 1
        if key[pygame.K_2]:
            self.board[x][y] = 2
        if key[pygame.K_3]:
            self.board[x][y] = 3
        if key[pygame.K_4]:
            self.board[x][y] = 4
        if key[pygame.K_5]:
            self.board[x][y] = 5
        if key[pygame.K_6]:
            self.board[x][y] = 6
        if key[pygame.K_7]:
            self.board[x][y] = 7
        if key[pygame.K_8]:
            self.board[x][y] = 8
        if key[pygame.K_9]:
            self.board[x][y] = 9

    def game_loop(self):
        """main game loop function"""
        # create the window
        screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Sudoku")
        screen.fill(self.black)

        # starting time
        start_time = time.time()

        # game loop
        while True:
            self.handle_events()

            self.update_display(screen, start_time)



if __name__ == '__main__':
    board = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
         [5, 2, 0, 0, 0, 0, 0, 0, 0],
         [0, 8, 7, 0, 0, 0, 0, 3, 1],
         [0, 0, 3, 0, 1, 0, 0, 8, 0],
         [9, 0, 0, 8, 6, 3, 0, 0, 5],
         [0, 5, 0, 0, 9, 0, 6, 0, 0],
         [1, 3, 0, 0, 0, 0, 2, 5, 0],
         [0, 0, 0, 0, 0, 0, 0, 7, 4],
         [0, 0, 5, 2, 0, 6, 3, 0, 0]]

    sudoku = Sudoku(board)
    sudoku.game_loop()