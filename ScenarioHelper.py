# -*- coding: utf-8 -*

from jira import JIRA
import pandas as pd

class ScenarioHelper:
	def __init__(self, username, password):
		self.username = username
		self.password = password

	def find_unprotected_done(self):
		#find all tickets that were done but without protected scenario:
		jira = JIRA('http://agile.intra.xiaojukeji.com/',basic_auth=(self.username, self.password))
		unprotected_done_list = jira.search_issues('project = VOYAGER AND issuetype = Bug AND labels = Triage AND labels != 海淀考试 AND labels != suzhou_demo AND labels != protected AND status = Done' )
		summary_list = []
		link_list = []
		component_list = []
		reporter_list = []
		comment_list = []
		for item in unprotected_done_list:
			ticket = jira.issue(item.key)
			ticket_link = 'http://agile.intra.xiaojukeji.com/browse/'+item.key
			print(ticket.fields.reporter)
			summary_list.append(ticket.fields.summary)
			link_list.append(ticket_link)
			reporter_list.append(str(ticket.fields.reporter))
			try:
				print(ticket.fields.components[0])
				component_list.append(str(ticket.fields.components[0]))
			except:
				component_list.append('to be categorized')
			
			found_reason = 0
			for comment in ticket.fields.comment.comments:	
				if ('non-protected reason' in comment.body):
					comment_list.append(comment.body)
					found_reason = 1
					break
			if(found_reason == 0):
				comment_list.append('')
			else:
				found_reason = 0



		
		dataframe = pd.DataFrame({'summary':summary_list,
				'link':link_list,
				'components':component_list,
				'reporter':reporter_list,
				'comment':comment_list})
		columns = ['summary','link','components','reporter','comment']
		dataframe = dataframe.sort_values(by = ['reporter'],axis = 0, ascending= True)
			
		dataframe.to_csv('unprotected_done.csv', encoding='utf_8_sig', columns = columns, index = False)
		print("Done")
		




if __name__ == "__main__":
	pass