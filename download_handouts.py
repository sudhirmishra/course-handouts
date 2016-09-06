import requests
import urllib
import os
import sys
from bs4 import BeautifulSoup

hostname = "http://172.18.6.180"
home_page_url = hostname + "/ID/Handouts.do"

html_home = requests.get(home_page_url,"html.parser")

soup = BeautifulSoup(html_home.text)

directory = "Rename Handouts/"

try:
	if not os.path.exists(directory):
		os.makedirs(directory)
except:
	print("Directory Error")
	sys.exit(1)

table = soup.find('div',{'class':'tableGrid'})

rows = table.find('table').findAll('tr')

mapping_table = {}

for row in rows:
	cols = row.findAll('td')
	if len(cols) == 4:
		key = cols[1].text.replace(" ","_") +"_"+cols[0].text
		value = cols[2].text
		href = row.find('a')
		print(key,value)
		try:
			urllib.request.urlretrieve( hostname+href['href'],
					filename=directory+value+"_"+href['href'].split('/')[-1] )
		except:
			print(href)
