import datetime
import time
import requests

print(requests.get("https://kultegr.pythonanywhere.com/api/v1/user/").json())