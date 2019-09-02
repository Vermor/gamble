"""
standard deck of cards submodule
"""
import random
from collections import Counter
from types import SimpleNamespace
from typing import Any, Dict, List, Union
from gamble.errors import InvalidCard


class Suit(SimpleNamespace):
    """suit namespace class"""


class Value(SimpleNamespace):
    """value namespace class"""


class Rank(SimpleNamespace):
    """hand ranks namespace class"""


class Card:
    """playing card model"""

    BLACK = 0
    RED = 1

    class Suits:
        """card suit enum"""

        SPADES = Suit(
            name="spades", char="S", symbol="♠", value=0, color=0, unicode=127136
        )
        CLUBS = Suit(
            name="clubs", char="C", symbol="♣", value=1, color=0, unicode=127184
        )
        DIAMONDS = Suit(
            name="diamonds", char="D", symbol="♦", value=2, color=1, unicode=127168
        )
        HEARTS = Suit(
            name="hearts", char="H", symbol="♥", value=3, color=1, unicode=127152
        )

        @classmethod
        def all(cls) -> List[Suit]:
            """get all suits"""
            return sorted(
                [
                    cls.__dict__[x]
                    for x in dir(cls)
                    if not x.startswith("_") and isinstance(cls.__dict__[x], Suit)
                ],
                key=lambda x: x.value,
            )

        @classmethod
        def dict(cls) -> Dict[str, Suit]:
            """dict of char -> Suit"""
            return {x.char: x for x in cls.all()}

    class Values:
        """card value enum"""

        ACE = Value(char="A", name="ace", value=1)
        TWO = Value(char="2", name="two", value=2)
        THREE = Value(char="3", name="three", value=3)
        FOUR = Value(char="4", name="four", value=4)
        FIVE = Value(char="5", name="five", value=5)
        SIX = Value(char="6", name="six", value=6)
        SEVEN = Value(char="7", name="seven", value=7)
        EIGHT = Value(char="8", name="eight", value=8)
        NINE = Value(char="9", name="nine", value=9)
        TEN = Value(char="T", name="ten", value=10)
        JACK = Value(char="J", name="jack", value=11)
        QUEEN = Value(char="Q", name="queen", value=12)
        KING = Value(char="K", name="king", value=13)

        @classmethod
        def all(cls) -> List[Value]:
            """get all suits"""
            return sorted(
                [
                    cls.__dict__[x]
                    for x in dir(cls)
                    if not x.startswith("_") and isinstance(cls.__dict__[x], Value)
                ],
                key=lambda x: x.value,
            )

        @classmethod
        def dict(cls) -> Dict[str, Value]:
            """dict of char -> Value"""
            return {x.char: x for x in cls.all()}

    def __init__(self, value: Value = Values.ACE, suit: Suit = Suits.SPADES) -> None:
        """card constructor"""
        self.value = value
        self.suit = suit

    @classmethod
    def get(cls, text: str) -> "Card":
        """get a card by text representation"""
        if not len(text) == 2:
            raise InvalidCard("Too many characters for a card!")
        vals = cls.Values.dict()
        suits = cls.Suits.dict()
        value_char, suit_char = list(text.upper())
        if value_char not in vals:
            raise InvalidCard("Invalid value for card!")
        if suit_char not in suits:
            raise InvalidCard("Invalid suit for card!")
        return cls(value=vals[value_char], suit=suits[suit_char])

    @property
    def color(self) -> int:
        """returns the color of the card"""
        return self.suit.color

    @property
    def full_name(self) -> str:
        """returns the full name for this card"""
        return "{} of {}".format(self.value.name, self.suit.name)

    @property
    def is_black(self) -> bool:
        """is_black property"""
        return self.color == Card.BLACK

    @property
    def unicode(self) -> str:
        """get the fun little unicode card for this card"""
        # we need to skip the 'knight' card if we're a queen or king
        hack = int(self.value.value >= 12)
        return chr(self.suit.unicode + self.value.value + hack)

    @property
    def is_red(self) -> bool:
        """is_red property"""
        return self.color == Card.RED

    def __str__(self) -> str:
        """string representation of this card"""
        return "{}{}".format(self.value.char, self.suit.symbol)

    def __repr__(self) -> str:
        """representation of this card"""
        return "<Card:{}>".format(str(self))

    def __lt__(self, other: "Card") -> bool:
        """less than dunder method"""
        return self.value.value < other.value.value

    def __gt__(self, other: "Card") -> bool:
        """greater than dunder method"""
        return self.value.value > other.value.value

    def __le__(self, other: "Card") -> bool:
        """less than or equal to dunder method"""
        return self < other or self == other

    def __ge__(self, other: "Card") -> bool:
        """greater than or equal to dunder method"""
        return self > other or self == other

    def __eq__(self, other: object) -> bool:
        """equal to dunder method"""
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit and self.value == other.value


