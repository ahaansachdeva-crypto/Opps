import random
import time

# ============================================================
# CLASSIC GAMES
# ============================================================

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


# ============================================================
# ARCADE GAMES
# ============================================================

def coin_flip():
    print("\n🪙 === COIN FLIP === 🪙")
    guess = input("Heads or Tails? ").lower()
    result = random.choice(["heads", "tails"])
    print("Coin landed on:", result)
    print("🎉 You win!" if guess == result else "❌ You lose!")


def dice_roll():
    print("\n🎲 === DICE ROLL === 🎲")
    input("Press Enter to roll...")
    print("You rolled:", random.randint(1, 6))


def higher_lower():
    print("\n🔼 === HIGHER OR LOWER === 🔽")
    num = random.randint(1, 20)
    print("Starting number:", num)
    guess = input("Will the next number be higher or lower? (h/l): ").lower()
    next_num = random.randint(1, 20)
    print("Next number:", next_num)

    if (guess == "h" and next_num > num) or (guess == "l" and next_num < num):
        print("🎉 Correct!")
    else:
        print("❌ Wrong!")


def reaction_timer():
    print("\n⚡ === REACTION TIMER === ⚡")
    print("Wait for GO...")
    time.sleep(random.uniform(1, 3))
    start = time.time()
    input("GO! Press Enter!")
    end = time.time()
    print("Your reaction time:", round(end - start, 3), "seconds")


def memory_sequence():
    print("\n🧠 === MEMORY SEQUENCE === 🧠")
    seq = [random.randint(1, 9) for _ in range(5)]
    print("Remember this sequence:", seq)
    time.sleep(2)
    print("\n" * 50)
    guess = input("Enter the sequence (no spaces): ")
    print("🎉 Correct!" if guess == "".join(map(str, seq)) else "❌ Wrong!")


def typing_test():
    print("\n⌨️ === TYPING TEST === ⌨️")
    word = random.choice(["python", "galaxy", "wizard", "volcano"])
    print("Type this word:", word)
    start = time.time()
    typed = input("Your input: ")
    end = time.time()

    if typed == word:
        print("⏱️ Time:", round(end - start, 2), "seconds")
    else:
        print("❌ Incorrect typing!")


# ============================================================
# PUZZLE GAMES
# ============================================================

def word_scramble():
    print("\n🔀 === WORD SCRAMBLE === 🔀")
    words = ["python", "castle", "dragon", "forest", "wizard", "planet"]
    word = random.choice(words)
    scrambled = "".join(random.sample(word, len(word)))
    print("Scrambled word:", scrambled)
    guess = input("Your guess: ").lower()
    print("🎉 Correct!" if guess == word else "❌ Wrong! The word was " + word)


def anagram_game():
    print("\n🧩 === ANAGRAM GAME === 🧩")
    words = ["listen", "earth", "finder", "silent", "heart", "friend"]
    word = random.choice(words)
    scrambled = "".join(random.sample(word, len(word)))
    print("Scrambled:", scrambled)
    guess = input("Your guess: ")
    print("🎉 Correct!" if guess == word else "❌ Wrong!")


def pattern_game():
    print("\n🔢 === PATTERN GAME === 🔢")
    seq = [2, 4, 6, 8]
    print("Sequence:", seq)
    guess = input("Next number: ")
    print("🎉 Correct!" if guess == "10" else "❌ Wrong!")


# ============================================================
# QUIZ GAMES
# ============================================================

def math_quiz():
    print("\n➗ === MATH QUIZ === ✖️")
    a, b = random.randint(1, 10), random.randint(1, 10)
    print(f"What is {a} + {b}?")
    guess = input("Answer: ")

    if guess.isdigit() and int(guess) == a + b:
        print("🎉 Correct!")
    else:
        print("❌ Wrong!")


def guess_emoji():
    print("\n😊 === GUESS THE EMOJI === 🤯")
    emojis = {"😀": "happy", "😡": "angry", "😢": "sad", "😴": "sleepy"}
    emoji, meaning = random.choice(list(emojis.items()))
    print("Emoji:", emoji)
    guess = input("Meaning: ").lower()
    print("🎉 Correct!" if guess == meaning else "❌ Wrong!")


def even_odd():
    print("\n🔢 === EVEN OR ODD === 🔢")
    num = random.randint(1, 50)
    print("Number:", num)
    guess = input("Even or Odd? ").lower()
    correct = "even" if num % 2 == 0 else "odd"
    print("🎉 Correct!" if guess == correct else "❌ Wrong!")


def prime_checker():
    print("\n🔍 === PRIME CHECKER === 🔍")
    num = random.randint(2, 50)
    print("Number:", num)

    guess = input("Is it prime? (y/n): ").lower()

    def is_prime(n):
        return all(n % i for i in range(2, int(n**0.5) + 1))

    correct = is_prime(num)
    print("🎉 Correct!" if (guess == "y") == correct else "❌ Wrong!")


