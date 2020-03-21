import os
import requests
import re
import csv
import camelot
import pandas as pd

data = requests.get('https://www.gob.mx/salud/documentos/coronavirus-covid-19-comunicado-tecnico-diario-238449')


pdf_link = re.findall(r'(\/cms\/uploads\/attachment\/file\/[0-9]+\/)(Tabla[ _-]casos[ _-]positivos[ _-a-zA-Z0-9]+[_a-zA-Z]+[0-9]+.[0-9]+.[0-9]+)(.pdf)', data.text)

pdf_url = "https://www.gob.mx/"+pdf_link[0][0] + pdf_link[0][1] + pdf_link[0][2]
pdf_filename = pdf_link[0][1]
pdf_filename_ext = pdf_link[0][1] + pdf_link[0][2]
pdf_download_filename = './downloads/'+pdf_filename_ext;
csv_filename = "csv/"+pdf_filename+".csv"

print("Documento PDF publicado")
print(pdf_url)


try:
		fo = open('./downloads/'+pdf_filename_ext)
		print("El documento fue previamente descargado")
		fo.close()
except FileNotFoundError:
		print("Documento nuevo, inicia descarga...")
		download = requests.get(pdf_url)
		with open(pdf_download_filename, 'wb') as f :
				f.write(download.content)
		
csv_tempfile = "csv/"+pdf_filename+"_temp.csv"

tables = camelot.read_pdf(pdf_download_filename, pages="all")
# tables.export('csv/foo.csv', f='csv')


tableList = []
for table in tables:
  tableList.append(table.df)
	
  
result = pd.concat(tableList)

result.to_csv(csv_filename, header=False, index=False)
