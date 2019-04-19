
#from rospkg import RosPack
import getpass
import subprocess
import json
import re
#from voy_data_utils import trail_utils
#from voy_data_utils.regions import global_region

class RunScenarioClass:
	def __init__(self, scenget,  username, password):
		# print("start run scenario")
		self.scenget = scenget
		# self.except_list = except_list
		# self.page_size = '100'
		# self.cookieObj = CookieClass(username, password)
		# self.username=username
		self.labellist = []
		self.idlist = []
		self.tiketlist = []
		self.scenario_name=[]
		self.scenario_result=[]


	def get_scenario_list(self):
		print("sscenget"+self.scenget)
		#tihuan
		scenget_after=self.scenget
		while scenget_after.find("  ") != -1:
			scenget_after=scenget_after.replace("  "," ")
		scengetlist=scenget_after.split(" ")
		#print("scenget_after"+scenget_after)
		print("scenget_list"+str(scengetlist))

		#group
		for item in scengetlist:
			if item[0:1] == "/":
				self.labellist.append(item[1:])
			else:
				if len(item) == 5:
					self.idlist.append(item)
				if len(item) == 4:
					self.labellist.append('VOYAGER-'+item)
				#if len(item) > 5:
					#idlist.append(item)
		for labelitem in self.labellist:
			print("labelitem--"+labelitem)
		for iditem in self.idlist:
			print("iditem--"+iditem)
		for tiketitem in self.tiketlist:
			print("tiketitem--"+tiketitem)

	def RunScenarioLocal(self):
		self.get_scenario_list()
		cleardir = subprocess.check_output('rm -rf ~/voyager/RunScenario/*', shell=True, executable='bash')
		cmd = "cd /home/%s/voyager/autobuild" % (getpass.getuser())
		cmd += ' && source devel/setup.bash'
		cmd += ' && roscd orion && cd apps/scenario_test'
		cmd += ' &&./gen_scenario_job.py -B -1'
		if len(self.labellist) != 0:
			for lableitem in self.labellist:
				cmd_label = cmd +' -l {}'.format(lableitem)
				cmd_label += ' -M exec_scenario_test.py | rosrun orion local_runner.py -m -k ~/voyager/RunScenario/{}'.format(lableitem)
				output = subprocess.check_output(cmd_label, shell=True, executable='bash')
				out=output.decode()
				print('output--label---------------: \n'+out)
				print('output--label------------end---\n')
		if len(self.idlist) != 0:
			cmd_id = cmd + ' -i {}'.format(' '.join(self.idlist))
			stridlist=str(self.idlist)
			cmd_id += ' -M exec_scenario_test.py | rosrun orion local_runner.py -m -k ~/voyager/RunScenario/{}'.format(re.sub("[\[\]\',]",'',str(self.idlist).replace(' ','_')))
			output2 = subprocess.check_output(cmd_id, shell=True, executable='bash')
			out2=output2.decode()
			print('output---id--------------: \n'+out2)
			print('output---id----------end---\n')
		self.StatisticOutput()

	def StatisticOutput(self):
		cmd_serach='find ~/voyager/RunScenario -name "grade-res*.json"'
		output_search = subprocess.check_output(cmd_serach, shell=True, executable='bash')
		out_search=output_search.decode()
		#print('out_search-----------------:\n '+out_search)
		#SSSSSprint('out_search--------------end---\n')
		print('========================scenario result===========================')
		json_file_list=out_search.strip().split('\n')
		for item_json in json_file_list:
			file = open(item_json, "r",encoding='utf-8')
			fileJson = json.load(file)
			scenarioName = fileJson["scenarioName"]
			isPassed = fileJson["isPassed"]
			print('scenario: {}---result: {}'.format(scenarioName,isPassed))
			self.scenario_name.append(scenarioName)
			self.scenario_result.append(isPassed)




if __name__ == "__main__":
	print("start run scenario")
	scenario_class=RunScenarioClass('',None,None)
	scenario_class.RunScenarioLocal()
