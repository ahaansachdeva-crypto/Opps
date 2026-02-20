import random
import time

# ============================================================
# GLOBAL DATA BANKS (Expanded for Variety)
# ============================================================

WORDS = [
    "python", "castle", "dragon", "stickman", "galaxy", "computer", "adventure",
    "mystery", "puzzle", "science", "planet", "wizard", "forest", "island",
    "treasure", "robot", "spaceship", "volcano", "algorithm", "binary",
    "encryption", "nebula", "starlight", "avalanche", "gladiator", "horizon",
    "telescope", "microscope", "keyboard", "software", "circuit", "gravity"
]

TRIVIA_DATA = {
    "What planet is known as the Red Planet?": "mars",
    "What is the capital of France?": "paris",
    "What is the largest mammal?": "blue whale",
    "Who painted the Mona Lisa?": "da vinci",
    "What is the square root of 64?": "8",
    "Which gas do plants absorb?": "carbon dioxide",
    "How many continents are there?": "7",
    "What is the hardest natural substance?": "diamond"
}

RIDDLES_DATA = {
    "What has to be broken before you use it?": "egg",
    "What has a face and two hands?": "clock",
    "The more of this there is, the less you see.": "darkness",
    "What gets wetter as it dries?": "towel",
    "What has keys but no locks?": "piano"
}

# ============================================================
# UTILITIES
# ============================================================

def safe_input(prompt, type_=str):
    while True:
        try:
            val = input(prompt).strip()
            if not val: continue
            return type_(val)
        except ValueError:
            print(f"⚠️ Invalid input. Please enter a {type_.__name__}.")

# ============================================================
# CLASSIC GAMES
# ============================================================

def hangman():
    print("\n🎯 === HANGMAN === 🎯")
    word = random.choice(WORDS)
    guessed, wrong, max_wrong = set(), 0, 6
    while True:
        display = " ".join([c if c in guessed else "_" for c in word])
        print(f"\n❌ Fails: {wrong}/{max_wrong} | Word: {display}")
        if all(c in guessed for c in word):
            print("🎉 You win!"); break
        if wrong >= max_wrong:
            print(f"💀 Lost! The word was: {word}"); break
        guess = safe_input("Guess a letter: ").lower()
        if len(guess) != 1 or not guess.isalpha() or guess in guessed: continue
        guessed.add(guess)
        if guess not in word: wrong += 1

def number_guess():
    print("\n🔢 === NUMBER GUESSING === 🔢")
    number = random.randint(1, 100)
    while True:
        guess = safe_input("Guess 1-100: ", int)
        if guess < number: print("⬆️ Higher!")
        elif guess > number: print("⬇️ Lower!")
        else: print("🎉 Correct!"); break

def rps():
    print("\n✊ === ROCK PAPER SCISSORS === ✋")
    choices = ["rock", "paper", "scissors"]
    while True:
        p = safe_input("Choose rock, paper, or scissors: ").lower()
        if p not in choices: continue
        cpu = random.choice(choices)
        print(f"CPU chose: {cpu}")
        if p == cpu: print("🤝 Tie!")
        elif (p == "rock" and cpu == "scissors") or (p == "paper" and cpu == "rock") or (p == "scissors" and cpu == "paper"):
            print("🏆 You win!")
        else: print("💀 You lose!")
        if safe_input("Play again? (y/n): ").lower() != 'y': break

def tic_tac_toe():
    print("\n⭕ === TIC TAC TOE === ❌")
    board = [" "] * 9
    def show():
        print(f"\n {board[0]} | {board[1]} | {board[2]} \n---+---+---\n {board[3]} | {board[4]} | {board[5]} \n---+---+---\n {board[6]} | {board[7]} | {board[8]}")
    def check(p):
        w = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        return any(board[a] == board[b] == board[c] == p for a,b,c in w)
    while True:
        show()
        move = safe_input("Choose spot (1-9): ", int) - 1
        if not (0 <= move <= 8) or board[move] != " ": continue
        board[move] = "X"
        if check("X"): show(); print("🏆 You win!"); break
        if " " not in board: show(); print("🤝 Tie!"); break
        cpu = random.choice([i for i in range(9) if board[i] == " "])
        board[cpu] = "O"
        if check("O"): show(); print("💀 CPU wins!"); break

def stickman_dodge():
    print("\n🏃 === STICKMAN DODGE === 🪨")
    pos, score = 2, 0
    while True:
        rock = random.randint(1, 3)
        view = [" ", " ", " "]; view[pos-1] = "🙂"
        print(f"\nScore: {score} | Rock Lane: {rock}\n|" + "|".join(view) + "|")
        move = safe_input("Move (a/d/stay): ").lower()
        if move == 'a' and pos > 1: pos -= 1
        elif move == 'd' and pos < 3: pos += 1
        if pos == rock: print("💥 Hit!"); break
        score += 1

