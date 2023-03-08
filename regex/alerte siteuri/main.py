import requests
import bs4
import re
from newspaper import Article

class Parameters:
    def __init__(self):
        self.base_links = "./base_links.links"
        self.unvisited_links = "./unvisited_links.links"
        self.visited_links = "./visited_links.links"

class Alerts:
    def __init__(self):
        self.wordsToMatch = ["pisica", "paine", 'putin', "zelenski", "loto"]
        self.params = Parameters()
        self.isVisited = dict()
        for x in open(self.params.visited_links, "r").readlines():
            self.isVisited[x] = True

    def parse_html(self, html):
        return bs4.BeautifulSoup(html, "html.parser")

    def get_list_of_links(self):
        return [x.strip() for x in open(self.params.base_links, "r").readlines()]
        
    def get_aux_links(self, link):
        res = requests.get(link)
        content = str(self.parse_html(res.content))

        urls = re.findall('(https?:\/\/[^ "]*\.html)', content)
        urls = [*set(urls)]
        return urls

    def match_article(self, link):
        art = Article(link, language="ro")
        art.download()
        art.parse()
        content = art.text
        
        foundMatch = False
        for w in self.wordsToMatch:
            matches = re.findall(w, content, re.IGNORECASE)
            if len(matches) != 0:
                if not foundMatch:
                    print(f"S-au gasit la {link}")
                    foundMatch = True
                print(f"{len(matches)} potriviri pentru '{w}'")
        return foundMatch

    def run(self):
        unvis = open(self.params.unvisited_links, 'w')
        vis = open(self.params.visited_links, 'w')

        for x in self.get_list_of_links():
            for y in self.get_aux_links(x):
                unvis.write(y + '\n')
        unvis = open(self.params.unvisited_links, 'r+')
        for x in unvis.readlines():
            x = x.strip()
            if x not in self.isVisited:
                self.match_article(x)
                self.isVisited[x] = True
                vis.write(x + '\n')

                new_links = self.get_aux_links(x)
                l = len(new_links)
                for i in range(l):
                    if new_links[i] not in self.isVisited:
                        unvis.write(new_links[i] + '\n')


if __name__ == "__main__":
    a = Alerts()
    a.run()
    


