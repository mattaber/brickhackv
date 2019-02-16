import requests as rq
from bs4 import BeautifulSoup as bs
from flask import Flask, request, render_template

app = Flask(__name__) # replace with wrapper

def get_name(item_tag):
    return str(item_tag.find(class_='item-title').get_text())

def get_cost(item_tag):
    #return str(item_tag.find(class_='price').get_text())
    return "this would be the price"

def get_savings(item_tag):
    #return item_tag.find('price-save-percent').get_text()
    return "hel;lo world"

class Item:
    def __init__(self, item_tag):
        self.name       = get_name(item_tag)
        self.cost       = get_cost(item_tag)
        self.savings    = get_savings(item_tag)


def generate_items(search):
    words = search.split(' ')
    str = 'https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&DEPA=0&Order=BESTMATCH&Description=' + '+'.join(words) + '&N=-1&isNodeId=1'

    page = rq.get(str)
    soup = bs(page.text, 'html.parser')
    item_containers = soup.find_all(class_='item-container')

    return [Item(i) for i in item_containers]

@app.route('/', methods=['GET', 'POST'])
def index(item_names = [], item_costs = [], item_savings = []):
    if(request.method == 'POST'):
        s = request.form['text']
        item_list = generate_items(s)
        item_names      = [item.name for item in item_list]
        item_costs      = [item.cost for item in item_list]
        item_savings    = [item.savings for item in item_list]
    return render_template('index.html', item_names = item_names, item_costs = item_costs, item_savings = item_savings, length = len(item_names))
