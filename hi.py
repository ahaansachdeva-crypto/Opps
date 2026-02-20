import random

# ---------------------------
# Game 1: Hangman
# ---------------------------

def hangman():
    print("\n=== HANGMAN ===")
    words = ["python", "castle", "dragon", "stickman", "galaxy", "computer"]
    word = random.choice(words)
    guessed = set()
    wrong = 0
    max_wrong = 6

    while True:
        print("\nWrong guesses:", wrong, "/", max_wrong)
        display = " ".join([c if c in guessed else "_" for c in word])
        print("Word:", display)

        if all(c in guessed for c in word):
            print("\nYou win!")
            break

        if wrong >= max_wrong:
            print("\nYou lost! The word was:", word)
            break

        guess = input("Guess a letter: ").lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Enter a single letter.")
            continue

        if guess in guessed:
            print("Already guessed.")
            continue

        guessed.add(guess)

        if guess not in word:
            wrong += 1

# ---------------------------
# Game 2: Number Guessing
# ---------------------------

def number_guess():
    print("\n=== NUMBER GUESSING ===")
    print("I'm thinking of a number between 1 and 50.")
    number = random.randint(1, 50)

    while True:
        guess = input("Your guess: ")

        if not guess.isdigit():
            print("Enter a number.")
            continue

        guess = int(guess)

        if guess < number:
            print("Too low!")
        elif guess > number:
            print("Too high!")
        else:
            print("Correct! You win!")
            break

# ---------------------------
# Game 3: Rock Paper Scissors
# ---------------------------

def rps():
    print("\n=== ROCK PAPER SCISSORS ===")
    choices = ["rock", "paper", "scissors"]

    while True:
        player = input("Choose rock, paper, or scissors: ").lower()

        if player not in choices:
            print("Invalid choice.")
            continue

        cpu = random.choice(choices)
        print("CPU chose:", cpu)

        if player == cpu:
            print("It's a tie!")
        elif (player == "rock" and cpu == "scissors") or \
             (player == "paper" and cpu == "rock") or \
             (player == "scissors" and cpu == "paper"):
            print("You win!")
        else:
            print("You lose!")

        again = input("Play again? (y/n): ").lower()
        if again != "y":
            break

# ---------------------------
# Game 4: Stickman Dodge (simple)
# ---------------------------

def stickman_dodge():
    print("\n=== STICKMAN DODGE ===")
    print("Avoid the falling rocks!")
    print("Move left (a) or right (d).")
    print("Survive as long as you can.\n")

    stick_pos = 2
    score = 0

    while True:
        rock_pos = random.randint(1, 3)

        print("\nRock falling in lane:", rock_pos)
        print("Your position (O):")

        lanes = [" ", " ", " "]
        lanes[stick_pos - 1] = "O"
        print(" ".join(lanes))

        move = input("Move (a/d): ").lower()

        if move == "a" and stick_pos > 1:
            stick_pos -= 1
        elif move == "d" and stick_pos < 3:
            stick_pos += 1

        if stick_pos == rock_pos:
            print("\nYou got hit!")
            break

        score += 1
        print("Score:", score)

    print("\nGame over! Final score:", score)

# ---------------------------
# Main Menu
# ---------------------------

def main():
    while True:
        print("\n=== PYTHON GAME HUB ===")
        print("1) Hangman")
        print("2) Number Guessing")
        print("3) Rock Paper Scissors")
        print("4) Stickman Dodge")
        print("5) Quit")

        choice = input("Choose a game: ")

        if choice == "1":
            hangman()
        elif choice == "2":
            number_guess()
        elif choice == "3":
            rps()
        elif choice == "4":
            stickman_dodge()
        elif choice == "5":
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice.")

main()
