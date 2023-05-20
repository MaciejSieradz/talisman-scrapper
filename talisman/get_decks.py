"""Module for saving different decks to database."""

from pymongo.server_api import ServerApi
from pymongo import MongoClient

import scrapper

main_url = 'http://wiki.magiaimiecz.eu/'

mountains_url = 'https://wiki.magiaimiecz.eu/Kategoria:Talia_G%C3%B3r'
forrest_url = 'https://wiki.magiaimiecz.eu/Kategoria:Talia_Lasu'
dungeon_url = 'https://wiki.magiaimiecz.eu/Kategoria:Talia_Podziemi'
city_url = 'https://wiki.magiaimiecz.eu/Kategoria:Talia_Miasta'
nether_url = 'https://wiki.magiaimiecz.eu/Kategoria:Talia_Nieszcz%C4%99%C5%9B%C4%87'
tunnel_url = 'https://wiki.magiaimiecz.eu/Kategoria:Talia_Tunelu'
bridge_url = 'https://wiki.magiaimiecz.eu/Kategoria:Talia_Mostu'
harbinger_url = 'https://wiki.magiaimiecz.eu/Kategoria:Talia_Proroka'
cataclysm_url = 'https://wiki.magiaimiecz.eu/Kategoria:Talia_Pozosta%C5%82o%C5%9Bci'


def _add_card_to_deck(card: scrapper.Card) -> dict:
    return {
        '_id': card.name,
        'type': card.card_type,
        'subtype': card.card_subtype,
        'fight_statistic': card.fighting_attribute,
        'fight_power': card.fighting_power,
        'meeting_number': card.meeting_number,
        'number_of_copies': card.number_of_copies,
        'description': card.description
    }


if __name__ == "__main__":

    with open('talisman/uri.txt') as f:
        uri = f.read().strip()

    client = MongoClient(uri, server_api=ServerApi('1'))

    card_scrapper = scrapper.Scrapper()

    cards_collection = {
        'mountain_deck': card_scrapper.create_cards(url=mountains_url, extension="Góry"),
        'forrest_deck': card_scrapper.create_cards(url=forrest_url, extension="Las"),
        'dungeon_deck': card_scrapper.create_cards(url=dungeon_url, extension="Podziemia"),
        'city_deck': card_scrapper.create_cards(url=city_url, extension="Miasto"),
        'nether_deck': card_scrapper.create_cards(url=nether_url, extension="Puszka Pandory"),
        'tunnel_deck': card_scrapper.create_cards(url=tunnel_url, extension="Krainy Odmętów"),
        'bridge_deck': card_scrapper.create_cards(url=bridge_url, extension="Krainy Odmętów"),
        'harbinger_deck': card_scrapper.create_cards(url=harbinger_url, extension="Zwiastun"),
        'residue_deck': card_scrapper.create_cards(url=cataclysm_url, extension="Kataklizm")
    }

    dbname = client['talisman']
    for card_collection_key, card_collection_value in cards_collection.items():
        collection = dbname[card_collection_key]
        for card in card_collection_value:
            collection.insert_one(_add_card_to_deck(card))

    client.close()
