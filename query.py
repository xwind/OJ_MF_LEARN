import numpy as np
import matplotlib.pyplot as plt  
import json
import math
import tkinter as tk

user_idx_name = json.load(open("user_name.txt",'r'))
user_done = json.load(open("user_done.txt",'r'))
problem_idx_name = json.load(open("problme_name.txt",'r'))
problem_tags = json.load(open("problem_tags.txt",'r'))
user_tags = json.load(open("user_tags.txt",'r'))
user_tags_sum = {}
final_w=np.load("final_w.npy")
final_h=np.load("final_h.npy")
res = final_w.dot(final_h)

for user_name in user_tags:
	val = 0
	for tag in user_tags[user_name]:
		val += user_tags[user_name][tag]
	user_tags_sum[user_name]=val;
x_list = []
y_list = []

def anay_user(user_name,ac_p=0.0150):
	xiper = ""
	for i in user_idx_name:
		if user_idx_name[i]==user_name:
			xiper=i
	if xiper == "":
		print ("No such a user in database")
		return 0
	done_list = user_done[xiper]
	problem_con = 0
	aveg = 0.
	max_acp = 0.
	problem_idx = 0
	for i in range(0,res[int(xiper)].shape[0]):
		aveg += res[int(xiper)][i]
		if i not in done_list:
			val = 0.
			for tag in problem_tags[str(i)]:
				if user_tags[user_name].get(tag) != None:
					val += user_tags[user_name][tag]
			val/=user_tags_sum[user_name]
			val = res[int(xiper)][i]*(1+val);
			if val > ac_p:	
				#print (problem_idx_name[str(i)])
				problem_con+=1
			if val > max_acp:
				max_acp = val
				problem_idx = i
	aveg /= res[int(xiper)].shape[0]

	if problem_con:
		#print ("%32s\'s  \tproblem doing/done: \t"%(user_name)+str(problem_con)+"/"+str( len(done_list)) +" \taveg: \t"+str(aveg))
		x_list.append( len(done_list) )
		y_list.append( problem_con )
	print("User:"+user_name+" Recommand Problem:"+problem_idx_name[str(problem_idx)]+" with Probability:"+str(max_acp) )
	fout = open("recommand.txt",'w')
	fout.write(str(problem_idx_name[str(problem_idx)])+'\n')
	fout.close()
	return problem_con

def show_graph_num_with_rij():
	x = np.array(x_list)
	y = np.array(y_list)
	fig = plt.figure()  
	ax1 = fig.add_subplot(111)  
	ax1.set_title('Problem Num Analysis') 
	plt.xlabel('Problem Done')
	plt.ylabel('Problem Doing')
	cValue = ['r','y','g','b','r','y','g','b','r']  
	ax1.scatter(x,y,c=cValue,marker='o')
	plt.legend('x1')
	plt.show() 

def show_graph_deg():
	x_list=[]	
	y_list=[]
	for ac_p in np.linspace(0.01, 0.02, 11):
		con = 0
		for i in range(0,585):
			con+=anay_user(user_idx_name[str(i)],ac_p)
		print (ac_p,con)
		x_list.append(ac_p)
		y_list.append(con)
	fig = plt.figure()  
	ax1 = fig.add_subplot(111)  
	ax1.set_title('Problem degs with Accepted Probability') 
	plt.xlabel('Accepted Probability')
	plt.ylabel('Predicted Problem')
	x = np.array(x_list)
	y = np.array(y_list)
	ax1.scatter(x,y,c='r',marker='s')
	plt.legend('x1')
	plt.show() 

def show_graph_sim(user_name):
	xiper = ""
	for i in user_idx_name:
		if user_idx_name[i]==user_name:
			xiper=i
			break
	if xiper == "":
		print ("No such a user in database")
		return 0
	count = 0
	user_num = int(xiper)
	duser = math.sqrt(final_w[user_num].dot(final_w[user_num]));
	x_list = []
	y_list = []
	min_cos = 2.
	far_user = ""	
	for user_other in final_w:	
		if count != user_num :	
			dmult=final_w[user_num].dot(user_other)
			dother= math.sqrt( user_other.dot(user_other) );
			cosine = dmult/(duser*dother)
			x_list.append(count)
			y_list.append(cosine)
			if cosine < min_cos:
				min_cos = cosine
				far_user = user_idx_name[str(count)]
		count += 1	
	print ("Farest user:"+user_name+" "+far_user+" max cosine:"+str(min_cos)+" problem done:"+str(user_tags_sum[far_user]) )
	fig = plt.figure()  
	ax1 = fig.add_subplot(111)  
	ax1.set_title('User Similarity') 
	plt.xlabel('User Idex')
	plt.ylabel('Simlarity by Cosine')
	x = np.array(x_list)
	y = np.array(y_list)
	ax1.scatter(x,y,c='b',marker='o')
	plt.legend('x1')
	plt.show() 
	
'''
for i in range(0,res.shape[0]):
	anay_user(user_idx_name[str(i)],0.08)
show_graph_num_with_rij()
'''

def analyse_user():
	user_name = username.get()
	show_graph_sim(user_name)

if __name__ == '__main__':
	root = tk.Tk()
	root.title('ML-by-xwind')
	root.geometry()
	
	topfrm = tk.Frame(root)
	namevar = tk.StringVar()
	namevar.set("")
	username = tk.Entry(topfrm, textvariable = namevar, width = 48)
	username.pack(side = tk.LEFT)
	anaybut = tk.Button(topfrm, text = 'Analyse User', command = analyse_user)
	anaybut.pack(side = tk.RIGHT)
	topfrm.pack(side = tk.TOP)

	root.mainloop()
