import random

# ---------------------------
# Game 1: Hangman
# ---------------------------

def hangman():
    print("\n🎯 === HANGMAN === 🎯")

    words = [
        "python","castle","dragon","stickman","galaxy","computer","adventure",
        "mystery","puzzle","science","planet","wizard","forest","island",
        "treasure","robot","spaceship","volcano","mountain","jungle","desert",
        "ocean","pirate","kingdom","magic","portal","battle","knight","shadow",
        "thunder","storm","lightning","crystal","energy","gravity","nebula",
        "asteroid","comet","universe","dimension","mission","explorer"
    ]

    word = random.choice(words)
    guessed = set()
    wrong = 0
    max_wrong = 6

    while True:
        print("\n❌ Wrong guesses:", wrong, "/", max_wrong)
        display = " ".join([c if c in guessed else "_" for c in word])
        print("🔤 Word:", display)

        if all(c in guessed for c in word):
            print("\n🎉 You win!")
            break

        if wrong >= max_wrong:
            print("\n💀 You lost! The word was:", word)
            break

        guess = input("Guess a letter: ").lower()

        if len(guess) != 1 or not guess.isalpha():
            print("⚠️ Enter a single letter.")
            continue

        if guess in guessed:
            print("⚠️ Already guessed.")
            continue

        guessed.add(guess)

        if guess not in word:
            wrong += 1

# ---------------------------
# Game 2: Number Guessing
# ---------------------------

def number_guess():
    print("\n🔢 === NUMBER GUESSING === 🔢")
    print("I'm thinking of a number between 1 and 100.")

    number = random.randint(1, 100)

    while True:
        guess = input("Your guess: ")

        if not guess.isdigit():
            print("⚠️ Enter a number.")
            continue

        guess = int(guess)

        if guess < number:
            print("⬆️ Too low!")
        elif guess > number:
            print("⬇️ Too high!")
        else:
            print("🎉 Correct! You win!")
            break

# ---------------------------
# Game 3: Rock Paper Scissors
# ---------------------------

def rps():
    print("\n✊ === ROCK PAPER SCISSORS === ✋")

    choices = ["rock", "paper", "scissors"]
    emojis = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}

    while True:
        player = input("Choose rock, paper, or scissors: ").lower()

        if player not in choices:
            print("⚠️ Invalid choice.")
            continue

        cpu = random.choice(choices)
        print("CPU chose:", emojis[cpu], cpu)

        if player == cpu:
            print("🤝 It's a tie!")
        elif (player == "rock" and cpu == "scissors") or \
             (player == "paper" and cpu == "rock") or \
             (player == "scissors" and cpu == "paper"):
            print("🏆 You win!")
        else:
            print("💀 You lose!")

        again = input("Play again? (y/n): ").lower()
        if again != "y":
            break

# ---------------------------
# Game 4: Stickman Dodge
# ---------------------------

def stickman_dodge():
    print("\n🏃 === STICKMAN DODGE === 🪨")
    print("Avoid the falling rocks!")
    print("Move left (a) or right (d).")
    print("Survive as long as you can.\n")

    stick_pos = 2
    score = 0

    while True:
        rock_pos = random.randint(1, 3)

        print("\n🪨 Rock falling in lane:", rock_pos)
        print("Your position (🙂):")

        lanes = [" ", " ", " "]
        lanes[stick_pos - 1] = "🙂"
        print(" ".join(lanes))

        move = input("Move (a/d): ").lower()

        if move == "a" and stick_pos > 1:
            stick_pos -= 1
        elif move == "d" and stick_pos < 3:
            stick_pos += 1

        if stick_pos == rock_pos:
            print("\n💥 You got hit!")
            break

        score += 1
        print("Score:", score)

    print("\nGame over! Final score:", score)

# ---------------------------
# Game 5: Tic Tac Toe
# ---------------------------

