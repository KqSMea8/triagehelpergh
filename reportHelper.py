# -*- coding: utf-8 -*
import time
import datetime
from jira import JIRA
import json
import re
import pandas as pd
from matplotlib import pyplot as plt

from DisHelper import DisHelperClass

class reportHelperClass:
	def __init__(self, username, password):
		self.dis = DisHelperClass(None, None, username, password)
		self.username = username
		self.password = password

	def find_releases_list(self):
		start_timestamp, end_timestamp = self.get_timerange(week = 1)
		release_list = self.dis.find_week_release(start_timestamp, end_timestamp)
		return release_list

	def weekly_report(self,release_list):
		release_jira, release_category = self.dis.weekly_report_filter(release_list)
		print(release_jira)
		
		for release in release_category.keys():
			if release_jira[release] == []:
				continue
			category_list = []
			count_list = []
			df_list = []

			# extract 
			planning_count = 0
			prediction_count = 0
			perception_count = 0
			control_count = 0
			infra_count = 0
			map_count = 0
			others_count = 0
			for category, count, tickets in release_category[release]:
				category_list.append(category)
				count_list.append(count)

				#get component count seperately here
				if (('planning' in category) and ('prediction' not in category)):
					planning_count += count
				elif ('prediction' in category):
					prediction_count += count
				elif ('perception' in category):
					perception_count += count
				elif ('control' in category):
					control_count += count
				elif ('infra' in category):
					infra_count += count
				elif ('map' in category):
					map_count += count
				else:
					others_count += count

				# get jira detail info and generate the table
				summary_list = []
				link_list = []
				issue_type_list = []
				status_list  = []
				priority_list = []
				category_ticket_list = []
				count_ticket_list = []

				for ticket in tickets:
					ticket_link, issue_type, summary, status, priority, component = self.get_ticket_info(ticket,release)
					summary_list.append(summary)
					link_list.append(ticket_link)
					issue_type_list.append(issue_type)
					status_list.append(status)
					priority_list.append(priority)
					category_ticket_list.append(category)
					count_ticket_list.append(count)
				print("category_list:",category_ticket_list)
				df = pd.DataFrame({'category':category_ticket_list,
					'issue count':count_ticket_list,
					'summary':summary_list, 
					'link':link_list,
					'new/known':issue_type_list,
					'priority':priority_list,
					'status':status_list})
				df = df.sort_values(by = ['priority','status'],axis = 0, ascending= True)
				df_list.append(df)
				print(release, category, 'dataframe generated')

			print ('concating the dataframes into one table.....')
			df_release = pd.concat(df_list , ignore_index=True)
			
			print('saving to csv......')
			columns = ['category','issue count' ,'summary','link','new/known','priority','status']
			df_release.to_csv(release+'_category_tickets.csv', columns = columns, encoding='utf_8_sig', index = False)
			print (release, 'category detail report generated')

			#pie chart for category statisitc
			self.category_pie(category_list, count_list,release, 'category')

			#pie chart for modules statistic
			module_list = ['perception', 'prediction', 'planning', 'control', 'map', 'infra']
			module_count_list = [perception_count, prediction_count, planning_count, control_count, map_count, infra_count]
			self.category_pie(module_list, module_count_list,release, 'module')


			print(release, 'pie chart generated')
			
		
		'''
		for release in release_jira.keys():
			summary_list = []
			link_list = []
			issue_type_list = []
			status_list  = []
			priority_list = []
			component_list = []
			issue_count_list=[]
			for jira_num, count in release_jira[release]:
				print(release,jira_num, count)
				ticket_link, issue_type, summary, status, priority, component = self.get_ticket_info (jira_num, release)
				summary_list.append(summary)
				link_list.append(ticket_link)
				issue_type_list.append(issue_type)
				status_list.append(status)
				priority_list.append(priority)
				issue_count_list.append(count)
				component_list.append(component)

			dataframe = pd.DataFrame({'summary':summary_list,
				'link':link_list,
				'new/known':issue_type_list,
				'priority':priority_list,
				'components':component_list,
				'issue count':issue_count_list,
				'status':status_list})
			columns = ['summary','link','new/known','priority','components','issue count','status']
			dataframe = dataframe.sort_values(by = ['components','priority','status'],axis = 0, ascending= True)
				
			dataframe.to_csv(release+'.csv', encoding='utf_8_sig', columns = columns, index = False)
		'''
		print("weekly report generated")


	def MPCI_report(self):
		pass

	def get_ticket_info (self, jira_num, release):
		jira = JIRA('http://agile.intra.xiaojukeji.com/',basic_auth=(self.username, self.password))
		ticket = jira.issue('VOYAGER-'+jira_num)
		ticket_link = 'http://agile.intra.xiaojukeji.com/browse/VOYAGER-'+jira_num
		description = ticket.fields.description

		rule = r'release_20(\d+)'
		try:
			original_version= 'release_20'+re.findall(rule, description)[0]
			if (original_version == release):
				issue_type = 'new issue'
			else:
				issue_type = 'known issue, found version is '+original_version
		except:
			issue_type = 'non-release'
		summary = ticket.fields.summary
		status = str(ticket.fields.status)
		priority = str(ticket.fields.priority)
		try:
			component = str(ticket.fields.components[0])
		except:
			component = 'to be categorized'
		return ticket_link, issue_type, summary, status, priority, component

	def get_timerange(self, week = 1):
		# get intersted time range, latest to current time.
		end_timestamp = time.time()
		end_timestamp = str(end_timestamp)[:9]+'0000'
		# week = 1 means current week, week = 0 means last week
		if (week ==1):
			week_num = datetime.datetime.now().weekday()
			Monday = datetime.datetime.now() + datetime.timedelta(days=-week_num)
			Monday = str(Monday)[0:10]+' 01:00'
			start_timestamp = self.dis.datetime_timestamp(Monday)
			start_timestamp = str(start_timestamp)[:9]+'0000'
		else:
			week_num = datetime.datetime.now().weekday()
			Monday = datetime.datetime.now() + datetime.timedelta(days=-(week_num+7))
			Monday = str(Monday)[0:10]+' 01:00'
			start_timestamp = self.dis.datetime_timestamp(Monday)
			start_timestamp = str(start_timestamp)[:9]+'0000'
			Friday = datetime.datetime.now() + datetime.timedelta(days=-(week_num+3))
			Friday = str(Friday)[0:10]+' 23:00'
			end_timestamp = self.dis.datetime_timestamp(Friday)
			end_timestamp = str(end_timestamp)[:9]+'0000'
		return start_timestamp, end_timestamp

	def category_pie(self, category_list, count_list, release, field):
		plt.figure(figsize = (18,6))
		
		labels = category_list
		sizes = count_list

		if(len(category_list) > 10):
			labels = category_list[:10]
			labels.append('other categories, find details in below table')
			sizes = count_list[:10]
			sizes.append(sum(count_list[10:]))

		#exclude the items that occupies below than 1%
		i = 0
		size_sum = sum(sizes)
		while (i <len(labels)):
			if (sizes[i]/size_sum<0.01):
				labels.pop(i)
				sizes.pop(i)
			else:
				i += 1

		colors = ['tomato', 'lightskyblue', 'goldenrod', 'green', 'y','bisque', 'slategrey', 'navy', 'r', 'purple', 'chocolate']
		patches,l_text,p_text = plt.pie(sizes,labels=labels,colors=colors,
			labeldistance = 1.1,autopct = '%3i%%',shadow = False,
			textprops={'fontsize': 12, 'color': 'w'},
			startangle = 90,pctdistance = 0.6)
		plt.axis('equal')
		plt.title(release)
		plt.legend(loc = "right", bbox_to_anchor=(0.95,0.5), bbox_transform=plt.gcf().transFigure)
		#plt.show()
		if (field == 'category'):
			plt.savefig(release+"_category.png", bbox_inches="tight")
		elif (field == 'module'):
			plt.savefig(release+"_module.png", bbox_inches="tight")
		

if __name__ == "__main__":
	pass