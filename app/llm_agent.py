import openai

class LLM_Agent:
    def __init__(self, name, api_key):
        self.name = name
        openai.api_key = api_key

    def get_action(self, game_state):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Given the game state: {game_state}, what action should the player take?",
            max_tokens=50
        )
        action = response.choices[0].text.strip()
        return action