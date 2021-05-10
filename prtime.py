from urllib.request import urlopen as uReg
from bs4 import BeautifulSoup 
import re
import csv
import numpy as np
import os,sys

os.chdir('D:/')
my_url = 'https://www.marr.jp/mainfo/news/202103'

uClient = uReg(my_url)
html_page = uClient.read()
uClient.close()
word_list=["資金","ファンド","Venture","Ventures","Fund","有限責任組合","ベンチャー","ベンチャーズ",
"Partners","CVC","出資","第三者割当増資"]
soup = BeautifulSoup(html_page,"html.parser")

csv_file = open('marr_scrape_02_new','w',encoding ='utf-8-sig',newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['title','link','deal amount'])

ol_tags= soup.find_all('li')
for tag in ol_tags:
	try:
		text = tag.a.text
	except Exception as e:
		text = None

	if text:
		if any(word in text for word in word_list):
			print("title: "+ text)
			amount =  re.findall('[0-9]{0,9}?[.]?[0-9]+.[円]',text)
			if amount:
				amount_input=amount[0]
				if '億' in amount_input:
					amount_input = int(float(amount_input.split('億')[0]))*100000000
				elif '千万' in amount_input:
					amount_input = int(float(amount_input.split('千万')[0]))*10000000
				elif '百万' in amount_input:
					amount_input = int(float(amount_input.split('百万')[0]))*1000000
			else:
				amount_input= np.nan

			try:
				hyperlink = tag.a.get('href').split('://')[1]
			except Exception as e:
				hyperlink = None 
			if hyperlink:
				print("link: "+hyperlink)
				csv_writer.writerow([text.strip(),hyperlink.strip(),amount_input])
		else:
			continue
	else:
		continue
csv_file.close()

#for tag in ol_tags:
	#print(tag.a.text)
	#print(tag.a.get('href'))