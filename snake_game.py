import curses
import random
import time

def main(stdscr):
    # Initialize curses
    curses.curs_set(0)  # Hide the cursor
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Snake color
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Food color
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Text color
    
    # Set up the screen
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    
    # Create game window with a border
    game_win = curses.newwin(height-2, width-2, 1, 1)
    game_win.keypad(True)  # Enable special keys
    game_win.timeout(100)  # Refresh rate (ms)
    
    # Initialize game variables
    snake_x = width // 4
    snake_y = height // 2
    snake = [
        [snake_y, snake_x],
        [snake_y, snake_x-1],
        [snake_y, snake_x-2]
    ]
    
    # Initial food position
    food = [height // 2, width // 2]
    game_win.addch(food[0], food[1], '*', curses.color_pair(2))
    
    # Initial direction (RIGHT)
    key = curses.KEY_RIGHT
    
    # Score
    score = 0
    
    # Draw border
    stdscr.box()
    stdscr.addstr(0, 2, " SNAKE GAME ", curses.color_pair(3) | curses.A_BOLD)
    stdscr.addstr(0, width - 15, " Score: 0 ", curses.color_pair(3))
    stdscr.refresh()
    
    # Game loop
    game_over = False
    while not game_over:
        # Display game info
        stdscr.addstr(0, width - 15, f" Score: {score} ", curses.color_pair(3))
        stdscr.refresh()
        
        # Get next key press (non-blocking)
        next_key = game_win.getch()
        
        # Update direction if valid key pressed
        if next_key != -1:
            key = next_key
        
        # Determine new head position based on direction
        new_head = [snake[0][0], snake[0][1]]
        
        if key == curses.KEY_DOWN:
            new_head[0] += 1
        elif key == curses.KEY_UP:
            new_head[0] -= 1
        elif key == curses.KEY_RIGHT:
            new_head[1] += 1
        elif key == curses.KEY_LEFT:
            new_head[1] -= 1
        
        # Add new head to snake
        snake.insert(0, new_head)
        
        # Check for game over conditions
        if (
            new_head[0] <= 0 or new_head[0] >= height-3 or  # Hit top/bottom borders
            new_head[1] <= 0 or new_head[1] >= width-3 or   # Hit left/right borders
            new_head in snake[1:]                           # Hit self
        ):
            game_over = True
            continue
        
        # Check if snake ate the food
        if snake[0] == food:
            score += 1
            # Generate new food
            while True:
                food = [
                    random.randint(1, height - 4),
                    random.randint(1, width - 4)
                ]
                if food not in snake:
                    break
            game_win.addch(food[0], food[1], '*', curses.color_pair(2))
        else:
            # Remove tail if no food was eaten
            tail = snake.pop()
            game_win.addch(tail[0], tail[1], ' ')
        
        # Draw snake head
        game_win.addch(snake[0][0], snake[0][1], 'O', curses.color_pair(1))
        # Draw snake body
        for segment in snake[1:]:
            game_win.addch(segment[0], segment[1], 'o', curses.color_pair(1))
    
    # Game over screen
    game_win.clear()
    game_over_msg = "GAME OVER!"
    score_msg = f"Final Score: {score}"
    exit_msg = "Press any key to exit..."
    
    game_win.addstr(height//2-2, (width-len(game_over_msg))//2, game_over_msg, curses.color_pair(2) | curses.A_BOLD)
    game_win.addstr(height//2, (width-len(score_msg))//2, score_msg, curses.color_pair(3))
    game_win.addstr(height//2+2, (width-len(exit_msg))//2, exit_msg, curses.color_pair(3))
    
    game_win.refresh()
    game_win.timeout(-1)  # Switch to blocking mode
    game_win.getch()      # Wait for a key press

if __name__ == "__main__":
    try:
        # Initialize and run curses application
        curses.wrapper(main)
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        pass
    finally:
        # Ensure terminal is reset properly
        curses.endwin()
        print("Thanks for playing Snake!")

