import random
import time

CHALLENGES = [
    {
        "text": "Find all prime numbers between 1 and 100.",
        "answer": [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
                   53, 59, 61, 67, 71, 73, 79, 83, 89, 97],
        "seconds": 60,
    },
    {
        "text": "What is the sum of all numbers from 1 to 100?",
        "answer": [5050],
        "seconds": 30,
    },
    {
        "text": "What is the factorial of 6?",
        "answer": [720],
        "seconds": 30,
    },
    {
        "text": "Find all even numbers between 1 and 30.",
        "answer": [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30],
        "seconds": 45,
    },
    {
        "text": "Find all numbers between 1 and 50 divisible by 7.",
        "answer": [7, 14, 21, 28, 35, 42, 49],
        "seconds": 30,
    },
    {
        "text": "What is the sum of all even numbers from 1 to 100?",
        "answer": [2550],
        "seconds": 30,
    },
    {
        "text": "What is 2 to the power of 10?",
        "answer": [1024],
        "seconds": 20,
    },
    {
        "text": "Find the first 10 Fibonacci numbers (starting with 1, 1).",
        "answer": [1, 1, 2, 3, 5, 8, 13, 21, 34, 55],
        "seconds": 45,
    },
    {
        "text": "Find all perfect squares between 1 and 100.",
        "answer": [1, 4, 9, 16, 25, 36, 49, 64, 81, 100],
        "seconds": 45,
    },
    {
        "text": "What is the sum of the digits of 98765?",
        "answer": [35],
        "seconds": 20,
    },
    {
        "text": "Find all divisors of 36.",
        "answer": [1, 2, 3, 4, 6, 9, 12, 18, 36],
        "seconds": 45,
    },
]


def parse_answer(raw):
    """Pretvara unos '2, 3, 5' u listu brojeva [2, 3, 5]."""
    parts = raw.replace(",", " ").split()
    return sorted(int(p) for p in parts)


def run():
    challenge = random.choice(CHALLENGES)
    print("\nYour challenge:\n")
    print(challenge["text"])
    print(f"\nYou have {challenge['seconds']} seconds!")
    print("(Separate numbers with commas or spaces)\n")

    start = time.time()
    raw = input("Enter your answer:\n> ")
    elapsed = time.time() - start

    if elapsed > challenge["seconds"]:
        print(f"Too slow! You took {elapsed:.1f}s.")
        return

    try:
        user_answer = parse_answer(raw)
    except ValueError:
        print("Invalid input. Please enter only numbers.")
        return

    if user_answer == challenge["answer"]:
        print(f"Correct! Solved in {elapsed:.1f}s.")
    else:
        correct = set(challenge["answer"])
        given = set(user_answer)
        missing = sorted(correct - given)
        extra = sorted(given - correct)
        print("Wrong answer.")
        if missing:
            print(f"Missing: {missing}")
        if extra:
            print(f"Not correct: {extra}")
