import requests
from bs4 import BeautifulSoup

url = "https://www.imdb.com/search/title/?release_date=2019-01-01,&sort=num_votes,desc"

res = requests.get(url)

soup = BeautifulSoup(res.text, 'html.parser')

movies = soup.find_all("div", class_="lister-item mode-advanced")

titles = []
years = []
imdb_ratings = []
metascores = []
votes = []


for movie in movies:
    # get title & year
    if movie.find("div", class_="inline-block ratings-metascore") is not None:
        title = movie.h3.text
        title = title.replace("\n", " ").split()
        title.remove(title[0])
        year = title.pop(-1)
        title = " ".join(title)

        titles.append(title)
        years.append(year)

        # get imdb rating
        imdb_rating = float(movie.find("div", class_="inline-block ratings-imdb-rating").strong.text)
        imdb_ratings.append(imdb_rating)

        # get metascore
        m_score = float(movie.find("div", class_="inline-block ratings-metascore").span.text)
        metascores.append(m_score)

        # get votes
        vote = movie.find("span", attrs={"name": "nv"})["data-value"]
        votes.append(vote)

