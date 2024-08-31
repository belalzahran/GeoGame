# from the_cat_api import RestAdapter
from geonames_api import RestAdapter
from countries_game import CountryGame


# geonames_api = RestAdapter(hostname="api.geonames.org/countryInfoJSON?")
# response = geonames_api.get()
# countries_list = response['geonames']


# for country in countries_list:
#     print(country['continentName'])
#     input()





newGame = CountryGame(game_mode="Classic", continent="Europe")

newGame.start_game()