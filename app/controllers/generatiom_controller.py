from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")


def generate_response(query, search_ret):

    completion = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {
                "role": "system",
                "content": f'You are a 3GPP specialized assistant that anwers to the user only based on the provided reference.' 
                            f'Let the user know if the answer cannot be found in the given reference. respond "I could not find an answer." ,  Here is the reference: {search_ret}.',
            },
            {"role": "user", "content": query},
        ],
        temperature=0.2,
        max_tokens=2000,
        stop=None,
    )

    response_message = completion.choices[0].message

    return response_message.content
