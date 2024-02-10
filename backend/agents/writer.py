import sys
import os
from datetime import datetime
import json5 as json

# commonモジュールをインポートする
COMMON_MOD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../common"))
print("COMMON_MOD_DIR=", COMMON_MOD_DIR)
sys.path.append(COMMON_MOD_DIR)


from yka_langchain import yka_langchain_raw


sample_json = """
{
  "title": title of the article,
  "date": today's date,
  "paragraphs": [
    "paragraph 1",
    "paragraph 2",
    "paragraph 3",
    "paragraph 4",
    "paragraph 5",
    ],
    "summary": "2 sentences summary of the article"
}
"""

sample_revise_json = """
{
    "paragraphs": [
        "paragraph 1",
        "paragraph 2",
        "paragraph 3",
        "paragraph 4",
        "paragraph 5",
    ],
    "message": "message to the critique"
}
"""


class WriterAgent:
    def __init__(self):
        pass

    def writer(self, query: str, sources: list):
        prompt = [
            {
                "role": "system",
                "content": "You are a newspaper writer. Your sole purpose is to write a well-written article about a "
                "topic using a list of articles.\n ",
            },
            {
                "role": "user",
                "content": f"Today's date is {datetime.now().strftime('%d/%m/%Y')}\n."
                f"Query or Topic: {query}"
                f"{sources}\n"
                f"Your task is to write a critically acclaimed article for me about the provided query or "
                f"topic based on the sources.\n "
                f"Please return nothing but a JSON in the following format:\n"
                f"{sample_json}\n ",
            },
        ]

        response = yka_langchain_raw(prompt)
        print("response=", response)
        return json.loads(response)

    def revise(self, article: dict):
        prompt = [
            {
                "role": "system",
                "content": "You are a newspaper editor. Your sole purpose is to edit a well-written article about a "
                "topic based on given critique\n ",
            },
            {
                "role": "user",
                "content": f"{str(article)}\n"
                f"Your task is to edit the article based on the critique given.\n "
                f"Please return json format of the 'paragraphs' and a new 'message' field"
                f"to the critique that explain your changes or why you didn't change anything.\n"
                f"please return nothing but a JSON in the following format:\n"
                f"{sample_revise_json}\n ",
            },
        ]

        response = yka_langchain_raw(prompt)
        response = json.loads(response)
        print(f"For article: {article['title']}")
        print(f"Writer Revision Message: {response['message']}\n")
        return response

    def run(self, article: dict):
        print("WriterAgent start")
        critique = article.get("critique")
        if critique is not None:
            article.update(self.revise(article))
        else:
            article.update(self.writer(article["query"], article["sources"]))
        print("WriterAgent end")
        return article
