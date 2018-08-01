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

import boto3

import requests
from bs4 import BeautifulSoup
from bs4.builder import _htmlparser

class Scrap ():
    '''
    web scapper
    '''
    def __init__ (self):
        #self.url = url
        self.headers  = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"}
        
    def test (self) :
        return 'hello Scrap'
    
    def url_scraping(self, url) :
        
        html = requests.get(url, headers=self.headers)
        #html_dic[url] = html.content
        return html
    
if  __name__=="__main__" :
    scp = Scrap(
        url = [
            "https://www.amazon.co.jp/gp/bestsellers/electronics/387464011/"
        ],
    )
    ret = scp.url_scraping()
    print(ret)
 

 
'''
 # amazong_top_selling -----
0 0 * * 0 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/electronics/387464011/ > $HOME/logs/DSLR.log 2>$HOME/logs/errlogs/DSLR_err.log &
0 3 * * 0 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/beauty/170092011/ > $HOME/logs/DSLR.log 2>$HOME/logs/errlogs/lotion.log &
0 6 * * 0 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/electronics/387455011/ > $HOME/logs/compact_digital_camera.log 2>$HOME/logs/errlogs/compact_digital_camera_err.log &
0 12 * * 0 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/electronics/2285020051/ > $HOME/logs/mirrorless_camera.log 2>$HOME/logs/errlogs/mirrorless_camera_err.log &
0 18 * * 0 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/electronics/3371371/ > $HOME/logs/digital_camera.log 2>$HOME/logs/errlogs/digital_camera_err.log &
0 0 * * 1 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/electronics/84825051/ > $HOME/logs/electronic_heater.log 2>$HOME/logs/errlogs/electronic_heater_err.log &
0 3 * * 1 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/kitchen/2276751051/ > $HOME/logs/DSLR.log 2>$HOME/logs/errlogs/toaster.log &
0 6 * * 1 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/electronics/3477981/ > $HOME/logs/head_phone.log 2>$HOME/logs/errlogs/head_phone_err.log &
#0 9 * * 1 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/beauty/5263261051 > $HOME/logs/head_phone.log 2>$HOME/logs/errlogs/shampoo_conditioner_set.log &
0 12 * * 1 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/pet-supplies/2155179051/ > $HOME/logs/dog_food.log 2>$HOME/logs/errlogs/dog_food_err.log &
0 15 * * 1 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/food-beverage/2436199051/ > $HOME/logs/dog_food.log 2>$HOME/logs/errlogs/soup.log &
0 18 * * 1 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/food-beverage/71323051/ > $HOME/logs/sweets.log 2>$HOME/logs/errlogs/sweets_err.log &
#0 21 * * 1 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/beauty/169694011 > $HOME/logs/head_phone.log 2>$HOME/logs/errlogs/hair_treatment.log &
0 0 * * 2 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/food-beverage/71458051/ > $HOME/logs/tea.log 2>$HOME/logs/errlogs/tea_err.log &
0 3 * * 2 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/beauty/170113011/ > $HOME/logs/DSLR.log 2>$HOME/logs/errlogs/moisturizer.log &
0 6 * * 2 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/food-beverage/4844225051/ > $HOME/logs/mineral_water.log 2>$HOME/logs/errlogs/mineral_water_err.log &
#0 9 * * 2 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/beauty/169747011 > $HOME/logs/head_phone.log 2>$HOME/logs/errlogs/hair_growth.log &
0 12 * * 2 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/food-beverage/71456051/ > $HOME/logs/soda.log 2>$HOME/logs/errlogs/soda_err.log &
#0 15 * * 2 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/beauty/169711011 > $HOME/logs/head_phone.log 2>$HOME/logs/errlogs/hair_color.log &
0 18 * * 2 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/food-beverage/71595051/ > $HOME/logs/beverage.log 2>$HOME/logs/errlogs/beverage_err.log &
#0 21 * * 2 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/beauty/5263269051 > $HOME/logs/head_phone.log 2>$HOME/logs/errlogs/hair_mascara.log &
0 0 * * 3 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/beauty/169681011/ > $HOME/logs/conditioner.log 2>$HOME/logs/errlogs/conditioner_err.log &
0 3 * * 3 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/beauty/169644011/ > $HOME/logs/DSLR.log 2>$HOME/logs/errlogs/body_soap.log &
0 6 * * 3 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/beauty/169668011/ > $HOME/logs/shampoo.log 2>$HOME/logs/errlogs/shampoo_err.log &
#0 9 * * 3 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/beauty/2356823051 > $HOME/logs/head_phone.log 2>$HOME/logs/errlogs/white_hair_color.log &
0 12 * * 3 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/beauty/169764011/ > $HOME/logs/tooth_paste.log 2>$HOME/logs/errlogs/tooth_paste_err.log &
#0 15 * * 3 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/hpc/170356011 > $HOME/logs/head_phone.log 2>$HOME/logs/errlogs/baby_soap.log &
0 18 * * 3 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/beauty/170228011/ > $HOME/logs/beauty.log 2>$HOME/logs/errlogs/beauty_err.log &
#0 21 * * 3 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/hpc/170365011 > $HOME/logs/head_phone.log 2>$HOME/logs/errlogs/wiper.log &
0 0 * * 4 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/hpc/170583011/ > $HOME/logs/bath_hpc.log 2>$HOME/logs/errlogs/bath_hpc_err.log &
0 3 * * 4 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/beauty/170134011/ > $HOME/logs/DSLR.log 2>$HOME/logs/errlogs/beauty_night.log &
0 6 * * 4 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/hpc/170589011/ > $HOME/logs/toilet_hpc.log 2>$HOME/logs/errlogs/toilet_hpc_err.log &
#0 9 * * 4 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/hpc/169927011 > $HOME/logs/head_phone.log 2>$HOME/logs/errlogs/hygiene_supplies.log &
0 12 * * 4 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/hpc/170565011/ > $HOME/logs/kitchen_hpc.log 2>$HOME/logs/errlogs/kitchen_hpc_err.log &
#0 15 * * 4 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/hpc/170498011 > $HOME/logs/head_phone.log 2>$HOME/logs/errlogs/panties.log &
0 18 * * 4 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/hpc/170665011/ > $HOME/logs/softener.log 2>$HOME/logs/errlogs/softener_err.log &
#0 21 * * 4 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/hpc/2356915051 > $HOME/logs/head_phone.log 2>$HOME/logs/errlogs/floor_wiper.log &
0 0 * * 5 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/hpc/2356927051/ > $HOME/logs/liquid_hpc.log 2>$HOME/logs/errlogs/liquid_hpc_err.log &
0 3 * * 5 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/beauty/170121011/ > $HOME/logs/DSLR.log 2>$HOME/logs/errlogs/milky_lotion.log &
0 6 * * 5 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/hpc/170664011/ > $HOME/logs/hpc.log 2>$HOME/logs/errlogs/hpc_err.log &
#0 9 * * 5 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/hpc/2356916051 > $HOME/logs/head_phone.log 2>$HOME/logs/errlogs/floor_wiper_sheet.log &
0 12 * * 5 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/hpc/2356929051/ > $HOME/logs/bleach.log 2>$HOME/logs/errlogs/bleach_err.log &
0 15 * * 5 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/hpc/202230011/ > $HOME/logs/bleach.log 2>$HOME/logs/errlogs/pain_killer.log &
0 18 * * 5 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/hpc/170329011/ > $HOME/logs/child_product.log 2>$HOME/logs/errlogs/child_product_err.log &
#0 21 * * 5 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/hpc/170578011 > $HOME/logs/head_phone.log 2>$HOME/logs/errlogs/disposable_cloth.log &
0 0 * * 6 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/electronics/16245081/ > $HOME/logs/electronic_kettle.log 2>$HOME/logs/errlogs/electronic_kettle_err.log &
0 3 * * 6 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/food-beverage/2436205051/ > $HOME/logs/DSLR.log 2>$HOME/logs/errlogs/okayu.log &
0 6 * * 6 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/electronics/2276690051/ > $HOME/logs/coffe_maker.log 2>$HOME/logs/errlogs/coffe_maker_err.log &
#0 9 * * 6 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/beauty/170059011 > $HOME/logs/head_phone.log 2>$HOME/logs/errlogs/facewash_foam.log &
0 12 * * 6 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/electronics/5059082051/ > $HOME/logs/espresso_machine.log 2>$HOME/logs/errlogs/espresso_machine_err.log &
0 15 * * 6 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/hpc/2505533051/ > $HOME/logs/espresso_machine.log 2>$HOME/logs/errlogs/cold_medicine.log &
0 18 * * 6 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/electronics/4083551/ > $HOME/logs/mixer.log 2>$HOME/logs/errlogs/mixer_err.log &
#0 21 * * 6 nohup python -u $HOME/amazonSalesRanking.py https://www.amazon.co.jp/gp/bestsellers/beauty/170058011 > $HOME/logs/head_phone.log 2>$HOME/logs/errlogs/facewash.log &

#- amazon_top_selling_to_td -------
0 8 * * 1 nohup python -u /home/da-dev/amazon_top_selling_to_td/amazon_top_selling_to_td.py 1> /home/da-dev/amazon_top_selling_to_td/logs/info.log 2> /home/da-dev/amazon_top_selling_to_td/logs/err.log &
'''   
