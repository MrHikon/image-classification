# ── FUNCTIONS ──────────────────────────────────────────────

def encrypt_message(plaintext, shift):
    result = ""

    for character in plaintext:

        # Keep spaces as they are
        if character == " ":
            result += " "

        elif character.isalpha():
            # Use 'A' as base for uppercase letters, 'a' for lowercase
            # This lets us work within the correct 0-25 range for each case
            base = ord('A') if character.isupper() else ord('a')

            # Shift the character forward, and wrap around using % 26
            # Example: shifting 'Z' by 1 gives 'A', not a character outside the alphabet
            shifted_pos = (ord(character) - base + shift) % 26
            result     += chr(base + shifted_pos)

        else:
            # Leave digits, punctuation and symbols unchanged
            result += character

    return result

def decrypt_message(ciphertext, shift):
    # Decryption is just encryption with a negative shift
    return encrypt_message(ciphertext, -shift)

def display_menu():
    print("\n" + "=" * 40)
    print("       CAESAR CIPHER TOOL")
    print("=" * 40)
    print("  1) Encrypt a message")
    print("  2) Decrypt a message")
    print("  3) Exit")
    print("=" * 40)

def get_shift_value():
    # Keep asking until the user enters a valid whole number
    while True:
        raw = input("Enter shift value (1-25): ").strip()
        if raw.lstrip('-').isdigit():
            # Use modulo to keep shift within 0-25 even if user enters a large number
            return int(raw) % 26
        print("  Please enter a whole number.")

# ── MAIN PROGRAM LOOP ──────────────────────────────────────

def run_cipher():
    while True:
        display_menu()
        option = input("Choose an option (1/2/3): ").strip()

        if option == "1":
            message   = input("\nEnter your message to encrypt: ")
            shift_val = get_shift_value()
            encrypted = encrypt_message(message, shift_val)

            # Show the original and encrypted messages side by side
            print(f"\n  Original message  : {message}")
            print(f"  Shift value used  : {shift_val}")
            print(f"  Encrypted message : {encrypted}")

        elif option == "2":
            message   = input("\nEnter the encrypted message to decrypt: ")
            shift_val = get_shift_value()
            decrypted = decrypt_message(message, shift_val)

            # Show the encrypted input and the recovered original
            print(f"\n  Encrypted message : {message}")
            print(f"  Shift value used  : {shift_val}")
            print(f"  Decrypted message : {decrypted}")

        elif option == "3":
            print("\n  Exiting Caesar Cipher Tool. Goodbye!")
            break

        else:
            print("  Invalid option. Please choose 1, 2, or 3.")

# ── ENTRY POINT ────────────────────────────────────────────
run_cipher()