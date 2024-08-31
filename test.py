# from the_cat_api import RestAdapter
from geonames_api import RestAdapter
from countries_game import CountryGame


# geonames_api = RestAdapter(hostname="api.geonames.org/countryInfoJSON?")
# response = geonames_api.get()
# countries_list = response['geonames']


# for country in countries_list:
#     print()
    

print("\n\n\nWelcome to my Country Guessing Game powered by the Geonames API")

print("The objective of the game is to guess as many countries as you can correctly!")

print("Also, capatalization does not matter and make sure to separate your answers with commmas and spaces!\n")

continent = input("Select a continent: ")

newGame = CountryGame(game_mode="Classic", continent=continent)

newGame.start_game()

