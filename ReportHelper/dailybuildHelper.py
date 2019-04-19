import sys
sys.path.append("..")

import re
import requests
from requests.cookies import RequestsCookieJar  
from cookieHelper import CookieClass
import utils.google_utils as google
from jira import JIRA


class CN_dbHelperClass:
	def __init__(self, username, password, TestReport_doc_ID, TriageReport_sheet_ID):
		self.cookieObj = CookieClass(username, password)
		self.username = username
		self.password = password
		self.TestReport_doc_ID = TestReport_doc_ID
		self.TriageReport_sheet_ID = TriageReport_sheet_ID

	def read_TestReport(self):
		
		creds = google.get_googleCred()
		# The ID of a sample document.
		data = google.read_googleDoc(creds, self.TestReport_doc_ID)

		#extract all numbers in the doc
		issue_list = []
		for item in data:
			try:
				content = item['paragraph']['elements'][0]['textRun']['content']
				issue_list.extend(re.findall(r"\d+",content))		
			except:
				print ("error in this line")
				pass

		#extract all issue numbers in the doc and convert to string
		issue_list = [x for x in issue_list if len(x)>5 and len(x)<=7]
		issue_list = str(issue_list).strip('[]').replace("'",'')

		return issue_list

		
	def read_TriageReport(self,sheet_name):
		creds = google.get_googleCred()
		RANGE_NAME = sheet_name+'!A:A'
		issue_list = google.read_googleSheet(creds, self.TriageReport_sheet_ID, RANGE_NAME)[1:]

		issue_list = str(issue_list).strip('[]').strip("'").replace("['",'').replace("']",'')
		print('issue list:',issue_list)

		url = 'http://voyager.intra.xiaojukeji.com/daypack/disengage/query/?currentZone=0&page=1&size=50&category_name=&id='+issue_list

		cookies = self.cookieObj.get_cookie()
		response = requests.get(url, cookies = cookies)
		content = response.content.decode('utf-8')
		content = eval(content)
		issues = content['data']['res']
		print([issue['id'] for issue in issues])

		issue_bag_jira = [(issue['id'],("NO","YES")[issue['bag_exist']], issue['jira']) for issue in issues]
		return issue_bag_jira

		



	def append_TriageReport(self,issue_list,sheet_name, sheet_id):
		if issue_list == '':
			print('no new issue appended')
		else:
			url = 'http://voyager.intra.xiaojukeji.com/daypack/disengage/query/?currentZone=0&page=1&size=50&category_name=&id='+issue_list
			cookies = self.cookieObj.get_cookie()
			response = requests.get(url, cookies = cookies)
			content = response.content.decode('utf-8')
			content = eval(content)
			issues = content['data']['res']

			data = {'values': [
					[
	                  '=HYPERLINK("http://voyager.intra.xiaojukeji.com/static/management/#/issue/list?id='+str(issue['id'])+'&category_name=&currentZone=0&page=1",'+str(issue['id'])+')'
	                 ,
	                 issue['create_time'],
	                 issue['version'],
	                 issue['car_id'],
	                 issue['driver_name'], 
	                 issue['tags'][0], 
	                 issue['description'], 
	                 ("NO","YES")[issue['bag_exist']],
	                 ('=HYPERLINK("http://agile.intra.xiaojukeji.com/browse/VOYAGER-'+str(issue['jira'])+'",'+str(issue['jira'])+')' , '')[issue['jira'] == ''],
	                 '', 
	                 '',
	                 '', 
	                 '', 
	                 ''] 
	                 for issue in issues]}
			
			SAMPLE_RANGE_NAME = sheet_name+'!A2'
			creds = google.get_googleCred()
			google.append_googleSheet(data, creds, self.TriageReport_sheet_ID, SAMPLE_RANGE_NAME)
			google.sort_by_column(creds, self.TriageReport_sheet_ID, 
									sheet_id = sheet_id, sortColumn = 0, sortOrder = 'DESCENDING', 
									sortRange = (1, 799, 0, 16))
			
			print ("finished appending new issues")


	def Update_TriageReport(self, sheet_name):
		issue_bag_jira = self.read_TriageReport(sheet_name)
		jira_list = [item[2] for item in issue_bag_jira]
		jira_info = self.find_jira_status(jira_list)
		

		data_bag = {'values': [[item[1] for item in issue_bag_jira]],
				'majorDimension': 'COLUMNS',
				'range': sheet_name+'!H2'
				}

		data_jira_id = {'values': [[('=HYPERLINK("http://agile.intra.xiaojukeji.com/browse/VOYAGER-'+str(item[2])+'",'+str(item[2])+')' , '')[item[2] == ''] for item in issue_bag_jira]],
				'majorDimension': 'COLUMNS',
				'range': sheet_name+'!I2'
				}

		data_jira_summary = {'values': [[item[0] for item in jira_info]],
				'majorDimension': 'COLUMNS',
				'range': sheet_name+'!J2'
				}

		data_jira_assignee = {'values': [[item[1] for item in jira_info]],
				'majorDimension': 'COLUMNS',
				'range': sheet_name+'!K2'
				}

		data_jira_status = {'values': [[item[2] for item in jira_info]],
				'majorDimension': 'COLUMNS',
				'range': sheet_name+'!L2'
				}

		body = {
				'valueInputOption': 'USER_ENTERED',
				'data': [data_bag, data_jira_id, data_jira_summary, data_jira_assignee, data_jira_status]
				}


		creds = google.get_googleCred()
		google.update_googleSheet(body, creds, self.TriageReport_sheet_ID)

		print ("finished update issue status")


	def find_jira_status(self, jira_list):
		jira = JIRA('http://agile.intra.xiaojukeji.com/',basic_auth=(self.username, self.password))
		#jira_info = [(summary, assignee, status),(...) .... (...)]
		jira_info = []
		for item in jira_list:
			if item =='':
				jira_info.append(('','',''))
				continue
			else:
				ticket = jira.issue('VOYAGER-'+item)
				jira_info.append((str(ticket.fields.summary),str(ticket.fields.assignee),str(ticket.fields.status)))
		return jira_info


if __name__ == "__main__":
	CN_TestReport_doc = '1pK6-nDpBEkgZnZkaDoqmEuuxKOHmsgdGDFggUx1PR3E'
	#CN_TriageReport_sheet = '1KpS_PqVA6alGllPVoIJNdehxGvVGlel7w9nt_nhOaVc'
	CN_TriageReport_sheet = '1XYe9mFid4yvcbOzVb2kZF64fRZbjKeuCe9H5GeKj708'
	dbHelper = CN_dbHelperClass('liufubo','Triage@198725', CN_TestReport_doc, CN_TriageReport_sheet)
	issue_list = dbHelper.read_TestReport()
	print(issue_list)
	dbHelper.append_TriageReport(issue_list,'Dailybuild-CN',1666613151)
	dbHelper.Update_TriageReport('Dailybuild-CN')
