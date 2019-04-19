# -*- coding: utf-8 -*


import re
import requests
import time
from cookieHelper import CookieClass

class DisHelperClass_us:
	def __init__(self,trip_id, except_list, username, password):
		self.trip_id = trip_id
		self.except_list = except_list
		self.page_size = '100'
		self.cookieObj = CookieClass(username, password)
		self.username=username


	def generalinfo_digger(self, issue_id):
		# url = 'http://voyager.intra.didiglobal.com/daypack/disengage/query/?category_name=&page=1&currentZone=0&id='+issue_id
		# url = 'http://voyager.intra.didiglobal.com/daypack/disengage/query/'
		# url = "http://voyager.intra.xiaojukeji.com/daypack/disengage/query/?tags=&id="+issue_id+"&description=&category_name=&version=&robot_number=&jira=&status=&lat_s=&lat_e=&lon_s=&lon_e=&user_name=&disengage_time_start=&disengage_time_end=&bag_exist=&page=1"
		#cookies = cookie_helper()
		url = "http://voyager.intra.didiglobal.com/daypack/disengage/query/?tags=&id=" + issue_id + "&description=&category_name=&version=&robot_number=&jira=&status=&lat_s=&lat_e=&lon_s=&lon_e=&user_name=&disengage_time_start=&disengage_time_end=&bag_exist=&page=1"
		print(url)
		#cookies = cookie_helper()
		cookies = self.cookieObj.get_cookie()
		# cookies = {"username": "zhuzhenxia:1h9KQy:QrN2q3CKWzR-Nv6s3Ltcy28BxVs", "ticket": "743df6b4dbee30908bbc11dd03e87e260001098000:1h9KQy:VH5k0L30Ktb_ONVfhp0mWwEzzoc"}

		headers = {'Host': 'voyager.intra.didiglobal.com',
				   'Connection': 'keep-alive',
				   # 'Content-Length': '45',
				   'Accept': 'application/json, text/plain, */*',
				   'Origin': 'http://voyager.intra.didiglobal.com',
					'x-requested-with': 'XMLHttpRequest',
				   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.28 Safari/537.36',
				   'Content-Type': 'application/x-www-form-urlencoded',
				   'Referer': 'http://voyager.intra.didiglobal.com/static/management/',
				   'Accept-Encoding': 'gzip, deflate',
				   'Accept-Language': 'zh-CN,zh;q=0.9',
				   'Cookie': 'ticket=2d347589a15ecf09611eea11d873a0120001098000:1hAb1Z:x7Q8mh4ghahYCshdfYkYeeJVYMI; username=zhuzhenxia:1h9l7n:M9QNOiLfEaS3mbUgkfgcnOEZzO8'
				   }
		# headers['Cookie'] = str(cookies)
		print(str(cookies))
		# response = requests.get(url,cookies=cookies,timeout=200)

		response = requests.get(url,cookies=cookies, headers=headers,timeout=10)


		content = response.content.decode('utf-8')  #for python3
		timestamp = self.find_timestamp(content)
		trip = self.find_trip(content)
		category, category_id = self.find_category(content)
		version = self.find_version(content)
		baglink = self.find_baglink(content)
		description = self.find_description(content)
		return timestamp, trip, category, version, baglink,description
		print(description)


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

	def find_description(self, content):
		rule = r'\"description\"\:\s\"(.+)'
		description = re.findall(rule, content)
		description = description[0].split('",')[0]
		return description


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
		robot_number= re.findall(rule, content)
		robot_number = robot_number[0].split('",')[0]
		return robot_number


if __name__ == "__main__":
	issue = DisHelperClass_us(None,None,'zhuzhenxia','pwd')
	output = issue.generalinfo_digger('313984')
	# output = issue.generalinfo_digger('598221')
	print(output)
	pass

