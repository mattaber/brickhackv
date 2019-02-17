import requests as rq
from bs4 import BeautifulSoup as bs
from flask import Flask, request, render_template

app = Flask(__name__) # replace with wrapper

def has_savings(item_tag, website):
    if(website == "Newegg"):
        return item_tag.find(class_="price-save-percent") != None
    elif(website == "Amazon"):
        # This is going to involve some calculations
        return True

def get_image(item_tag, website):
    if(website == "Newegg"):
        return "http:" + str(item_tag.find('img')['src'])
    elif(website == "Amazon"):
        return ""#"http:" + str(item_tag.find('img')['src'])

def get_name(item_tag, website):
    if(website == "Newegg"):
        return str(item_tag.find(class_='item-title').get_text())
    elif(website == "Amazon"):
        return ""#str(item_tag.find(class_='a-size-medium s-inline s-access-title a-text-normal')['data-attribute'])

def get_cost(item_tag, website):
    if(website == "Newegg"):
        temp_str = str(item_tag.find(class_='price-current').get_text())
        if("|" in temp_str):
            temp_str = temp_str[4:]
        return temp_str
    elif(website == "Amazon"):
        #print("UHH = " + str(item_tag.find('span', {'class' : 'a-row a-spacing-none'}).get_text()))
        return "" #str(item_tag.find('span', {'class' : 'a-row a-spacing-none'}).get_text())

def get_savings(item_tag, website):
    if(website == "Newegg"):
        return str(item_tag.find(class_="price-save-percent").get_text()) + " off"
    elif(website == "Amazon"):
        # This is going to require some calculations
        return ""

def get_link(item_tag, website):
    if(website == "Newegg"):
        return str(item_tag.find(class_='item-title')['href'])
    elif(website == "Amazon"):
        return ""#str(item_tag.find(class_='a-link-normal s-access-detail-page s-color-twister-title-link a-text-normal')['href'])

class Item:
    def __init__(self, item_tag, website):
        self.tag        = item_tag
        self.image      = get_image(item_tag, website)
        self.name       = get_name(item_tag, website)
        self.cost       = get_cost(item_tag, website)
        self.savings    = get_savings(item_tag, website)
        self.link       = get_link(item_tag, website)


def generate_items(search, website):
    words = search.split(' ')
    if(website == "Newegg"):
        str = 'https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&DEPA=0&Order=BESTMATCH&Description=' + '+'.join(words) + '&N=4803&isNodeId=1'

        page = rq.get(str)
        soup = bs(page.text, 'html.parser')
        item_containers = soup.find(class_='items-view is-grid').find_all(class_='item-container')
    elif(website == "Amazon"):
        str = "https://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=" + '+'.join(words)

        page = rq.get(str)
        soup = bs(page.text, 'html.parser')
        item_containers = soup.find(class_="a-row s-result-list-parent-container").find_all(class_='s-item-container') # ISSUE: THIS PRODUCES AN EMPTY LIST; JAVASCRIPT PROBABLY RENDERS THE HTML :(
        print(item_containers)

    return [Item(i,website) for i in item_containers if has_savings(i,website)]

@app.route('/', methods=['GET', 'POST'])
def index(item_list = []):
    if(request.method == 'POST'):
        s = request.form['text']
        #item_list = generate_items(s)
        temp_list1 = generate_items(s, "Newegg")
        temp_list2 = generate_items(s, "Amazon")
        item_list = temp_list2
        item_list.sort(key = lambda x : int(x.savings[:-5]), reverse=True)
    #prices = [float(item.cost[item.cost.find("$")+1:item.cost.find(".")+3]) for item in item_list]
    #min_price = min(prices)                   # Useful for displaying the lowest item in the html
    #min_price_index = prices.index(min_price) # ^
    return render_template('index.html', item_list = item_list, length = len(item_list))
