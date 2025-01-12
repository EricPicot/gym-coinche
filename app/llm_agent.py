import openai
import os
from dotenv import load_dotenv
import json


load_dotenv()  # Load environment variables from .env file

def extract_annonce(json_string):
    data = json.loads(json_string)
    annonce = data.get('annonce')
    return annonce

def get_partner(player_name):
    partners = {
        "South": "North",
        "North": "South",
        "East": "West",
        "West": "East"
    }
    return partners.get(player_name, "Unknown")
class LLM_Agent:
    def __init__(self, name, model='gpt-4o-2024-08-06'):
        self.name = name
        self.model = model
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def get_action(self, game_state):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a player in a game of Coinche, a French card game similar to Belote."},
                {"role": "user", "content": f"Given the game state: {game_state}, what action should the player take?"}
            ]
        )
        action = response.choices[0].message['content'].strip()
        return action

    def get_annonce(self, player_name, player_hand, current_contract, current_contract_holder):
        prompt = (
            f"You are playing a game of Coinche. The current phase is the annonce phase. "
            f"You are {player_name}. "
            f"Your partner is {get_partner(player_name)}. "
            f"Your hand is: {player_hand}. "
            f"The current highest contract value is {current_contract}, "
            f"and the current contract holder is {current_contract_holder}. "
            "Based on this information, what should your annonce be? "
            "Annonces are in the format 'value of suit'. for example, '80 of hearts'. Don't add any other text."
            "If you cannot make a higher annonce, respond with 'pass'."
        )
        print(f"You are {player_name}. ")
        print(f"Your partner is {get_partner(player_name)}. ")
        print(f"Your hand is: {player_hand}. ")
        print(f"The current highest contract is {current_contract}, ")
        print(f'and the current contract holder is {current_contract_holder}. ')

        response = self.client.chat.completions.create(model=self.model, 
                                          messages=[ { "role": "developer", "content": "You are a player in a game of Coinche, a French card game similar to Belote." },
                                                     { "role": "user", "content": prompt } ], 
                                        response_format={
                                            "type": "json_schema",
                                            "json_schema": {
                                                "name": "annonce",
                                                "schema": {
                                                    "type": "object",
                                                    "properties": {
                                                        "annonce": {
                                                            "description": "the contract you are willing to bet",
                                                            "type": "string"
                                                        }
                                                    },
                                                    "additionalProperties": False
                                                }
                                            }
                                        })
        
        print()
        annonce = extract_annonce(response.choices[0].message.content)
        print()
        print("Annonce:", annonce)  # Debug log

        print(50*"-")

        return annonce