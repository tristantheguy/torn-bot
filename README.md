# High-Low Card Simulator

This repository contains a simple Python tool that tracks a standard 52-card deck. Instead of drawing cards randomly, you enter each card as it is revealed. After every card, the tool calculates the probability that the next card will be higher or lower and suggests whether guessing "high" or "low" would be smarter.

## Usage

Run the simulator with Python 3:

```bash
python3 highlow.py
```

When you run the script, you'll be asked for the first face-up card (e.g. `7` or `Q`). After each entry the program prints:

- How many cards remain in the deck
- The probability the next card is higher or lower
- The suggested guess

Enter the rank of each new card as it is revealed or type `quit` to exit. When no cards remain, the game ends automatically.
