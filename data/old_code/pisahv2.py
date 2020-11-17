import json
from pymongo import MongoClient
from datetime import datetime
from itertools import groupby
import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
import os.path
from os import path
import sys

client = MongoClient('mongodb://localhost:27017/')
db = client['dataSaham']

period = int(sys.argv[1])
col_name = 'data'
if period != 1:
    col_name += str(period)

col = db[col_name]

name_list = col.find({'period': period}).distinct('name')
name_list.sort()

for nama in name_list:
    data_saham = [x for x in col.find({'name': nama})]
    print(nama, data_saham)