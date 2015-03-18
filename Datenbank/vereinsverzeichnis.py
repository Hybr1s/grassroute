#!/usr/bin/env python3
from bs4 import BeautifulSoup
import codecs
import urllib
import unicodecsv as csv
import requests

with open('VereinsVerzeichniseu.csv', 'w') as csvfile:
	fieldnames = ['Name','Beschreibung','Anschrift','PLZ','Stadt','Ansprechpartner','Telefon', 'Telefax', 'Mail', 'Website']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	v=0

	link_list=[]
	
	for v in range(0,9):
		response = requests.get('http://www.vereinsverzeichnis.eu/stadt,Siegen,'+str(v)+'.html')
		soup = BeautifulSoup(response.text)
		v+=1
		stuff = soup.find_all("img", src="grafiken_und_bilder/eintrag.jpg")
		linkstuff = list(map(lambda x: x.parent.a['href'], stuff))
		for i in linkstuff:
			link_list.append('http://www.vereinsverzeichnis.eu/'+str(i))
	
	
	for link in link_list:
		name=''
		description=''
		street=''
		contact=''
		plz=''
		city=''
		tel=''
		mail=''
		web=''
		fax=''
		
		response=requests.get(link)
		response.encoding="utf-8"
		
		soup = BeautifulSoup(response.text)
		
		content = soup.find_all('table', width="564", border="0", align="center", cellpadding="0", cellspacing="0")[0]
		
		name = content.find_all('td', class_="title")[0].text
		
		street = content.find_all('span', class_="anschriftstrasse")[0].text
		
		plz = content.find_all('span', class_="anschriftplz")[0].text.split(' ')[0]
		
		city = content.find_all('span', class_="anschriftplz")[0].text.split(' ')[1]
		
		web_list = content.find_all('a', target="_blank")
		if len(web_list)!=0:
			web= web_list[0].text
		
		cont_list = content.find_all('strong', text="Kontakt:")
		if len(cont_list)!=0:
			contact= cont_list[0].parent.find_next('td').text

		tel_list= content.find_all('strong', text="Telefon:")
		if len(tel_list)!=0:
			tel= tel_list[0].parent.find_next('td').text
			tel= tel.replace('/', '')
			tel= tel.replace('(', '')
			tel= tel.replace(')', '')
			tel= tel.replace(' ', '')
			tel= tel.replace('-', '')
			
		fax_list= content.find_all('strong', text="Telefax:")
		if len(fax_list)!=0:
			fax= fax_list[0].parent.find_next('td').text
			fax= fax.replace('/', '')
			fax= fax.replace('(', '')
			fax= fax.replace(')', '')
			fax= fax.replace(' ', '')
			fax= fax.replace('-', '')
		
		print(name)
		print(description)
		print(street)
		print(contact)
		print(plz)
		print(city)
		print(tel)
		print(fax)
		print(mail)
		print(web)

			
			
		data={}
	
		data['Name']=name.replace(',','').replace(';','').strip()
		data['Beschreibung']=description.replace(',','').replace(';','').strip()
		data['Anschrift']=street.replace(',','').replace(';','').strip()
		data['PLZ']=plz.replace(',','').replace(';','').strip()
		data['Stadt']=city.replace(',','').replace(';','').strip()
		data['Ansprechpartner']=contact.replace(',','').replace(';','').strip()
		data['Telefon']=tel.replace(',','').replace(';','').strip()
		data['Telefax']=fax.replace(',','').replace(';','').strip()
		data['Mail']=mail.replace(',','').replace(';','').strip()
		data['Website']=web.replace(',','').replace(';','').strip()
	
		writer.writerow(data)	
