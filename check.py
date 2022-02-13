import pandas as pd
import sqlite3
from items import fetch
import requests
import json
res=requests.get("http://127.0.0.1:5000/incoming")
j_data=json.loads(res.json())
print(pd.DataFrame(j_data))