# ============================================================
# ARCADE GAMES
# ============================================================

def memory_sequence():
    seq = "".join([str(random.randint(1, 9)) for _ in range(5)])
    print(f"\n🧠 Remember: {seq}"); time.sleep(2)
    print("\n" * 50)
    guess = safe_input("Sequence: ")
    print("🎉 Correct!" if guess == seq else f"❌ It was {seq}")

def reaction_timer():
    print("\n⚡ Wait for GO..."); time.sleep(random.uniform(2, 4))
    start = time.time()
    safe_input("GO! (Press Enter)")
    print(f"⏱️ Time: {round(time.time() - start, 4)}s")

def typing_test():
    word = random.choice(WORDS)
    print(f"\n⌨️ Type fast: {word}")
    start = time.time()
    if safe_input("> ") == word:
        print(f"⏱️ Time: {round(time.time() - start, 2)}s")
    else: print("❌ Incorrect!")

# ============================================================
# PUZZLE & QUIZ
# ============================================================

def word_scramble():
    word = random.choice(WORDS)
    scrambled = "".join(random.sample(word, len(word)))
    print(f"\n🔀 Unscramble: {scrambled}")
    if safe_input("Guess: ").lower() == word: print("🎉 Correct!")
    else: print(f"❌ It was {word}")

def trivia_quiz():
    q, a = random.choice(list(TRIVIA_DATA.items()))
    if safe_input(f"\n❓ {q}: ").lower() == a: print("✅ Correct!")
    else: print(f"❌ No, it was {a}")

# ============================================================
# CASINO GAMES
# ============================================================

def blackjack():
    p, c = random.randint(2, 21), random.randint(2, 21)
    while p < 21:
        print(f"\nYour total: {p}")
        if safe_input("Hit or Stand? (h/s): ").lower() == 'h': p += random.randint(1, 11)
        else: break
    print(f"You: {p}, CPU: {c}")
    if p <= 21 and (p > c or c > 21): print("🏆 You win!")
    else: print("💀 You lose!")

# ============================================================
# CHILL GAMES (New Category)
# ============================================================

def digital_garden():
    print("\n🌿 === DIGITAL GARDEN === 🌿")
    h, health = 1, 100
    while health > 0:
        print(f"\nPlant: {h}cm | Health: {health}%")
        act = safe_input("Action (water/sun/quit): ").lower()
        if act == "water": h += 2; health = min(100, health + 10)
        elif act == "sun": h += 1; health += 5
        elif act == "quit": break
        if h >= 15: print("🌻 A beautiful flower bloomed!"); break

def zen_breathing():
    print("\n🌬️  Relax...")
    for _ in range(3):
        print("Breathe in..."); time.sleep(3)
        print("Hold..."); time.sleep(2)
        print("Breathe out..."); time.sleep(4)
    print("✨ Peace.")

# ============================================================
# MAIN MENU
# ============================================================



def main():
    while True:
        print("\n🎮 === THE ULTIMATE PYTHON ARCADE === 🎮")
        print("1) Classic  2) Arcade  3) Puzzle  4) Quiz  5) Casino  6) Chill  7) Quit")
        cat = safe_input("Select Category (1-7): ")

        if cat == "1":
            print("\n1) Hangman 2) Numbers 3) RPS 4) TicTacToe 5) Stickman 6) Back")
            g = safe_input("> ")
            if g == "1": hangman()
            elif g == "2": number_guess()
            elif g == "3": rps()
            elif g == "4": tic_tac_toe()
            elif g == "5": stickman_dodge()

        elif cat == "2":
            print("\n1) Memory 2) Reaction 3) Typing 4) Back")
            g = safe_input("> ")
            if g == "1": memory_sequence()
            elif g == "2": reaction_timer()
            elif g == "3": typing_test()

        elif cat == "3":
            word_scramble()

        elif cat == "4":
            print("\n1) Trivia 2) Riddles 3) Back")
            g = safe_input("> ")
            if g == "1": trivia_quiz()
            elif g == "2":
                q, a = random.choice(list(RIDDLES_DATA.items()))
                if safe_input(f"\n🧠 {q}: ").lower() == a: print("✅")

        elif cat == "5":
            blackjack()

        elif cat == "6":
            print("\n1) Garden 2) Zen 3) Back")
            g = safe_input("> ")
            if g == "1": digital_garden()
            elif g == "2": zen_breathing()

        elif cat == "7":
            print("👋 Goodbye!"); break

if __name__ == "__main__":
    main()
