import requests as rq
from bs4 import BeautifulSoup as bs
from flask import Flask, request, render_template

app = Flask(__name__) # replace with wrapper

def has_savings(item_tag):
    return item_tag.find(class_="price-save-percent") != None

def get_image(item_tag):
    return "http:" + str(item_tag.find('img')['src'])

def get_name(item_tag):
    return str(item_tag.find(class_='item-title').get_text())

def get_cost(item_tag):
    if("|" in str(item_tag.find(class_='price-current').get_text())):
        return str(item_tag.find(class_='price-current').get_text())[4:]
    return str(item_tag.find(class_='price-current').get_text())

def get_savings(item_tag):
    return str(item_tag.find(class_="price-save-percent").get_text()) + " off"

def get_link(item_tag):
    return str(item_tag.find(class_='item-title')['href'])

class Item:
    def __init__(self, item_tag):
        self.tag        = item_tag
        self.image      = get_image(item_tag)
        self.name       = get_name(item_tag)
        self.cost       = get_cost(item_tag)
        self.savings    = get_savings(item_tag)
        self.link       = get_link(item_tag)


def generate_items(search):
    words = search.split(' ')
    str = 'https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&DEPA=0&Order=BESTMATCH&Description=' + '+'.join(words) + '&N=4803&isNodeId=1'

    page = rq.get(str)
    soup = bs(page.text, 'html.parser')
    item_containers = soup.find(class_='items-view is-grid').find_all(class_='item-container')

    return [Item(i) for i in item_containers if has_savings(i)]

@app.route('/', methods=['GET', 'POST'])
def index(item_list = []):
    if(request.method == 'POST'):
        s = request.form['text']
        item_list = generate_items(s)
        item_list.sort(key = lambda x : int(x.savings[:-5]), reverse=True)
    return render_template('index.html', item_list = item_list, length = len(item_list))