class Hand:
    """playing card hand model"""

    class Ranks:
        """hand ranks for poker"""

        STRAIGHT_FLUSH = Rank(value=8, name="straight flush")
        FOUR_OF_A_KIND = Rank(value=7, name="four of a kind")
        FULL_HOUSE = Rank(value=6, name="full house")
        FLUSH = Rank(value=5, name="flush")
        STRAIGHT = Rank(value=4, name="straight")
        THREE_OF_A_KIND = Rank(value=3, name="three of a kind")
        TWO_PAIR = Rank(value=2, name="two pair")
        PAIR = Rank(value=1, name="pair")
        HIGH_CARD = Rank(value=0, name="high card")

    def __init__(self, cards: List[Card]) -> None:
        """hand constructor"""
        self._cards = cards
        self.cards = sorted(self._cards)
        self.size = len(self.cards)
        self.value_counts = Counter([x.value.value for x in self.cards])
        self.suit_counts = Counter([x.suit.value for x in self.cards])

    def __lt__(self, other: "Hand") -> bool:
        """less than dunder method"""
        return self.rank.value < other.rank.value

    def __gt__(self, other: "Hand") -> bool:
        """greater than dunder method"""
        return self.rank.value > other.rank.value

    def __len__(self) -> int:
        """dunder len method"""
        return len(self.cards)

    def __str__(self) -> str:
        """string representation of the hand"""
        return "[{}]".format(", ".join([str(x) for x in self.cards]))

    def __repr__(self) -> str:
        """repr of the hand"""
        return "<Hand[{}]({}) {}>".format(self.size, self.rank.name, str(self))

    @classmethod
    def get(cls, text: str) -> "Hand":
        """get a hand by text representations"""
        card_strings = text.replace(" ", "").upper().split(",")
        cards = [Card.get(x) for x in card_strings]
        return cls(cards=cards)

    @property
    def rank(self) -> Rank:
        """get the rank of this hand"""
        if self.is_straight_flush:
            return Hand.Ranks.STRAIGHT_FLUSH
        if self.is_four_of_a_kind:
            return Hand.Ranks.FOUR_OF_A_KIND
        if self.is_full_house:
            return Hand.Ranks.FULL_HOUSE
        if self.is_flush:
            return Hand.Ranks.FLUSH
        if self.is_straight:
            return Hand.Ranks.STRAIGHT
        if self.is_three_of_a_kind:
            return Hand.Ranks.THREE_OF_A_KIND
        if self.is_two_pair:
            return Hand.Ranks.TWO_PAIR
        if self.is_one_pair:
            return Hand.Ranks.PAIR
        return Hand.Ranks.HIGH_CARD

    @property
    def _vals(self) -> List[int]:
        """values helper to make the following checks less verbose"""
        return sorted(list(self.value_counts.values()), reverse=True)

    @property
    def is_straight_flush(self) -> bool:
        """check if the hand is a straight flush"""
        return self.is_flush and self.is_straight

    @property
    def is_four_of_a_kind(self) -> bool:
        """check if the hand is four of a kind"""
        return self._vals[0] == 4

    @property
    def is_full_house(self) -> bool:
        """check if the hand is a full house"""
        return self._vals[0:2] == [3, 2]

    @property
    def is_flush(self) -> bool:
        """check if the hand is a flush"""
        return len(set([x.suit.value for x in self.cards])) == 1

    @property
    def is_straight(self) -> bool:
        """check if the hand is a straight"""

        def check(value_set: set) -> bool:
            """check if the given set is a straight"""
            value_range = max(value_set) - min(value_set)
            return (value_range == self.size - 1) and (len(value_set) == self.size)

        values = [x.value.value for x in self.cards]
        low_ace = set(values)
        high_ace = set(x if x != 1 else 14 for x in values)
        return check(low_ace) or check(high_ace)

    @property
    def is_three_of_a_kind(self) -> bool:
        """check if the hand is three of a kind"""
        return self._vals[0] == 3

    @property
    def is_two_pair(self) -> bool:
        """check if the hand contains two pair"""
        return self._vals[0:2] == [2, 2]

    @property
    def is_one_pair(self) -> bool:
        """check if the hand contains one pair"""
        return self._vals[0] == 2


class Deck:
    """playing card deck model"""

    def __init__(self, cards: List[Card] = None, shuffle: bool = True) -> None:
        """deck constructor"""
        if cards:
            self.cards = cards
        else:
            # lets start with a default deck of 52
            self.cards = []
            for suit in Card.Suits.all():
                for value in Card.Values.all():
                    self.cards.append(Card(value=value, suit=suit))
            self.cards.reverse()
        self.shuffles = 0
        self.draws = 0
        if shuffle:
            self.shuffle()

    def __contains__(self, item: object) -> bool:
        """dunder contains method"""
        if not isinstance(item, Card):
            return False
        return item in self.cards

    def __str__(self) -> str:
        """string representation of a deck"""
        return "<Deck[{}]>".format(self.cards_left)

    def __repr__(self) -> str:
        """term representation of a deck"""
        return str(self)

    @property
    def top(self) -> Card:
        """the top card of the deck"""
        return self.cards[-1]

    @property
    def bottom(self) -> Card:
        """the bottom card of the deck"""
        return self.cards[0]

    @property
    def cards_left(self) -> int:
        """number of cards left in the deck"""
        return len(self.cards)

    def draw(self, times: int = 1) -> Union[Card, List[Card]]:
        """draws the given number of cards from the deck"""
        if times == 1:
            self.draws += 1
            return self.cards.pop()
        cards = []
        for _ in range(times):
            self.draws += 1
            cards.append(self.cards.pop())
        return cards

    def draw_hand(self, size: int = 5) -> Hand:
        """draw a hand from this deck"""
        cards = self.draw(times=size)
        return Hand(cards=cards if isinstance(cards, list) else [cards])

    def shuffle(self, times: int = 1) -> None:
        """shuffle the deck"""
        for _ in range(times):
            self.shuffles += 1
            random.shuffle(self.cards)


class EuchreDeck(Deck):
    """deck specifically for euchre"""

    def __init__(self, **kwargs: Any) -> None:
        """euchre deck constructor"""
        cards: List[Card] = []

        # euchre uses 9, 10, J, Q, K, A of all suits
        values = [x for x in Card.Values.all() if x.value >= 9 or x.value == 1]
        for suit in Card.Suits.all():
            for value in values:
                cards.append(Card(value=value, suit=suit))
        cards.reverse()
        super().__init__(cards=cards)
