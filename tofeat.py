import feather 
import pandas as pd
import numpy as np

fout = open("user_problem_mat.txt","r")
user_idx = 0
problem_idx = 0
idx_con = 0
for line in fout.readlines():
	col,row,rating = line.strip().split(' ')
	user_idx = max( user_idx,int(col) )
	problem_idx = max( problem_idx,int(row) )	
	idx_con += 1
fout.close()

rating_mat = np.empty( (idx_con,3),dtype=int )

print(user_idx+1,problem_idx+1)

fout = open("user_problem_mat.txt","r")
i = 0
for line in fout.readlines():
	col,row,rating = map(int,line.strip().split(' '))
	rating_mat[i][0]=col
	rating_mat[i][1]=row
	rating_mat[i][2]=rating
	i+=1

sf = pd.DataFrame(rating_mat,columns=['user_id', 'item_id','rating'])
sf = sf.copy()
print (sf)
feather.write_dataframe(sf,"C:\\Users\\xwind\\Desktop\\mat.feather")
