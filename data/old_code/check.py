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
db = client.dataSaham
a = [x for x in db.data.distinct('name')]
y = {}
for x in a:
    z = db.data.count_documents({'name':x})
    y[x] = z
print(y)
