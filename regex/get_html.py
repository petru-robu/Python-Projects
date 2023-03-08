import bs4
import requests

def html_parser(link):
    return bs4.BeautifulSoup(link, "html.parser")

def get_html(link):
    res = requests.get(link)
    return str(html_parser(res.content))

link = "https://www.digi24.ro/stiri/actualitate"
print(get_html(link))