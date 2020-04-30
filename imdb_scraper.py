import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep, time
from random import randint
from IPython.core.display import clear_output
from warnings import warn

# defina page for the url
pages = [p * 50 + 1 for p in range(72)]

# preparing the monitoring of the loop
start_time = time()
request = 0

titles = []
years = []
imdb_ratings = []
metascores = []
votes = []

for p in pages:
    url = f"https://www.imdb.com/search/title/?release_date=2019-01-01,&sort=num_votes,desc&start={p}"
    res = requests.get(url)

    # pause the loop
    sleep(randint(2, 5))

    # monitor the request
    request += 1
    elapsed_time = time() - start_time
    print(f'Request:{request}; Frequency:{request / elapsed_time} requests/s')
    clear_output(wait=True)

    if res.status_code != 200:
        warn(f'Request: {request}; Status code: {res.status_code}')

    # Parse the output
    soup = BeautifulSoup(res.text, 'html.parser')

    movies = soup.find_all("div", class_="lister-item mode-advanced")

    for movie in movies:
        # get title & year
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
        try:
            # get metascore
            m_score = float(movie.find("div", class_="inline-block ratings-metascore").span.text)
            metascores.append(m_score)
        except:
            metascores.append(None)

        # get votes
        vote = movie.find("span", attrs={"name": "nv"})["data-value"]
        votes.append(vote)

df = pd.DataFrame({
    'titles': titles,
    'years': years,
    'imdb_ratings': imdb_ratings,
    'metascores': metascores,
    'votes': votes
})
#
# # convert year to integer
# df.loc[:, 'years'] = df['years'].str[-5:-1].astype(int)
#
# # add n_imdb columns
# df["n_imdb"] = df["imdb_ratings"] * 10
#
# print(df.info())

df.to_csv("imdb_ratings.csv")

print(f"finish in {time() - start_time} seconds")
