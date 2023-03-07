#-*-coding=utf-8 -*-
'''
这是用来生成CRT输入文件 HRU_CASC.DAT
流域类型-1
非流域类型-0
湖泊类型-2
input: ./input/fishnet_hrutype.txt，此文件注意按照Grid——ID排序
output: ./output/CRT/HRU_CASC.DAT
'''
import csv
import numpy

#===============================Item 1=======================================
#Grid ID 与 HRU ID是否一致：一致=0(默认)；不一致=1，额外需要HRU_ID.DAT文件
HRUFLG=0

#0-no stream reaches will be included in cascades,onlu HRU;1-selected stream reaches will be
#included in cascades.for this options, ON_OFF in the STREAM_CELLS.DAT input file should be considered.
STRMFLG=1

#how outflow fractions will be calculated.
# 0-flows will be apportioned evenly among the number of outfow cascade links.
# 1-outflow fractions will be calculated on the basis of relative slopes among the outflow cascade links
FLOWFLG=1

# 0- no visualization;1-visualization data will be written to vis.txt and XY.DAT is required.
VISFLG=1

#1-expanded output will be written in outputstat.txt. Expanded output includes all input
#information and output information from CRT operation;0-expanded output will not be written.
IPRN=1

# 0-CRT Fill Procedure will not be used;1-CRT Fill Procedure will be used
IFILL=1

#the value to which an HRU elevation will be adjusted during an iteration of the CRT Fill Procedure
DPIT=0.1

#The maximum number of CRT Fill Procedure iteratons.
OUTITMAX=10000

line0=[HRUFLG,STRMFLG,FLOWFLG,VISFLG,IPRN,IFILL,DPIT,OUTITMAX,'HRUFLG STRMFLG FLOWFLG VISFLG IPRN IFILL DPIT OUTITMAX']

#===============================Item2=======================================
file= open("./fishnet_hrutype.txt",'r')
name = file.readline()
index_HRU_type=name.rstrip("\n").split(',').index('hrutype')
index_row=name.rstrip("\n").split(',').index('row')
index_col=name.rstrip("\n").split(',').index('col')

hru_type=[]
row=[]
col=[]
with open("./fishnet_hrutype.csv",'r') as csvfile:
	csvreader=csv.reader(csvfile)
	data=[r for r in csvreader]
	del data[0]
	for d in data:
		hru_type.append(int(d[index_HRU_type]))
		row.append(int(d[index_row]))
		col.append(int(d[index_col]))
csvfile.close()
nrow=max(row)
ncol=max(col)
array_hru_type=numpy.array(hru_type).reshape(nrow,ncol)
array_hru_type=array_hru_type.tolist()
#print(array_hru_type[27][55])

with open('./HRU_CASC.DAT','w') as f:
	for ll in line0:
		f.write(str(ll)+' ')
	f.write('\n')
	for line in array_hru_type:
		n=0
		for line2 in line:
			#print(str(line2)+',')
			f.write(str(line2)+' ')
			n=n+1
		#print('\n')
		print(n)
		f.write('\n')
f.close()	


