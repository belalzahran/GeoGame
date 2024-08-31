from typing import List, Dict
from geonames_api import RestAdapter
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import json

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
            return self.get_country_list(game_settings['continent'])
            

    def get_country_list(self, continent: str) -> List:

        unfiltered_api_countries_list = self.get_countries_from_API()
        if continent is None:
            result = [country['countryName'].lower() for country in unfiltered_api_countries_list if country['countryName'] in country_list_easier]
           
        else:
            result = [country["countryName"].lower() for country in unfiltered_api_countries_list if (country['continentName'] == continent) and (country['countryName'] in country_list_easier)]
        
        return result


    def get_countries_from_API(self) -> List[Dict]:

        try: 
            geonames_api = RestAdapter(hostname="api.geonames.org/countryInfoJSON?")
            response = geonames_api.get()
            countries_list = response['geonames']
            
            return countries_list
        
        except Exception as e:

            # print("Error: Something went wrong while requesting from the API")
            # print("Using Countries.json instead")

            with open('countries_list.json','r') as file:
                countries_list = json.load(file)
            
            return countries_list


    def get_score(self) -> str:

        return "{} out of {}".format(len(self.correct_user_guesses),len(self.correct_answers))


    def start_game_introduction(self):

        
        print(f"Game Mode: {self.game_mode}")


        # if self.continent is not None:
        #     print(f"Continent: {self.continent}")
        print(f"Number of Countries: {len(self.correct_answers)}")

        print(f"Controls: \n\t\"show\": Displays all correct responses\n\t\"hint\": Gives hint on an unguessed Country")
        
        print("Begin!\n")


    def start_game(self):

        self.start_game_introduction()


        user_input = input("\t")

        while self.game_won is False:

            if user_input == "show":
                print(f"\n\t\t{sorted(self.correct_user_guesses)}\n")
            elif user_input == "hint":

                unguessed_correct_countries = [country for country in self.correct_answers if country not in self.correct_user_guesses]
                print(f"\n\t\tCountry starting with {unguessed_correct_countries[0][:2]}\n")



            else:
                self.parse_user_input(user_input)
                print(f"\n\t\t{self.get_score()}\n")
                if self.game_won:
                    break

            user_input = input("\t")


        print(f"Congrats, you beat the game!")
        

    def parse_user_input(self, user_input: str) -> None:

        guesses = user_input.split(", ")

        for guess in guesses:
            raw_guess = guess
            guess = guess.lower()
        

            closest_match, score = process.extractOne(guess, self.correct_answers, scorer=fuzz.ratio)

            if score >= 80:

                if score <= 99:
                    print(f"\n\t\tAuto Correcting {raw_guess} to {closest_match}. Similarity Score: {score}/100")

                if closest_match not in self.correct_user_guesses:
                    self.correct_user_guesses.append(closest_match)
                else:
                    print(f"\n\t\tYou already answered {closest_match}")
            else:
                self.incorrect_user_guesses.append(guess)
                
        if len(self.correct_user_guesses) == len(self.correct_answers):
            self.game_won = True




country_list_easier = [
    "Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina", 
    "Bulgaria", "Croatia", "Czech Republic", "Denmark", "Estonia", "Finland", 
    "France", "Germany", "Greece", "Hungary", "Iceland", "Ireland", "Italy", 
    "Kosovo", "Latvia", "Liechtenstein", "Lithuania", "Luxembourg", "Malta", 
    "Moldova", "Monaco", "Montenegro", "Netherlands", "North Macedonia", "Norway", 
    "Poland", "Portugal", "Romania", "Russia", "San Marino", "Serbia", "Slovakia", 
    "Slovenia", "Spain", "Sweden", "Switzerland", "Ukraine", "United Kingdom", 
    "Vatican City", "Asia", "Afghanistan", "Armenia", "Azerbaijan", "Bahrain", 
    "Bangladesh", "Bhutan", "Brunei", "Cambodia", "China", "Cyprus", "East Timor", 
    "Georgia", "India", "Indonesia", "Iran", "Iraq", "Israel", "Japan", "Jordan", 
    "Kazakhstan", "Kuwait", "Kyrgyzstan", "Laos", "Lebanon", "Malaysia", "Maldives", 
    "Mongolia", "Myanmar", "Nepal", "North Korea", "Oman", "Pakistan", "Philippines", 
    "Qatar", "Saudi Arabia", "Singapore", "South Korea", "Sri Lanka", "Syria", 
    "Taiwan", "Tajikistan", "Thailand", "Turkey", "Turkmenistan", 
    "United Arab Emirates", "Uzbekistan", "Vietnam", "Yemen", "Africa", "Algeria", 
    "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cameroon", "Cape Verde", 
    "Central African Republic", "Chad", "Comoros", "Democratic Republic of the Congo", 
    "Djibouti", "Egypt", "Equatorial Guinea", "Eritrea", "Eswatini", "Ethiopia", 
    "Gabon", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Ivory Coast", "Kenya", 
    "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania", 
    "Mauritius", "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", 
    "Republic of the Congo", "Rwanda", "São Tomé and Príncipe", "Senegal", 
    "Seychelles", "Sierra Leone", "Somalia", "South Africa", "South Sudan", 
    "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe", 
    "North America", "Antigua and Barbuda", "Bahamas", "Barbados", "Belize", 
    "Canada", "Costa Rica", "Cuba", "Dominica", "Dominican Republic", "El Salvador", 
    "Grenada", "Guatemala", "Haiti", "Honduras", "Jamaica", "Mexico", "Nicaragua", 
    "Panama", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", 
    "Trinidad and Tobago", "United States", "South America", "Argentina", 
    "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Guyana", "Paraguay", 
    "Peru", "Suriname", "Uruguay", "Venezuela", "Oceania", "Australia", 
    "Federated States of Micronesia", "Fiji", "Kiribati", "Marshall Islands", 
    "Nauru", "New Zealand", "Palau", "Papua New Guinea", "Samoa", 
    "Solomon Islands", "Tonga", "Tuvalu", "Vanuatu"
]
