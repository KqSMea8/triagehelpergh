import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QFileDialog, QLineEdit
from PyQt5.QtCore import QStringListModel
from PyQt5 import QtGui
import datetime
import time
from TriageHelper import *
from DisHelper import DisHelperClass
from reportHelper import reportHelperClass
from ticket_creator import Creator
from ticket_creator_LSD import Creator_LSD
from ticket_creator_us import Creator_us
from ScenarioHelper import ScenarioHelper
from sampling import stasticsHelperClass
import os


# from stastics import getdata
  

class Window(QDialog):
	def __init__(self, parent = None):
		super(Window, self).__init__(parent)
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)
		self.ui.btn_createjira.clicked.connect(self.call_createJira)
		self.ui.LSD_createjira.clicked.connect(self.call_createJira_LSD)
		self.ui.btn_GetReleases.clicked.connect(self.call_getReleases)
		self.ui.btn_weeklyReport.clicked.connect(self.call_WeeklyReport_generator)
		self.ui.btn_AddRelease.clicked.connect(self.call_AddRelease)
		self.ui.btn_NonProtected.clicked.connect(self.call_ScenarioHelper)
		self.ui.Sample.clicked.connect(self.call_sampling)
		self.ui.update_release.clicked.connect(self.call_disengage_issue_by_release)
		self.ui.observer.clicked.connect(self.call_observer_process)
		self.ui.clear.clicked.connect(self.call_clear)
		self.ui.DownL_iss_assi.clicked.connect(self.call_disengage_issue_by_observer_task)
		self.ui.reviewer.clicked.connect(self.call_reviewer_task)
		self.ui.cut.clicked.connect(self.call_cut)
		self.ui.btn_downlaod.clicked.connect(self.call_download_simulation)
		self.ui.btn_txtOutput.clicked.connect(self.call_txt_output)


		fileLineEdit = QLineEdit()
		self.ui.open_assignment_txt.clicked.connect(lambda: self.call_pointto_assignment_file(fileLineEdit.text()))



	def call_download_simulation(self):
		username = self.ui.input_usr.text()
		password = self.ui.input_pwd.text()
		disHelper = DisHelperClass(None, None, username, password)
		disHelper.download_simulation()

	def call_txt_output(self):
		username = self.ui.input_usr.text()
		password = self.ui.input_pwd.text()
		disHelper = DisHelperClass(None, None, username, password)
		disHelper.txt_output()

	def call_createJira(self):
		username = self.ui.input_usr.text()
		password = self.ui.input_pwd.text()
		issue_id = self.ui.input_issue.text()
		safety_id = None if self.ui.input_rt.text() =='' else self.ui.input_rt.text()
		creator = Creator(username, password, issue_id, safety_id)
		creator.create_jira()

	def call_createJira_LSD(self):
		"""
		v1.1 新增LSD ticket creator 2018.11.08
		v2.0 适应orion系统仿真结果链接，自动提取更多参数
		"""
		username = self.ui.input_usr.text()
		password = self.ui.input_pwd.text()
		LSD_job_id = self.ui.LSD_job_id .text()
		LSD_event_id = self.ui.LSD_event_id.text()
		collision_type = self.ui.LSD_Status.currentText()
		print(collision_type)
		creator = Creator_LSD(username, password, LSD_job_id, LSD_event_id, collision_type)
		creator.createJira_LSD()


	def call_getReleases(self):
		'''
		v2.0 add release finder
		'''
		username = self.ui.input_usr.text()
		password = self.ui.input_pwd.text()
		reportHelper = reportHelperClass(username, password)
		release_list = reportHelper.find_releases_list()
		print(release_list)
		self.model = QtGui.QStandardItemModel()

		for release in release_list:
			item = QtGui.QStandardItem(release)
			item.setCheckState(False)
			item.setCheckable(True)
			self.model.appendRow(item)
			self.ui.listView_ReleaseList.setModel(self.model)

	def call_AddRelease(self):
		'''
		v2.0 add release to release_list ListView
		'''
		release = self.ui.input_AddRelease.text()
		item = QtGui.QStandardItem(release)
		item.setCheckState(False)
		item.setCheckable(True)
		self.model.appendRow(item)



	def call_WeeklyReport_generator(self):
		'''
		v2.0 add weekly report generator
		'''
		username = self.ui.input_usr.text()
		password = self.ui.input_pwd.text()

		checked_release = []
		for i in range(self.model.rowCount()):
			if self.model.item(i).checkState():
				checked_release.append(self.model.item(i).text())
		print(checked_release)
		reportHelper = reportHelperClass(username, password)
		reportHelper.weekly_report(checked_release)


	def call_ScenarioHelper(self):
		'''
		v2.0 add scenario helper to get all fixed issue without perotected scenario
		'''
		username = self.ui.input_usr.text()
		password = self.ui.input_pwd.text()
		scenarioHelper = ScenarioHelper(username, password)
		scenarioHelper.find_unprotected_done()


	def sampling_int(self):
		username = self.ui.input_usr.text()
		password = self.ui.input_pwd.text()
		release = self.ui.sample_release_version.text()
		start_date = self.ui.start_date.text()
		end_date = self.ui.end_date.text()
		weekly_sampling = stasticsHelperClass(username, password, release, start_date, end_date)
		return (weekly_sampling)

	def call_disengage_issue_by_release(self):
		"""
		v1.0 According to release version to update Disengage.csv from server
		"""
		weekly_sampling = self.sampling_int()
		weekly_sampling.get_disengage_issue_by_release()

	def call_disengage_issue_by_observer_task(self):
		"""
		v1.0 According to assignment txt to update Disengage.csv from server
		"""
		weekly_sampling = self.sampling_int()
		filepath = self.ui.assignment_txt_path.text()
		try:
			weekly_sampling.get_disengage_issue_by_observer_task(filepath)
		except FileNotFoundError:
			print('please point to the assignment txt file firstly!')
			fileLineEdit = QLineEdit()
			self.call_pointto_assignment_file(fileLineEdit.text())
			# print('A187',self.ui.assignment_txt_path.text())

			if self.ui.assignment_txt_path.text() == '':

				exit()
			else:
				self.call_disengage_issue_by_observer_task()

	def call_cut(self):
		"""
		v1.0 filtering the issues from start_date to end_date
		"""
		weekly_sampling = self.sampling_int()
		weekly_sampling.cut()

	def call_sampling(self):
		"""
		v1.0 randomly get 500issues from Disengage list and assign them to observers
		"""
		weekly_sampling = self.sampling_int()
		weekly_sampling.sample()

	def call_pointto_assignment_file(self,filePath):
		if os.path.exists(filePath):
			path = QFileDialog.getOpenFileName(self, "Open File Dialog", filePath,"Text files(*.txt);;All type(*.*)")
		else:
			path = QFileDialog.getOpenFileName(self, "Open File Dialog", "/", "Text files(*.txt);;All type(*.*)")
		self.ui.assignment_txt_path.setText(str(path[0]))

	def call_observer_process(self):
		weekly_sampling = self.sampling_int()
		try:
			weekly_sampling.observer_process()
		except FileNotFoundError:
			print('please download the data_disengage_observer.csv firstly! ')
			download = input('Do you want to download the disengage_observer.csv ? Y/N')
			print(download)
			print(download == 'Y' or '')
			if download in ['Y', 'y', 'yes']:
				self.call_disengage_issue_by_observer_task()
				self.call_observer_process()
			elif download in ['N', 'n', 'not']:
				exit()
			else:
				self.call_observer_process()

	def call_reviewer_task(self):
		weekly_sampling = self.sampling_int()
		weekly_sampling.reviewer_task()

	def call_clear(self):
		weekly_sampling = self.sampling_int()
		weekly_sampling.clear_all_tasks()
		print('clear Done !')


	# def timerange_handler(self, input_timerange):
	# 	try:
	# 		datetime_list = input_timerange.split('-')
	# 		if ('_' in input_timerange):
	# 			start_datetime = datetime.datetime.strptime(datetime_list[0], "%Y%m%d_%H%M")
	# 			start_timestamp = str(time.mktime(time.strptime(str(start_datetime),'%Y-%m-%d %H:%M:%S')))[:10]+'000'
	# 			end_datetime = datetime.datetime.strptime(datetime_list[1], "%Y%m%d_%H%M")
	# 			end_timestamp = str(time.mktime(time.strptime(str(end_datetime),'%Y-%m-%d %H:%M:%S')))[:10]+'000'
	# 		else:
	# 			start_datetime = datetime.datetime.strptime(datetime_list[0], "%Y%m%d")
	# 			start_timestamp = str(time.mktime(time.strptime(str(start_datetime),'%Y-%m-%d %H:%M:%S')))[:10]+'000'
	# 			end_datetime = datetime.datetime.strptime(datetime_list[1], "%Y%m%d")
	# 			end_timestamp = str(time.mktime(time.strptime(str(end_datetime)[:11]+'23:00:00','%Y-%m-%d %H:%M:%S')))[:10]+'000'
	# 	except:
	# 		print(input_timerange, 'is a wrong format, use default time range (the whole day containing the issue)' )
	# 		start_timestamp = None
	# 		end_timestamp = None
	# 	return (start_timestamp,end_timestamp)

	# def get_data(self):
	# 	pass


if __name__ == '__main__':  
	app = QApplication(sys.argv)
	login = Window()
	login.show()
	sys.exit(app.exec())
