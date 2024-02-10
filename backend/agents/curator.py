import sys
import os

from datetime import datetime

# commonモジュールをインポートする
COMMON_MOD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../common"))
print("COMMON_MOD_DIR=", COMMON_MOD_DIR)
sys.path.append(COMMON_MOD_DIR)


from yka_langchain import yka_langchain_raw


class CuratorAgent:
    def __init__(self):
        pass

    def curate_sources(self, query: str, sources: list):
        """
        Curate relevant sources for a query
        :param input:
        :return:
        """
        prompt = [
            {
                "role": "system",
                "content": "You are a personal newspaper editor. Your sole purpose is to choose 5 most relevant article "
                "for me to read from a list of articles.\n ",
            },
            {
                "role": "user",
                "content": f"Today's date is {datetime.now().strftime('%d/%m/%Y')}\n."
                f"Topic or Query: {query}\n"
                f"Your task is to return the 5 most relevant articles for me to read for the provided topic or "
                f"query\n "
                f"Here is a list of articles:\n"
                f"{sources}\n"
                f"Please return nothing but a list of the strings of the URLs in this structure: ['url1',"
                f"'url2','url3','url4','url5'].\n ",
            },
        ]

        response = yka_langchain_raw(prompt)
        chosen_sources = response
        for i in sources:
            if i["url"] not in chosen_sources:
                sources.remove(i)
        return sources

    def run(self, article: dict):
        print("CuratorAgent start")
        article["sources"] = self.curate_sources(article["query"], article["sources"])
        print("CuratorAgent end")
        return article