def trivia_quiz():
    print("\n❓ === TRIVIA QUIZ === ❓")
    q = {
        "What planet do we live on? ": "earth",
        "What is 2+2? ": "4",
        "What color is the sky? ": "blue"
    }
    question, answer = random.choice(list(q.items()))
    guess = input(question).lower()
    print("🎉 Correct!" if guess == answer else "❌ Wrong!")


def morse_game():
    print("\n📡 === MORSE CODE GAME === 📡")
    morse = {".-": "a", "-...": "b", "-.-.": "c"}
    code, letter = random.choice(list(morse.items()))
    print("Morse code:", code)
    guess = input("Letter: ").lower()
    print("🎉 Correct!" if guess == letter else "❌ Wrong!")


def capital_quiz():
    print("\n🌍 === CAPITAL QUIZ === 🌍")
    data = {"france": "paris", "japan": "tokyo", "egypt": "cairo"}
    country, capital = random.choice(list(data.items()))
    guess = input(f"Capital of {country}: ").lower()
    print("🎉 Correct!" if guess == capital else "❌ Wrong!")


def riddle_game():
    print("\n🧠 === RIDDLE GAME === 🧠")
    r = {
        "What has to be broken before you use it? ": "egg",
        "What has a face and two hands? ": "clock"
    }
    question, answer = random.choice(list(r.items()))
    guess = input(question).lower()
    print("🎉 Correct!" if guess == answer else "❌ Wrong!")


# ============================================================
# CASINO GAMES
# ============================================================

def blackjack():
    print("\n🃏 === BLACKJACK === 🃏")

    def draw():
        return random.randint(1, 11)

    player = draw() + draw()
    cpu = draw() + draw()

    print("Your total:", player)

    while player < 21:
        move = input("Hit or Stand? (h/s): ").lower()
        if move == "h":
            player += draw()
            print("New total:", player)
        else:
            break

    print("CPU total:", cpu)

    if player > 21:
        print("💀 Bust! CPU wins!")
    elif cpu > 21 or player > cpu:
        print("🎉 You win!")
    else:
        print("💀 CPU wins!")


def poker():
    print("\n🃏 === POKER (5-CARD DRAW) === 🃏")

    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    suits = ["♠", "♥", "♦", "♣"]

    deck = [r + s for r in ranks for s in suits]
    random.shuffle(deck)

    def card_value(card):
        return ranks.index(card[:-1])

    def deal_hand(n=5):
        hand = deck[:n]
        del deck[:n]
        return hand

    def is_flush(hand):
        return len({c[-1] for c in hand}) == 1

    def is_straight(values):
        values = sorted(values)
        # A-2-3-4-5
        if values == [0, 1, 2, 3, 12]:
            return True, 3
        for i in range(4):
            if values[i+1] - values[i] != 1:
                return False, max(values)
        return True, max(values)

    def classify(hand):
        values = [card_value(c) for c in hand]
        counts = {}
        for v in values:
            counts[v] = counts.get(v, 0) + 1
        count_vals = sorted(counts.values(), reverse=True)
        unique_vals = sorted(counts.keys(), key=lambda x: (-counts[x], -x))

        flush = is_flush(hand)
        straight, high_straight = is_straight(values)

        # Straight flush
        if flush and straight:
            return (8, high_straight, unique_vals)
        # Four of a kind
        if count_vals == [4, 1]:
            return (7, unique_vals, [])
        # Full house
        if count_vals == [3, 2]:
            return (6, unique_vals, [])
        # Flush
        if flush:
            return (5, sorted(values, reverse=True), [])
        # Straight
        if straight:
            return (4, high_straight, [])
        # Three of a kind
        if count_vals == [3, 1, 1]:
            return (3, unique_vals, [])
        # Two pair
        if count_vals == [2, 2, 1]:
            return (2, unique_vals, [])
        # One pair
        if count_vals == [2, 1, 1, 1]:
            return (1, unique_vals, [])
        # High card
        return (0, sorted(values, reverse=True), [])

    def hand_name(rank_tuple):
        rank = rank_tuple[0]
        names = [
            "High Card", "One Pair", "Two Pair", "Three of a Kind",
            "Straight", "Flush", "Full House", "Four of a Kind",
            "Straight Flush"
        ]
        return names[rank]

    # Deal initial hands
    player_hand = deal_hand()
    cpu_hand = deal_hand()

    print("\nYour hand:")
    print(" ".join(player_hand))

    # Player draw phase
    change = input("Enter card positions to replace (1-5, space-separated), or press Enter to keep: ").strip()
    if change:
        positions = []
        for x in change.split():
            if x.isdigit() and 1 <= int(x) <= 5:
                positions.append(int(x) - 1)
        positions = sorted(set(positions))
        for pos in positions:
            if deck:
                player_hand[pos] = deck.pop(0)

    # Simple CPU strategy: replace up to 3 random cards
    cpu_replace_count = random.randint(0, 3)
    cpu_positions = random.sample(range(5), cpu_replace_count)
    for pos in cpu_positions:
        if deck:
            cpu_hand[pos] = deck.pop(0)

    print("\nFinal hands:")
    print("Your hand: ", " ".join(player_hand))
    print("CPU hand:  ", " ".join(cpu_hand))

    player_rank = classify(player_hand)
    cpu_rank = classify(cpu_hand)

    print("\nYour hand is:", hand_name(player_rank))
    print("CPU hand is:", hand_name(cpu_rank))

    if player_rank > cpu_rank:
        print("🏆 You win!")
    elif player_rank < cpu_rank:
        print("💀 CPU wins!")
    else:
        print("🤝 It's a tie!")


