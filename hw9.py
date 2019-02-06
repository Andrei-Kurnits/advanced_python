from collections import namedtuple
from collections import OrderedDict
import csv


Record = namedtuple('Record', 'name, weight, value')
dic = dict()
for i in map(Record._make, csv.reader(open("data.csv", "r"))):
    dic.update({i.name: {'weight': int(i.weight), 'value': int(i.value)}})
dic = OrderedDict(sorted(dic.items(),
                         key=lambda t: t[1]['value'] / t[1]['weight']))

total = 0
while True:
    item = dic.popitem(last=True)
    total = total + item[1]['weight']
    if total > 400:
        break
    print(item[0], end=" ")
    print(total, 'dag')
