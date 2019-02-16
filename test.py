import requests as rq
from bs4 import BeautifulSoup as bs
from flask import Flask, request, render_template

app = Flask(__name__) # replace with wrapper

class Item:
    def __init__(self, item_tag):
        self.name = ....
        self.cost = ....

def generate_items(search):
    words = search.split(' ')
    str = 'https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&DEPA=0&Order=BESTMATCH&Description=' + '+'.join(words) + '&N=-1&isNodeId=1'

    page = rq.get(str)
    soup = bs(page.text, 'html.parser')
    item_containers = soup.find_all(class_='item-container')

    return [Item(i) for i in item_containers]

@app.route('/', methods=['GET', 'POST'])
def index(s=None):
    if(request.method == 'POST'):
        s = request.form['text']
        item_list = generate_items(s)
    return render_template('index.html', s=s)