# ============================================================
# UTILITY / EXTRA
# ============================================================

def password_cracker():
    print("\n🔐 === PASSWORD CRACKER === 🔐")
    password = random.randint(100, 999)
    print("Cracking password...")
    for i in range(100, 1000):
        if i == password:
            print("Password found:", i)
            break


# ============================================================
# MAIN MENU
# ============================================================

def main():
    while True:
        print("\n🎮 === PYTHON GAME HUB === 🎮")
        print("Choose a category:")
        print("1) Classic Games")
        print("2) Arcade Games")
        print("3) Puzzle Games")
        print("4) Quiz Games")
        print("5) Casino Games")
        print("6) Extra")
        print("7) Quit")

        cat = input("Category: ")

        if cat == "1":
            print("\n=== CLASSIC GAMES ===")
            print("1) Hangman")
            print("2) Number Guessing")
            print("3) Rock Paper Scissors")
            print("4) Tic Tac Toe")
            print("5) Stickman Dodge")
            print("6) Emoji Quiz")
            print("7) Back")
            choice = input("Choose a game: ")
            if choice == "1": hangman()
            elif choice == "2": number_guess()
            elif choice == "3": rps()
            elif choice == "4": tic_tac_toe()
            elif choice == "5": stickman_dodge()
            elif choice == "6": emoji_quiz()

        elif cat == "2":
            print("\n=== ARCADE GAMES ===")
            print("1) Coin Flip")
            print("2) Dice Roll")
            print("3) Higher or Lower")
            print("4) Reaction Timer")
            print("5) Memory Sequence")
            print("6) Typing Test")
            print("7) Back")
            choice = input("Choose a game: ")
            if choice == "1": coin_flip()
            elif choice == "2": dice_roll()
            elif choice == "3": higher_lower()
            elif choice == "4": reaction_timer()
            elif choice == "5": memory_sequence()
            elif choice == "6": typing_test()

        elif cat == "3":
            print("\n=== PUZZLE GAMES ===")
            print("1) Word Scramble")
            print("2) Anagram Game")
            print("3) Pattern Game")
            print("4) Back")
            choice = input("Choose a game: ")
            if choice == "1": word_scramble()
            elif choice == "2": anagram_game()
            elif choice == "3": pattern_game()

        elif cat == "4":
            print("\n=== QUIZ GAMES ===")
            print("1) Math Quiz")
            print("2) Guess the Emoji")
            print("3) Even or Odd")
            print("4) Prime Checker")
            print("5) Trivia Quiz")
            print("6) Morse Code Game")
            print("7) Capital Quiz")
            print("8) Riddle Game")
            print("9) Back")
            choice = input("Choose a game: ")
            if choice == "1": math_quiz()
            elif choice == "2": guess_emoji()
            elif choice == "3": even_odd()
            elif choice == "4": prime_checker()
            elif choice == "5": trivia_quiz()
            elif choice == "6": morse_game()
            elif choice == "7": capital_quiz()
            elif choice == "8": riddle_game()

        elif cat == "5":
            print("\n=== CASINO GAMES ===")
            print("1) Blackjack")
            print("2) Poker (5-Card Draw)")
            print("3) Back")
            choice = input("Choose a game: ")
            if choice == "1": blackjack()
            elif choice == "2": poker()

        elif cat == "6":
            print("\n=== EXTRA ===")
            print("1) Password Cracker Simulation")
            print("2) Back")
            choice = input("Choose an option: ")
            if choice == "1": password_cracker()

        elif cat == "7":
            print("👋 Thanks for playing!")
            break
        else:
            print("⚠️ Invalid choice.")

if __name__ == "__main__":
    main()