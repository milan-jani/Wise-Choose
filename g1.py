import pygame
import random
import math

# Initialize Pygame and its mixer for sound
pygame.init()
pygame.mixer.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("WISE CHOOSE")

# Load assets
background_image = pygame.image.load("M:/Balance Scale/assets/images/background.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Sound effects
win_sound = pygame.mixer.Sound("M:/Balance Scale/assets/sound/win.wav")
pygame.mixer.music.load("M:/Balance Scale/assets/sound/background_music.mp3")
pygame.mixer.music.play(-1)  # Loop the background music

# Game variables
font = pygame.font.Font(None, 36)
players = ["You", "Friend 1", "Friend 2", "Friend 3"]
player_guesses = {player: None for player in players}  # Stores each player's guess
player_scores = {player: 0 for player in players}  # Initialize player scores
current_player_index = 0
winning_number = 0
round_winner = None
round_number = 1
game_over = False
input_active = True
user_input = ""  # Current player's input

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GOLD = (255, 223, 0)

# Function to display text
def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Function to calculate the winning number and determine the winner
def calculate_winner():
    global winning_number, round_winner
    guesses = list(player_guesses.values())
    winning_number = round(sum(guesses) / len(guesses) * 0.8)

    closest_player = None
    closest_difference = math.inf
    for player, guess in player_guesses.items():
        difference = abs(winning_number - guess)
        if difference < closest_difference:
            closest_difference = difference
            closest_player = player

    round_winner = closest_player
    player_scores[round_winner] += 1  # Winner gets +1 point

    # Update scores and eliminate players with -5 points
    for player in player_scores:
        if player != round_winner:
            player_scores[player] -= 1  # Other players get -1 point
    
    # Eliminate players with -5 points
    for player in list(player_scores.keys()):
        if player_scores[player] <= -5:
            player_scores.pop(player)
            players.remove(player)
            if current_player_index >= len(players):  # Adjust index if last player was removed
                current_player_index = 0
            break

    win_sound.play()  # Play the winning sound

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle input for guessing numbers
        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_RETURN and user_input.isdigit():
                player_guesses[players[current_player_index]] = int(user_input)
                user_input = ""  # Clear the input after submission
                current_player_index += 1
                if current_player_index == len(players):
                    input_active = False
                    calculate_winner()
            elif event.key == pygame.K_BACKSPACE:  # Handle backspace
                user_input = user_input[:-1]
            elif event.unicode.isdigit() and len(user_input) < 3:  # Limit input length
                user_input += event.unicode

    # Drawing on the screen
    screen.blit(background_image, (0, 0))  # Background image

    # Display the current round
    draw_text(f"Round: {round_number}", 48, WHITE, SCREEN_WIDTH // 2 - 50, 10)

    if input_active:
        # Prompt current player to input their guess
        current_player = players[current_player_index]
        draw_text(f"{current_player}'s Turn - Enter a number:", 36, WHITE, 10, SCREEN_HEIGHT - 100)
        draw_text(user_input, 36, RED, 10, SCREEN_HEIGHT - 50)
    else:
        # Display the guesses
        guess_y_offset = 150
        for i, player in enumerate(players):
            draw_text(f"{player}: {player_guesses[player]}", 36, WHITE, SCREEN_WIDTH // 2 - 100, guess_y_offset + i * 40)

        # Animate the calculation of the average
        draw_text(f"Calculating average...", 36, WHITE, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50)
        pygame.display.flip()
        pygame.time.wait(1000)  # Wait for 1 second to create suspense

        # Show the winning number after calculation
        draw_text(f"Winning Number: {winning_number}", 36, WHITE, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
        pygame.display.flip()
        pygame.time.wait(1000)  # Wait for 1 second

        # Animate winner announcement
        draw_text(f"Round Winner: {round_winner}", 36, GOLD, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50)
        pygame.display.flip()
        pygame.time.wait(1000)  # Wait for 1 second

        # Display results after winner is calculated
        draw_text(f"Press R to start a new round or Q to quit.", 36, WHITE, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 100)

    # Display player names and scores at each corner
    draw_text(f"{players[0]}: {player_scores[players[0]]}", 36, WHITE, 10, 10)  # Top-left
    if len(players) > 1:
        draw_text(f"{players[1]}: {player_scores[players[1]]}", 36, WHITE, SCREEN_WIDTH - 200, 10)  # Top-right
    if len(players) > 2:
        draw_text(f"{players[2]}: {player_scores[players[2]]}", 36, WHITE, 10, SCREEN_HEIGHT - 60)  # Bottom-left
    if len(players) > 3:
        draw_text(f"{players[3]}: {player_scores[players[3]]}", 36, WHITE, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 60)  # Bottom-right

    # Check for restarting or quitting
    if not input_active and not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:  # Restart round
            round_number += 1
            player_guesses = {player: None for player in players}
            current_player_index = 0
            input_active = True
        elif keys[pygame.K_q]:  # Quit game
            running = False

    # Check if there is only one player left
    if len(players) == 1:
        draw_text(f"{players[0]} Wins!", 72, WHITE, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2)
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False  # End the game

    # Update the screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()