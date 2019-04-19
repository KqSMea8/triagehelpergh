# -*- coding: utf-8 -*

import getopt
from jira import JIRA
from jira.exceptions import JIRAError
import json
import re
import requests
from requests.cookies import RequestsCookieJar  
import sys
import string
import time
import math
from cookieHelper import CookieClass
import os
import getpass

class DisHelperClass:
	def __init__(self,trip_id, except_list, username, password):
		self.trip_id = trip_id
		self.except_list = except_list
		self.page_size = '100'
		self.cookieObj = CookieClass(username, password)
		self.username=username

	def download_simulation(self):
		print('请确定在Ubuntu系统下进行该操作！')
		print("开始下载与仿真")
		# trip_url = 'http://voyager.intra.xiaojukeji.com/daypack/disengage/query/?categoryname=&currentZone=0&page=1&id=' + self.issue_id
		trip_url = 'http://voyager.intra.xiaojukeji.com/daypack/disengage/query/?uncategorized=1&category_name=uncategorized&currentZone=0&page=1&size=100&reviewer=' + self.username
		cookies = self.cookieObj.get_cookie()
		filter_resp = requests.get(trip_url, cookies=cookies)
		resp_content = filter_resp.content.decode('utf-8')
		# print(resp_content)
		issue_id_list = self.find_issue_id_list(resp_content)
		print("issue_id_list: \n"+",".join(issue_id_list))
		trip_id_list = self.find_trip_id_list(resp_content)
		# print(trip_id_list)
		disengage_time_list = self.find_disengage_time_list(resp_content)
		#执行命令行
		os.chdir('/home/'+getpass.getuser()+'/voyager')
		file = open('disengagelist.txt', 'w')
		file.write(" ".join(issue_id_list))
		file.write("\n")
		file.write(" ".join(trip_id_list))
		file.write("\n")
		file.write(" ".join(disengage_time_list))
		file.close()
		#执行命令行
		#print(getpass.getuser())

		os.system("bash /home/%s/voyager/DownloadSimlation.sh"%(getpass.getuser()))
		#output=os.popen("./DownloadSimlation.sh",'r')
		#print(output.read())

	# print(disengage_time_list)

	def txt_output(self):
		print('开始生成txt')
		# trip_url = 'http://voyager.intra.xiaojukeji.com/daypack/disengage/query/?categoryname=&currentZone=0&page=1&id=' + self.issue_id
		trip_url = 'http://voyager.intra.xiaojukeji.com/daypack/disengage/query/?uncategorized=1&category_name=uncategorized&currentZone=0&page=1&size=100&reviewer=' + self.username
		cookies = self.cookieObj.get_cookie()
		# print(self.username)
		filter_resp = requests.get(trip_url, cookies=cookies)
		resp_content = filter_resp.content.decode('utf-8')
		# print(resp_content)
		issue_id_list = self.find_issue_id_list(resp_content)
		print(issue_id_list)
		trip_id_list = self.find_trip_id_list(resp_content)
		# print(trip_id_list)
		disengage_time_list = self.find_disengage_time_list(resp_content)
		# print(disengage_time_list)
		# 写入txt
		file = open('disengagelist.txt', 'w')
		file.write(" ".join(issue_id_list))
		file.write("\n")
		file.write(" ".join(trip_id_list))
		file.write("\n")
		file.write(" ".join(disengage_time_list))
		file.close()
		print('txt已生成')

	def generalinfo_digger(self, issue_id):
		url = "http://voyager.intra.xiaojukeji.com/daypack/disengage/query/?tags=&id="+issue_id+"&description=&category_name=&version=&robot_number=&jira=&status=&lat_s=&lat_e=&lon_s=&lon_e=&user_name=&disengage_time_start=&disengage_time_end=&bag_exist=&page=1"		#cookies = cookie_helper()
		cookies = self.cookieObj.get_cookie()
		response = requests.get(url, cookies = cookies)
		content = response.content.decode('utf-8')  #for python3
		timestamp = self.find_timestamp(content)
		trip = self.find_trip(content)
		category, category_id = self.find_category(content)
		version = self.find_version(content)
		baglink = self.find_baglink(content)
		return timestamp, trip, category, version, baglink



	def find_week_release(self, start_timestamp, end_timestamp):
		#find page_count per week
		url = 'http://voyager.intra.xiaojukeji.com/daypack/disengage/query/?tags=&id=&description=&category_name=&version=release_20&robot_number=&jira=&status=&lat_s=&lat_e=&lon_s=&lon_e=&user_name=&disengage_time_start='+start_timestamp+'&disengage_time_end='+end_timestamp+'&bag_exist=&page=10000&size=500'
		cookies = self.cookieObj.get_cookie()
		resp = requests.get(url, cookies = cookies)
		content = resp.content.decode('utf-8')
		issue_count = self.find_count(content)
		page_count = int(math.ceil(int(issue_count) / 500))
		#find all related release in this week:
		release_list = []
		for i in range(page_count):
			url = 'http://voyager.intra.xiaojukeji.com/daypack/disengage/query/?tags=&id=&description=&category_name=&version=release_20&robot_number=&jira=&status=&lat_s=&lat_e=&lon_s=&lon_e=&user_name=&disengage_time_start='+start_timestamp+'&disengage_time_end='+end_timestamp+'&bag_exist=&page='+str(i+1)+'&size=500'

			cookies = self.cookieObj.get_cookie()
			filter_resp = requests.get(url, cookies = cookies)
			resp_content = filter_resp.content.decode('utf-8')
			release_list.extend(self.find_release_list(resp_content))
			release_list = list(set(release_list))
		return release_list

	def weekly_report_filter(self, release_list):		
		all_jira = {}
		all_category = {}
		for release in release_list:
			all_jira[release] = []
			all_category[release] = []
			#find page_count per release
			url = 'http://voyager.intra.xiaojukeji.com/daypack/disengage/query/?tags=&id=&description=&category_name=&version='+release+'&robot_number=&jira=&status=1&lat_s=&lat_e=&lon_s=&lon_e=&user_name=&disengage_time_start=&disengage_time_end=&bag_exist=&page=1&size=500'
			cookies = self.cookieObj.get_cookie()
			resp = requests.get(url, cookies = cookies)
			content = resp.content.decode('utf-8')
			issue_count = self.find_count(content)
			page_count = int(math.ceil(int(issue_count) / 500))

			#find all jira and category related to this release
			jira_list = []
			category_list = []
			for i in range(page_count):
				url = 'http://voyager.intra.xiaojukeji.com/daypack/disengage/query/?tags=&id=&description=&category_name=&version='+release+'&robot_number=&jira=&status=1&lat_s=&lat_e=&lon_s=&lon_e=&user_name=&disengage_time_start=&disengage_time_end=&bag_exist=&page='+str(i+1)+'&size=500'
				cookies = self.cookieObj.get_cookie()
				resp = requests.get(url, cookies = cookies)
				content = resp.content.decode('utf-8')
				jira_list.extend(self.find_jira_list(content))
				jira_list = list(set(jira_list))
				category_list.extend(self.find_category_list(content))

			#how many issues are categorized into the same category
			category_set = set(category_list)
			IssueCount_in_category = {}
			for category in category_set:
				IssueCount_in_category[category] = category_list.count(category)
			# get sorted category list
			IssueCount_in_category = sorted(IssueCount_in_category.items(),key = lambda x:x[1], reverse = True)
			#IssueCount_in_category_top5 = IssueCount_in_category[:5]
			#all_category[release] = IssueCount_in_category
			#print(IssueCount_in_category)



			#how many issues are related to certain jira in this release?
			for jira in jira_list:
				url = 'http://voyager.intra.xiaojukeji.com/daypack/disengage/query/?tags=&id=&description=&category_name=&version='+release+'&robot_number=&jira='+jira+'&status=1&lat_s=&lat_e=&lon_s=&lon_e=&user_name=&disengage_time_start=&disengage_time_end=&bag_exist=&page=1&size=10'
				cookies = self.cookieObj.get_cookie()
				resp = requests.get(url, cookies = cookies)
				content = resp.content.decode('utf-8')
				issue_count = self.find_count(content)
				all_jira[release].append((jira,issue_count))

			#which jira was linked to this category?
			for category, count in IssueCount_in_category:
				category_tree = category.split('/')
				category_2 = ''
				for each in category_tree:
					category_2 = category_2 + each +'%2F'
				category_2 = category_2[:-3]
				url = 'http://voyager.intra.xiaojukeji.com/daypack/disengage/query/?tags=&id=&uncategorized=&category_name=["'+category_2+'"]&version='+release+'&description=&robot_number=&jira=&status=1&trip_id=&lat_s=&lat_e=&lon_s=&lon_e=&user_name=&publish_date_start=&publish_date_end=&bag_exist=&page=1&size=500'
				cookies = self.cookieObj.get_cookie()
				resp = requests.get(url, cookies = cookies)
				content = resp.content.decode('utf-8')
				issue_count = self.find_count(content)
				tickets = self.find_jira_list(content)
				tickets = list(set(tickets))
				print(category, tickets)
				all_category[release].append((category, count, tickets))

		return all_jira, all_category 



	def timestamp_datatime(self, value):
		format = '%Y-%m-%d %H:%M'
		value = time.localtime(value)
		dt = time.strftime(format,value)
		return dt

	def datetime_timestamp(self, dt):
		time.strptime(dt,'%Y-%m-%d %H:%M')
		s = time.mktime(time.strptime(dt,'%Y-%m-%d %H:%M'))
		return s

	def find_count(self, content):
		rule = r'\"count\"\:\s(\d+)'
		count= re.findall(rule, content)[0]
		return count

	def find_release_list(self,content):
		rule = r'\"version\"\:\s\"(.{16})'
		release_list= re.findall(rule, content)
		return release_list

	def find_issue_list(self, content):
		rule = r'\"id\"\:\s(\d+)'
		issue_list= re.findall(rule, content)
		return issue_list

	def find_issue_id_list(self, content):
		rule = r'\"id\"\:\s(\d+)'
		issue_id_list= re.findall(rule, content)
		return issue_id_list

	def find_trip_id_list(self, content):
		rule = r'\"disengage_time\"\:\s(\d+)'
		timestamp = re.findall(rule, content)
		return timestamp


	def find_disengage_time_list(self, content):
		rule = r'\"trip_id\"\:\s\"(.{21})'
		trip = re.findall(rule, content)
		return trip

	def find_jira_list(self, content):
		rule = r'\"jira\"\:\s\"(\d+)'
		jira_id= re.findall(rule, content)
		return jira_id

	def find_jira(self, content):
		rule = r'\"jira\"\:\s\"(\d+)'
		jira_id= re.findall(rule, content)
		jira_id.append('')
		return jira_id[0]

	def find_timestamp(self, content):
		rule = r'\"disengage_time\"\:\s(\d+)'
		timestamp= re.findall(rule, content)
		return timestamp[0]

	def find_trip(self, content):
		rule = r'\"trip_id\"\:\s\"(.{21})'
		trip= re.findall(rule, content)
		return trip[0]
	
	def find_category(self, content):
		rule = r'\"category_name\"\:\s\"(.+)'
		category = re.findall(rule, content)
		category = category[0].split('",')[0]
		rule = r'\"category_id\"\:\s(\d+)'
		category_id = re.findall(rule, content)[0]
		return category, category_id
	

	def find_category_list(self, content):
		rule = r'\"category_name\"\:\s\"(.*?)\"'
		category = re.findall(rule, content)
		#category = category[0].split('",')
		return category

	def find_version(self, content):
		rule = r'\"version\"\:\s\"(.+)'
		version= re.findall(rule, content)
		version = version[0].split('",')[0]
		return version

	def find_baglink(self, content):
		rule = r'\"car_id\"\:\s\"(\d+)'
		robot_number= re.findall(rule, content)
		#timestamp = long(find_timestamp(content))  #for python2
		timestamp = int(self.find_timestamp(content))
		start_time = str(timestamp - 20000)
		end_time = str(timestamp + 20000)
		baglink = 'http://voyager.intra.xiaojukeji.com/static/management/#/segment/list?robot_number='+robot_number[0]+'&start_time='+start_time+'&end_time='+end_time
		return baglink

	def find_coordinates(self, content):
		rule = r'\"lon\"\:\s\"(.+)'
		lon = re.findall(rule, content)
		lon = lon[0].split('",')[0]
		rule = r'\"lat\"\:\s\"(.+)'
		lat= re.findall(rule, content)
		lat = lat[0].split('",')[0]
		return lon,lat

	def find_tag(self, content):
		rule = r'\"tags\"\:\s\[\"(.+)'
		tag = re.findall(rule, content)
		tag = tag[0].split('"],')[0]
		return tag

	def find_robotnum(self, content):
		rule = r'\"car_id\"\:\s\"(.+)'
		robot_number = re.findall(rule, content)
		robot_number = robot_number[0].split('",')[0]
		return robot_number


if __name__ == "__main__":
	pass

