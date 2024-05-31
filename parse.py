import requests as rq
from bs4 import BeautifulSoup
from datetime import datetime

class Program:
    def __init__(self, url: str):
        self.count = 1
        r = rq.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        if r.status_code == 200:
            self.title = soup.find("h1", class_="post-header__title title-1 pb-1").text
            self.category = soup.select_one(".movie-info__field > .programm-day__title").text
            self.genre = [x.text for x in soup.find_all("span", class_="programm-day__title")]
            self.kp_r, self.imdb_r = get_rating(self.title) 
        else:
            self.title = "Невозможно получить детальную информацию"


   
def get_list_programs(url: str, day = datetime.now()):
    programs_list = []
    r = rq.get(url + str(day))
    soup = BeautifulSoup(r.text, "lxml")
    day_programs = soup.find_all("a", class_="programm-list__title")
    time = soup.find_all("div", class_="programm-list__time")
    for p in zip(time, day_programs):
        programs_list.append(p[0].text + " - " + str(p[1].text).strip())
    return programs_list

def get_actual_programs_info(ch):
    programs_dict = {}
    for c, href in ch.items():
        r = rq.get(href + str(datetime.now()))
        soup = BeautifulSoup(r.text, "lxml")
        p = soup.find("li", class_="is-on-air")
        p = p.find("a")
        programs_dict[c] = Program(p["href"])
    return programs_dict

def get_next_page_of_tvprogamm(page_num):
    url = "https://www.comboplayer.ru/tv-guide/city/sankt-peterburg/today?page="
    r = rq.get(url + str(page_num))
    soup = BeautifulSoup(r.text, "lxml")

    channels = soup.find_all("a", class_="guide-channel__title")
    return channels

def get_main_channels(num_of_channels=20):
    ch = dict()
    page_num = 1
    while len(ch) < num_of_channels:
        channels = get_next_page_of_tvprogamm(page_num)
        for c in channels: 
            ch[(c.text.lstrip().rstrip()).upper()] = c["href"].rsplit("today")[0]
            if len(ch) == num_of_channels:
                break
        page_num += 1
    return ch

def get_id_from_kp(query: str):
    query = query.lower()
    query = query.replace(" ", "+")
    url = f"https://www.kinopoisk.ru/index.php?kp_query={query}"
    r = rq.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "lxml")
        if soup is not None:
            soup = soup.find("div", class_="most_wanted")
            soup = None if soup is None else soup.find("p", class_="pic")
            soup = None if soup is None else soup.find("a")
            # print(soup["data-url"])
        return 0 if soup is None else soup["data-id"]
    else:
        return 0

def get_url_from_kp(query: str):
    query = query.lower()
    query = query.replace(" ", "+")
    url = f"https://www.kinopoisk.ru/index.php?kp_query={query}"
    r = rq.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "lxml")
        if soup is not None:
            soup = soup.find("div", class_="most_wanted")
            soup = None if soup is None else soup.find("p", class_="pic")
            soup = None if soup is None else soup.find("a")
        return 0 if soup is None else soup["data-url"]
    else:
        return 0

def get_rating(title):
    id = get_id_from_kp(title)
    if id == 0:
        return None, None
    url = f"https://rating.kinopoisk.ru/{id}.xml"
    # print(url)
    r = rq.get(url)
    soup = BeautifulSoup(r.text, "xml")

    kp_r = None if soup.find("kp_rating") is None else float(soup.find("kp_rating").text)
    imdb_r = None if soup.find("imdb_rating") is None else float(soup.find("imdb_rating").text)
    #print(url, soup.find("kp_rating").text, soup.find("imdb_rating").text)
    return(kp_r, imdb_r)

def get_actual_programs(ch):
    programs_list = []
    for c, href in ch.items():
        r = rq.get(href + str(datetime.now()))
        soup = BeautifulSoup(r.text, "lxml")
        p = soup.find("li", class_="is-on-air")
        p = p.find("a")
        programs_list.append(c + ": " + p.text.strip())
    return programs_list

def main():
    kp = get_rating("Трое в лодке")
    print(kp)