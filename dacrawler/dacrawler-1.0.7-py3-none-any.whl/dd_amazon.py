#-------------------------------------------------------------------------
# Copyright (c) DATA ARTIST
# All rights reserved.
#
# MIT License:
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#--------------------------------------------------------------------------
'''
Created on 2018. 7. 25.

@author: kim
'''

from bs4 import BeautifulSoup
from bs4.builder import _htmlparser
import pandas as pd
import re
import urllib
from datetime import datetime
from datetime import date
import time
import logging
import argparse

class DDAmazon ():
    
    def __init__ (self, html):
        self.html = html
        
    def test (self) :
        return 'hello Parse'
    
    def salesPage(self):

        ''' DataFrame List '''
        rank_list=[]
        product_id_list=[]
        product_list=[]
        maker_list=[]
        price_list=[]
        review_list=[]
        star_list=[]

        try:
            ''' 1ページ目 '''
            #r = requests.get(url, headers=self.headers)
            #html = requests.get("https://www.amazon.co.jp/gp/bestsellers/electronics/387464011/#2")
            soup = BeautifulSoup(self.html.text, 'lxml')

            '''title'''
            title=soup.find('h1', id='zg_listTitle').text

            '''find top 20 items'''
            itemList = soup.find_all("div", class_="zg_itemRow")

            for item in itemList:

                ''' star '''
                stars = item.find_all("span", class_="a-icon-alt")
                if stars:
                    starText = [star.text for star in stars]
                    starText = list(filter(lambda text: re.match("5つ星のうち", text), starText))

                    if starText:
                        star_list.append(starText[0].replace("5つ星のうち","").strip())
                    else:
                        star_list.append("")
                else:
                    star_list.append("")

                ''' rank '''
                rankNum = item.find("span", class_="zg_rankNumber")
                if rankNum:
                    rank_list.append(rankNum.text.replace(".","").strip())
                else:
                    rank_list.append(rankNum)

                ''' productName and Maker '''
                productName = item.find("div", class_="p13n-sc-truncate p13n-sc-line-clamp-2")
                if productName:
                    product_list.append(productName.text.strip())
                    maker_list.append(productName.text.split()[0])
                else:
                    product_list.append("")
                    maker_list.append("")

                ''' product id '''
                col = item.find('div', class_='a-fixed-left-grid-col a-col-right')
                if col:
                    pUrl = col.find('a', class_='a-link-normal')
                    if pUrl:
                        matched = re.findall("(?<=dp/)(.+?)(?=/|$|\?)", pUrl['href'])
                        matRep = matched[0]
                        product_id_list.append(matRep)
                    else:
                        product_id_list.append("")
                else:
                    product_id_list.append("")


                ''' price '''
                price = item.find("span", class_="p13n-sc-price")
                if price:
                    price_list.append(price.text.replace("￥","").strip())
                else:
                    price_list.append("")

                ''' review '''
                review = item.find("a", class_="a-size-small a-link-normal")
                if review:
                    review_list.append(review.text)
                else:
                    review_list.append("")


                unix_time = datetime.now().strftime('%s')
                unix_time = str(date.today())

            df_page1 = pd.DataFrame({
                        'page_title': title,
                        'time': unix_time,
                        'rank' : rank_list,
                        'maker' : maker_list,
                        'product_id' : product_id_list,
                        'product_name' : product_list,
                        'price': price_list,
                        'review': review_list,
                        'star': star_list
                     })

            return df_page1
        except Exception as e:
            logging.exception("Exception!")
            pass
    
if  __name__=="__main__" :
    prs = Parse(
        html          = ""
    )
    ret = prs.salesPage()
    print(ret)
