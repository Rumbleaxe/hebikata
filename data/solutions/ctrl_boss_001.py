lives = 2
score = 1500
if lives == 0:
    game_state = "game_over"
elif score >= 1000:
    game_state = "victory"
else:
    game_state = "playing"
