import sys
import sudoku_gui
from sudoku_variables import *

texture = pygame.image.load('assets/lightblue.webp')

def main():
    pygame.init()
    header = pygame.font.Font('assets/MabryPro-Regular.ttf', 50) #header font and size being set
    subheader = pygame.font.Font('assets/MabryPro-Regular.ttf',28) #subheader font and size being set
    cell_font = pygame.font.Font('assets/MabryPro-Regular.ttf', 30) # Font for cell numbers
    sketch_font = pygame.font.Font('assets/MabryPro-Regular.ttf', 20) # Font for sketched numbers
    screen = pygame.display.set_mode((600,600))
    screen.fill(white)
    pygame.display.set_caption("Sudoku")
    current_screen = 'Main Menu'


    # Initialize game variables
    board = None
    game_won = False
    game_over = False

    while True:
        if current_screen == 'Main Menu':
            menu_screen()
        elif current_screen == 'Game Screen':
            screen.fill(white)
            board.draw()

            # Check if game is over
            if board.is_full():
                if board.check_board():
                    current_screen = 'Game Won'
                else:
                    current_screen = 'Game Over'
        elif current_screen == 'Game Won':
            game_win_screen()
        elif current_screen == 'Game Over':
            game_over_screen()

        for event in pygame.event.get():  # checks for new events
            if event.type == pygame.QUIT:  # quit window functionality
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if current_screen == 'Main Menu':
                    # Check which difficulty button was clicked
                    button1 = pygame.Rect(40, 400, 150, 60)
                    button2 = pygame.Rect(220, 400, 150, 60)
                    button3 = pygame.Rect(400, 400, 150, 60)
                    buttons = [button1, button2, button3]

                    for i, button in enumerate(buttons):
                        if button.collidepoint(x, y):
                            difficulty = difficulty_levels[i]
                            screen = pygame.display.set_mode((600, 670))
                            board = sudoku_gui.Board(600, 600, screen, difficulty)
                            current_screen = 'Game Screen'

                elif current_screen == 'Game Screen':
                    result = board.click((x, y))
                    if result == "Reset":
                        board.reset_to_original()
                    elif result == "Restart":
                        current_screen = 'Main Menu'
                    elif result == "Exit":
                        pygame.quit()
                        sys.exit()
                    elif result is not None and isinstance(result, tuple):
                        row, col = result
                        board.select(row, col)

                elif current_screen == 'Game Won':
                    exit_button = pygame.Rect(225, 350, 150, 60)
                    if exit_button.collidepoint(x, y):
                        pygame.quit()
                        sys.exit()

                elif current_screen == 'Game Over':
                    restart_button = pygame.Rect(225, 350, 150, 60)
                    if restart_button.collidepoint(x, y):
                        current_screen = 'Main Menu'

            if event.type == pygame.KEYDOWN and current_screen == 'Game Screen':
                if board.selected_row is not None and board.selected_col is not None:
                    if event.key == pygame.K_1:
                        board.sketch(1)
                    elif event.key == pygame.K_2:
                        board.sketch(2)
                    elif event.key == pygame.K_3:
                        board.sketch(3)
                    elif event.key == pygame.K_4:
                        board.sketch(4)
                    elif event.key == pygame.K_5:
                        board.sketch(5)
                    elif event.key == pygame.K_6:
                        board.sketch(6)
                    elif event.key == pygame.K_7:
                        board.sketch(7)
                    elif event.key == pygame.K_8:
                        board.sketch(8)
                    elif event.key == pygame.K_9:
                        board.sketch(9)
                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        board.clear()
                    elif event.key == pygame.K_RETURN:
                        # Get the sketched value and place it
                        cell = board.cells[board.selected_row][board.selected_col]
                        if cell.sketched_value != 0:
                            board.place_number(cell.sketched_value)
                            cell.sketched_value = 0
                    # Arrow key navigation
                    elif event.key == pygame.K_UP and board.selected_row > 0:
                        board.select(board.selected_row - 1, board.selected_col)
                    elif event.key == pygame.K_DOWN and board.selected_row < 8:
                        board.select(board.selected_row + 1, board.selected_col)
                    elif event.key == pygame.K_LEFT and board.selected_col > 0:
                        board.select(board.selected_row, board.selected_col - 1)
                    elif event.key == pygame.K_RIGHT and board.selected_col < 8:
                        board.select(board.selected_row, board.selected_col + 1)

        pygame.display.update()  # updates display w/loop

def draw_lines():
    for i in range(1, 3):  # The following 4 for loops create the grid structure in the GUI.
        pygame.draw.line(
            screen,
            'black',
            (i * space_per_line, 0),
            (i * space_per_line, 600),
            3
        )
    for i in range(1, 4):
        pygame.draw.line(
            screen,
            'black',
            (0, i * space_per_line),
            (600, i * space_per_line),
            3
        )
    for i in range(1, 9):
        pygame.draw.line(
            screen,
            'black',
            (i * space_per_box, 0),
            (i * space_per_box, 600),
            1
        )
    for i in range(1, 9):
        pygame.draw.line(
            screen,
            'black',
            (0, i * space_per_box),
            (600, i * space_per_box),
            1
        )


def menu_screen():
    button1 = pygame.Rect(40, 400, 150, 60)
    button2 = pygame.Rect(220, 400, 150, 60)
    button3 = pygame.Rect(400, 400, 150, 60)
    buttons = [button1, button2, button3]

    screen.blit(texture, (0, 0))
    menu_header = header.render('Welcome to Sudoku!', True, 'black')
    screen.blit(menu_header, (75, 200))
    menu_subheader = subheader.render('Group 77', True, 'black')
    screen.blit(menu_subheader, (250, 250))
    difficulty_text = subheader.render('Choose difficulty level to begin!', True, 'black')
    screen.blit(difficulty_text, (110, 360))

    for index in buttons:  # This creates the difficulty buttons on the menu screen.
        pygame.draw.rect(
            screen,
            dark_brown,
            index,
            border_radius=20
        )

    for i in range(len(difficulty_levels)):
        button_text = subheader.render(difficulty_levels[i], True, 'white')
        text_rect = button_text.get_rect(center=buttons[i].center)
        screen.blit(button_text, (text_rect))


def game_win_screen():
    screen.blit(texture, (0, 0))
    win_text = header.render('Game Won!', True, 'black')
    screen.blit(win_text, (150, 250))

    # Draw exit button
    exit_button = pygame.Rect(225, 350, 150, 60)
    pygame.draw.rect(screen, dark_brown, exit_button, border_radius=20)
    exit_text = subheader.render('Exit', True, 'white')
    screen.blit(exit_text, (270, 365))


def game_over_screen():
    screen.blit(texture, (0, 0))
    over_text = header.render('Game Over :(', True, 'black')
    screen.blit(over_text, (150, 250))

    # Draw restart button
    restart_button = pygame.Rect(225, 350, 150, 60)
    pygame.draw.rect(screen, dark_brown, restart_button, border_radius=20)
    restart_text = subheader.render('Restart', True, 'white')
    screen.blit(restart_text, (250, 365))

if __name__ == '__main__':
    main()