def tic_tac_toe():
    print("\n⭕ === TIC TAC TOE === ❌")
    board = [" "] * 9

    def print_board():
        print("\n")
        print(board[0], "|", board[1], "|", board[2])
        print("--+---+--")
        print(board[3], "|", board[4], "|", board[5])
        print("--+---+--")
        print(board[6], "|", board[7], "|", board[8])
        print("\n")

    def check_win(player):
        wins = [
            (0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)
        ]
        return any(board[a] == board[b] == board[c] == player for a,b,c in wins)

    while True:
        print_board()
        move = input("Choose a spot (1-9): ")

        if not move.isdigit() or not 1 <= int(move) <= 9:
            print("⚠️ Invalid move.")
            continue

        move = int(move) - 1

        if board[move] != " ":
            print("⚠️ Spot taken.")
            continue

        board[move] = "X"

        if check_win("X"):
            print_board()
            print("🏆 You win!")
            break

        if " " not in board:
            print_board()
            print("🤝 It's a tie!")
            break

        cpu_move = random.choice([i for i in range(9) if board[i] == " "])
        board[cpu_move] = "O"

        if check_win("O"):
            print_board()
            print("💀 CPU wins!")
            break

# ---------------------------
# Game 6: Emoji Quiz
# ---------------------------

def emoji_quiz():
    print("\n😎 === EMOJI QUIZ === 🤔")
    quizzes = {
        "🌧️☔": "rain",
        "🔥🐉": "dragon",
        "🚗💨": "car",
        "🐍💻": "python",
        "⭐🚀": "space",
        "🏰🐴": "castle",
        "🎮🕹️": "game",
        "🌋🔥": "volcano",
        "🌲🏕️": "camp",
        "🍎📱": "apple",
        "⚽🥅": "football",
        "🎬🍿": "movie"
    }

    emoji, answer = random.choice(list(quizzes.items()))
    print("\nGuess the word:", emoji)

    guess = input("Your answer: ").lower()

    if guess == answer:
        print("🎉 Correct!")
    else:
        print("❌ Wrong! The answer was:", answer)

# ---------------------------
# Game 7: Word Scramble
# ---------------------------

def word_scramble():
    print("\n🔤 === WORD SCRAMBLE === 🔀")

    words = [
        "python","castle","dragon","galaxy","forest","planet","wizard",
        "energy","gravity","nebula","island","treasure","portal","battle",
        "shadow","thunder","storm","crystal","mission","explorer"
    ]

    word = random.choice(words)
    scrambled = "".join(random.sample(word, len(word)))

    print("\nUnscramble this word:", scrambled)

    guess = input("Your guess: ").lower()

    if guess == word:
        print("🎉 Correct!")
    else:
        print("❌ Wrong! The word was:", word)

# ---------------------------
# Game 8: Math Quiz
# ---------------------------

def math_quiz():
    print("\n🧮 === MATH QUIZ === 📘")

    score = 0

    for _ in range(5):
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        op = random.choice(["+", "-", "*"])

        if op == "+":
            answer = a + b
        elif op == "-":
            answer = a - b
        else:
            answer = a * b

        print(f"\nSolve: {a} {op} {b}")
        guess = input("Your answer: ")

        if guess.isdigit() and int(guess) == answer:
            print("✅ Correct!")
            score += 1
        else:
            print("❌ Wrong! The answer was:", answer)

    print("\nFinal score:", score, "/ 5")

# ---------------------------
# Main Menu
# ---------------------------

def main():
    while True:
        print("\n🎮 === PYTHON GAME HUB === 🎮")
        print("1) Hangman")
        print("2) Number Guessing")
        print("3) Rock Paper Scissors")
        print("4) Stickman Dodge")
        print("5) Tic Tac Toe")
        print("6) Emoji Quiz")
        print("7) Word Scramble")
        print("8) Math Quiz")
        print("9) Quit")

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
            tic_tac_toe()
        elif choice == "6":
            emoji_quiz()
        elif choice == "7":
            word_scramble()
        elif choice == "8":
            math_quiz()
        elif choice == "9":
            print("👋 Thanks for playing!")
            break
        else:   
            print("⚠️ Invalid choice.")

main()
