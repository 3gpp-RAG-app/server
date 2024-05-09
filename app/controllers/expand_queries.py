from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")


def expand_query(query):

    completion = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {
                "role": "system",
                "content": """Your task is to convert user questions into database queries. \
                You have access to a database of 3GPP technical specifications. Your objective is to transform user questions into effective database queries. Follow these guidelines: \
                Query Expansion: \
                    1. If there are multiple common ways of phrasing a user question or common synonyms for key words, provide multiple versions of the query with different phrasings. \
                    2. Expand queries to cover relevant variations. \

                Handling Acronyms and Unfamiliar Words: \
                If you encounter acronyms or unfamiliar terms, do not attempt to rephrase them. Leave them as-is. \
                Output Format: \
                Return at least three versions of the query. \
                Include the original user query as the fourth item in the returned list. \

                            """,
            },
            {"role": "user", "content": query},
        ],
        temperature=0,
        max_tokens=3000,
    )

    response_message = completion.choices[0].message
    query_list = []
    lines = response_message.content.split("\n")

    lines = [line.split(".")[1].strip() for line in lines]
    query_list.extend(lines)
    print(query_list)

    return query_list
