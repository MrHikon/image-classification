import random

# ── FUNCTIONS ──────────────────────────────────────────────

def get_computer_choice():
    # Randomly pick one of the three weapons for the computer
    weapons = ["rock", "paper", "scissors"]
    return random.choice(weapons)

def decide_winner(player, computer):
    # If both chose the same thing, it's a draw
    if player == computer:
        return "draw"

    # Dictionary maps each weapon to the one it beats
    winning_combos = {
        "rock":     "scissors",   # rock crushes scissors
        "scissors": "paper",      # scissors cuts paper
        "paper":    "rock",       # paper covers rock
    }

    # Check if the player's weapon beats the computer's weapon
    if winning_combos[player] == computer:
        return "player"

    # Otherwise the computer wins
    return "computer"

def display_banner():
    print("=" * 45)
    print("       ROCK  |  PAPER  |  SCISSORS")
    print("=" * 45)

# ── MAIN GAME LOOP ─────────────────────────────────────────

def play_game():
    display_banner()

    valid_choices = ["rock", "paper", "scissors"]

    # Score counters for the session
    player_wins   = 0
    computer_wins = 0
    draws         = 0
    round_number  = 1

    while True:
        print(f"\n--- Round {round_number} ---")
        print("Your options: rock / paper / scissors / quit")
        player_choice = input("Your choice: ").strip().lower()

        # Exit the game loop if the user types quit
        if player_choice == "quit":
            break

        # Reject anything that is not a valid weapon
        if player_choice not in valid_choices:
            print("  Invalid input. Please type rock, paper, scissors, or quit.")
            continue

        # Get the computer's random choice
        computer_choice = get_computer_choice()
        print(f"  You chose     : {player_choice}")
        print(f"  Computer chose: {computer_choice}")

        # Determine and display the round result
        outcome = decide_winner(player_choice, computer_choice)

        if outcome == "player":
            print("  >> You WIN this round!")
            player_wins += 1
        elif outcome == "computer":
            print("  >> Computer WINS this round.")
            computer_wins += 1
        else:
            print("  >> It's a DRAW.")
            draws += 1

        round_number += 1

    # ── FINAL SCOREBOARD ───────────────────────────────────
    print("\n" + "=" * 45)
    print("           FINAL SCOREBOARD")
    print("=" * 45)
    print(f"  Rounds played  : {round_number - 1}")
    print(f"  Your wins      : {player_wins}")
    print(f"  Computer wins  : {computer_wins}")
    print(f"  Draws          : {draws}")

    # Declare the overall winner based on total wins
    if player_wins > computer_wins:
        print("\n  OVERALL WINNER: YOU! Well played.")
    elif computer_wins > player_wins:
        print("\n  OVERALL WINNER: Computer. Better luck next time!")
    else:
        print("\n  OVERALL RESULT: It's an even match!")

    print("=" * 45)
    print("  Thanks for playing. Goodbye!")

# ── ENTRY POINT ────────────────────────────────────────────
play_game()