import random
import time

# ---------------------------
# Game 1: Hangman
# ---------------------------

def hangman():
    print("\n🎯 === HANGMAN === 🎯")

    words = [
        "python", "castle", "dragon", "stickman", "galaxy", "computer",
        "adventure", "mystery", "puzzle", "science", "planet", "wizard",
        "forest", "island", "treasure", "robot", "spaceship", "volcano"
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
    print("I'm thinking of a number between 1 and 50.")

    number = random.randint(1, 50)

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
        "🌋🔥": "volcano"
    }

    emoji, answer = random.choice(list(quizzes.items()))
    print("\nGuess the word:", emoji)

    guess = input("Your answer: ").lower()

    if guess == answer:
        print("🎉 Correct!")
    else:
        print("❌ Wrong! The answer was:", answer)

# ---------------------------
# Game 7: Higher or Lower
# ---------------------------

def higher_lower():
    print("\n⬆️⬇️ === HIGHER OR LOWER === 🎲")
    print("Guess if the next number will be higher or lower!")

    score = 0
    current = random.randint(1, 20)

    while True:
        print("\nCurrent number:", current)
        guess = input("Higher or Lower (h/l): ").lower()

        if guess not in ["h", "l"]:
            print("⚠️ Invalid choice.")
            continue

        next_num = random.randint(1, 20)
        print("Next number:", next_num)

        if (guess == "h" and next_num > current) or \
           (guess == "l" and next_num < current):
            print("✅ Correct!")
            score += 1
        else:
            print("❌ Wrong!")
            break

        current = next_num

    print("Final score:", score)

# ---------------------------
# Game 8: Math Quiz
# ---------------------------

def math_quiz():
    print("\n➗ === MATH QUIZ === ✖️")

    a = random.randint(1, 12)
    b = random.randint(1, 12)
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
        print("🎉 Correct!")
    else:
        print("❌ Wrong! The answer was:", answer)

# ---------------------------
# Game 9: Word Scramble
# ---------------------------

def word_scramble():
    print("\n🔀 === WORD SCRAMBLE === 🧠")

    words = ["python", "castle", "dragon", "wizard", "planet", "forest"]
    word = random.choice(words)
    scrambled = "".join(random.sample(word, len(word)))

    print("\nUnscramble this word:", scrambled)
    guess = input("Your guess: ").lower()

    if guess == word:
        print("🎉 Correct!")
    else:
        print("❌ Wrong! The word was:", word)

# ---------------------------
# Game 10: Memory Match
# ---------------------------

def memory_match():
    print("\n🧠 === MEMORY MATCH === 🎴")

    cards = ["🐍", "🐍", "🔥", "🔥", "⭐", "⭐", "🚗", "🚗"]
    random.shuffle(cards)

    revealed = ["❓"] * 8
    score = 0

    while score < 4:
        print("\nBoard:")
        print(" ".join(revealed))

        try:
            a = int(input("Pick first card (1-8): ")) - 1
            b = int(input("Pick second card (1-8): ")) - 1
        except:
            print("⚠️ Invalid input.")
            continue

        if a == b or not (0 <= a < 8 and 0 <= b < 8):
            print("⚠️ Invalid picks.")
            continue

        print("Cards:", cards[a], cards[b])

        if cards[a] == cards[b]:
            print("🎉 Match!")
            revealed[a] = cards[a]
            revealed[b] = cards[b]
            score += 1
        else:
            print("❌ No match.")

    print("\n🏆 You matched all pairs!")

# ---------------------------
# Game 11: Snake (Text Version)
# ---------------------------

def snake_game():
    print("\n🐍 === SNAKE (TEXT VERSION) === 🍎")
    print("This is a simplified snake simulation.")

    length = 1
    score = 0

    while True:
        print(f"\nSnake length: {length} | Score: {score}")
        move = input("Move (w/a/s/d): ").lower()

        if move not in ["w", "a", "s", "d"]:
            print("⚠️ Invalid move.")
            continue

        if random.random() < 0.3:
            print("🍎 You found an apple!")
            length += 1
            score += 1

        if random.random() < 0.1:
            print("💥 You hit a wall!")
            break

    print("\nGame over! Final score:", score)

