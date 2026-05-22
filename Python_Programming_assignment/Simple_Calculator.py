# ── ARITHMETIC FUNCTIONS ───────────────────────────────────

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    # Return None to signal division by zero instead of crashing
    if b == 0:
        return None
    return a / b

# ── INPUT HELPERS ──────────────────────────────────────────

def get_number(prompt):
    # Keep asking until the user enters something that can be a number
    while True:
        try:
            return float(input(prompt).strip())
        except ValueError:
            # float() throws ValueError if the input is not a valid number
            print("  That is not a valid number. Try again.")

def show_menu():
    print("\n" + "+" * 35)
    print("       SIMPLE CALCULATOR")
    print("+" * 35)
    print("  1.  Addition       (+)")
    print("  2.  Subtraction    (-)")
    print("  3.  Multiplication (x)")
    print("  4.  Division       (/)")
    print("  5.  View History")
    print("  6.  Exit")
    print("+" * 35)

# ── MAIN PROGRAM LOOP ──────────────────────────────────────

def run_calculator():
    # List to store every valid calculation as a readable string
    history = []

    while True:
        show_menu()
        choice = input("Choose operation (1-6): ").strip()

        if choice in ("1", "2", "3", "4"):
            num1 = get_number("Enter first number : ")
            num2 = get_number("Enter second number: ")

            # Call the correct function based on the user's choice
            if   choice == "1": answer, operator = add(num1, num2),      "+"
            elif choice == "2": answer, operator = subtract(num1, num2), "-"
            elif choice == "3": answer, operator = multiply(num1, num2), "x"
            else:               answer, operator = divide(num1, num2),   "/"

            if answer is None:
                # divide() returned None, meaning the user tried to divide by zero
                print("\n  ERROR: Cannot divide by zero!")
            else:
                # Show whole numbers without a decimal point (e.g. 6 instead of 6.0)
                display = int(answer) if answer == int(answer) else round(answer, 4)
                print(f"\n  {num1} {operator} {num2} = {display}")

                # Save this calculation to history
                history.append(f"{num1} {operator} {num2} = {display}")

        elif choice == "5":
            # Print all saved calculations, or a message if none exist yet
            if not history:
                print("\n  No calculations yet.")
            else:
                print("\n  --- Calculation History ---")
                for i, entry in enumerate(history, 1):
                    print(f"  {i}. {entry}")

        elif choice == "6":
            print("\n  Calculator closed. Goodbye!")
            break

        else:
            print("  Invalid choice. Please select 1 to 6.")

# ── ENTRY POINT ────────────────────────────────────────────
run_calculator()