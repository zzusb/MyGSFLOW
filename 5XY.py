
#-*-coding=utf-8 -*-
'''
生成CRT XY.DAT
input:./input/fishnet_hrutype.txt
output:./output/CRT/XY.DAT
'''
import csv
import os
def generateXY(filepath,savepath):
	if  not os.path.exists(savepath):
		os.makedirs(savepath)
	file= open(filepath+"fishnet_hrutype.txt",'r')
	#file= open("./0025/input/fishnet_hrutype.txt",'r')
	name = file.readline()
	index_GridID=name.rstrip("\n").split(',').index('Grid_ID')
	index_x=name.rstrip("\n").split(',').index('x_center')
	index_y=name.rstrip("\n").split(',').index('y_center')

	GridID=[]
	x=[]
	y=[]
	with open(".//fishnet_hrutype.csv",'r') as csvfile:
		csvreader=csv.reader(csvfile)
		data=[r for r in csvreader]
		del data[0]
		for d in data:
			#hru_type.append(int(d[index_HRU_type]))
			GridID.append(int(d[index_GridID]))
			x.append(float(d[index_x]))
			y.append(float(d[index_y]))
	csvfile.close()
	#item 1
	with open(savepath+'/XY.DAT','w') as f:
		for g in range (len(GridID)):
			f.write(str(GridID[g])+' '+str(x[g])+' '+str(y[g]))
			f.write('\n')
	f.close()
if __name__=="__main__":
	path1=".//"
	path2=".//"
	generateXY(path1,path2)

