import random


WORDS = ["python", "github", "keyboard", "monitor", "network"]

HANGMAN_STAGES = [
    """
       -----
       |   |
           |
           |
           |
           |
    =========
    """,
    """
       -----
       |   |
       O   |
           |
           |
           |
    =========
    """,
    """
       -----
       |   |
       O   |
       |   |
           |
           |
    =========
    """,
    """
       -----
       |   |
       O   |
      /|   |
           |
           |
    =========
    """,
    """
       -----
       |   |
       O   |
      /|\\  |
           |
           |
    =========
    """,
    """
       -----
       |   |
       O   |
      /|\\  |
      /    |
           |
    =========
    """,
    """
       -----
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    =========
    """,
]

MAX_WRONG = 6


def get_display_word(word, guessed_letters):
    """Return the word with unguessed letters hidden as underscores."""
    return " ".join(letter if letter in guessed_letters else "_" for letter in word)


def play_game():
    word = random.choice(WORDS)
    guessed_letters = set()
    wrong_guesses = 0

    print("\n=============================")
    print("       HANGMAN GAME")
    print("=============================")
    print(f"The word has {len(word)} letters.\n")

    while wrong_guesses < MAX_WRONG:
        print(HANGMAN_STAGES[wrong_guesses])
        print(f"Word: {get_display_word(word, guessed_letters)}")
        print(f"Wrong guesses left: {MAX_WRONG - wrong_guesses}")

        if guessed_letters:
            print(f"Letters guessed: {', '.join(sorted(guessed_letters))}")

        # Check win condition
        if all(letter in guessed_letters for letter in word):
            print(f"\n✅ You won! The word was: {word.upper()}")
            return True

        # Get input
        guess = input("\nGuess a letter: ").strip().lower()

        if len(guess) != 1 or not guess.isalpha():
            print("⚠  Please enter a single letter.")
            continue

        if guess in guessed_letters:
            print(f"⚠  You already guessed '{guess}'. Try a different letter.")
            continue

        guessed_letters.add(guess)

        if guess in word:
            print(f"✅ '{guess}' is in the word!")
        else:
            wrong_guesses += 1
            print(f"❌ '{guess}' is NOT in the word.")

    # Game over - show final stage
    print(HANGMAN_STAGES[wrong_guesses])
    print(f"\n💀 Game over! The word was: {word.upper()}")
    return False


def main():
    while True:
        play_game()
        again = input("\nPlay again? (yes/no): ").strip().lower()
        if again not in ("yes", "y"):
            print("\nThanks for playing. Goodbye!\n")
            break


if __name__ == "__main__":
    main()
