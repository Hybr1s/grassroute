#!/usr/bin/env python3
from bs4 import BeautifulSoup
import codecs
import urllib
import csv

#Bei der Seite http://www.siegen.de/vereinsregister/page.sys/62.htm wird eine leere Suchanfrage gestellt, 
#wodurch alle Datensaetze zurueckgegeben werden. Der Response wurde manuel als vereinsregister.html gespeichert

soup = BeautifulSoup(codecs.open("vereinsregister.html", "r", "iso-8859-1")) 
stuff = soup.find_all("div", class_="content_padding")
links = list(map(lambda x: x["href"], stuff[0].find_all("a")))

with open('VereinsregisterSiegen.csv', 'w') as csvfile:
	fieldnames = ['Name','Beschreibung','Anschrift','PLZ','Stadt','Ansprechpartner','Telefon', 'Telefax', 'Mail', 'Website']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	
	writer.writeheader()

	for i in links:
		verein = BeautifulSoup(urllib.urlopen(i).read())
		content = str(verein.find_all("div", class_="content_padding")[0])
		content = content.replace('<br>','')
		content = content.replace('<div class=\"content_padding\">','')
		content = content.replace('</strong>','')
		content = content.replace('<strong>','')
		content = content.replace('<a class="link" href=','')
		content = content.replace('<a class="link" href="','')
		content = content.split('" target="_blank"><u>')[0]
		content = content.replace('</u></a>','')
		content = content.replace('<a class=\"olsbutton\"','')
		content = content.split('href="page.')[0]
		content_list = content.split('\"mailto')
		content = content_list[0]+content_list[1].split('\"><u>')[1]
		content = content.replace('\"','')
		content = content.split('<div class=sondermodule_hg_hell>')[0]
		
		striped_lines=content.split('\n')
		striped_lines=list(map(lambda x: x.strip(),striped_lines))
		striped_lines=list(filter(lambda x: x!='',striped_lines))
		
		anschrift_index= striped_lines.index('Anschrift:')
		kontakt_index= striped_lines.index('Kontakt:')
		
		
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
		
		
		name=striped_lines[0]
		if anschrift_index>1:
			description= '\n'.join(striped_lines[1:anschrift_index])
		
		street=striped_lines[anschrift_index+1]
		plz_list=striped_lines[anschrift_index+2].split(' ')
		if len(plz_list)>1:
			plz=plz_list[0]
			city=plz_list[1]
		else:
			city=plz_list[0]
	
		contact_list=striped_lines[kontakt_index+1:]
		contact=contact_list[0]
		
		fon_list=list(filter(lambda x: x.startswith('Telefon'),contact_list))
		if len(fon_list)!=0:
			tel=fon_list[0].split(':')[1].strip()
			tel= tel.replace('/', '')
			tel= tel.replace('(', '')
			tel= tel.replace(')', '')
			tel= tel.replace(' ', '')
			tel= tel.replace('-', '')
			
		fax_list=list(filter(lambda x: x.startswith('Telefax'),contact_list))
		if len(fax_list)!=0:
			fax=fax_list[0].split(':')[1].strip()
			fax= fax.replace('/', '')
			fax= fax.replace('(', '')
			fax= fax.replace(')', '')
			fax= fax.replace(' ', '')
			fax= fax.replace('-', '')

		mail_list=list(filter(lambda x: x.startswith('E-Mail:'),contact_list))
		if len(mail_list)!=0:
			mail=mail_list[0].split(':')[1].strip()


		web_list=list(filter(lambda x: x.startswith('Internet:'),contact_list))
		if len(web_list)!=0:
			web="".join(web_list[0].split(':')[1:])


		print web

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

		




