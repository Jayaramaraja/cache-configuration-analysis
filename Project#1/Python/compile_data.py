import os
import sys
import csv
import glob,xlwt

wb = xlwt.Workbook()
for filename in glob.glob("./results/bench*.csv"):
	(f_path, f_name) = os.path.split(filename)
	(f_short_name, f_extension) = os.path.splitext(f_name)
	f_short_name = f_short_name.replace("bench_","",1)
	print f_short_name
	print filename
	ws = wb.add_sheet(f_short_name)
	spamReader = csv.reader(open(filename, 'rb'))
	for rowx, row in enumerate(spamReader):
		for colx, value in enumerate(row):
			if (rowx == 0):
				ws.write(rowx, colx, value)
			else:
				ws.write(rowx, colx, float(value))

wb.save("./results/compiled.xls")
