# High-Low Card Simulator

This repository contains a simple Python tool to simulate drawing cards from a standard 52-card deck. It keeps track of which cards have been played and calculates the probability that the next card will be higher or lower than the one just drawn. Based on these probabilities, it suggests whether guessing "high" or "low" would be smarter.

## Usage

Run the simulator with Python 3:

```bash
python3 highlow.py
```

Press Enter to draw a new card. After each draw, the script prints:

- The card drawn
- The number of cards left in the deck
- Probability that the next card is higher or lower
- The suggested guess

When no cards remain, the game ends.
