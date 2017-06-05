import mincemeat
import glob
import csv

text_files = glob.glob('join/*')

def file_contents(file_name):
	f = open(file_name)
	try:
		return f.read()
	finally:
		f.close()

source = dict((file_name, file_contents(file_name)) for file_name in text_files)

def mapfn(k, v):
	print 'map ' + k
	for line in v.splitlines():
		if k == 'join/filiais.csv':
			print line
			yield line.split(';')[0], 'Filial' + ':' + line.split(';')[1]
		if k == 'join/vendas.csv':
			yield line.split(';')[0], 'Vendas' + ':' + line.split(';')[5]

def reducefn(k, v):
	print 'reduce ' + k
	total = 0
	for index, item in enumerate(v):
		if item.split(":")[0] == 'Vendas':
			print item
			total += int(item.split(':')[1])
		if item.split(":")[0] == 'Filial':
			NomeFilial = item.split(':')[1]
	L = list();
	L.append(NomeFilial + ' , ' + str(total))
	return L

print 'instancia server'
s = mincemeat.Server()

print 'define atributos do server'
# A fonte de dados pode ser qualquer objeto do tipo dicionario
s.datasource = source
s.mapfn = mapfn
s.reducefn = reducefn

print 'run server'
results = s.run_server(password="changeme")

print 'write results'
w = csv.writer(open("result.csv", 'w'))
for k, v in results.items():
	w.writerow([k, str(v).replace('[', '').replace(']', '').replace("'", '').replace(' ', '')])
