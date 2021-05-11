def print_grid(grid):
    """a function for testing purposes to print the board in the terminal"""
    for i in range(9):
        for j in range(9):
            if j == 2 or j == 5:
                print(grid[i][j], end=' | ')
            else:
                print(grid[i][j], end='  ')
        print()
        if i == 2 or i == 5:
            print('-' * 27)


def find_zero(grid):
    """a function that finds the first cell missing a number"""
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return (i, j, True)
    return (0, 0, False)


def is_safe(grid, n, row, col):
    """a function checking if given number can be put in a given cell.
       Looks through its row and col and 3x3 square to check if the
       number is there already"""
    # check row
    for i in range(9):
        if grid[i][col] == n:
            return False

    # check col
    for i in range(9):
        if grid[row][i] == n:
            return False

    # check 3x3 square
    for i in range(3):
        for j in range(3):
            if grid[i + row - row % 3][j + col - col % 3] == n:
                return False

    return True


def solve(grid):
    """the main function that solves the sudoku board with backtracking"""
    row, col, found_zero = find_zero(grid)


    # we are successful if the board is complete
    if not found_zero:
        return True

    for n in range(1, 10):
        if is_safe(grid, n, row, col):
            grid[row][col] = n

            if solve(grid):
                return True

            grid[row][col] = 0

    # backtrack if no number can be put in these coordinates
    return False


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
    solve(board)
    print_grid(board)
