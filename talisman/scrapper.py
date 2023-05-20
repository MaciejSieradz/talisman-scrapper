"""Module for basic scrapper."""

from typing import List
import requests
from bs4 import BeautifulSoup, Tag
import re

from objects.card import Card, EnemyCard


class Scrapper():
    """Basic class representing a scrapper."""

    main_url = 'http://wiki.magiaimiecz.eu/'

    def __init__(self) -> None:
        """Create a scrapper object."""

    def create_cards(self, url: str, extension: str) -> List[Card]:
        """Crete list of card with given url."""
        cards_url = []
        cards = []
        cards_names = self._get_cards_text(url)

        self.extension = extension

        for card_name in cards_names:
            cards_url.append(self.main_url + card_name)

        if 'http://wiki.magiaimiecz.eu/Karty_Przygód_(Talisman)' in cards_url:
            cards_url.remove(
                'http://wiki.magiaimiecz.eu/Karty_Przygód_(Talisman)')

        for card_url in cards_url:
            cards.append(self._create_card_from_url(card_url))

        return cards

    def _get_cards_text(self, url):
        cards_html = self._get_cards(url)
        cards_text = []

        for card_html in cards_html:
            cards_text.append(card_html.text)

        cards_text = list(map(lambda card: card.replace(' ', '_'), cards_text))
        return cards_text

    def _get_cards(self, url):
        """Get cards in html format from main page."""
        bs = self._create_soup(self._create_request(url))

        div = bs.find('div', {'id': 'mw-pages'})

        cards_html = []

        if isinstance(div, Tag):
            cards_html = div.find_all('a', {})

        return cards_html

    def _create_card_from_url(self, url):
        bs = self._create_soup(self._create_request(url))

        text_properties = []

        div = self._find_content_div(bs)

        uls = str(div.find_all('ul', limit=2))

        description = bs.find('p')
        if description is not None:
            description = description.get_text()

        rolls = div.find('ol')

        if rolls is not None and isinstance(rolls, Tag):
            lis = rolls.find_all('li')

            start = 1
            dice_rolls = ''

            for li in lis:
                dice_rolls += f'{start}. {li.get_text()} \n'
                start += 1

            description = str(description) + dice_rolls

        bs1 = self._create_soup(uls)

        card_properties = bs1.find_all('li', {}, limit=5)

        if 'Angielska nazwa' in str(card_properties[1].get_text()):
            card_properties = bs1.find_all('li', {}, limit=6)
            card_properties.pop(1)

        self._remove_not_matched_properties(card_properties, '^Liczba')

        for card_property in card_properties:
            text = str(card_property)
            text_soup = BeautifulSoup(text, 'html.parser')

            b_tag = text_soup.b
            if b_tag is not None:
                b_tag.extract()

            property = text_soup.find('li')

            if property is not None:
                text_properties.append(
                    self._obtain_property_from_li(property.get_text()))

        return self._create_card_from_properties(text_properties, str(description))

    def _find_content_div(self, bs: BeautifulSoup) -> Tag:

        content_div = bs.find('div', {'id': 'mw-content-text'})

        if isinstance(content_div, Tag):
            return content_div

        raise Exception("No div found!")

    def _remove_not_matched_properties(self, card_properties: list, regex: str):
        """
        Remove blank properties.

        Some cards have empty li's in html which creates gives a blank property.This ensures that we will get only correct properties.
        """
        if len(card_properties) is not None:

            card_property = card_properties[-1]

            proper_property = re.search(regex, str(card_property.get_text()))

            while proper_property is None:
                card_properties.pop()
                card_property = card_properties[-1]
                proper_property = re.search(
                    regex, str(card_property.get_text()))

    def _obtain_property_from_li(self, card_property: str) -> str:
        """Obtain property from HTML li tag."""
        card_property = card_property.replace(':', ' ')
        card_property = card_property.strip()

        return card_property

    def _create_card_from_properties(self, text_properties: List, card_description: str) -> Card:
        """
        Create card.

        This method is taking properties in text format and returns a card based on how many properties this card has.
        """
        if self._is_enemy_card(text_properties[1]):
            return self._create_enemy_card(text_properties, card_description)

        if len(text_properties) == 4:
            return self._create_card(text_properties, card_description)
        return self._create_card_with_subtype(text_properties, card_description)

    def _is_enemy_card(self, text_property: str) -> bool:
        if 'Wróg' in text_property:
            return True
        return False

    def _create_enemy_card(self, text_properties: List, card_description: str) -> EnemyCard:

        name = text_properties[0]
        type_of_card = 'Wróg'
        if len(str(text_properties[1]).split(' ')) >= 3:
            subtype_of_card = str(text_properties[1]).split(' ')[2]
        else:
            subtype_of_card = None
        number_of_meeting = int(text_properties[2])
        number_of_copies = int(self._get_number_of_copies(text_properties[3]))

        fight_information = self._get_information_about_enemy(
            card_description.partition('\n')[0])

        card = EnemyCard(name, type_of_card, number_of_meeting, number_of_copies,
                         card_description, subtype_of_card, fight_information[0], fight_information[1])

        return card

    def _get_information_about_enemy(self, description_of_enemy: str) -> list[str]:
        fight_info = description_of_enemy
        fight_info = fight_info.strip()
        fight_info = fight_info.replace(':', '')
        fight_info = " ".join(fight_info.split())
        fight_info = fight_info.split(' ')

        return fight_info

    def _create_card(self, text_properties: List, description: str) -> Card:
        text_properties[2] = int(text_properties[2])
        text_properties[3] = self._get_number_of_copies(text_properties[3])
        card = Card(text_properties[0], text_properties[1],
                    text_properties[2], text_properties[3], description)

        return card

    def _create_card_with_subtype(self, text_properties: List, description: str) -> Card:
        text_properties[3] = int(text_properties[3])
        text_properties[4] = self._get_number_of_copies(text_properties[4])
        card = Card(text_properties[0], text_properties[1], text_properties[3],
                    text_properties[4], description, card_subtype=text_properties[2])
        return card

    def _get_number_of_copies(self, text) -> int:
        match = re.search(r'[0-9] w ' + self.extension, text)

        if match:
            number_of_copies = match.group()
            return int(number_of_copies[0])

        return 0

    def _create_request(self, url) -> bytes:
        html = requests.get(url)

        return html.content

    def _create_soup(self, content) -> BeautifulSoup:
        return BeautifulSoup(content, 'html.parser')
