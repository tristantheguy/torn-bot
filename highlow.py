from dataclasses import dataclass
from typing import Dict

RANK_NAMES = {11: 'Jack', 12: 'Queen', 13: 'King', 14: 'Ace'}
ALL_RANKS = list(range(2, 15))


def parse_rank(text: str) -> int:
    """Parse a rank given as '2'-'10', 'J', 'Q', 'K', 'A'."""
    text = text.strip().upper()
    mapping = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    if text in mapping:
        return mapping[text]
    try:
        val = int(text)
    except ValueError as exc:
        raise ValueError(f"invalid rank: {text}") from exc
    if 2 <= val <= 10:
        return val
    raise ValueError(f"invalid rank: {text}")


@dataclass
class Deck:
    counts: Dict[int, int]

    def __init__(self) -> None:
        self.counts = {rank: 4 for rank in ALL_RANKS}

    def remove(self, rank: int) -> None:
        if self.counts.get(rank, 0) == 0:
            raise ValueError("card not available in deck")
        self.counts[rank] -= 1

    def remaining(self) -> int:
        return sum(self.counts.values())


def probability_next(deck: Deck, current_rank: int):
    higher = sum(count for rank, count in deck.counts.items() if rank > current_rank)
    lower = sum(count for rank, count in deck.counts.items() if rank < current_rank)
    total = deck.remaining()
    if total == 0:
        return 0.0, 0.0, 'none'
    p_high = higher / total
    p_low = lower / total
    if p_high > p_low:
        suggestion = 'high'
    elif p_low > p_high:
        suggestion = 'low'
    else:
        suggestion = 'either'
    return p_high, p_low, suggestion


def main() -> None:
    deck = Deck()
    print("Interactive High-Low probability tool")
    start = input("Enter the first card rank (2-10, J, Q, K, A): ")
    current_rank = parse_rank(start)
    deck.remove(current_rank)
    while True:
        p_high, p_low, suggestion = probability_next(deck, current_rank)
        total = deck.remaining()
        print(f"Cards left: {total}")
        print(f"Probability next card is higher: {p_high:.2%}")
        print(f"Probability next card is lower: {p_low:.2%}")
        print(f"Suggested guess: {suggestion}")
        if total == 0:
            print("No cards left in the deck.")
            break
        nxt = input("Enter the next card revealed (or 'quit' to stop): ").strip()
        if nxt.lower() in {'q', 'quit', 'exit'}:
            break
        next_rank = parse_rank(nxt)
        deck.remove(next_rank)
        current_rank = next_rank


if __name__ == "__main__":
    main()
