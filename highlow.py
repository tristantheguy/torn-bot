import random
import argparse
from dataclasses import dataclass

RANK_NAMES = {11: 'Jack', 12: 'Queen', 13: 'King', 14: 'Ace'}
SUITS = ['hearts', 'diamonds', 'clubs', 'spades']
RANK_LOOKUP = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
    '9': 9, '10': 10,
    'j': 11, 'jack': 11,
    'q': 12, 'queen': 12,
    'k': 13, 'king': 13,
    'a': 14, 'ace': 14,
}

@dataclass(frozen=True)
class Card:
    rank: int
    suit: str

    def __str__(self) -> str:
        name = RANK_NAMES.get(self.rank, str(self.rank))
        return f"{name} of {self.suit}"


def parse_rank(value: str) -> int:
    """Convert user input into a card rank number."""
    key = value.strip().lower()
    if key not in RANK_LOOKUP:
        raise ValueError(f"Unknown card rank: {value}")
    return RANK_LOOKUP[key]

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

    def remove_rank(self, rank: int) -> Card:
        """Remove one card of the given rank from the deck."""
        for i, card in enumerate(self.remaining):
            if card.rank == rank:
                self.played.append(self.remaining.pop(i))
                return card
        raise RuntimeError(f"No card of rank {rank} left in the deck")

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


def automatic_game() -> None:
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


def manual_game() -> None:
    deck = Deck()
    print("Manual High-Low assistant. Type 'exit' to quit.")
    while deck.remaining:
        down = input("\nFirst card face down (rank): ").strip()
        if not down or down.lower() in {"exit", "quit"}:
            break
        try:
            rank = parse_rank(down)
            deck.remove_rank(rank)
        except Exception as exc:
            print(exc)
            continue
        if deck.remaining:
            p_high, p_low, suggestion = deck.probability_next(Card(rank, ''))
            print(f"Probability next card is higher: {p_high:.2%}")
            print(f"Probability next card is lower: {p_low:.2%}")
            print(f"Suggested guess: {suggestion}")
        reveal = input("Revealed card (rank): ").strip()
        if not reveal:
            break
        try:
            deck.remove_rank(parse_rank(reveal))
        except Exception as exc:
            print(exc)
            continue
        print(f"Cards left: {len(deck.remaining)}")
    print("Game over.")


def main() -> None:
    parser = argparse.ArgumentParser(description="High-Low card simulator")
    parser.add_argument("--manual", action="store_true", help="Manually enter cards")
    args = parser.parse_args()
    if args.manual:
        manual_game()
    else:
        automatic_game()

if __name__ == "__main__":
    main()
