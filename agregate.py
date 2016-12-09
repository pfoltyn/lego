import sys
import collections

lego = {}

with open(sys.argv[1]) as f:
    lines = f.readlines()
    for line in lines:
        id, price, url = line.split(",")[:3]
        if id not in lego:
            lego[id] = { 0:{}, 1:{} }
        if float(price) < 500.0:
            continue
        lego[id][0][float(price)] = url.strip()

with open(sys.argv[2]) as f:
    lines = f.readlines()
    for line in lines:
        id, price, url = line.split(",")[:3]
        if id not in lego:
            lego[id] = { 0:{}, 1:{} }
        lego[id][1][float(price)] = url.strip()

for id, value in lego.iteritems():
    vlen0 = len(value[0].keys())
    vlen1 = len(value[1].keys())
    value[0] = collections.OrderedDict(sorted(value[0].items()))
    value[1] = collections.OrderedDict(sorted(value[1].items()))
    for x in range(min(vlen0, vlen1)):
        print "{},{},={}*$H$1,{},{}".format(id, value[0].keys()[x], value[1].keys()[x], value[0][value[0].keys()[x]], value[1][value[1].keys()[x]])
    if vlen0 > 0 and vlen1 > 0:
        if vlen0 > vlen1:
            for x in range(vlen0 - vlen1):
                x += vlen1
                print "{},{},{},{},{}".format(id, value[0].keys()[x], "", value[0][value[0].keys()[x]], "")
        else:
            for x in range(vlen1 - vlen0):
                x += vlen0
                print "{},{},={}*$H$1,{},{}".format(id, "", value[1].keys()[x], "", value[1][value[1].keys()[x]])
        print
    