#-*- coding=utf-8 -*-
'''
用来生成reach序号。

输入文件：arcgis得到的stream和fishnet的intesct表格。stream_intersect.txt
在arcgis中需要额外添加计算7个字段，见下。

输出文件：reachID_to_arcgis.txt用于返回arcgis 连接join reaches文件

Author: LXT 
Time:6/10/2020
'''
import csv
import numpy as np

with open("./stream_intersect.txt") as f:
	category=f.readline().rstrip("\n").split(',')
	print (category)
	index_objectforvs=category.index('ID_for_vs')# object_for_vs=ARCGIS中的Fid
	index_segmentID=category.index('stream_ID')#
	index_x_star_resa=category.index('x_start')#22
	index_y_star_resa=category.index('y_start')#23
	index_x_end_resa=category.index('x_end')#24
	index_y_end_resa=category.index('y_end')#25
	index_hru_id=category.index('HRU_ID')#17

objectforvsID=[]
segmentID=[]
x_star_resa=[]
y_star_resa=[]
x_end_resa=[]
y_end_resa=[]
#hru_id=[]
reach_id=[]
with open("./stream_intersect.txt",'r') as csvf:
	csvread=csv.reader(csvf)
	data=[i for i in csvread]
	csvf.close()

del data[0]#csv键有问题用txt读的代替
#data=np.array(data)
for d in data:
	objectforvsID.append(d[index_objectforvs])
	segmentID.append(d[index_segmentID])
	x_star_resa.append(d[index_x_star_resa])
	y_star_resa.append(d[index_y_star_resa])
	x_end_resa.append(d[index_x_end_resa])
	y_end_resa.append(d[index_y_end_resa])
	reach_id.append(99999)
	#hru_id.append(d[index_hru_id])
objectforvsID=np.array(objectforvsID)
segmentID=np.array(segmentID)
x_star_resa=np.array(x_star_resa)
y_star_resa=np.array(y_star_resa)
x_end_resa=np.array(x_end_resa)
y_end_resa=np.array(y_end_resa)

data2=data[:]#防止更改原始数组
reaches_in_segment=[]

while (data2):
	for dd in data2:#当前是第一条记录index=0
		ID=1
		#找到与当前记录dd一样的segment编号的记录,当前记录的segment编号为dd[index_segmentID]，
		#记录下在data里对应的唯一的下表索引
		index_same_segment=np.array(np.where(segmentID==dd[index_segmentID]))[0]
		#
		seg_x_end_resa=[]
		seg_x_start_resa=[]
		seg_y_end_resa=[]
		seg_y_start_resa=[]
		obj=[]
		for iss1 in index_same_segment:
			seg_x_start_resa.append(x_star_resa[iss1])
			seg_y_start_resa.append(y_star_resa[iss1])
			seg_x_end_resa.append(x_end_resa[iss1])
			seg_y_end_resa.append(y_end_resa[iss1])
			obj.append(objectforvsID[iss1])

		#下面进行组内reaches的比较和编号
		for iss in index_same_segment:
			#找到segment的第一个上游reach
			if (x_star_resa[iss] not in seg_x_end_resa) and (y_star_resa[iss] not in seg_y_end_resa):
				reach_id[iss]=ID#index_same_segment[0][iss]是同一个segment的索引
			##通过索引找到当前记录的唯一编号==记录的行号，
			#返回行号在当前数据集中的索引，为什么要多此一举是因为下面需要删掉已经计算过的记录会改变记录的索引，但是有唯一编
			#号所以找到唯一编号的index就可以了
				next_x_start=x_end_resa[iss]
				next_y_start=y_end_resa[iss]
				#去掉第一个已经编号的reach
				index_same_segment2=index_same_segment.tolist()
				index_same_segment2.remove(iss)

				#a=np.array(np.where(objectforvsID[iss]))[0][0]
				#del data2[a]
				#去掉已经编号的数据
				data2=np.array(data2)
				del_target=[np.where(data2[:,index_objectforvs]==objectforvsID[iss])][0][0][0]#%%%%%%%%%%%
				data2=data2.tolist()
				del data2[del_target]
				break
			else:#未验证
				continue
		#编号剩下的reach
	
		while(index_same_segment2):
			#for iss2 in index_same_segment2:
			index_seg_reach_x=np.array(np.where(np.array(seg_x_start_resa)==next_x_start))[0]
				#可能的一种情况是：出现两个x,需要进一步比较y;出现一个x，直接用x即可
			if len(index_seg_reach_x)>1:
				index_seg_reach_y=np.array(np.where(np.array(seg_y_start_resa)==next_y_start))[0]
				index_seg_reach=list(set(index_seg_reach_x)&set(index_seg_reach_y))[0]#此时应该只有一个值
				index_next_reach=np.array(np.where(np.array(objectforvsID)==obj[index_seg_reach]))[0][0]
			else:
				index_seg_reach=index_seg_reach_x[0]
				index_next_reach=np.array(np.where(np.array(objectforvsID)==obj[index_seg_reach]))[0][0]
			ID=ID+1
			reach_id[index_next_reach]=ID
				#记录下下一个起始的x,y
			next_x_start=x_end_resa[index_next_reach]
			next_y_start=y_end_resa[index_next_reach]
				
				#去掉已经编号过的数据记录
				#1.去掉同一个segment已经完成编号的ID
				#index_same_segment2.remove(iss2)
			index_same_segment2.remove(index_next_reach)
				#a=np.array(np.where(objectforvsID[iss2]))[0][0]
				#2.在原数据集中删除已经编号过的数据记录
			data2=np.array(data2)
			del_target=[np.where(data2[:,index_objectforvs]==objectforvsID[index_next_reach])][0][0][0]
			data2=data2.tolist()
			del data2[del_target]
			#break
			continue
		#结束了当前的segment
		break

		

if len(reach_id)==len(objectforvsID):
	with open('./reachID_to_arcgis.txt','w') as wf:
		wf.write('object_for_vs'+' '+'reachID_in_segment'+'\n')
		for n in range(len(reach_id)):
			wf.write(str(objectforvsID[n])+' '+str(reach_id[n])+"\n")
	wf.close()
else:print('the number is different between reachID and objectforvsID, please check')			

print ('')
