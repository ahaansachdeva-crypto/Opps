import random
import time

# 🎉 Welcome message
print("🔥 Welcome to the Ultimate Math Challenge! 🔥")
print("Answer as fast as you can ⏱️😎\n")

score = 0
questions = 5  # number of questions

start_time = time.time()  # Start timer

for i in range(questions):
    # Generate random numbers and operator
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    operator = random.choice(["+", "-", "*"])

    # Calculate correct answer
    if operator == "+":
        correct = num1 + num2
    elif operator == "-":
        correct = num1 - num2
    else:
        correct = num1 * num2

    # Ask question
    print(f"🧮 Question {i+1}: What is {num1} {operator} {num2}?")
    user_answer = int(input("👉 Your answer: "))

    # Check answer
    if user_answer == correct:
        print("✅ Correct! You're on fire! 🔥\n")
        score += 1
    else:
        print(f"❌ Oops! The right answer was {correct} 😅\n")

end_time = time.time()  # End timer
total_time = round(end_time - start_time, 2)

# 🎉 Final results
print("🎯 Quiz Complete!")
print(f"🏆 Your Score: {score}/{questions}")
print(f"⏱️ Total Time: {total_time} seconds")
print("🤖 Thanks for playing! Come back for more brain gains 💪🧠")
