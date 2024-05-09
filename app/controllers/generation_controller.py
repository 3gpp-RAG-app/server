'''
import os

import requests, json



def generate_response(query, ret_list):
    
    references = "\n".join([f"Reference Text: {ret[1]}, Reference Doc Title: {ret[2]}" for ret in ret_list])


    url = "http://localhost:11434/api/generate"


    prompt = f'Your task is to response to the user only based on the provided reference. If the answer can not be found in the given reference. respond "I could not find an answer.",Here is the refrences: {references}, here is user question:{query}'
    payload = {
        "model":  "mistral",
        "prompt": prompt,
        "temperature": 0,
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    response_text=''
    for line in response.text.split('\n'):
            if line.strip() != '':
                data = json.loads(line)
                response_text += data['response']

    return response_text'''
    
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")


def generate_response(query, ret_list):
    
    references = "\n".join([f"Reference Text: {ret[2]}, Reference Doc Title: {ret[3]}" for ret in ret_list])

    completion = client.chat.completions.create(
        model="gpt-4-turbo-preview",
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
