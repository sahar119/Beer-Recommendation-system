from bs4 import BeautifulSoup as bs
import requests
import datetime
import aspose.words as aw
import csv
import re
import pandas as pd
from itertools import zip_longest


provinces = ['ab','bc','qc','mb','nl','ns','on','pei','sk','yt','nb']
def extract(province):
    url = f'https://www.beeradvocate.com/beer/top-rated/ca/{province}/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}
    r = requests.get(url, headers)  # go to website
    soup = bs(r.content, 'lxml')
    return soup

def transfom(soup):

    profiles = []
    tables = soup.find('table')
    spans = soup.find_all('span', class_ = 'muted')
    for table in tables.find_all('a'):
        profile = table.get('href') # I used getattr as my.text function was not working
        if profile is not None:
            profiles.append(profile)
    return [profiles]
#c= extract()

final_profile = []
for province in provinces:

      c = extract(province)
      main_list = transfom(c)[0][0::3]
      final_profile.append(main_list)

final_lists = []
for lists in final_profile:
    for i in lists:
        if i not in final_lists:
           final_lists.append(i)

def extract(name):
    url = f'https://www.beeradvocate.com{name}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}
    r = requests.get(url, headers)  # go to website
    soup = bs(r.content, 'lxml')
    return soup

def transfom(soup):

    Rating = []
    user_name = []
    images = []
    beer_name = []
    abv = []
    province = []
    country= []
    comments = []
    divs = soup.find_all(id='rating_fullview_content_2')
    divs_1 = soup.find_all(id='rating_fullview_container')
    spans = soup.find_all('span', class_ = 'muted')
    div_name = soup.find_all('div',class_ = 'titleBar')
    span_2 = soup.find_all('span', class_= 'Tooltip')
    dds  = soup.find_all('dd', class_= 'beerstats')
    elements = soup.find_all('img')

    for name in div_name:
        brand = getattr(name.find('h1'),'text',None)
        beer_name.append(brand)
    for element in elements:
        url= element['src']
        images.append(url)
    for span in span_2:
        per = getattr(span.find('b'),'text',None)
        abv.append(per)
    for dd in dds:
        pro = getattr(dd.find('a'),'text',None)
        cout=getattr(dd.select_one(":nth-child(2)"),'text',None)
        province.append(pro)
        country.append(cout)


    for div in divs:
        brand = getattr(div.find('b'),'text',None) # I used getattr as my.text function was not working
        if brand is not None:
            try:
                Rating.append(float(brand))
            except ValueError:
                    brand = getattr(div.find('span', class_='BAscore_norm'),'text',None)
                    if brand is not None:
                        Rating.append(float(brand))
    for div in divs_1:
        review = getattr(div.find('div',style='margin:10px 0px; padding:10px; border-left:2px solid #A9A9A9; font-size:11pt; line-height:1.4;'),'text',None)
        if review is None:
            comments.append(str('-'))
        else:
            comments.append(review)
    for div in divs:
        brand = getattr(div.find('a', class_='username'),'text',None) # I used getattr as my.text function was not working
        if brand is not None:
           user_name.append(brand)
    return [beer_name,user_name,Rating,comments,[abv[3]],[province[1]],[country[1]],[images[2]]]


# c=extract(name)
# main_list = transfom(c)
# print(main_list)


def zip_longest_repeating(*iterables):
    iters = [iter(i) for i in iterables]
    sentinel = object()
    vals = tuple(next(it, sentinel) for it in iters)
    if any(val is sentinel for val in vals):
        return
    yield vals
    while True:
        cache = vals
        vals = tuple(next(it, sentinel) for it in iters)
        if all(val is sentinel for val in vals):
            return
        vals = tuple(old if new is sentinel else new for old, new in zip(cache, vals))
        yield vals

#print(list(zip_longest_repeating(*main_list)))


for name in final_lists:
      c = extract(name)
      main_list = transfom(c)
      header = ['U', 'R']
      with open('C:\\Users\\15147\\PycharmProjects\\pythonProject\\Airbnb\\beer_final1.csv', 'a', newline='', encoding='UTF8') as f:
          writer = csv.writer(f)
          for items in list(zip_longest_repeating(*main_list)):
                if isinstance(items[-1], list):  # Check if last element is list.
                      writer.writerow(items)
                else:
                      writer.writerow(items)

f.close()
















