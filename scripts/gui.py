import sys
import pygame

# Screen dimensions and colors
WIDTH, HEIGHT = 540, 600  # Increased height for footer
CELL_SIZE = WIDTH // 9
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


class SudokuGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Sudoku")
        self.clock = pygame.time.Clock()
        self.selected_cell = (0, 0)  # Start by selecting the top-left cell
        self.user_inputs = set()  # Tracks cells manually entered by the user
        self.status = "Status: Ready"  # Initial status
        self.sudoku_problem = [
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

    def draw_grid(self):
        """Draw the Sudoku grid"""
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(
                self.screen, BLACK if x % (3 * CELL_SIZE) == 0 else GRAY, 
                (x, 0), (x, HEIGHT - 60), 2 if x % (3 * CELL_SIZE) == 0 else 1
            )
        for y in range(0, HEIGHT - 60, CELL_SIZE):
            pygame.draw.line(
                self.screen, BLACK if y % (3 * CELL_SIZE) == 0 else GRAY, 
                (0, y), (WIDTH, y), 2 if y % (3 * CELL_SIZE) == 0 else 1
            )

    def draw_numbers(self):
        """Draw the numbers on the Sudoku board"""
        font = pygame.font.Font(None, 50)
        for row in range(9):
            for col in range(9):
                if self.sudoku_problem[row][col] != 0:
                    color = RED if (row, col) in self.user_inputs else BLACK
                    text = font.render(str(self.sudoku_problem[row][col]), True, color)
                    self.screen.blit(text, (col * CELL_SIZE + 20, row * CELL_SIZE + 10))

    def draw_footer(self):
        """Draw the footer with instructions and status"""
        font = pygame.font.Font(None, 30)
        instructions = [
            "Select a cell and input a number (backspace to delete)",
            "C: Clear All   R: Reset Calculations   S: Solve Puzzle",
            self.status
        ]
        footer_y = HEIGHT - 60
        for i, line in enumerate(instructions):
            text = font.render(line, True, BLACK)
            self.screen.blit(text, (10, footer_y + i * 20))

    def move_selection(self, direction):
        """Move the selected cell with arrow keys"""
        row, col = self.selected_cell
        if direction == "UP" and row > 0:
            row -= 1
        elif direction == "DOWN" and row < 8:
            row += 1
        elif direction == "LEFT" and col > 0:
            col -= 1
        elif direction == "RIGHT" and col < 8:
            col += 1
        self.selected_cell = (row, col)

    def solve_sudoku(self, board):
        """Solve Sudoku using backtracking"""
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(board, row, col, num):
                            board[row][col] = num
                            if self.solve_sudoku(board):
                                return True
                            board[row][col] = 0
                    return False
        return True

    def is_valid(self, board, row, col, num):
        """Check if placing num in (row, col) is valid"""
        if num in board[row]:
            return False
        if num in [board[i][col] for i in range(9)]:
            return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False
        return True

    def reset_calculated(self):
        """Reset cells calculated by the solver"""
        for row in range(9):
            for col in range(9):
                if (row, col) not in self.user_inputs:
                    self.sudoku_problem[row][col] = 0

    def reset_board(self):
        """Clear the entire board"""
        self.sudoku_problem = [[0 for _ in range(9)] for _ in range(9)]
        self.user_inputs.clear()

    def solve_current_board(self):
        """Solve the current board"""
        self.status = "Status: Solving..."  # Update status
        pygame.display.flip()  # Immediately update status
        temp_board = [row[:] for row in self.sudoku_problem]
        if self.solve_sudoku(temp_board):
            for row in range(9):
                for col in range(9):
                    if (row, col) not in self.user_inputs:
                        self.sudoku_problem[row][col] = temp_board[row][col]
            self.status = "Status: Solved!"
        else:
            self.status = "Status: No solution found"

    def run(self):
        """Main loop"""
        running = True
        while running:
            self.screen.fill(WHITE)
            self.draw_grid()
            self.draw_numbers()
            self.draw_footer()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if y < HEIGHT - 60:  # Ignore clicks in the footer area
                        self.selected_cell = (y // CELL_SIZE, x // CELL_SIZE)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.move_selection("UP")
                    elif event.key == pygame.K_DOWN:
                        self.move_selection("DOWN")
                    elif event.key == pygame.K_LEFT:
                        self.move_selection("LEFT")
                    elif event.key == pygame.K_RIGHT:
                        self.move_selection("RIGHT")
                    elif self.selected_cell:
                        row, col = self.selected_cell
                        if event.unicode.isdigit() and event.unicode != '0':
                            self.sudoku_problem[row][col] = int(event.unicode)
                            self.user_inputs.add((row, col))
                        elif event.key == pygame.K_BACKSPACE or event.unicode == '0':
                            self.sudoku_problem[row][col] = 0
                            self.user_inputs.discard((row, col))
                    if event.key == pygame.K_c:
                        self.reset_board()
                        self.status = "Status: Cleared"
                    if event.key == pygame.K_s:
                        self.solve_current_board()
                    if event.key == pygame.K_r:
                        self.reset_calculated()
                        self.status = "Status: Reset calculated values"

            if self.selected_cell:
                row, col = self.selected_cell
                pygame.draw.rect(self.screen, BLUE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    SudokuGUI().run()
