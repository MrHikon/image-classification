import random

# ── SETUP FUNCTIONS ────────────────────────────────────────

def get_difficulty():
    # Let the player choose their difficulty before each round
    print("\n  Select Difficulty:")
    print("  1) Easy   (1 - 50,  unlimited guesses)")
    print("  2) Normal (1 - 100, 10 guesses max)")
    print("  3) Hard   (1 - 200,  5 guesses max)")

    while True:
        level = input("  Your choice (1/2/3): ").strip()

        # Return (low, high, max_guesses) for the chosen level
        # 999 is used for Easy to represent "unlimited"
        if   level == "1": return 1,  50,  999
        elif level == "2": return 1, 100,  10
        elif level == "3": return 1, 200,   5
        else: print("  Please enter 1, 2, or 3.")

def give_hint(guess, secret):
    # Calculate how far away the guess is from the secret number
    gap = abs(guess - secret)

    # Return a hint based on how close the guess is
    if   gap == 0:  return ""
    elif gap <= 5:  return "  (Hint: Very warm! Almost there.)"
    elif gap <= 15: return "  (Hint: Getting warm.)"
    elif gap <= 30: return "  (Hint: Cold.)"
    else:           return "  (Hint: Freezing cold!)"

# ── ONE ROUND OF THE GAME ──────────────────────────────────

def play_round(low, high, max_guesses):
    # Pick a random secret number within the difficulty range
    secret   = random.randint(low, high)
    attempts = 0

    print(f"\n  I have picked a number between {low} and {high}.")

    if max_guesses < 999:
        print(f"  You have {max_guesses} guesses. Good luck!\n")
    else:
        print("  You have unlimited guesses. Good luck!\n")

    while attempts < max_guesses:
        # Show remaining guesses for limited modes, or a count for unlimited
        remaining = max_guesses - attempts
        prompt = f"  Guess ({remaining} left): " if max_guesses < 999 else f"  Guess #{attempts+1}: "

        raw = input(prompt).strip()

        # Reject anything that is not a whole number
        if not raw.lstrip('-').isdigit():
            print("  Please enter a whole number.")
            continue

        guess     = int(raw)
        attempts += 1

        if guess < secret:
            print("  Too LOW!")
            print(give_hint(guess, secret))
        elif guess > secret:
            print("  Too HIGH!")
            print(give_hint(guess, secret))
        else:
            # Correct guess — exit the loop and signal a win
            return True, secret, attempts

    # Player ran out of guesses — signal a loss
    return False, secret, attempts

# ── MAIN GAME LOOP ─────────────────────────────────────────

def run_game():
    print("=" * 45)
    print("        NUMBER GUESSING GAME")
    print("=" * 45)

    # Track wins and losses across all rounds in this session
    total_rounds = 0
    total_wins   = 0

    while True:
        low, high, max_guesses = get_difficulty()
        won, secret, attempts  = play_round(low, high, max_guesses)
        total_rounds += 1

        if won:
            total_wins += 1
            print(f"\n  CORRECT! The number was {secret}.")
            print(f"  You guessed it in {attempts} attempt(s). Well done!")
        else:
            print(f"\n  GAME OVER! The number was {secret}.")
            print("  Better luck next time.")

        # Ask if the player wants another round
        again = input("\n  Play another round? (yes/no): ").strip().lower()
        if again not in ("yes", "y"):
            break

    # ── SESSION SUMMARY ────────────────────────────────────
    print("\n" + "=" * 45)
    print(f"  Rounds played : {total_rounds}")
    print(f"  Rounds won    : {total_wins}")
    print(f"  Rounds lost   : {total_rounds - total_wins}")
    print("=" * 45)
    print("  Thanks for playing. Goodbye!")

# ── ENTRY POINT ────────────────────────────────────────────
run_game()