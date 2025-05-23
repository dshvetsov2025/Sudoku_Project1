from sudoku_variables import *
from sudoku_generator import generate_sudoku
import sudoku

# Class representing a single cell in the sudoku board
class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.sketched_value = 0
        self.selected = False
        self.editable = (value == 0)  # Only cells with initial value 0 are editable
        self.width = space_per_box
        self.height = space_per_box
        self.rect = pygame.Rect(col * space_per_box, row * space_per_box,
                               space_per_box, space_per_box)

    def set_cell_value(self, value):
        if self.editable:
            self.value = value

    def set_sketched_value(self, value):
        if self.editable:
            self.sketched_value = value

    def draw(self):
        # Draw cell border if selected
        if self.selected:
            pygame.draw.rect(self.screen, 'red', self.rect, 3)

        # Display the cell value if it's not 0
        if self.value != 0:
            # Different color for original values vs. user input values
            color = dark_brown if not self.editable else 'blue'
            value_text = cell_font.render(str(self.value), True, color)
            text_rect = value_text.get_rect(center=(self.col * space_per_box + space_per_box // 2,
                                                  self.row * space_per_box + space_per_box // 2))
            self.screen.blit(value_text, text_rect)
        # Display sketched value if cell value is 0
        elif self.sketched_value != 0:
            sketch_text = sketch_font.render(str(self.sketched_value), True, 'gray')
            # Position sketched text in top left corner of cell
            self.screen.blit(sketch_text, (self.col * space_per_box + 5, self.row * space_per_box + 5))

# Class representing the entire sudoku board
class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.rows = 9
        self.cols = 9
        self.selected_row = None
        self.selected_col = None
        self.cells = []

        # Map difficulty to number of cells to remove
        if difficulty == 'Easy':
            removed_cells = 30
        elif difficulty == 'Medium':
            removed_cells = 40
        else:  # Hard
            removed_cells = 50

        # Generate board based on difficulty
        self.original_board = generate_sudoku(9, removed_cells)
        self.solution_board = generate_sudoku(9, 0)  # Get a fully solved board

        # Create Cell objects
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                cell = Cell(self.original_board[i][j], i, j, screen)
                row.append(cell)
            self.cells.append(row)

    def draw(self):
        # Draw all cells
        for row in self.cells:
            for cell in row:
                cell.draw()

        # Draw grid lines
        sudoku.draw_lines()

        # Draw buttons
        self.draw_buttons()

    def draw_buttons(self):
        # Create three buttons below the board: Reset, Restart, Exit
        button_width = 120
        button_height = 40
        button_y = 615  # Position buttons at bottom of screen
        button_margin = 20  # Space between buttons

        reset_button = pygame.Rect(80, button_y, button_width, button_height)
        restart_button = pygame.Rect(240, button_y, button_width, button_height)
        exit_button = pygame.Rect(400, button_y, button_width, button_height)

        buttons = [reset_button, restart_button, exit_button]
        button_texts = ["Reset", "Restart", "Exit"]

        for i, button in enumerate(buttons):
            pygame.draw.rect(screen, dark_brown, button, border_radius=10)
            button_text = subheader.render(button_texts[i], True, white)
            text_rect = button_text.get_rect(center=button.center)
            screen.blit(button_text, text_rect)

    def select(self, row, col):
        # Deselect previously selected cell
        if self.selected_row is not None and self.selected_col is not None:
            self.cells[self.selected_row][self.selected_col].selected = False

        # Select new cell
        self.selected_row = row
        self.selected_col = col
        self.cells[row][col].selected = True

    def click(self, pos):
        x, y = pos

        # Check if click is within board
        if x < self.width and y < self.height:
            # Calculate which cell was clicked
            col = x // space_per_box
            row = y // space_per_box

            # If the click is in bounds, return cell coordinates
            if 0 <= row < 9 and 0 <= col < 9:
                return (row, col)

        # Check button clicks
        button_y = 615
        button_width = 120
        button_height = 40

        # Reset button
        if 80 <= x <= 80 + button_width and button_y <= y <= button_y + button_height:
            result = 'Reset'
            return result
        # Restart button
        elif 240 <= x <= 240 + button_width and button_y <= y <= button_y + button_height:
            result = 'Restart'
            return result
        # Exit button
        elif 400 <= x <= 400 + button_width and button_y <= y <= button_y + button_height:
            result = 'Exit'
            return result

        return None

    def clear(self):
        # Clear the sketched and actual value of the selected cell if it's editable
        if self.selected_row is not None and self.selected_col is not None:
            cell = self.cells[self.selected_row][self.selected_col]
            if cell.editable:
                cell.value = 0
                cell.sketched_value = 0

    def sketch(self, value):
        # Sketch a value in the selected cell
        if self.selected_row is not None and self.selected_col is not None:
            self.cells[self.selected_row][self.selected_col].set_sketched_value(value)

    def place_number(self, value):
        # Place a number in the selected cell
        if self.selected_row is not None and self.selected_col is not None:
            self.cells[self.selected_row][self.selected_col].set_cell_value(value)

    def reset_to_original(self):
        # Reset board to original state
        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.cells[i][j]
                if cell.editable:
                    cell.value = 0
                    cell.sketched_value = 0

    def is_full(self):
        # Check if the board is full (no empty cells)
        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

    def update_board(self):
        # Update the underlying 2D board with current cell values
        board = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(self.cells[i][j].value)
            board.append(row)
        return board

    def find_empty(self):
        # Find an empty cell and return its coordinates
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cells[i][j].value == 0:
                    return (i, j)
        return None

    def check_board(self):
        # Check if the board is solved correctly
        current_board = self.update_board()

        # Check rows
        for row in current_board:
            if sorted(row) != [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                return False

        # Check columns
        for j in range(9):
            col = [current_board[i][j] for i in range(9)]
            if sorted(col) != [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                return False

        # Check 3x3 boxes
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box = []
                for i in range(3):
                    for j in range(3):
                        box.append(current_board[box_row + i][box_col + j])
                if sorted(box) != [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                    return False

        return True

