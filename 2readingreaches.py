#-*-coding=utf-8 -*-
'''
生成STREAM_CELLS.DAT
input: ./input/reaches_to_vs.txt
output: ./output/CRT/STREAM_CELLS.DAT
'''
import csv
import numpy

file= open("./reaches_to_vs.txt",'r')
name = file.readline()
#index_HRU_type=name.rstrip("\n").split(',').index('HRU_type')
index_row=name.rstrip("\n").split(',').index('row')
index_col=name.rstrip("\n").split(',').index('col')
index_segment=name.rstrip("\n").split(',').index('stream_ID')#segment ID
index_reaches=name.rstrip("\n").split(',').index('reachID')

#hru_type=[]
row=[]
col=[]
segment=[]
reaches=[]
with open("./reaches_to_vs.csv",'r') as csvfile:
	csvreader=csv.reader(csvfile)
	data=[r for r in csvreader]
	del data[0]
	for d in data:
		#hru_type.append(int(d[index_HRU_type]))
		row.append(int(d[index_row]))
		col.append(int(d[index_col]))
		segment.append(int(d[index_segment]))
		reaches.append(int(d[index_reaches]))
csvfile.close()
#nrow=max(row)
#ncol=max(col)
#array_segment=numpy.array(segment).reshape(nrow,ncol)
#array_segment=array_segment.tolist()

#array_reaches=numpy.array(reaches).reshape(nrow,ncol)
#array_reaches=array_reaches.tolist()
if len(row)==len(col)==len(segment)==len(reaches):
	with open('./STREAM_CELLS.DAT','w') as f:
		f.write(str(len(data))+' '+'NREACH')
		f.write('\n')
		for i in range (0,len(row)):
			f.write(str(row[i])+' '+str(col[i])+' '+str(segment[i])+' '+str(reaches[i])+' 1'+'\n')
	f.close()	

