import requests
from bs4 import BeautifulSoup
import json
from botapp.models import Words


URL = "https://1000mostcommonwords.com/1000-most-common-uzbek-words/"

words = []

def get_words():
    request = requests.get(URL)
    soup = BeautifulSoup(request.text, "html.parser")

    tables = soup.find_all("tr")
    for table in tables:
        datas = table.find_all("td")
        words.append({"uzbek": datas[1].text, 
                      "english": datas[2].text,
                      })
        with open("words.json", "w") as f:
            json.dump(words, f)


def read_words():
    with open("words.json", "r") as f:
        data = json.load(f)
        return data
        
def add_words():
    print(Words.objects.all())
    


def main():
    # read_words()
    # get_words()
    add_words()
    print("ok")
    pass

if __name__ == "__main__":
    main()