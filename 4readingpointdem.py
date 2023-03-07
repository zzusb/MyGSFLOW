#-*-coding=utf-8 -*-
'''
生成CRT LAND_ELEV.DAT
input: ./input/fishnet_hrutype.txt
output: ./output/CRT/LAND_ELEV.DAT
'''
import csv
import numpy


file= open("./fishnet_hrutype.txt",'r')
name = file.readline()
index_dem=name.rstrip("\n").split(',').index('DEM')
index_row=name.rstrip("\n").split(',').index('row')
index_col=name.rstrip("\n").split(',').index('col')

row=[]
col=[]
dem=[]
with open("./fishnet_hrutype.csv",'r') as csvfile:
	csvreader=csv.reader(csvfile)
	data=[r for r in csvreader]
	del data[0]
	for d in data:
		d=['-9,999' if x=='-999' else x for x in d]
		#hru_type.append(int(d[index_HRU_type]))
		row.append(int(d[index_row]))
		col.append(int(d[index_col]))
		dem.append(float(d[index_dem].replace(',','')))
csvfile.close()
#item 1
nrow=max(row)
ncol=max(col)
#item 2
array_dem=numpy.array(dem).reshape(nrow,ncol)
array_dem=array_dem.tolist()
with open('./LAND_ELEV.DAT','w') as f:
	f.write(str(nrow)+' ')
	f.write(str(ncol)+' ')
	f.write('NROW'+' ')
	f.write('NCOL'+' ')
	f.write('\n')
	for line in array_dem:
		n=0
		for line2 in line:
			#print(str(line2)+',')
			f.write(str(line2)+' ')
			n=n+1
		#print('\n')
		print(n)
		f.write('\n')
f.close()	

