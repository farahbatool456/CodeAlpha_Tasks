# Hangman Game 🎮

A simple text-based Hangman game built in Python. Guess the hidden word one letter at a time before the hangman is complete.

## Features

- 5 predefined words chosen at random each round
- 6 incorrect guesses allowed before game over
- ASCII art hangman that updates with each wrong guess
- Tracks all guessed letters
- Replay option after each round

## How to Play

1. The game picks a random word and shows you how many letters it has.
2. Enter one letter at a time.
3. A correct guess reveals the letter in the word.
4. A wrong guess adds a body part to the hangman.
5. Win by guessing all letters before 6 wrong guesses.

## Requirements

- Python 3.6 or higher
- No external libraries needed

## Run the Game

```bash
python hangman.py
```

## Project Structure

```
hangman/
├── hangman.py   # Main game logic
└── README.md    # This file
```

## Concepts Used

- `random` — randomly selects a word each game
- `while` loop — keeps the game running until win or loss
- `if-else` — handles guess validation and win/loss conditions
- Strings and sets — tracks the word and guessed letters

## Example Output

```
=============================
       HANGMAN GAME
=============================
The word has 6 letters.

   -----
   |   |
       |
       |
       |
       |
=========

Word: _ _ _ _ _ _
Wrong guesses left: 6

Guess a letter: p
✅ 'p' is in the word!
```

## License

MIT License — free to use and modify.
