from pwn import *
conn = remote('beta.hackac.live', 5002)

try:

    def is_valid(board, row, col, num):
        # Check row and column constraints
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False

        # Check subgrid constraints
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True

    def solve_sudoku(board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    for num in range(1, 10):
                        if is_valid(board, i, j, num):
                            board[i][j] = num
                            if solve_sudoku(board):
                                return True
                            board[i][j] = 0
                    return False
        return True

    def print_board(board):
        ans = ''
        for row in board:
            ans += ' '.join(map(str, row)) + '\n'
        return ans

    def process_input(input_string):
        lines = input_string.split('\n')
        puzzle_lines = []
        puzzle_started = False
        for line in lines:
            if line.strip() == '':
                break
            puzzle_lines.append([int(num) for num in line.split()])
        return puzzle_lines


    sample_input = conn.recvline()
    sample = sample_input.decode()


    if __name__ == "__main__":
        for i in range(100):
            string = ''
            while not sample.startswith('Puzzle #'):
                sample_input = conn.recvline()
                sample = sample_input.decode()
            for i in range(9):
                sample_input = conn.recvline()    
                #print(count)
                #print(sample_input)
                sample = sample_input.decode()
                #print(sample_input)
                string += sample
            print(string)
            puzzle = process_input(string)
            if len(puzzle) == 9 and all(len(row) == 9 for row in puzzle):
                if solve_sudoku(puzzle):
                    ans = print_board(puzzle)
                    # print(ans)
                    ans = ans.encode('utf-8')
                    conn.sendline(ans)
                else:
                    print('NO SOLUTION')
            else:
                print('Invalid Sudoku puzzle format or dimensions.')
        while not flag.startswith('ACSI'):
            flag = conn.recvline()
            flag = flag.decode()
finally:
    print('test')
