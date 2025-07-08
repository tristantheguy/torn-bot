import random
from dataclasses import dataclass

RANK_NAMES = {11: 'Jack', 12: 'Queen', 13: 'King', 14: 'Ace'}
SUITS = ['hearts', 'diamonds', 'clubs', 'spades']

@dataclass(frozen=True)
class Card:
    rank: int
    suit: str

    def __str__(self) -> str:
        name = RANK_NAMES.get(self.rank, str(self.rank))
        return f"{name} of {self.suit}"

class Deck:
    """Represents a deck of playing cards."""
    def __init__(self) -> None:
        self.remaining = [Card(rank, suit) for suit in SUITS for rank in range(2, 15)]
        self.played = []
        self.shuffle()

    def shuffle(self) -> None:
        random.shuffle(self.remaining)

    def draw(self) -> Card:
        if not self.remaining:
            raise RuntimeError("No cards left in the deck")
        card = self.remaining.pop()
        self.played.append(card)
        return card

    def probability_next(self, current: Card):
        """Return probability that next card is higher or lower than ``current``."""
        higher = sum(c.rank > current.rank for c in self.remaining)
        lower = sum(c.rank < current.rank for c in self.remaining)
        total = len(self.remaining)
        if total == 0:
            return 0.0, 0.0, 'none'
        p_high = higher / total
        p_low = lower / total
        suggestion = 'high' if p_high > p_low else 'low' if p_low > p_high else 'either'
        return p_high, p_low, suggestion


def main() -> None:
    deck = Deck()
    print("High-Low deck simulator. Press Enter to draw a card.")
    while deck.remaining:
        input("\nDraw a card...")
        card = deck.draw()
        print(f"Drawn card: {card}")
        if deck.remaining:
            p_high, p_low, suggestion = deck.probability_next(card)
            print(f"Cards left: {len(deck.remaining)}")
            print(f"Probability next card is higher: {p_high:.2%}")
            print(f"Probability next card is lower: {p_low:.2%}")
            print(f"Suggested guess: {suggestion}")
        else:
            print("No cards left in the deck.")

if __name__ == "__main__":
    main()
