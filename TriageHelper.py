# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TriageHelper.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(835, 719)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 10, 59, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 40, 41, 16))
        self.label_2.setObjectName("label_2")
        self.frame_2 = QtWidgets.QFrame(Dialog)
        self.frame_2.setGeometry(QtCore.QRect(20, 80, 371, 71))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.btn_createjira = QtWidgets.QPushButton(self.frame_2)
        self.btn_createjira.setGeometry(QtCore.QRect(280, 30, 71, 41))
        self.btn_createjira.setObjectName("btn_createjira")
        self.label_6 = QtWidgets.QLabel(self.frame_2)
        self.label_6.setGeometry(QtCore.QRect(150, 40, 81, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.frame_2)
        self.label_7.setGeometry(QtCore.QRect(10, 40, 59, 16))
        self.label_7.setObjectName("label_7")
        self.input_issue = QtWidgets.QLineEdit(self.frame_2)
        self.input_issue.setGeometry(QtCore.QRect(70, 40, 71, 21))
        self.input_issue.setObjectName("input_issue")
        self.input_rt = QtWidgets.QLineEdit(self.frame_2)
        self.input_rt.setGeometry(QtCore.QRect(210, 40, 71, 21))
        self.input_rt.setText("")
        self.input_rt.setObjectName("input_rt")
        self.label_8 = QtWidgets.QLabel(self.frame_2)
        self.label_8.setGeometry(QtCore.QRect(110, 10, 141, 16))
        self.label_8.setObjectName("label_8")
        self.input_usr = QtWidgets.QLineEdit(Dialog)
        self.input_usr.setGeometry(QtCore.QRect(80, 10, 113, 21))
        self.input_usr.setObjectName("input_usr")
        self.input_pwd = QtWidgets.QLineEdit(Dialog)
        self.input_pwd.setGeometry(QtCore.QRect(80, 40, 113, 21))
        self.input_pwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.input_pwd.setObjectName("input_pwd")
        self.frame_3 = QtWidgets.QFrame(Dialog)
        self.frame_3.setGeometry(QtCore.QRect(20, 160, 371, 151))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.LSD_createjira = QtWidgets.QPushButton(self.frame_3)
        self.LSD_createjira.setGeometry(QtCore.QRect(250, 47, 101, 71))
        self.LSD_createjira.setObjectName("LSD_createjira")
        self.label_11 = QtWidgets.QLabel(self.frame_3)
        self.label_11.setGeometry(QtCore.QRect(120, 0, 141, 20))
        self.label_11.setObjectName("label_11")
        self.layoutWidget = QtWidgets.QWidget(self.frame_3)
        self.layoutWidget.setGeometry(QtCore.QRect(100, 30, 127, 81))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.LSD_job_id = QtWidgets.QLineEdit(self.layoutWidget)
        self.LSD_job_id.setObjectName("LSD_job_id")
        self.verticalLayout.addWidget(self.LSD_job_id)
        self.LSD_event_id = QtWidgets.QLineEdit(self.layoutWidget)
        self.LSD_event_id.setText("")
        self.LSD_event_id.setObjectName("LSD_event_id")
        self.verticalLayout.addWidget(self.LSD_event_id)
        self.layoutWidget1 = QtWidgets.QWidget(self.frame_3)
        self.layoutWidget1.setGeometry(QtCore.QRect(9, 29, 81, 81))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_10 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_2.addWidget(self.label_10)
        self.label_9 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_2.addWidget(self.label_9)
        self.LSD_Status = QtWidgets.QComboBox(self.frame_3)
        self.LSD_Status.setGeometry(QtCore.QRect(90, 124, 130, 22))
        self.LSD_Status.setObjectName("LSD_Status")
        self.LSD_Status.addItem("")
        self.LSD_Status.addItem("")
        self.LSD_Status.addItem("")
        self.label_5 = QtWidgets.QLabel(self.frame_3)
        self.label_5.setGeometry(QtCore.QRect(20, 120, 51, 20))
        self.label_5.setObjectName("label_5")
        self.frame_5 = QtWidgets.QFrame(Dialog)
        self.frame_5.setGeometry(QtCore.QRect(20, 420, 371, 151))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.label_20 = QtWidgets.QLabel(self.frame_5)
        self.label_20.setGeometry(QtCore.QRect(130, 10, 261, 16))
        self.label_20.setObjectName("label_20")
        self.btn_weeklyReport = QtWidgets.QPushButton(self.frame_5)
        self.btn_weeklyReport.setGeometry(QtCore.QRect(230, 100, 131, 41))
        self.btn_weeklyReport.setAutoRepeatInterval(96)
        self.btn_weeklyReport.setObjectName("btn_weeklyReport")
        self.label_21 = QtWidgets.QLabel(self.frame_5)
        self.label_21.setGeometry(QtCore.QRect(10, 30, 81, 16))
        self.label_21.setObjectName("label_21")
        self.btn_GetReleases = QtWidgets.QPushButton(self.frame_5)
        self.btn_GetReleases.setGeometry(QtCore.QRect(230, 60, 121, 41))
        self.btn_GetReleases.setAutoRepeatInterval(96)
        self.btn_GetReleases.setObjectName("btn_GetReleases")
        self.listView_ReleaseList = QtWidgets.QListView(self.frame_5)
        self.listView_ReleaseList.setGeometry(QtCore.QRect(30, 50, 191, 71))
        self.listView_ReleaseList.setObjectName("listView_ReleaseList")
        self.input_AddRelease = QtWidgets.QLineEdit(self.frame_5)
        self.input_AddRelease.setGeometry(QtCore.QRect(30, 120, 161, 21))
        self.input_AddRelease.setObjectName("input_AddRelease")
        self.btn_AddRelease = QtWidgets.QPushButton(self.frame_5)
        self.btn_AddRelease.setGeometry(QtCore.QRect(191, 120, 51, 32))
        self.btn_AddRelease.setAutoRepeatInterval(96)
        self.btn_AddRelease.setObjectName("btn_AddRelease")
        self.graphicsView = QtWidgets.QGraphicsView(self.frame_5)
        self.graphicsView.setGeometry(QtCore.QRect(0, -20, 371, 192))
        self.graphicsView.setObjectName("graphicsView")
        self.frame_7 = QtWidgets.QFrame(Dialog)
        self.frame_7.setGeometry(QtCore.QRect(420, 0, 411, 331))
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.sample_release_version = QtWidgets.QLineEdit(self.frame_7)
        self.sample_release_version.setGeometry(QtCore.QRect(130, 50, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.sample_release_version.setFont(font)
        self.sample_release_version.setObjectName("sample_release_version")
        self.update_release = QtWidgets.QPushButton(self.frame_7)
        self.update_release.setGeometry(QtCore.QRect(280, 40, 111, 45))
        self.update_release.setObjectName("update_release")
        self.label_25 = QtWidgets.QLabel(self.frame_7)
        self.label_25.setGeometry(QtCore.QRect(10, 60, 111, 16))
        self.label_25.setObjectName("label_25")
        self.label_26 = QtWidgets.QLabel(self.frame_7)
        self.label_26.setGeometry(QtCore.QRect(120, 10, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_26.setFont(font)
        self.label_26.setObjectName("label_26")
        self.assignment_txt_path = QtWidgets.QLineEdit(self.frame_7)
        self.assignment_txt_path.setGeometry(QtCore.QRect(170, 200, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.assignment_txt_path.setFont(font)
        self.assignment_txt_path.setObjectName("assignment_txt_path")
        self.label_27 = QtWidgets.QLabel(self.frame_7)
        self.label_27.setGeometry(QtCore.QRect(10, 200, 151, 21))
        self.label_27.setObjectName("label_27")
        self.open_assignment_txt = QtWidgets.QToolButton(self.frame_7)
        self.open_assignment_txt.setGeometry(QtCore.QRect(358, 200, 30, 22))
        self.open_assignment_txt.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.open_assignment_txt.setObjectName("open_assignment_txt")
        self.splitter = QtWidgets.QSplitter(self.frame_7)
        self.splitter.setGeometry(QtCore.QRect(20, 160, 211, 32))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.Sample = QtWidgets.QPushButton(self.splitter)
        self.Sample.setObjectName("Sample")
        self.clear = QtWidgets.QPushButton(self.splitter)
        self.clear.setObjectName("clear")
        self.splitter_2 = QtWidgets.QSplitter(self.frame_7)
        self.splitter_2.setGeometry(QtCore.QRect(10, 230, 397, 32))
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.DownL_iss_assi = QtWidgets.QPushButton(self.splitter_2)
        self.DownL_iss_assi.setObjectName("DownL_iss_assi")
        self.observer = QtWidgets.QPushButton(self.splitter_2)
        self.observer.setObjectName("observer")
        self.reviewer = QtWidgets.QPushButton(self.splitter_2)
        self.reviewer.setObjectName("reviewer")
        self.label_30 = QtWidgets.QLabel(self.frame_7)
        self.label_30.setGeometry(QtCore.QRect(10, 130, 311, 16))
        self.label_30.setObjectName("label_30")
        self.layoutWidget2 = QtWidgets.QWidget(self.frame_7)
        self.layoutWidget2.setGeometry(QtCore.QRect(10, 90, 381, 33))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_28 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_28.setObjectName("label_28")
        self.horizontalLayout.addWidget(self.label_28)
        self.start_date = QtWidgets.QLineEdit(self.layoutWidget2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.start_date.setFont(font)
        self.start_date.setObjectName("start_date")
        self.horizontalLayout.addWidget(self.start_date)
        self.label_29 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_29.setObjectName("label_29")
        self.horizontalLayout.addWidget(self.label_29)
        self.end_date = QtWidgets.QLineEdit(self.layoutWidget2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.end_date.setFont(font)
        self.end_date.setObjectName("end_date")
        self.horizontalLayout.addWidget(self.end_date)
        self.cut = QtWidgets.QPushButton(self.layoutWidget2)
        self.cut.setObjectName("cut")
        self.horizontalLayout.addWidget(self.cut)
        self.btn_NonProtected = QtWidgets.QPushButton(self.frame_7)
        self.btn_NonProtected.setGeometry(QtCore.QRect(10, 270, 151, 32))
        self.btn_NonProtected.setObjectName("btn_NonProtected")
        self.btn_NonProtected_2 = QtWidgets.QPushButton(self.frame_7)
        self.btn_NonProtected_2.setGeometry(QtCore.QRect(250, 270, 141, 32))
        self.btn_NonProtected_2.setObjectName("btn_NonProtected_2")
        self.frame_8 = QtWidgets.QFrame(Dialog)
        self.frame_8.setGeometry(QtCore.QRect(20, 320, 371, 81))
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.label_31 = QtWidgets.QLabel(self.frame_8)
        self.label_31.setGeometry(QtCore.QRect(0, 10, 371, 20))
        self.label_31.setAlignment(QtCore.Qt.AlignCenter)
        self.label_31.setObjectName("label_31")
        self.btn_txtOutput = QtWidgets.QPushButton(self.frame_8)
        self.btn_txtOutput.setGeometry(QtCore.QRect(20, 34, 151, 32))
        self.btn_txtOutput.setObjectName("btn_txtOutput")
        self.btn_downlaod = QtWidgets.QPushButton(self.frame_8)
        self.btn_downlaod.setGeometry(QtCore.QRect(200, 34, 151, 32))
        self.btn_downlaod.setObjectName("btn_downlaod")
        self.US = QtWidgets.QFrame(Dialog)
        self.US.setGeometry(QtCore.QRect(420, 350, 411, 211))
        self.US.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.US.setFrameShadow(QtWidgets.QFrame.Raised)
        self.US.setObjectName("US")
        self.btn_createjira_us = QtWidgets.QPushButton(self.US)
        self.btn_createjira_us.setGeometry(QtCore.QRect(305, 170, 83, 32))
        self.btn_createjira_us.setObjectName("btn_createjira_us")
        self.label_13 = QtWidgets.QLabel(self.US)
        self.label_13.setGeometry(QtCore.QRect(10, 170, 36, 32))
        self.label_13.setObjectName("label_13")
        self.input_issue_us = QtWidgets.QLineEdit(self.US)
        self.input_issue_us.setGeometry(QtCore.QRect(53, 170, 97, 32))
        self.input_issue_us.setObjectName("input_issue_us")
        self.label_14 = QtWidgets.QLabel(self.US)
        self.label_14.setGeometry(QtCore.QRect(140, 20, 141, 16))
        self.label_14.setObjectName("label_14")
        self.city_US = QtWidgets.QComboBox(self.US)
        self.city_US.setGeometry(QtCore.QRect(160, 170, 70, 32))
        self.city_US.setObjectName("city_US")
        self.city_US.addItem("")
        self.city_US.addItem("")
        self.test_type_US = QtWidgets.QComboBox(self.US)
        self.test_type_US.setGeometry(QtCore.QRect(240, 170, 67, 32))
        self.test_type_US.setObjectName("test_type_US")
        self.test_type_US.addItem("")
        self.test_type_US.addItem("")
        self.label_15 = QtWidgets.QLabel(self.US)
        self.label_15.setGeometry(QtCore.QRect(10, 150, 141, 16))
        self.label_15.setObjectName("label_15")
        self.input_scenario = QtWidgets.QLineEdit(Dialog)
        self.input_scenario.setGeometry(QtCore.QRect(20, 580, 210, 30))
        self.input_scenario.setObjectName("input_scenario")
        self.scenario_local = QtWidgets.QPushButton(Dialog)
        self.scenario_local.setGeometry(QtCore.QRect(240, 580, 70, 30))
        self.scenario_local.setObjectName("scenario_local")
        self.scenario_online = QtWidgets.QPushButton(Dialog)
        self.scenario_online.setGeometry(QtCore.QRect(320, 580, 70, 30))
        self.scenario_online.setObjectName("scenario_online")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.input_usr, self.input_pwd)
        Dialog.setTabOrder(self.input_pwd, self.input_issue)
        Dialog.setTabOrder(self.input_issue, self.input_rt)
        Dialog.setTabOrder(self.input_rt, self.btn_createjira)
        Dialog.setTabOrder(self.btn_createjira, self.LSD_job_id)
        Dialog.setTabOrder(self.LSD_job_id, self.LSD_event_id)
        Dialog.setTabOrder(self.LSD_event_id, self.LSD_createjira)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "User*"))
        self.label_2.setText(_translate("Dialog", "PWD*"))
        self.btn_createjira.setText(_translate("Dialog", "Create"))
        self.label_6.setText(_translate("Dialog", "RT jira ID"))
        self.label_7.setText(_translate("Dialog", "issue ID*"))
        self.label_8.setText(_translate("Dialog", "Disengage Tickets"))
        self.LSD_createjira.setText(_translate("Dialog", "Create"))
        self.label_11.setText(_translate("Dialog", "LSD Tickets"))
        self.label_10.setText(_translate("Dialog", "Job ID *"))
        self.label_9.setText(_translate("Dialog", "Event ID*"))
        self.LSD_Status.setItemText(0, _translate("Dialog", "TP"))
        self.LSD_Status.setItemText(1, _translate("Dialog", "HPE"))
        self.LSD_Status.setItemText(2, _translate("Dialog", "FP"))
        self.label_5.setText(_translate("Dialog", "Type"))
        self.label_20.setText(_translate("Dialog", "Report Generator"))
        self.btn_weeklyReport.setText(_translate("Dialog", "Generate Report"))
        self.label_21.setText(_translate("Dialog", "Release List"))
        self.btn_GetReleases.setText(_translate("Dialog", "Get Releases"))
        self.btn_AddRelease.setText(_translate("Dialog", "Add"))
        self.update_release.setText(_translate("Dialog", "Download"))
        self.label_25.setText(_translate("Dialog", "Release Version:"))
        self.label_26.setText(_translate("Dialog", "Team Manager"))
        self.label_27.setText(_translate("Dialog", "Issues assignment (.txt):"))
        self.open_assignment_txt.setText(_translate("Dialog", "..."))
        self.Sample.setText(_translate("Dialog", "500 tasks"))
        self.clear.setText(_translate("Dialog", "Clear"))
        self.DownL_iss_assi.setText(_translate("Dialog", "Download"))
        self.observer.setText(_translate("Dialog", "Observer Process"))
        self.reviewer.setText(_translate("Dialog", "Reviewers Tasks"))
        self.label_30.setText(_translate("Dialog", "Date format: year-mon-day i.e. 2019-03-03"))
        self.label_28.setText(_translate("Dialog", "Start_date:"))
        self.start_date.setText(_translate("Dialog", "2019-01-01"))
        self.label_29.setText(_translate("Dialog", "End_date:"))
        self.end_date.setText(_translate("Dialog", "2019-12-31"))
        self.cut.setText(_translate("Dialog", "Cut"))
        self.btn_NonProtected.setText(_translate("Dialog", "Fixed w/o protected "))
        self.btn_NonProtected_2.setText(_translate("Dialog", "Rejected scenario"))
        self.label_31.setText(_translate("Dialog", "Bag auto download & simulation"))
        self.btn_txtOutput.setText(_translate("Dialog", "Output TXT Doc"))
        self.btn_downlaod.setText(_translate("Dialog", "Ubuntu Simulation"))
        self.btn_createjira_us.setText(_translate("Dialog", "Create"))
        self.label_13.setText(_translate("Dialog", "Issue "))
        self.label_14.setText(_translate("Dialog", "Release Manger"))
        self.city_US.setItemText(0, _translate("Dialog", "MTV"))
        self.city_US.setItemText(1, _translate("Dialog", "Fremont"))
        self.test_type_US.setItemText(0, _translate("Dialog", "DB"))
        self.test_type_US.setItemText(1, _translate("Dialog", "RC"))
        self.label_15.setText(_translate("Dialog", "US"))
        self.scenario_local.setText(_translate("Dialog", "local"))
        self.scenario_online.setText(_translate("Dialog", "online"))
