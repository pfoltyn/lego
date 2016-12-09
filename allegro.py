#!/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import re
import mechanize

URL = r"http://allegro.pl/klocki-lego-17865?buyNew=1&offerTypeBuyNow=1&order=dd&a_enum%5B128068%5D%5B3%5D=3&p="

max_page_prog = re.compile('<a class="last" href=".*?">(\d+)</a>', re.DOTALL)
offer_prog = re.compile('<div class="offer-info".+?</article>', re.DOTALL)
title_prog = re.compile('<a class="offer-title" href="(.+?)">(.+?)</a>', re.DOTALL)
lego_id_prog = re.compile('.*?(\d{5,})')
price_prog = re.compile('<span class="statement">(.+?)<span', re.DOTALL)

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def create_browser():
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.set_handle_refresh(False)
    br.addheaders = [('User-agent', 'Firefox')]
    return br

def get_max_page_num(page, curr_max_page_num):
    result = max_page_prog.search(page)
    if result:
        return int(result.group(1))
    return curr_max_page_num

def process_offer(offer):
    result = title_prog.search(offer)
    if result == None:
        eprint("Title not found")
        return
    url = result.group(1)
    title = result.group(2)
    lego_id = lego_id_prog.search(title)
    if lego_id == None:
        return
    lego_id = int(lego_id.group(1))
    prices = price_prog.findall(offer)
    buynow = int("".join(prices[0].split()).replace("\xc2\xa0", "").split(",")[0])
    try:
        postage = int("".join(prices[1].split()).replace("\xc2\xa0", "").split(",")[0])
    except:
        postage = 0
    price = max(buynow, postage)
    print("{},{},{}".format(lego_id, price, url))

def main(argc, argv):
    b = create_browser()
    page_num = int(argv[1]) if argc > 1 else 0
    max_page_num = 0
    while True:
        page_num += 1
        page = b.open(URL + str(page_num)).read()

        max_page_num = get_max_page_num(page, max_page_num)
        if page_num >= max_page_num:
            eprint("Exiting because page_num({}) >= max_page_num({})".format(page_num, max_page_num))
            break

        eprint("Processing page {} of {}".format(page_num, max_page_num))
        offers = offer_prog.findall(page)
        if offers == None:
            eprint("No offers on page {} of {}".format(page_num, max_page_num))
            continue
            
        eprint("Found {} offers".format(len(offers)))
        for offer in offers:
            process_offer(offer)

    return 0

if __name__ == "__main__":
    ret = main(len(sys.argv), sys.argv)
    sys.exit(ret)

