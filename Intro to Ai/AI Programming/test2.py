import sys
import csv
import time

#Common Utility functions
def is_valid_assignment(row, col, num):
    """
    Checks if the given assignment is valid.
    """
    # Check row and column
    for i in range(9):
        if (grid[row][i] == num and col != i) or (grid[i][col] == num and row != i):
            return False

    # Check 3x3 box
    box_row = row // 3 * 3
    box_col = col // 3 * 3
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if grid[r][c] == num and (row != r or col != c):
                return False

    return True

def print_sudoku_grid(grid):
    horizontal_line = "------+-------+------"
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print(horizontal_line)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            if grid[i][j] == "X":
                print("X", end=" ")
            else:
                print(grid[i][j], end=" ")
        print()
  
# Bruteforce

numNodes=0

def is_valid_move(grid, row, col, num):
    # Check row, column, and box for duplicates
    for i in range(9):
        if grid[row][i] == num or grid[i][col] == num:
            return False
        if grid[3 * (row // 3) + i // 3][3 * (col // 3) + i % 3] == num:
            return False
    return True

def solve_sudoku_bruteforce(grid):
    
    def dfs(grid, empty_cells):
        global numNodesExplored
        if not empty_cells:
            return True

        row, col = empty_cells.pop()
        for num in range(1, 10):
            
            numNodesExplored+=1
            if is_valid_move(grid, row, col, str(num)):
                grid[row][col] = str(num)
                if dfs(grid, empty_cells):
                    return True
                grid[row][col] = 'X'
            
        empty_cells.append((row, col))
        return False

    empty_cells = []
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 'X':
                empty_cells.append((i, j))

    dfs(grid, empty_cells)
    return grid



#Backtracking      
def get_unassigned_cell_BT():
    """
    Returns the first unassigned cell (cell with 'X') in the grid.
    """
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 'X':
                return row, col
    return None

    """
    Checks if a given assignment is valid based on Sudoku constraints.
    """
    # Check row
    for c in range(9):
        if grid[row][c] == num:
            return False

    # Check column
    for r in range(9):
        if grid[r][col] == num:
            return False

    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for r in range(3):
        for c in range(3):
            if grid[r + start_row][c + start_col] == num:
                return False

    return True

def solve_sudoku_BT():
    """
    Solves the Sudoku puzzle using CSP and backtracking.
    """
    global numNodesExplored
    
    
    
    unassigned_cell = get_unassigned_cell_BT()
    if unassigned_cell is None:
        return True  # All cells are assigned, puzzle solved!

    row, col = unassigned_cell
    
    for num in range(1, 10):
        numNodesExplored+=1
        if is_valid_assignment(row, col, str(num)):
            grid[row][col] = str(num)
            if solve_sudoku_BT():
                return True
            grid[row][col] = 'X'  # Undo the assignment

    return False        


#CSPForwardChecking

def get_unassigned_cell_FC():
    """
    Returns the first unassigned cell in the grid.
    """
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 'X':
                return r, c
    return None, None


def get_valid_values(row, col):
    """
    Returns the valid values that can be assigned to the given cell.
    """
    valid_values = set('123456789')

    # Remove values in the same row and column
    for i in range(9):
        valid_values.discard(grid[row][i])
        valid_values.discard(grid[i][col])

    # Remove values in the same 3x3 box
    box_row = row // 3 * 3
    box_col = col // 3 * 3
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            valid_values.discard(grid[r][c])

    return valid_values


def forward_checking(row, col, num):
    """
    Performs forward checking to reduce the domain of neighboring cells
    based on the assigned value.
    """
    grid[row][col] = num

    for r in range(9):
        if grid[r][col] == 'X':
            grid[r][col] = grid[r][col].replace(num, '')

    for c in range(9):
        if grid[row][c] == 'X':
            grid[row][c] = grid[row][c].replace(num, '')

    box_row = row // 3 * 3
    box_col = col // 3 * 3
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if grid[r][c] == 'X':
                grid[r][c] = grid[r][c].replace(num, '')


def undo_forward_check(row, col, num):
    """
    Undoes the effect of forward checking for the given assignment.
    """
    for i in range(9):
        if grid[row][i] == num:
            grid[row][i] = 'X'

        if grid[i][col] == num:
            grid[i][col] = 'X'

    box_row = row // 3 * 3
    box_col = col // 3 * 3
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if grid[r][c] == num:
                grid[r][c] = 'X'



def solve_sudoku_forward():
    """
    Solves the Sudoku puzzle using MRV heuristic and Forward Checking.
    """
    global numNodesExplored
    
    
    row, col = get_unassigned_cell_FC()
    
    if row is None and col is None:
        return True  # All cells are assigned, puzzle solved!
    
    valid_values = get_valid_values(row, col)
    for num in valid_values:
        numNodesExplored+=1
        if is_valid_assignment(row, col, num):
            grid[row][col] = num
            forward_checking(row, col, num)

            if solve_sudoku_forward():
                return True

            undo_forward_check(row, col, num)
            grid[row][col] = 'X'  # Undo the assignment

    return False

#Check if already given puzzle dont contain duplicates
def is_valid_input_sudoku(grid):
    """
    Checks if a given grid is a valid Sudoku grid without duplicates.
    """
    # Check rows for duplicates
    for row in grid:
        seen = set()
        for num in row:
            if num != 'X':
                if num in seen:
                    return False
                seen.add(num)

    # Check columns for duplicates
    for col in range(9):
        seen = set()
        for row in range(9):
            num = grid[row][col]
            if num != 'X':
                if num in seen:
                    return False
                seen.add(num)

    # Check sub-grids for duplicates
    for row_start in range(0, 9, 3):
        for col_start in range(0, 9, 3):
            seen = set()
            for row_offset in range(3):
                for col_offset in range(3):
                    num = grid[row_start + row_offset][col_start + col_offset]
                    if num != 'X':
                        if num in seen:
                            return False
                        seen.add(num)

    return True

#Sum of all elements in solved sudoku will be 405
def is_valid_and_solved_sudoku(grid):
    total_sum = 0
    for row in grid:
        for val in row:
            if val != "X":
                total_sum += int(val)
    if total_sum==405:
        return True
    else:
        return False
    
#Driver code
if __name__ == "__main__":


    if len(sys.argv) != 3:
        print("\nERROR: Not enough or too many input arguments\n")
        exit()
    else:
        FileName=sys.argv[1]
        Algo=sys.argv[2]
        
        grid=[]
        
        with open(FileName, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                grid.append(row)
        print("")
        print("Sumanth, Donthula, A20519856 solution:")
        print("")
        print("Input file: "+FileName)
        
               
        
        if Algo == '1': 
            numNodesExplored=0
            print("Algorithm: BruteForce")
            print("")
            print("InputPuzzle:")
            print(" ")
            print_sudoku_grid(grid)          
            if is_valid_input_sudoku(grid): 
                t1=time.time()
                solution = solve_sudoku_bruteforce(grid)
                t2=time.time()
                print(" ")
                print("Number of search tree nodes generated: "+str(numNodesExplored))
                print("Search time: "+str(t2-t1)+" Seconds")
                print("")
                print("Solved Puzzle:")
                print(" ")
                print_sudoku_grid(solution)
            else:
                print("")
                print_sudoku_grid(grid)
                print("Please check duplicates in Input file")

        elif Algo == '2':   
            numNodesExplored=0
            print("Algorithm: CSP Backtracking")
            print("")
            print("InputPuzzle:")
            print(" ")
            print_sudoku_grid(grid)
            
            if is_valid_input_sudoku(grid): 
                t1=time.time()
                solve_sudoku_BT()
                t2=time.time()
                print(" ")
                print("Number of search tree nodes generated: "+str(numNodesExplored))
                print("Search time: "+str(t2-t1)+" Seconds")
                print("")
                print("Solved Puzzle:")
                print(" ")
                print_sudoku_grid(grid)
            else:
                print("")
                print_sudoku_grid(grid)
                print("Please check duplicates in Input file")
        
        elif Algo == '3':
            numNodesExplored=0
            print("Algorithm: CSP Forward Checking and MRV")
            print("")
            print("InputPuzzle:")
            print(" ")
            print_sudoku_grid(grid)
            if is_valid_input_sudoku(grid): 
                t1=time.time()
                solve_sudoku_forward()
                t2=time.time()
                print(" ")
                print("Number of search tree nodes generated: "+str(numNodesExplored))
                print("Search time: "+str(t2-t1)+" Seconds")
                print("")
                print("Solved Puzzle:")
                print(" ")
                print_sudoku_grid(grid)
            else:
                print("")
                print_sudoku_grid(grid)
                print("Please check duplicates in Input file")
        elif Algo == '4':
            if is_valid_and_solved_sudoku(grid)==True:
                print("Algorithm: TEST")
                print("")
                print("InputPuzzle:")
                print(" ")
                print_sudoku_grid(grid)
                print(" ")
                print("Number of search tree nodes generated: 0")
                print("Search time: 0 Seconds")
                print("")
                print("This is a valid, solved, Sudoku puzzle.")

            else:
                print("Algorithm: TEST")
                print("")
                print("InputPuzzle:")
                print(" ")
                print_sudoku_grid(grid)
                print(" ")
                print("Number of search tree nodes generated: 0")
                print("Search time: 0 Seconds")
                print("")
                print("ERROR: This is NOT a solvedSudoku puzzle.")