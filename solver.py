import grids

backtracks = 0


def solve(grid):
    global backtracks
    empty_square_pos = find_empty_square(grid)
    if not empty_square_pos:
        return True
    else:
        row, col = empty_square_pos
    for i in range(1, 10):
        if is_valid(grid, i, (row, col)):
            grid[row][col] = i
            if solve(grid):
                return True
            grid[row][col] = 0
    backtracks = backtracks + 1
    return False


def is_valid(grid, num, pos):
    # Check row
    for i in range(len(grid[0])):
        if grid[pos[0]][i] == num and pos[1] != i:
            return False
    # Check column
    for i in range(len(grid)):
        if grid[i][pos[1]] == num and pos[0] != i:
            return False
    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if grid[i][j] == num and (i, j) != pos:
                return False
    return True


def print_grid(grid):
    for i in range(len(grid)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")
        for j in range(len(grid[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(grid[i][j])
            else:
                print(str(grid[i][j]) + " ", end="")


def find_empty_square(grid):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 0:
                return row, col
    return None


print_grid(grids.board)
solved = solve(grids.board)
print(">>>>>> SOLUTION")
if (solved == False):
    print(">>>>>> CANNOT BE SOLVED!!!")
print_grid(grids.board)
print("Backtracks = " + str(backtracks))
