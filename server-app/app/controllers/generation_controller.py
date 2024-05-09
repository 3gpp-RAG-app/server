from openai import OpenAI
from config.settings import Config

client = OpenAI()
client.api_key = Config.OPENAI_API_KEY


def generate_response(query, ret_list):
    
    references = "\n".join([f"Reference Text: {ret[2]}, Reference Doc Title: {ret[3]}" for ret in ret_list])

    completion = client.chat.completions.create(
        model=Config.OPENAI_GEN_ENGINE,
        messages=[
            {
                "role": "system",
                "content": f'You are a 3GPP specialized assistant that search in the provided refrence and answers to the user only based on the provided reference.' 
                            f'If the answer can not be found in the given reference. respond "I could not find an answer."'
                            f'Here is the reference between brackets:[{references}].',
            },
            {"role": "user", "content": query},
        ],
        temperature=0.2,
        max_tokens=3000,
    )

    response_message = completion.choices[0].message

    return response_message.content
