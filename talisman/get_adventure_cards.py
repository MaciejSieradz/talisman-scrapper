"""Module for saving adventure cards to database."""
from pymongo.server_api import ServerApi
from pymongo import MongoClient

import scrapper

main_url = 'http://wiki.magiaimiecz.eu/'

adventure_url_one = 'http://wiki.magiaimiecz.eu/Kategoria:Karty_Przyg%C3%B3d'

mountains_adventure_url = 'https://wiki.magiaimiecz.eu/Kategoria:Karty_Przyg%C3%B3d_(G%C3%B3ry)'
forrest_adventure_url = 'https://wiki.magiaimiecz.eu/Kategoria:Karty_Przyg%C3%B3d_(Las)'
dungeon_adventure_url = 'https://wiki.magiaimiecz.eu/Kategoria:Karty_Przyg%C3%B3d_(Podziemia)'
werewolf_adventure_url = 'https://wiki.magiaimiecz.eu/Kategoria:Karty_Przyg%C3%B3d_(Wilko%C5%82ak)'
reaper_adventure_url = 'https://wiki.magiaimiecz.eu/Kategoria:Karty_Przyg%C3%B3d_(%C5%BBniwiarz)'
fireland_adventure_url = 'https://wiki.magiaimiecz.eu/Kategoria:Karty_Przyg%C3%B3d_(Kraina_Ognia)'
queen_of_ice_adventure_url = 'https://wiki.magiaimiecz.eu/Kategoria:Karty_Przyg%C3%B3d_(Kr%C3%B3lowa_Lodu)'
lake_queen_adventure_url = 'https://wiki.magiaimiecz.eu/Kategoria:Karty_Przyg%C3%B3d_(Pani_Jeziora)'
cataclysm_adventure_url = 'https://wiki.magiaimiecz.eu/Kategoria:Karty_Przyg%C3%B3d_(Kataklizm)'
adventure_url = 'https://wiki.magiaimiecz.eu/Kategoria:Karty_Przyg%C3%B3d_(Talisman)'


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

    adventure_cards_from_expansions = {
        'reaper_adventure_cards': card_scrapper.create_cards(url=reaper_adventure_url, extension="Żniwiarz"),
        'mountain_adventure_cards': card_scrapper.create_cards(url=mountains_adventure_url, extension="Góry"),
        'forrest_adventure_cards': card_scrapper.create_cards(url=forrest_adventure_url, extension="Las"),
        'dungeon_adventure_cards': card_scrapper.create_cards(url=dungeon_adventure_url, extension="Podziemia"),
        'werewolf_adventure_cards': card_scrapper.create_cards(url=werewolf_adventure_url, extension="Wilkołak"),
        'fireland_adventure_cards': card_scrapper.create_cards(url=fireland_adventure_url, extension="Kraina Ognia"),
        'queen_of_ice_adventure_cards': card_scrapper.create_cards(url=queen_of_ice_adventure_url, extension="Królowa Lodu"),
        'lake_queen_adventure_cards': card_scrapper.create_cards(url=lake_queen_adventure_url, extension="Pani Jeziora"),
        'cataclysm_adventure_cards': card_scrapper.create_cards(url=cataclysm_adventure_url, extension="Kataklizm"),
        'talisman_adventure_cards': card_scrapper.create_cards(url=adventure_url, extension="Talisman Magia i Miecz"),
    }

    adventure_deck = [] 

    for cards in adventure_cards_from_expansions.values():
        for card in cards:
            adventure_deck.append(card)



    for i in range(len(adventure_deck) - 1):
        for j in range(i + 1, len(adventure_deck) - 1):
            if adventure_deck[i].name == adventure_deck[j].name:
                adventure_deck[i].number_of_copies += adventure_deck[j].number_of_copies
                adventure_deck[j].name = None

    for card in adventure_deck:
        if card.name is None:
            adventure_deck.remove(card)

    print('Number of cards: ' + str(len(adventure_deck)))


    dbname = client['talisman']
    collection = dbname['adventure_deck']
    for adventure_card in sorted(adventure_deck, key=lambda card: card.name):
        collection.insert_one(_add_card_to_deck(adventure_card))

    client.close()
