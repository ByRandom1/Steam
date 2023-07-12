import numpy as np
import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd


def get_reviewscore(review, language):
    gamereview = []
    for i in range(len(review)):
        try:
            if language == 'English':
                score = re.search('br&gt;(\d\d)%', str(review[i]))[1]
            elif language == 'Chinese':
                score = re.search('有\s(\d\d)%', str(review[i]))[1]
            else:
                score = ''
        except:
            score = ''
        gamereview.append(score)
    return gamereview


def get_reviewers(review, language):
    reviewers = []
    for i in range(len(review)):
        try:
            if language == 'English':
                ppl = (re.search('the\s(.*?)(\s)user', str(review[i]))[1])
            elif language == 'Chinese':
                ppl = (re.search('的\s(.*?)(\s)篇', str(review[i]))[1])
            else:
                ppl = ''
        except:
            ppl = ''
        reviewers.append(ppl)
    return reviewers


def get_finalprice(price):
    finalprice = []
    for i in range(len(price)):
        pricelist = int(re.search('final(\W+?)(\d+)(\W)', str(price[i]))[2]) / 100
        finalprice.append(pricelist)
    return finalprice


def get_price(price, region):
    oripricelist = []
    for i in range(len(price)):
        try:
            oripricelist.append(price[i].find_all(class_="col search_price responsive_secondrow")[0].text)
        except:
            oripricelist.append(price[i].find_all(class_="col search_price discounted responsive_secondrow")[0].text)

    ori_price = []
    for i in range(len(oripricelist)):
        try:
            search = re.search('Free', oripricelist[i])[0].replace('Free', '0')
        except:
            if oripricelist[i] == '\n':
                search = ''
            else:
                try:
                    if region == 'China':
                        search = re.search('¥.*?(\d+\.\d+)\D', oripricelist[i])[1]
                    elif region == 'HongKong':
                        search = re.search('HK.*?(\d+\.\d+)\D', oripricelist[i])[1]
                    elif region == 'Argentina':
                        search = re.search('ARS\$.*?(\d+\.?\d+,?\d+)\D', oripricelist[i])[1]
                    elif region == 'Turkey':
                        search = re.search('(\d+,?\d+).*?TL', oripricelist[i])[1]
                    else:
                        search = ''
                except:
                    search = ''
        ori_price.append(search)
    return ori_price


def get_discount(price):
    discountlist = []
    for i in range(len(price)):
        discountlist.append(price[i].find_all(class_="col search_discount responsive_secondrow")[0].text)

    discount_ = []
    for i in range(len(discountlist)):
        try:
            search = re.search('-(\d+)%', discountlist[i])[1]
        except:
            search = ''
        discount_.append(search)
    return discount_


gamename = []
gamereview = []
gamereviewers = []
gamerelease = []
final_price = []
oriprice = []
discount = []
appid = []
website = []


# 只显示打折；隐藏免费；语言：简中繁中；游戏类型：游戏；单人；排除VR独占；系统：WIN
def get_all(start, count):
    url = 'https://store.steampowered.com/search/results/?query&start=' + str(start) + '&count=' + str(
        count) + '&dynamic_data=&sort_by=_ASC&snr=1_7_7_globaltopsellers_7&specials=1&hidef2p=1&filter=globaltopsellers&supportedlang=schinese%2Ctchinese&category1=998&category3=2&unvrsupport=401&os=win&infinite=1'
    content = requests.get(url).content
    print('get ', start, '--', start + count, ' succ')
    jsontext = json.loads(content)
    soup = BeautifulSoup(jsontext['results_html'], 'html.parser')

    name = soup.find_all('span', class_='title')
    for i in name:
        gamename.append(i.text)

    review = soup.find_all('div', class_='col search_reviewscore responsive_secondrow')
    getreview = get_reviewscore(review, 'English')
    for i in getreview:
        gamereview.append(i)
    getreviewers = get_reviewers(review, 'English')
    for i in getreviewers:
        gamereviewers.append(i)

    listdate = soup.find_all('div', class_='col search_released responsive_secondrow')
    for i in listdate:
        gamerelease.append(i.text)

    price = soup.find_all('div', class_='col search_price_discount_combined responsive_secondrow')
    getprice = get_price(price, 'HongKong')
    for i in getprice:
        oriprice.append(i)
    getfinalprice = get_finalprice(price)
    for i in getfinalprice:
        final_price.append(i)
    getdiscount = get_discount(price)
    for i in getdiscount:
        discount.append(i)

    href = soup.find_all(class_='search_result_row ds_collapse_flag')
    for i in range(len(href)):
        appid.append(eval(soup.find_all(class_='search_result_row ds_collapse_flag')[i].attrs['data-ds-appid']))
        website.append(soup.find_all(class_='search_result_row ds_collapse_flag')[i].attrs['href'])


def parse_all(filename, region):
    soup = BeautifulSoup(open(filename), 'html.parser')

    name = soup.find_all('span', class_='title')
    for i in name:
        gamename.append(i.text)

    review = soup.find_all('div', class_='col search_reviewscore responsive_secondrow')
    getreview = get_reviewscore(review, 'Chinese')
    for i in getreview:
        gamereview.append(i)
    getreviewers = get_reviewers(review, 'Chinese')
    for i in getreviewers:
        gamereviewers.append(i)

    listdate = soup.find_all('div', class_='col search_released responsive_secondrow')
    for i in listdate:
        gamerelease.append(i.text)

    price = soup.find_all('div', class_='col search_price_discount_combined responsive_secondrow')
    getprice = get_price(price, region)
    for i in getprice:
        oriprice.append(i)
    getfinalprice = get_finalprice(price)
    for i in getfinalprice:
        final_price.append(i)
    getdiscount = get_discount(price)
    for i in getdiscount:
        discount.append(i)

    href = soup.find_all(class_='search_result_row ds_collapse_flag')
    for i in range(len(href)):
        appid.append(eval(soup.find_all(class_='search_result_row ds_collapse_flag')[i].attrs['data-ds-appid']))
        website.append(soup.find_all(class_='search_result_row ds_collapse_flag')[i].attrs['href'])


def run(type, total_num, region):
    if type == 'global':
        for num in np.arange(0, total_num, 100):
            if total_num - num >= 100:
                get_all(num, 100)
            else:
                get_all(num, total_num - num)
    else:
        for i in range(total_num / 25 + 1):
            parse_all('Steam 搜索' + str(i + 1) + str(region[0]) + '.html', region)


# https://store.steampowered.com/search/?supportedlang=schinese%2Ctchinese&category1=998&category3=2&unvrsupport=401&os=win&specials=1&hidef2p=1&ndl=1&ignore_preferences=1&page=1
type = input("global/file:")
total_num = input("total num:")
region = input("China/Argentina/Turkey/HongKong:")
run(type, int(total_num), region)

df = pd.DataFrame(data=[gamename, gamereview, gamereviewers, final_price, discount, oriprice, gamerelease, appid, website]).T
df.columns = ['name', 'review_score', 'reviewers', 'final_price', 'discount', 'ori_price', 'release_date', 'id', 'link']

df.to_csv('Steam' + '_' + type + '_' + total_num + '_' + region + '.csv', encoding='utf_8_sig')
