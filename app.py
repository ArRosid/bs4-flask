from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
from proxy_scraper import *

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/results')
def results():
    scraper = ProxyScraper()
    scraper.run()

    return render_template('results.html', proxies=scraper.results)


@app.route('/download')
def download():
    return send_from_directory('', 'proxy_list.csv', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
