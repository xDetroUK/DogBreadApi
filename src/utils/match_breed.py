from openai import OpenAI
from src.config.settings import settings
from src.repositories.dog_api import fetch_breeds

client = OpenAI(api_key=settings.openai_api_key)

async def match_best_breed(user_preferences: str) -> str:
    breeds = await fetch_breeds()

    # Build a simple readable breed list
    breed_descriptions = "\n".join([
        f"- {breed.get('name')}: temperament={breed.get('temperament', 'N/A')}, "
        f"bred_for={breed.get('bred_for', 'N/A')}, "
        f"group={breed.get('breed_group', 'N/A')}, "
        f"lifespan={breed.get('life_span', 'N/A')}"
        for breed in breeds
    ])

    response = client.responses.create(
        model="gpt-4.1",
        instructions="You are a dog breed advisor. Based on the user's preferences, recommend the best breed match and explain why.",
        input=(
            f"User preferences: {user_preferences}\n\n"
            f"Available dog breeds:\n{breed_descriptions}"
        )
    )

    return response.output_text.strip()
