import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wise Choose Game")

# Load assets
background_image = pygame.image.load("M:/Balance Scale/assets/images/background.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

win_sound = pygame.mixer.Sound("M:/Balance Scale/assets/sound/win.wav")
pygame.mixer.music.load("M:/Balance Scale/assets/sound/background_music.mp3")
pygame.mixer.music.play(-1)

# Game variables
font = pygame.font.Font(None, 36)
players = ["You", "Friend 1", "Friend 2", "Friend 3"]
player_scores = {player: 0 for player in players}
player_guesses = {player: None for player in players}
current_player_index = 0
round_number = 1
winning_number = 0
eliminated_players = []
round_in_progress = True
round_winner = None  # Variable to store the winner of the round

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 223, 0)
RED = (255, 0, 0)

# Function to display text
def draw_text(text, size, color, x, y, center=False):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    if center:
        rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, rect)
    else:
        screen.blit(text_surface, (x, y))

# Calculate the winning number and determine round results
def calculate_winner():
    global winning_number, round_in_progress, round_winner

    guesses = list(player_guesses.values())
    winning_number = round(sum(guesses) / len(guesses) * 0.8)

    closest_player = None
    closest_difference = math.inf
    for player, guess in player_guesses.items():
        difference = abs(winning_number - guess)
        if difference < closest_difference:
            closest_difference = difference
            closest_player = player

    # Update scores
    player_scores[closest_player] += 1
    for player in player_scores:
        if player != closest_player:
            player_scores[player] -= 1

    # Check for elimination
    for player in list(player_scores.keys()):
        if player_scores[player] <= -5:
            eliminated_players.append(player)
            players.remove(player)
            del player_scores[player]
            del player_guesses[player]

    # Store the round winner
    round_winner = closest_player
    round_in_progress = False
    win_sound.play()

# Game loop
running = True
user_input = ""
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and round_in_progress:
            if event.key == pygame.K_RETURN and user_input.isdigit():
                player_guesses[players[current_player_index]] = int(user_input)
                user_input = ""
                current_player_index += 1
                if current_player_index == len(players):
                    calculate_winner()
            elif event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            elif event.unicode.isdigit() and len(user_input) < 3:
                user_input += event.unicode

    screen.blit(background_image, (0, 0))
    draw_text(f"Round: {round_number}", 48, WHITE, SCREEN_WIDTH // 2, 30, center=True)

    # Display scores
    score_y = 50
    for i, player in enumerate(players):
        score_x = 50 if i % 2 == 0 else SCREEN_WIDTH - 200
        y_offset = 30 if i < 2 else SCREEN_HEIGHT - 60
        draw_text(f"{player}: {player_scores[player]}", 36, WHITE, score_x, y_offset)

    if round_in_progress:
        draw_text(f"{players[current_player_index]}'s Turn - Enter your number:", 36, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, center=True)
        hidden_input = '*' * len(user_input) if user_input else ""
        draw_text(hidden_input, 36, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
    else:
        # Display guesses and results
        guess_y = 150
        for player, guess in player_guesses.items():
            draw_text(f"{player}: {guess}", 36, WHITE, SCREEN_WIDTH // 2, guess_y, center=True)
            guess_y += 40

        draw_text(f"Winning Number: {winning_number}", 48, GOLD, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 4 - 55)
        draw_text(f"Round Winner: {round_winner}", 48, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, center=True)
        pygame.display.flip()
        pygame.time.wait(5000)  # Pause before next round

        round_number += 1
        player_guesses = {player: None for player in players}
        current_player_index = 0
        round_in_progress = True

    if len(players) == 1:
        draw_text(f"{players[0]} Win the Game!", 72, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    pygame.display.flip()

pygame.quit()