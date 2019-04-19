# -*- coding: utf-8 -*
"""
v2.5 2019.03.22
	a. Add on the link to main issue in ticket description √
	b. If it is a Dailybuild issue, create a Dailybuild ticket
	c. Rename the ticket title begin with the last level of disengage category. √
	d. Assign to internal owner √
	e. Add scenario link √
	f. fill in the verision with release_version √

"""

from DisHelper import DisHelperClass
import getopt
from jira import JIRA
from jira.exceptions import JIRAError
import json
import re
import requests
from requests.cookies import RequestsCookieJar  
import sys


class Creator:
	def __init__(self, username, password, issue_id, safety_id):
		self.username = username
		self.password = password
		self.issue_id = issue_id
		self.safety_id = safety_id
		self.dis = DisHelperClass(None, None, username, password)


	def safety_issue(self):
		jira = JIRA('http://agile.intra.xiaojukeji.com/',basic_auth=(self.username, self.password))
		safety_issue = jira.issue(self.safety_id);
		head_summary = safety_issue.fields.summary
		head_summary = re.split(r']', head_summary)[0]+']['+ self.safety_id + ']'
		return head_summary

	def create_jira(self):

		timestamp, trip, category, version, baglink = self.dis.generalinfo_digger(str(self.issue_id))

		jira = JIRA('http://agile.intra.xiaojukeji.com/',basic_auth=(self.username, self.password))
		#meta = jira.createmeta(projectKeys='VOYAGER', issuetypeIds=1)

		owner = ''
		if 'perception' in category:
			owner = 'baijing'
		if 'prediction' in category:
			owner = 'georgegaoqi'
		if 'planning' in category:
			owner = 'fionabaige'
		if 'map' in category:
			owner = 'lihongyun'
		if 'control' in category:
			owner = 'zhuzhenxia'
		if 'Infra' in category:
			owner = 'liufubo'

		issue_type = category.split('/')[-1]
		print('issue_type: ', issue_type)

		summary = '[#'+str(self.issue_id)+']' + issue_type + '.'
		release_version = version.split('.')[1]
		release_version = re.sub('-', '_', release_version)
		print(release_version)
		# release_version = 'release_20190125'
		issue_dict = {
			'project':{'id':'11936','key':'VOYAGER'},
			'issuetype':{'id':'1'},
			'summary': summary,
			'labels':['triage-medium-state'],
					}
		try:
			new_issue = jira.create_issue(fields=issue_dict)
		except JIRAError as e:
			print(e.status_code, e.text)


		update_issue = jira.search_issues('project = VOYAGER AND issuetype = Bug AND labels = triage-medium-state' )
		update_issue = update_issue[0]
		task_id = str(update_issue.key).split('-')[1]
		print('ticket:', task_id)
		issue_link = 'http://voyager.intra.xiaojukeji.com/static/management/#/issue/list?tags=&id=&description=&category_name=&version=&robot_number=&jira='+task_id+'&status=&lat_s=&lat_e=&lon_s=&lon_e=&user_name=&disengage_time_start=&disengage_time_end=&bag_exist=&page=1'
		# release_version = version[:16]
		description = 'h3. General info:\n' \
					'	1. Trip ID：'+trip+'\n' \
					'	2. Exact version is '+version+'\n' \
					'	3. Category: \n* '+category+'\r\n\n' \
					'	4. Timestamp: '+timestamp+' [rosbag|'+baglink+']\n' \
					'	5. [Issues list link|'+issue_link+']\n' \
					'	6. Main issue:['+str(self.issue_id)+'|http://voyager.intra.xiaojukeji.com/static/management/#/issue/list?id='+str(self.issue_id)+'&category_name=&currentZone=0&page=1]\n'\
					'	7. [Scenarios|http://voyager.intra.xiaojukeji.com/static/management/#/scenario/list?page=1&size=50&labels=VOYAGER-'+task_id+']\n'\
					'h3. Description of issue '+str(self.issue_id)+':\n' \
					'h3. Triage comments：'

		if self.safety_id != None:
			self.safety_id = 'VOYAGERRT-'+ str(self.safety_id)
			head_summary = self.safety_issue()
			jira.create_issue_link(type="relates to",inwardIssue=update_issue.key, outwardIssue=self.safety_id)

			issueupdate = {
				'summary': head_summary + summary,
				'description': description,
				'labels': ['Triage', '日报高优（Triage）'],
			}
		else:
			issueupdate = {
					'description': description,
					'labels':['Triage'],
					'assignee': {'name': owner},
				}
			print('owner:', owner)
			update_issue.update(issueupdate)

		try:
			issueupdate = {
					'versions': [{'name': release_version}]
				}
			update_issue.update(issueupdate)
			print('release_version: ', release_version)
		except JIRAError:
			print('[Warining]: Version {} does NOT excist! \n Please contact Fubo to add it to jira. \n'.format(release_version) *3)



if __name__ == "__main__":

	ticket = Creator('zhuzhenxia', 'pwd', 598221, None)
	ticket.create_jira()
	pass

	
