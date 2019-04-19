# -*- coding: utf-8 -*
"""
	v2.5 2019.03.22
	a. create ticket for US road test

"""

from DisHelper import DisHelperClass
from DisHelper_us import DisHelperClass_us
import getopt
from jira import JIRA
from jira.exceptions import JIRAError
import json
import re
import requests
from requests.cookies import RequestsCookieJar
import sys


class Creator_us:
    def __init__(self, username, password, issue_id):
        self.username = username
        self.password = password
        self.issue_id = issue_id
        self.dis = DisHelperClass_us(None, None, username, password)


    def create_jira(self):

        timestamp, trip, category, version, baglink, description = self.dis.generalinfo_digger(str(self.issue_id))
        jira = JIRA('http://agile.intra.xiaojukeji.com/', basic_auth=(self.username, self.password))

        summary = '[#' + str(self.issue_id) + ']' + description
        release_version = version.split('.')[1]
        release_version = re.sub('-', '_', release_version)
        print(release_version)
        issue_dict = {
            'project': {'id': '11936', 'key': 'VOYAGER'},
            'issuetype': {'id': '1'},
            'summary': summary,
            'labels': ['triage-medium-state'],
        }
        try:
            new_issue = jira.create_issue(fields=issue_dict)
        except JIRAError as e:
            print(e.status_code, e.text)

        update_issue = jira.search_issues('project = VOYAGER AND issuetype = Bug AND labels = triage-medium-state')
        update_issue = update_issue[0]
        task_id = str(update_issue.key).split('-')[1]
        print('ticket:', task_id)
        issue_link = 'http://voyager.intra.didiglobal.com/static/management/#/issue/list?category_name=&page=1&currentZone=0&jira='+str(task_id)

        description ='h3. General info:\n' \
		        '1. Trip ID：' + trip + '\n' \
	            '2. Exact version is ' + version + '\n' \
                '3. Op report link:\n'\
				'4. Timestamp: ' + timestamp +'\n' \
				'5. [All related Issues link|' + issue_link + ']\n' \
			   	'6. Main issue:[' + str(self.issue_id) + '|http://voyager.intra.didiglobal.com/static/management/#/issue/list?category_name=&page=1&currentZone=0&id='+ str(self.issue_id)+']\n'\
			 	'7. [Scenarios|http://voyager.intra.xiaojukeji.com/static/management/#/scenario/list?page=1&size=50&labels=VOYAGER-' + task_id + ']\n' \
  				'h3. Description of issue ' + str(self.issue_id) + ' from Ops:\n* '+ description +'\n\n' \
			 	'h3. Triage comments：\n\n'

        issueupdate = {'description': description,
                       'labels': ['Triage', 'dailybuild-US']
                       }
        update_issue.update(issueupdate)

        try:
            issueupdate = {
                'versions': [{'name': release_version}]
            }
            update_issue.update(issueupdate)
            print('release_version: ', release_version)
        except JIRAError:
            print('[Warining]: Version {} does NOT excist! \n Please contact Fubo to add it to jira. \n'.format(release_version) * 3)


if __name__ == "__main__":
    ticket = Creator_us('zhuzhenxia', 'pwd', 313984)
    ticket.create_jira()
    pass