# ---------------------------
# Game 12: Sliding Puzzle
# ---------------------------

def sliding_puzzle():
    print("\n🧩 === SLIDING PUZZLE (3x3) === 🎯")

    puzzle = ["1", "2", "3", "4", "5", "6", "7", "8", " "]
    random.shuffle(puzzle)

    def show():
        print("\n")
        print(puzzle[0], puzzle[1], puzzle[2])
        print(puzzle[3], puzzle[4], puzzle[5])
        print(puzzle[6], puzzle[7], puzzle[8])

    while True:
        show()

        if puzzle == ["1","2","3","4","5","6","7","8"," "]:
            print("\n🏆 You solved it!")
            break

        move = input("Move tile (1-8): ")

        if move not in puzzle:
            print("⚠️ Invalid tile.")
            continue

        i = puzzle.index(move)
        b = puzzle.index(" ")

        valid = {
            0:[1,3], 1:[0,2,4], 2:[1,5],
            3:[0,4,6], 4:[1,3,5,7], 5:[2,4,8],
            6:[3,7], 7:[4,6,8], 8:[5,7]
        }

        if b in valid[i]:
            puzzle[i], puzzle[b] = puzzle[b], puzzle[i]
        else:
            print("⚠️ Can't move that tile.")

# ---------------------------
# Game 13: Guess the Song (Emoji Edition)
# ---------------------------

def guess_song():
    print("\n🎵 === GUESS THE SONG (EMOJI) === 🎤")

    songs = {
        "🧊❄️👸": "let it go",
        "🕺✨": "uptown funk",
        "🔥🎸": "we will rock you",
        "💃🌹": "despacito",
        "👑🎤": "royals"
        
    
    }

    emoji, answer = random.choice(list(songs.items()))
    print("\nGuess the song:", emoji)

    guess = input("Your answer: ").lower()

    if guess == answer:
        print("🎉 Correct!")
    else:
        print("❌ Wrong! The answer was:", answer)

# ---------------------------
# Game 14: RPG Battle
# ---------------------------

def rpg_battle():
    print("\n⚔️ === RPG BATTLE === 🐉")

    hp = 20
    enemy = 15

    while hp > 0 and enemy > 0:
        print(f"\nYour HP: {hp} | Enemy HP: {enemy}")
        move = input("Attack (a) or Heal (h): ").lower()

        if move == "a":
            dmg = random.randint(3, 7)
            print("You hit for", dmg)
            enemy -= dmg
        elif move == "h":
            heal = random.randint(2, 5)
            print("You heal", heal)
            hp += heal
        else:
            print("⚠️ Invalid move.")
            continue

        enemy_dmg = random.randint(2, 6)
        print("Enemy hits you for", enemy_dmg)
        hp -= enemy_dmg

    if hp <= 0:
        print("\n💀 You died!")
    else:
        print("\n🏆 You defeated the enemy!")

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
        print("7) Higher or Lower")
        print("8) Math Quiz")
        print("9) Word Scramble")
        print("10) Memory Match")
        print("11) Snake (Text Version)")
        print("12) Sliding Puzzle")
        print("13) Guess the Song (Emoji)")
        print("14) RPG Battle")
        print("15) Quit")

        choice = input("Choose a game: ")

        if choice == "1": hangman()
        elif choice == "2": number_guess()
        elif choice == "3": rps()
        elif choice == "4": stickman_dodge()
        elif choice == "5": tic_tac_toe()
        elif choice == "6": emoji_quiz()
        elif choice == "7": higher_lower()
        elif choice == "8": math_quiz()
        elif choice == "9": word_scramble()
        elif choice == "10": memory_match()
        elif choice == "11": snake_game()
        elif choice == "12": sliding_puzzle()
        elif choice == "13": guess_song()
        elif choice == "14": rpg_battle()
        elif choice == "15":
            print("👋 Thanks for playing!")
            break
        else:
            print("⚠️ Invalid choice.")

main()