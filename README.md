# talisman-scrapper

This is a scrapper to gather information about cards in the Talisman Magic & Sword board game. This application is part of my project to create
web application, which allows users to get information about probabilities, numbers, and all that stuff from the game.

## Running 

In order to be able to run application, you need to set your environment:

```bash
source environment/bin/activate
```
You also need to create file `talisman/uri.txt` with your mongoDB URI. Check mongoDB documentation here:  [MongoDB Atlas Documentation](https://www.mongodb.com/docs/manual/reference/connection-string/).

After that you can just run both scripts
 - `get_decks.py` - Scrapping and adding every deck(except of adventure deck) to your database.
 - `get_adventure_cards.py` - Scrapping and adding adventure deck to your database.

## Important notes

Unfortunately, there is only a Polish version of Talisman Wiki. Although there is an English version, it contains many bugs and missed pages, and I wasn't
able to retrieve all pieces of information.
Moreover, this is not game-precise, as some cards may be duplicated or be missing from a deck because there is simply not enough information in
talismanwiki. If you want to be 100% sure about every single card, probably the best idea is to simply check every single card by hand.

## Special thanks

I would also like to thank creators of [Talisman wiki](https://wiki.magiaimiecz.eu/Strona_g%C5%82%C3%B3wna). Huge credits for their work!
