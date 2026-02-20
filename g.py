import random
import time
import os

# ============================================================
# GLOBAL DATA BANKS (Expanded for 36+ Games)
# ============================================================
WORDS = ["algorithm", "binary", "cipher", "database", "encryption", "firewall", "hardware", "interface", "protocol", "quantum", "software", "terminal", "velocity", "starlight", "horizon", "labyrinth", "cryptic", "nebula", "avalanche", "gladiator", "obsidian", "voyage", "phantom", "circuit", "gravity", "telescope", "microscope", "keyboard", "silicon", "asteroid", "nebula", "atmosphere", "metropolis", "synchronize", "bandwidth"]

TRIVIA = {
    "Largest ocean?": "pacific", "Capital of Italy?": "rome", "Gas plants absorb?": "carbon dioxide", 
    "Who painted Mona Lisa?": "da vinci", "Square root of 144?": "12", "Red Planet?": "mars", 
    "Continents?": "7", "Hardest substance?": "diamond", "Largest desert?": "antarctica", 
    "First man on moon?": "armstrong", "Chemical symbol for Gold?": "au", "Fastest bird?": "peregrine falcon",
    "Company that made Java?": "sun", "Smallest country?": "vatican", "Hottest planet?": "venus"
}

RIDDLES = {
    "Broken before use?": "egg", "Face and two hands?": "clock", "Wetter as it dries?": "towel", 
    "Keys but no locks?": "piano", "More of it, less you see?": "darkness", "Goes up but never down?": "age", 
    "Has an eye but cannot see?": "needle", "Has a neck but no head?": "bottle", "The more you take, the more you leave behind?": "footsteps"
}

