import json

def push_user(u_id,p_id,user_map):
	if user_map.get(u_id)==None:
		user_map[u_id]=[p_id]
	else:
		user_map[u_id].append(p_id)

def process_data():
	fp = open("user_problem_data.txt",'r')
	fout = open("user_problem_mat.txt",'w')
	u_id = 0
	p_id = 0
	problem_name = {}
	user_name = {}
	user = {}
	user_idx = {}
	problem_idx = {}
	problem_tag = {}
	user_topic = {}
	user_done = {}
	for lines in fp.readlines():
		contents=[]
		for content in lines.strip().split(' '):
			contents.append(content)
		#0 user_name
		if user_idx.get(contents[0]) == None:
			user_idx[ contents[0] ] = u_id
			user_name[ u_id ] = contents[0]
			u_id += 1
		problemname = contents[1] + contents[2]
		if problem_idx.get(problemname) == None:
			problem_idx[ problemname ] = p_id
			problem_name[ p_id ] = problemname
			p_id += 1
		push_user( user_idx[ contents[0] ], problem_idx[ problemname ] ,user_done)
		pass_con = contents[3]
		tags = []
		for tag in range(4,len(contents)):
			if user_topic.get( contents[0] ) == None:
				user_topic[ contents[0] ] = { contents[tag]:1 }
			elif user_topic[ contents[0] ].get( contents[tag] ) == None:
				user_topic[ contents[0] ][ contents[tag] ] = 1
			user_topic[ contents[0] ][ contents[tag] ] += 1
			tags.append(contents[tag])
		if problem_tag.get( problem_idx[problemname] ) == None:
			problem_tag[ problem_idx[problemname] ] = tags
		fout.write(str(user_idx[ contents[0] ])+' '+str(problem_idx[ problemname ] )+' 1\n')
	fout.close()

	user_tags={}
	for username in user_topic:
		tags={}
		for tag in user_topic[username]:
			tags[tag]=user_topic[username][tag];
		user_tags[username]=tags

	fout = open("user_tags.txt",'w')
	json.dump(user_tags,fout)
	fout.close()

	fout = open("user_name.txt",'w')
	json.dump(user_name,fout)
	fout.close()

	fout = open("problme_name.txt",'w')
	json.dump(problem_name,fout)
	fout.close()
	
	fout = open("problem_tags.txt",'w')
	json.dump(problem_tag,fout)
	fout.close()

	fout = open("user_done.txt",'w')
	json.dump(user_done,fout)
	fout.close()

process_data()
