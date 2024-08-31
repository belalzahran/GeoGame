from typing import List, Dict
from geonames_api import RestAdapter
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class CountryGame:

    def __init__(self, game_mode: str, continent: str = None):

        
        self.correct_user_guesses = []
        self.incorrect_user_guesses = []
        self.game_mode = game_mode
        self.continent = continent
        self.game_settings = {'game_mode': game_mode, 'continent': self.continent}
        self.correct_answers = self.get_correct_answers(game_settings=self.game_settings)
        self.game_won = False
     

        
    def get_correct_answers(self, game_settings: Dict):

        if game_settings['game_mode'] == "Classic":
            return self.get_countries_from(game_settings['continent'])
            

    def get_countries_from(self, continent: str) -> List:

        unfiltered_api_countries_list = self.get_countries_from_API()
        if continent is None:
            result = [country['countryName'].lower() for country in unfiltered_api_countries_list]
           
        else:
            result = [country["countryName"].lower() for country in unfiltered_api_countries_list if country['continentName'] == continent]
        
        return result


    def get_countries_from_API(self) -> List[Dict]:

        geonames_api = RestAdapter(hostname="api.geonames.org/countryInfoJSON?")
        response = geonames_api.get()
        countries_list = response['geonames']



        return countries_list


    def get_score(self) -> str:

        return "{} out of {}".format(len(self.correct_user_guesses),len(self.correct_answers))

    def start_game_introduction(self):

        print("Welcome to my Country Guessing Game powered by the Geonames API")

        print("The objective of the game is to guess as many countries as you can correctly!")

        print("Also, capatalizatoin does not matter and make sure to separate your answers with commmas and spaces!\n")
        print(f"Game Mode: {self.game_mode}")
        if self.continent is not None:
            print(f"Continent: {self.continent}")
        
        print("Begin!\n")


    def start_game(self):

        self.start_game_introduction()


        user_input = input("\t")

        while self.game_won is False:

            self.parse_user_input(user_input)

            print(f"\n\t\t{self.get_score()}\n")

            user_input = input("\t")


        print(f"Congrats, you beat the game with a score of {self.get_score()}")
        

    def parse_user_input(self, user_input: str):

        guesses = user_input.split(", ")


        for guess in guesses:
            raw_guess = guess
            guess = guess.lower()
        

            closest_match, score = process.extractOne(guess, self.correct_answers, scorer=fuzz.ratio)

            if score >= 80:

                if score <= 99:
                    print(f"\n\t\tAuto Correcting {raw_guess} to {closest_match}. Similarity Score: {score}/100\n")
                self.correct_user_guesses.append(closest_match)
            else:
                self.incorrect_user_guesses.append(guess)
                
        if len(self.correct_user_guesses) == len(self.correct_answers):
            self.game_won = True