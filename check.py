import pandas as pd
import sqlite3
from items import fetch
k=[(i,i) for i in fetch()["name"].tolist()]
print(k)
