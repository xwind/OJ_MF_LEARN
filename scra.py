import urllib.request
import os
import re
import json
import sys

def getdata(uname):
	url="https://vjudge.net/status/#un="+uname+"&OJId=All&probNum=&res=1&orderBy=run_id&language="
	#print (url)
	req = urllib.request.Request(url)
	req.add_header('Referer','https://vjudge.net/status/data/')
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')
	tmp = urllib.request.urlopen(req)	
	page =tmp.read()
	return page.decode('utf8')

def getsub(uname):
	url="http://codeforces.com/api/user.status?handle="+uname+"&from=1"
	while True:
		try:
			req = urllib.request.Request(url)
			req.add_header('Referer','https://vjudge.net/status/data/')
			req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')
			tmp = urllib.request.urlopen(req)	
			break
		except:
			sys.stderr.write("network error")
	js=json.loads(tmp.read().decode('utf-8'))
	if js['status'] == 'OK' :
		return js['result']
	else:
		return []

def getuser():
	fout = open('user2.txt','w')
	for i in range(10,20):
		print ('process: '+str(i)+' page')
		url="http://codeforces.com/problemset/standings/page/"+str(i)
		req = urllib.request.Request(url)
		req.add_header('Referer','https://vjudge.net/status/data/')
		req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')
		tmp = urllib.request.urlopen(req)	
		html=tmp.read()
		users = re.findall('"rated-user user-(orange|red|violet)">([\w\d_]+)</a>',str(html))
		for name in users:
			fout.write(str(name[1])+' ')
	fout.close()

def getuserinfo(uname):
	js = getsub(uname)
	#fout = open(user+".dat",'w')
	for entry in js:
		if entry['verdict'] == 'OK' :
			print (uname,entry['problem']['contestId'],entry['problem']['index'],entry['passedTestCount'],end=' ')
			for tag in entry['problem']['tags']:
				print (tag['name'],end=' ')
			print ()
			#fout.write(str(entry)+'\n')

ulst = input().split()
#getuserinfo('StefanoT')
sys.stderr.write(str(len(ulst))+'\n')
sys.stderr.flush()
for uname in ulst:
	sys.stderr.write(uname+'\n')	
	sys.stderr.flush()
	getuserinfo(uname)
