import requests
from datetime import datetime
import humanize
from dateutil.parser import parse


url = "https://youtube138.p.rapidapi.com/video/details/"

querystring = {"id":"koBFYReA28Y","hl":"en","gl":"US"}

headers = {
	"content-type": "application/octet-stream",
	"X-RapidAPI-Key": "366db20a39msh465197bace7a6cep1222fdjsn5102d449ed4e",
	"X-RapidAPI-Host": "youtube138.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
res=response.json()
print(res)
