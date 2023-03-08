import psycopg2, bs4
import requests, re
from newspaper import Article
import chardet

regexes = {
    'default': '(https?:\/\/[^ "]*\.html)',
    'digi': 'stiri[^ "]*'
}


class DataBaseManager:
    def __init__(self):
        self.db_name = "alert-system"
        self.db_user = "postgres"
        self.db_password = "admin"
        self.host = '127.0.0.1'
        self.port = '54321'

        self.conn = psycopg2.connect(
            database = self.db_name,
            user = self.db_user,
            password = self.db_password,
            host = self.host,
            port = self.port
        )

    def __del__(self):
        self.conn.close()

    def query(self, q):
        cursor = self.conn.cursor()
        cursor.execute(q)
        self.conn.commit()
    
    def fetch_content_from_table(self, table_name):
        sel = f"SELECT * FROM {table_name}"
        cursor = self.conn.cursor()
        cursor.execute(sel)
        return cursor.fetchall()

db = DataBaseManager()

class URLTable:
    def __init__(self, name):
        self.table_name = name
        create_one_col = f'''
            CREATE TABLE IF NOT EXISTS {name.upper()}
            (
                URL TEXT NOT NULL
            );
        '''
        db.query(create_one_col)

    def post_URL(self, url_to_insert):
        insert_url_in_db = f'''
            INSERT INTO {self.table_name}
            VALUES
            (
                '{url_to_insert}'
            );
        '''
        db.query(insert_url_in_db)

    def get_url_list(self):
        content = db.fetch_content_from_table(self.table_name)
        res = []
        for link in content:
            res.append(link[0])
        return res
    
    def clear(self):
        clear_table = f'''
           TRUNCATE TABLE {self.table_name};
        '''
        db.query(clear_table)

class URLUtil:
    def __init__(self, link):
        self.url = link
        self.art = Article(self.url, language="ro")
        self.art.download()
        self.art.parse()
    
    def parse_html(self, html):
        return bs4.BeautifulSoup(html, "html.parser")

    def parse_romanian(self, content):
        content = content.lower()
        for ch in content:
            match ch:
                case 'ș':
                    content = content.replace(ch,'s')
                case 'ț':
                    content = content.replace(ch,'t')
                case 'ă':
                    content = content.replace(ch,'a')
                case 'â':
                    content = content.replace(ch,'a')
                case 'î':
                    content = content.replace(ch,'i')
        return content
                    
    def get_aux_urls(self, regex=regexes['default']):
        res = requests.get(self.url)
        content = str(self.parse_html(res.content))

        urls = re.findall(regex, content)
        urls = [*set(urls)]
        return urls
    
    def match(self, word):
        raw_text = self.art.text
        raw_text = self.parse_romanian(raw_text)
        
        matches = re.findall(word, raw_text, re.IGNORECASE)
        return len(matches)

class Alerts:
    def __init__(self):
        self.vis_table = URLTable("visited_links")
        self.base_table = URLTable("base_links")
        self.wordList = ["putin", "zelenski"]

        self.base_table.clear()
        self.base_table.post_URL("https://stirileprotv.ro/ultimele-stiri/")

        self.url_queue = self.base_table.get_url_list()
        self.is_visited = set(self.vis_table.get_url_list())

    def bfs(self):
        while len(self.url_queue) > 0:
            url = self.url_queue.pop(0)
            curr_url = URLUtil(url)

            self.vis_table.post_URL(url)
            self.is_visited.add(url)

            print(f"Incepe cercetarea la {curr_url.url}")
            for w in self.wordList:
                print(f"S-au gasit {curr_url.match(w)} ap. pentru '{w}'")
                
            additional_urls = curr_url.get_aux_urls()
            no_of_new_url = 0
            for new_url in additional_urls:
                if new_url not in self.is_visited:
                    no_of_new_url+=1
                    self.url_queue.append(new_url)

            print(f"S-au adunat {len(additional_urls)}|{no_of_new_url} noi linkuri de aici")
            print('\n')


main = Alerts()
main.bfs()