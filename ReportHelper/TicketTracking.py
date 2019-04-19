import sys
sys.path.append("..")

import re
import requests
from requests.cookies import RequestsCookieJar  
from cookieHelper import CookieClass
import utils.google_utils as google
from jira import JIRA


class MultiModuleTicketClass:
	def __init__(self, username, password, MultiModuleTicketReport_ID):
		self.cookieObj = CookieClass(username, password)
		self.username = username
		self.password = password
		self.MultiModuleTicketReport_ID = MultiModuleTicketReport_ID

	def read_jira(self):
		jira = JIRA('http://agile.intra.xiaojukeji.com/',basic_auth=(self.username, self.password))
		jira_list = jira.search_issues('project = VOYAGER AND issuetype = Bug AND labels = Triage AND labels = multi-module' )
		#jira_info = [(summary, assignee, status),(...) .... (...)]
		jira_info = []
		for item in jira_list:
			ticket = jira.issue(item.key)
			cause_tickets = re.findall(r"VOYAGER-\d+",str(ticket.fields.description))
			cause_tickets = list(set(cause_tickets))
			print(item.key, cause_tickets)
			if len(cause_tickets) == 0:
				jira_info.append((str(item.key),str(ticket.fields.summary),str(ticket.fields.reporter),str(ticket.fields.assignee),str(ticket.fields.status),'TBD','TBD','TBD','TBD'))
			else:
				for subitem in cause_tickets:
					cause_ticket = jira.issue(subitem)
					jira_info.append((str(item.key),str(ticket.fields.summary),str(ticket.fields.reporter),str(ticket.fields.assignee),str(ticket.fields.status),str(subitem),str(cause_ticket.fields.summary),str(cause_ticket.fields.assignee),str(cause_ticket.fields.status)))
		print(jira_info)
		return jira_info


	def Update_TriageReport(self):
		jira_info = self.read_jira()
		
		data_ticket_link = {'values': [['=HYPERLINK("http://agile.intra.xiaojukeji.com/browse/'+str(item[0])+'","'+str(item[0])+'")' for item in jira_info]],
				'majorDimension': 'COLUMNS',
				'range': 'A2'
				}

		data_ticket_summary = {'values': [[item[1] for item in jira_info]],
				'majorDimension': 'COLUMNS',
				'range': 'B2'
				}

		data_ticket_reporter = {'values': [[item[2] for item in jira_info]],
				'majorDimension': 'COLUMNS',
				'range': 'C2'
				}

		data_ticket_assignee = {'values': [[item[3] for item in jira_info]],
				'majorDimension': 'COLUMNS',
				'range': 'D2'
				}

		data_ticket_status = {'values': [[item[4] for item in jira_info]],
				'majorDimension': 'COLUMNS',
				'range': 'E2'
				}

		data_subticket_link = {'values': [[('=HYPERLINK("http://agile.intra.xiaojukeji.com/browse/VOYAGER-'+str(item[5])+'","'+str(item[5])+'")' , 'TBD')[item[5] == 'TBD'] for item in jira_info]],
				'majorDimension': 'COLUMNS',
				'range': 'F2'
				}

		data_subticket_summary = {'values': [[item[6] for item in jira_info]],
				'majorDimension': 'COLUMNS',
				'range': 'G2'
				}


		data_subticket_assignee = {'values': [[item[7] for item in jira_info]],
				'majorDimension': 'COLUMNS',
				'range': 'H2'
				}

		data_subticket_status = {'values': [[item[8] for item in jira_info]],
				'majorDimension': 'COLUMNS',
				'range': 'I2'
				}


		body = {
				'valueInputOption': 'USER_ENTERED',
				'data': [data_ticket_link, data_ticket_summary, data_ticket_reporter, data_ticket_assignee, data_ticket_status,data_subticket_link, data_subticket_summary, data_subticket_assignee, data_subticket_status]
				}


		creds = google.get_googleCred()
		google.update_googleSheet(body, creds, self.MultiModuleTicketReport_ID)

		print ("finished update issue status")


	


if __name__ == "__main__":
	MultiModuleTicketReport= '1XYe9mFid4yvcbOzVb2kZF64fRZbjKeuCe9H5GeKj708'
	multimodule = MultiModuleTicketClass('liufubo','Triage@198725', MultiModuleTicketReport)
	multimodule.Update_TriageReport()

