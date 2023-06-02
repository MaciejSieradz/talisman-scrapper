"""Module that contains a class which represents a talisman adventure card."""


class Card():
    """This class represents a talisman adventure card."""

    def __init__(self, name: str, card_type: str, meeting_number: int, number_of_copies: int, description: str, card_subtype=None):
        """Create a card from given properties."""
        self.name = name
        self.card_type = card_type.upper()
        self.meeting_number = meeting_number
        self.number_of_copies = number_of_copies
        self.card_subtype = card_subtype
        self.description = description
        self.fighting_attribute = None
        self.fighting_power = None

    def get_description(self):
        """Give a description of card."""
        if self.card_subtype is None:
            return f'nazwa={self.name}, typ={self.card_type}, numer_spotkania={self.meeting_number}, liczba_kopii={self.number_of_copies}'
        else:
            return f'nazwa={self.name}, typ={self.card_type}, podtyp={self.card_subtype}, numer_spotkania={self.meeting_number}, liczba_kopii={self.number_of_copies}'

class EnemyCard(Card):
    """This class creates an enemy card. Enemy card is standard card, but has two additional fields: type of attribute used and total power of the enemy."""

    def __init__(self, name: str, card_type: str, meeting_number: int, number_of_copies: int, description: str, card_subtype: str, fighting_attribute: str, fighting_power: str):
        """Create an enemy card."""
        super().__init__(name, card_type, meeting_number,
                         number_of_copies, description, card_subtype)
        if fighting_attribute == "Siła/Moc":
            fighting_attribute = "Siła_Moc"
        self.fighting_attribute = fighting_attribute.upper()
        self.fighting_power = fighting_power
