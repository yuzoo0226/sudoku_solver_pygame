def is_valid(board, row, col, num):
    """チェック：numを (row, col) に配置して良いか"""
    # 行の中に重複がないか
    if num in board[row]:
        return False
    # 列の中に重複がないか
    if num in [board[i][col] for i in range(9)]:
        return False
    # 3x3ブロックの中に重複がないか
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True

def solve_sudoku(board):
    """バックトラッキングでナンプレを解く"""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:  # 空きマスを探す
                for num in range(1, 10):  # 1から9を試す
                    if is_valid(board, row, col, num):
                        board[row][col] = num  # 候補を置く
                        if solve_sudoku(board):  # 再帰
                            return True
                        board[row][col] = 0  # 元に戻す（バックトラック）
                return False
    return True

# ナンプレ問題（0は空きマス）
sudoku_problem = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# 解を求める
if solve_sudoku(sudoku_problem):
    for row in sudoku_problem:
        print(row)
else:
    print("解けない問題です")
