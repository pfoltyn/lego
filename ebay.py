#!/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import re
import mechanize
import httplib

URL = r"http://www.ebay.co.uk/sch/LEGO-Complete-Sets-Packs/19006/i.html?Type=Complete%2520Set%252FPack&LH_ItemCondition=1000&LH_BIN=1&_sop=16&LH_PrefLoc=3&_pgn="

max_page_prog = re.compile('<span class="listingscnt"\s*>([\d,]+) listings</span>')
offer_prog = re.compile('<li id="item[a-f0-9]{5,}".+?</ul></li>', re.DOTALL)
title_prog = re.compile('listingId="(\d+)".+?title="(.+?)"', re.DOTALL)
lego_id_prog = re.compile('.*?(\d{5,})')
price_prog = re.compile('£([\d\.,]+)')

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
        return int(result.group(1).replace(",", "")) / 50
    return curr_max_page_num

def process_offer(offer):
    result = title_prog.search(offer)
    if result == None:
        print(offer)
        eprint("Title not found")
        return
    url = "http://www.ebay.co.uk/itm/" + result.group(1)
    title = result.group(2)
    lego_id = lego_id_prog.search(title)
    if lego_id == None:
        return
    lego_id = int(lego_id.group(1))
    prices = price_prog.findall(offer)
    buynow = float(prices[0].replace(",", ""))
    try:
        postage = float(prices[1].replace(",", ""))
    except:
        postage = 0
    price = buynow + postage
    print("{},{:.2f},{}".format(lego_id, price, url))

def main(argc, argv):
    b = create_browser()
    page_num = int(argv[1]) if argc > 1 else 0
    max_page_num = 0
    while True:
        page_num += 1
        try:
            page = b.open(URL + str(page_num) + "&_skc=" + str((page_num - 1) * 50)).read()
        except httplib.IncompleteRead as e:
            eprint("Incompleate read exception")
            eprint(e.partial)
            eprint("Retrying page {} from {}".format(page_num, max_page_num))
            page_num -= 1
            continue

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

