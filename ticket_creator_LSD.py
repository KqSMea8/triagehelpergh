# -*- coding: utf-8 -*
"""
	软件：LSD ticket Creator
	版本：v2.3
	作者：朱振夏
	时间：08/11/2018
	功能：1.1 根据用户输入的LSD Job ID，Event ID 和 Binary ID 自动创建 Jira Ticket
	2.0：a. 根据用户输入的 Job ID 自动获取 Binary ID
		 b. 根据用户填写的 Event ID 自动获取 review status （2- True positive，3- False positive）
		 c. 自动获取Trip ID 、 collision 时间，time range
		 d. 自动获取用户选择了哪个Module
		 e. 生成tickets的时候，增加一个TP / FP 的标签
		 f. 由于仿真平台更新至orion了，自动生成的链接访问不到event了，修复。
	2.1 a. binary 链接更改至orion
		b. 标签改成planningV2 和 predictionV2 ✘
	3.0 a. 允许用户选择 TP/FP/HPE 三种 collision type
		b. 生成的ticket中加入了 All events 链接

"""
from DisHelper import DisHelperClass
from jira import JIRA
from jira.exceptions import JIRAError
import requests
from cookieHelper import CookieClass


class Creator_LSD:
	def __init__(self, username, password, LSD_job_id, LSD_event_id, collision_type):
		self.username = username
		self.password = password
		self.LSD_job_id = LSD_job_id
		self.LSD_event_id = LSD_event_id
		self.cookieObj = CookieClass(username, password)
		self.dis = DisHelperClass(None, None, username, password)
		self.collision_type = collision_type

	def get_binary_ID(self):
		LSD_job_id = self.LSD_job_id
		url = 'http://voyager.intra.xiaojukeji.com/simulation/lsdjobreport/query/?id=' + LSD_job_id + '&ids=' + LSD_job_id +' &previous=0&size=1'
		cookies = self.cookieObj.get_cookie()
		response = requests.get(url, cookies = cookies)
		content = response.content.decode('utf-8')
		try:
			binary_id = eval(content)['data']['res'][0]['binary_id']
			print('binary id = %s' % binary_id)
		except IndexError:
			print('Please check the Job ID')
			binary_id = ''

		return binary_id


	def get_event_info(self):
		job_id = self.LSD_job_id
		event_id = self.LSD_event_id

		url = 'http://voyager.intra.xiaojukeji.com/simulation/lsdevent/query/?name_icontains=collision&orion_job_id=' + job_id + '&populate_extra_fields=1&id='+event_id
		cookies = self.cookieObj.get_cookie()
		response = requests.get(url, cookies = cookies)
		try:
			content = response.content.decode('utf-8')
			dct = eval(content)['data']['res'][0]
			info_dict = dict(zip(['trip_id', 'collision_time', 'start_time',
								'end_time', 'review_status', 'module'],
								[str(dct['trip_id']), str(dct["timestamp"]), str(dct['segment_start_timestamp']),
								str(dct['segment_end_timestamp']),dct['review_status'], dct['module']]))
		except:
			print('Please check Job ID and Event ID')
			print('Create Ticket Failed !')
			info_dict = {}

		return info_dict

	def createJira_LSD(self):
		collision_type = self.collision_type
		job_id = str(self.LSD_job_id)
		event_id = str(self.LSD_event_id)
		binary_id = str(self.get_binary_ID())
		info_dict = self.get_event_info()

		[trip_id, timestamp, start_time, end_time, review_status, module] = info_dict.values()

		print(info_dict.keys())
		print([trip_id, timestamp, start_time, end_time])
		[trip_id, timestamp, start_time, end_time] = \
			[str(trip_id), str(timestamp), str(start_time), str(end_time)]

		status = collision_type
		if collision_type == 'HPE':
			status = 'FP'


		jira = JIRA('http://agile.intra.xiaojukeji.com/',basic_auth=(self.username, self.password))
		summary = '[LSD] 请插入问题描述'
		issue_dict = {
			'project': {'id': '11936', 'key' : 'VOYAGER'},
			'issuetype': {'id': '1'},
			'summary': summary,
			'labels': ['triage-medium-state']
		}

		try:
			new_issue = jira.create_issue(fields=issue_dict)
		except JIRAError as e:
			print(e.status_code, e.text)

		update_issue = jira.search_issues('project = VOYAGER AND issuetype = Bug AND labels = triage-medium-state' )
		update_issue = update_issue[0]
		task_id = str(update_issue.key).split('-')[1]
		description = 'h3. General info:\n' \
					'1. Job ID: [' + job_id +'|http://voyager.intra.xiaojukeji.com/static/management/#/lsd/job/report?id=' + job_id + '&ids=' + job_id + '&previous=0]\n\n' \
					'2. Binary: [' + binary_id + '|http://voyager.intra.xiaojukeji.com/static/management/#/orion/binary/list?page=1&size=50&id='+ binary_id + ' ]\n\n' \
					'3. Main Event: [' + event_id + '|http://voyager.intra.xiaojukeji.com/static/management/#/lsd/event/grids?name_icontains=collision&orion_job_id='+ job_id + '&populate_extra_fields=1&labels=&id=' + event_id + ']\n\n' \
					'4. [All Event links. |http://voyager.intra.xiaojukeji.com/static/management/#/lsd/event/grids?name_icontains=collision&populate_extra_fields=1&issue_id='+ task_id + ']\n\n' \
					'5. Collision Type: ' + status + '\n\n' \
					'6. Trip ID: ' + trip_id + '\n\n' \
					'7. Segment Time Range:'+ start_time + '-' + end_time + '\n\n ' \
					'8. Collision Timestamp:'+ timestamp + ' \n\n h3. Description of the main event：\n\n'

		issueupdate = {
			    'description': description,
			    'labels':['Triage','LSD', collision_type]
			}

		update_issue.update(issueupdate)

		print('New ticket is created!  Jira ID is :' + task_id)

def main():
	lsd_ticket = Creator_LSD('zhuzhenxia', 'pwd', '22515', '2757181', 'HPE')
	lsd_ticket.createJira_LSD()
	print('done')



if __name__ == "__main__":
	main()
