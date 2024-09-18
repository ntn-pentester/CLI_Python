from asyncio import subprocess
import requests
import html
import argparse
import re
import sys
import os
from os import listdir
from os.path import isfile

parser = argparse.ArgumentParser(description="Python Exam")
parser.add_argument('--exploit EXPLOIT',type=str,metavar="",help="exploit ID")
parser.add_argument('--page PAGE',type=int,metavar="",help="get page")
parser.add_argument('--search SEARCH',type=str,metavar="",help="Search keyword")
args = vars(parser.parse_args())

path = './exploit-db'
try:
	os.mkdir(path)
except:
    pass

def exploit_func(id):
	if not os.path.exists(id):
		search_id = re.search(r'([http|https]\:\/\/)?([a-zA-Z0-9\.\/\?\:@\-_=#]+\.[a-zA-Z]{2,6}\/)?([a-zA-Z0-9\.\/\?\:@\-_=#]+\/)?(\d+)', id)			
		if search_id:
			id = search_id.group(4)
		else:
			return	
		url = 'https://exploit-db.com/exploits/{}'.format(id)
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
		res = requests.get(url, headers = headers)

		exploit = res.text[res.text.find('<code') : res.text.find('</code>')]
		exploit = html.unescape(exploit[exploit.find('">') +2 :])
		
		file_output = open('exploit-db\\' + str(id) + ".txt", 'w', encoding='utf-8')
		file_output.write(exploit)
		file_output.close()
		if os.name == "nt":
			os.system("notepad exploit-db\\" + str(int(id))+".txt")
		elif os.name == "posix":
			os.system("xdg-open exploit-db\\" + str(int(id))+".txt")
  
def page_func(id):
	# print('===> Run page')
	list_poc = []
	onlyfiles = []
	for f in listdir(path):
		if isfile(path +"/"+ f):
			onlyfiles.append(f)
	for filename in onlyfiles:
		basename = os.path.basename(filename)
		basename_split = os.path.splitext(basename)
		list_poc.append(int(basename_split[0]))
	list_poc.sort()
	pages = list([list_poc[i:i + 5] for i in range(0, len(list_poc), 5)])
	for poc in pages[id]:
		print(poc)	
 
def search_func(keyword):
    # print('===> Run search')
	for file in listdir(path):
		data = open(path+"/"+file, 'r', encoding='utf-8')
		for each_keyword in keyword:
			if re.search("\\b{}\\b".format(each_keyword), data.read()):
				print(path+"/"+file)

if __name__ == '__main__':
	exploit = args['exploit EXPLOIT']
	page = args['page PAGE']
	search = args['search SEARCH']
	try:
		if len(sys.argv) < 3:
			parser.print_help()
		else:
			if exploit:
				exploit_func(exploit)
			elif page != None:
				page_func(page)
			elif search:
				search_func(search)
	except:
		parser.print_help()
		sys.exit(0)