# ============================================================
# UTILITIES
# ============================================================
def slow_print(text, speed=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(speed)
    print()

def safe_input(prompt, type_=str):
    while True:
        try:
            val = input(prompt).strip()
            if not val: continue
            return type_(val)
        except:
            print("⚠️ Invalid format.")
# --- CLASSIC LOGIC ---
def hangman():
    word = random.choice(WORDS); guessed = set(); wrong = 0
    while wrong < 6:
        display = " ".join([c if c in guessed else "_" for c in word])
        print(f"\n❌ Fails: {wrong}/6 | {display}")
        if all(c in guessed for c in word): print("🎉 You Win!"); return
        g = input("Guess: ").lower()
        if g not in guessed:
            guessed.add(g)
            if g not in word: wrong += 1
    print(f"💀 Lost! Word was: {word}")

def tic_tac_toe():
    board = [" "] * 9
    def show(): print(f"\n {board[0]}|{board[1]}|{board[2]}\n-+-+-\n {board[3]}|{board[4]}|{board[5]}\n-+-+-\n {board[6]}|{board[7]}|{board[8]}")
    for i in range(9):
        show()
        if i % 2 == 0:
            m = safe_input("Spot (1-9): ", int) - 1
            if board[m] == " ": board[m] = "X"
            else: continue
        else:
            board[random.choice([i for i in range(9) if board[i]==" "])] = "O"
    show(); print("Game Over!")

# --- ARCADE LOGIC ---
def stickman_dodge():
    pos, score = 2, 0
    while score < 15:
        rock = random.randint(1, 3)
        print(f"\nScore: {score} | Rock coming to Lane {rock}!")
        m = input("Move (a/d): ").lower()
        if m == 'a' and pos > 1: pos -= 1
        elif m == 'd' and pos < 3: pos += 1
        if pos == rock: print("💥 Hit!"); return
        score += 1
    print("🏆 Ultimate Survivor!")

# --- CASINO LOGIC ---
def blackjack():
    p, c = random.randint(10, 21), random.randint(10, 21)
    print(f"🃏 You: {p}, Dealer: {c}")
    if p > c: print("💰 Win!")
    elif p == c: print("🤝 Push!")
    else: print("💸 Lose!")

def slots():
    syms = ["🍒", "💎", "7️⃣", "🍀", "🔔"]
    r = [random.choice(syms) for _ in range(3)]
    print(f"🎰 | {' | '.join(r)} |")
    if r[0] == r[1] == r[2]: print("🔥 JACKPOT!")
    elif r[0] == r[1] or r[1] == r[2]: print("✨ Minor Win!")
    else: print("❌ No luck.")
def main():
    while True:
        print("\n" + "="*40)
        print("🎮 THE MEGA PYTHON ARCADE (36+ MODES) 🎮")
        print("="*40)
        print("1) Classic  2) Arcade  3) Puzzle  4) Quiz  5) Casino  6) Chill  7) Quit")
        cat = input("Select Category: ")

        if cat == "1":
            print("\n1)Hangman 2)NumberGuess 3)RPS 4)TicTacToe 5)SpinBottle 6)CoinFlip")
            g = input("> ")
            if g=="1": hangman()
            elif g=="2": 
                n = random.randint(1,20); 
                if safe_input("Guess (1-20): ", int) == n: print("✅")
            elif g=="3": print(f"CPU: {random.choice(['Rock','Paper','Scissors'])}")
            elif g=="4": tic_tac_toe()
            elif g=="5": print(f"Points at: {random.choice(['You', 'Friend', 'The Wall'])}")
            elif g=="6": print(f"Result: {random.choice(['Heads', 'Tails'])}")

        elif cat == "2":
            print("\n1)Stickman 2)Reaction 3)Snake 4)Typing 5)ColorMatch 6)ReflexClick")
            g = input("> ")
            if g=="1": stickman_dodge()
            elif g=="2":
                print("Wait..."); time.sleep(random.randint(2,4)); start=time.time()
                input("!!! GO !!!"); print(f"{round(time.time()-start, 3)}s")
            elif g=="3": 
                spos = 5; food = random.randint(0,9)
                for _ in range(5):
                    grid = ["_"]*10; grid[food]="A"; grid[spos]="S"
                    print("".join(grid)); m = input("a/d: "); 
                    if m=='a': spos-=1 
                    else: spos+=1
            elif g=="4":
                w = random.choice(WORDS); print(f"Type: {w}")
                if input("> ") == w: print("Perfect!")
            elif g=="5":
                colors = ["Red", "Blue", "Green"]; t = random.choice(colors)
                if input(f"Type the color {t}: ").capitalize() == t: print("✅")
            elif g=="6":
                print("Click when you see '!'"); time.sleep(1.5); print("!"); input(); print("Nice!")

        elif cat == "3":
            print("\n1)Scramble 2)MathBlitz 3)LogicGate 4)Pattern 5)Anagram 6)Memory")
            g = input("> ")
            if g=="1":
                w = random.choice(WORDS); s = "".join(random.sample(w, len(w)))
                print(f"Unscramble: {s}"); 
                if input("> ") == w: print("✅")
            elif g=="2":
                a,b = random.randint(1,12), random.randint(1,12)
                if safe_input(f"{a}x{b}= ", int) == a*b: print("Smart!")
            elif g=="3":
                print("OR Gate: If A=True and B=False, result? (t/f)"); 
                if input("> ").lower() == 't': print("✅")
            elif g=="4":
                print("1, 2, 4, 8, ?"); 
                if input("> ") == "16": print("✅")
            elif g=="5":
                print("Listen = ? (Anagram of Listen)"); 
                if input("> ").lower() == "silent": print("✅")
            elif g=="6":
                code = random.randint(1000,9999); print(f"Remember: {code}"); time.sleep(2); print("\n"*50)
                if safe_input("Code? ", int) == code: print("✅")

        elif cat == "4":
            print("\n1)Trivia 2)Riddles 3)True/False 4)Geography 5)Science 6)Facts")
            g = input("> ")
            if g=="1":
                q,a = random.choice(list(TRIVIA.items()))
                if input(f"{q}: ").lower() == a: print("✅")
            elif g=="2":
                q,a = random.choice(list(RIDDLES.items()))
                if input(f"{q}: ").lower() == a: print("✅")
            elif g=="3":
                print("Is Python named after the snake? (y/n)"); 
                if input("> ").lower() == 'n': print("Correct! (Named after Monty Python)")
            elif g=="4":
                print("Which country is the Nile in?"); 
                if input("> ").lower() == "egypt": print("✅")
            elif g=="5":
                print("H2O is the formula for?"); 
                if input("> ").lower() == "water": print("✅")
            elif g=="6": print(f"Fact: {random.choice(['Honey never spoils', 'Bananas are berries'])}")

        elif cat == "5":
            print("\n1)Blackjack 2)Slots 3)Dice 4)Roulette 5)HorseRace 6)Hi-Lo")
            g = input("> ")
            if g=="1": blackjack()
            elif g=="2": slots()
            elif g=="3": print(f"Rolled: {random.randint(1,6)}")
            elif g=="4": print(f"Land on: {random.randint(0,36)} {'Red' if random.random()>0.5 else 'Black'}")
            elif g=="5": print(f"Winner: Horse #{random.randint(1,5)}")
            elif g=="6":
                n1 = random.randint(1,10); print(f"Current: {n1}")
                if input("Higher or Lower (h/l)? ") == ('h' if random.randint(1,10)>n1 else 'l'): print("Win!")

        elif cat == "6":
            print("\n1)Garden 2)Zen 3)ASMR 4)PetCare 5)CloudWatch 6)StarGaze")
            g = input("> ")
            if g=="1": print("Growing..."); time.sleep(1); print("🌻 Done!")
            elif g=="2": print("Breathe in... Breathe out..."); time.sleep(2)
            elif g=="3": print("Listening to rain sounds... 🌧️")
            elif g=="4": print("The dog is happy! 🐶")
            elif g=="5": print(f"You see a {random.choice(['Dino', 'Car', 'Hat'])} shaped cloud.")
            elif g=="6": print(f"You spotted the {random.choice(['North Star', 'Orion', 'Big Dipper'])}!")

        elif cat == "7": break

if __name__ == "__main__":
    main()