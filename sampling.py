"""
    名称：Disengage Issue统计
    作者：朱振夏 / Triage / Voyager
    时间：03/03/2019
    版本：v2.4
    功能：对驾驶员上报的Disengage问题进行分类和统计
    0.1：对json文件进行解析，转成csv文件
    0.2: 从网站上爬取文件内容，直接储存成csv文件。改成面向对象编程
    0.3 进行分类统计：
        a. 没有处理过的issue 占 总 issue的百分比
        b. 按照'标签' tag 分类统计
        c. 按照 catagery  分类统计
    1.0 a. 输出柱状图和pie图，按照少龙的要求输出每个人的event ID √
        b. 修复bug：只对uncategerized 的issue 作为 task 进行任务分配 √
    1.1 a. 把'M其他'标签列入抽样的blacklist √
        b. 根据每个reviewer 分别统计category完成率和Jira绑定的数量 √
        c. 把更新Disengage状态和抽样功能分开 √
    1.2 a. 统计共有多少个Jira使用了，每个jira被使用的次数 √
        b. 统计每位triage 多少个 No Issue √
        c. 统计每位triage名下用到了哪些jira，及对应的数量，对应的evnet √
        d. 每个工程师分配的任务数量通过observer_issues_number.txt来配置 √
        e. 自动创建tickets，包含observer，reviewer，ticket id 和 count √
    2.0 重构Disengage issue reviewer机制
        a. 根据上周分配任务的txt文档里的issue id 查询Disengage系统，爬取数据
        b. 按照每个observer进行查找
            b.1 查找出所有绑定了jira的 issue，按照jira id进行聚类，每一个jira id 形成一个reviewer task
            b.2 查找出所有未绑定jira的 issue，按照catagery进行聚类，每一个catagery形成一个reviewer task
        c. 循环完每一个observer后形成reviewer task 列表，分配给reviewers
        d. 生成对应的ticket
            d.1 每个ticket包含 observer、reviewer
            d.2 按照jira id 和 reviewer name 查找出 每一个 有jira task下包含的 issue，生成查询链接
            d.2 按照jira 状态和 category  和reviewer name查找出 每一个 无jira task下包含的 issue，生成查询链接
    2.4 指定一段日期内的issue进行抽样
        a. 根据输入的起止日期进行cut，统计出在此时间段中有多少有效issue数量
        b.



"""
import csv
import math
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime
import re
from DisHelper import DisHelperClass
from jira import JIRA
from jira.exceptions import JIRAError
import requests
from cookieHelper import CookieClass
# import DisHelperGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QFileDialog, QLineEdit

plt.rcParams['font.family'] = 'Microsoft YaHei'
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 修改字体格式保证plot中的汉字正常显示
pd.set_option('display.max_columns', 10)



class stasticsHelperClass:
    def __init__(self, username, password, release, start_date, end_date):
        self.username = username
        self.password = password
        self.release = release
        self.start_date = start_date
        self.end_date = end_date
        self.issue_list = []
        self.cookieObj = CookieClass(username, password)
        self.dis = DisHelperClass(None, None, username, password)
        self.name_list = ['liufubo', 'georgegaoqi', 'zhuzhenxia', 'baijing', 'lihongyun', 'fionabaige', 'chengxiaoming',
                     'lichangyuan', 'gaohao', 'cuican', 'frankyangzhiwei']
        self.reviewer_tuple = ('liufubo', 'georgegaoqi', 'zhuzhenxia', 'baijing')


    def get_disengage_issue_by_release(self):
        release = self.release
        url = 'http://voyager.intra.xiaojukeji.com/daypack/disengage/query/?tags=&id=&description=&category_name=&version=' + release + '&robot_number=&jira=&status=&lat_s=&lat_e=&lon_s=&lon_e=&user_name=&disengage_time_start=&disengage_time_end=&bag_exist=1&size=500&page='
        self.get_data(url, 'data_disengage_release.csv')

    def get_disengage_issue_by_observer_task(self, filepath):

        # with open('data_500task_assignment_2019-01-13_21-57.txt') as f:
        with open(filepath) as f:
            content = f.read()
        issues = ''
        for c in content:
            if c.isnumeric() or c == ',':
                issues += c
            else:
                continue
        url = 'http://voyager.intra.xiaojukeji.com/daypack/disengage/query/?tags=&id='+issues+\
              '&description=&category_name=&version=&robot_number=&jira=&status=&lat_s=&lat_e=&lon_s=&lon_e=' \
              '&user_name=&disengage_time_start=&disengage_time_end=&bag_exist=1&size=500&page='
        self.get_data(url,'data_disengage_observer.csv')


    def get_data(self,url, file_path):

        # 首先根据release查询有多少个issue(有bag的)
        cookies = self.cookieObj.get_cookie()
        resp = requests.get(url+"1", cookies=cookies)
        # print('A99', resp)
        # print('A100', url+'1')
        content = eval(resp.content.decode('utf-8'))
        issue_count = content['data']['count']

        page_count = int(math.ceil(int(issue_count) / 500)) # 计算要爬几页

        # 使用一个循环，按照page逐页读取内容
        issue_list = []
        for i in range(page_count):
            url_page = url + str(i + 1)
            # print(url_page)
            # cookies = self.cookieObj.get_cookie()
            resp = requests.get(url_page, cookies=cookies)
            content = resp.content.decode('utf-8')
            issue_list += eval(content)['data']['res'] # 把新一页的内容接到上一页的列表后面
            print(' Page %s  finished，  %s pages in total' % (i+1, page_count))
        print(' %d  issues have been downloaded' % issue_count)

        # 结果保存成csv文件
        self.issue_list_csv(issue_list, file_path)

    def issue_list_csv(self, issue_list, file_path ):
        # 把爬下来的数据整理成csv文件格式
        print(" \n saving to csv file......")
        # csv文件的写入
        with open(file_path, mode='w', encoding='utf-8') as f:
            writer = csv.writer(f)
            # csv表头
            header = []
            for key in issue_list[0]:
                header.append(key)
            writer.writerow(header)
            # csv内容
            row = list(range(len(issue_list[0])))
            for issue in issue_list:
                for i, key in enumerate(issue):
                    row[i] = issue[key]
                writer.writerow(row)
        print('Create %s successfully !' % file_path)

    def sub_version_groupby(self):
        df = pd.read_csv('data_disengage_release.csv')
        df_gp_version = df.groupby('version')
        print(df_gp_version.size())

        df_find_subversion

    def mpci(self):
        df = pd.read_csv('data_disengage_release.csv')
        # MPCI统计：统计出正常Disengage所占比例
        exclude_list = ['正常', '黄灯', '三轮车']
        clean_df_disengage = self.clean_data(df_disengage, 'tags', exclude_list)
        exclude_list = ['施工', '修路', '正常', '预防', '防御']
        clean_df_disengage = self.clean_data(clean_df_disengage, 'description', exclude_list)
        print('清洗掉"正常"和"施工"等外部条件引起的接管后', len(clean_df_disengage))

        # MPCI 统计：计算出有效Disengage中No Issue的比例
        df_disengage_categoried = df_disengage[df_disengage.category_status == 1]
        exclude_list = ['No issue']
        df_disengage_hasissue = self.clean_data(df_disengage_categoried, 'category_name', exclude_list)

        print('经Triage 分析过的Disengage次数', len(df_disengage_categoried))
        print('经Triage 分析过Disengage 中有效接管的次数', len(df_disengage_hasissue))
        print('有效接管率 = ', len(df_disengage_hasissue) / len(df_disengage_categoried))
        print('最终1207版本目前的有效接管次数为 = ',
        len(clean_df_disengage) * len(df_disengage_hasissue) / len(df_disengage_categoried))

        # 只保留Disengage的Issues
        clean_df = clean_df[clean_df.type == 1]
        clean_df.to_csv('data_cleaned.csv', index=False)

        # 根据标签tags进行分类统计和频率排序,保存为csv文件，画图
        tags_gp = clean_df.groupby('tags')
        tags_distribution = tags_gp.size().sort_values(ascending=False)
        tags_distribution.to_csv('data_tags_distribution.csv')
        self.draw_top50_bar_graph(tags_distribution, '使用频率最高的50个标签(清洗后）')


    def classification_statistic(self):
        df = pd.read_csv('data_disengage_release.csv')

        # 数据清洗：把“正常”，“黄灯”...的数据清洗掉。
        exclude_list = ['正常', '黄灯', '三轮车', 'DISENGA自动', 'DISENGA失败', 'M自检红', 'M退出', '其他M', 'ProcessFault']
        clean_df = self.clean_data(df, 'tags', exclude_list)
        clean_df= clean_df[(clean_df['version'] == "0.release-20181207.144") | (clean_df['version'] == "0.release-20181207.110") ]
        clean_df.to_csv('data_cleaned.csv', index=False)

        # 根据标签tags进行分类统计和频率排序,保存为csv文件，画图
        tags_gp = clean_df.groupby('tags')
        tags_distribution = tags_gp.size().sort_values(ascending=False)
        tags_distribution.to_csv('data_tags_distribution.csv')
        # self.draw_top50_bar_graph(tags_distribution, '使用频率最高的50个标签(清洗后）')
        return clean_df

    def cut(self):
        df = self.classification_statistic()
        start_date = datetime.strptime(self.start_date,"%Y-%m-%d")
        end_date = datetime.strptime(self.end_date,"%Y-%m-%d")
        df_clean = df[df["create_time"].apply(lambda x: start_date <= datetime.strptime(x[:10], "%Y-%m-%d") <= end_date)]
        df_clean.to_csv('cut.csv', encoding='UTF-8')
        print('Effective Issue number: ', len(df_clean))
        return df_clean


    def sample(self):
        clean_df = self.cut()
        today = datetime.today()
        now = today.strftime('%Y-%m-%d_%H-%M')
        name_list = self.name_list
        with open("observers_issues_number.txt", 'r+') as fr:
            observer_dict = eval(fr.read())

        # 随机抽样出总的task
        clean_df = clean_df[clean_df['category_status'] == 0] # 筛选出未分类的case
        n = sum(observer_dict.values())
        sample_df_data = clean_df.sample(n=n, axis=0, replace=False)

        sample_df_data.to_csv('data_sample_list_%s.csv' % now)
        print('Create data_%stasks_list_%s.csv successfully!' % (n,now))

        # 按照抽样前的tags排名重新整理，并作图：
        tags_distribution = list(clean_df.groupby('tags').size().sort_values(ascending=False).index) # 获取抽样前的tag list
        sample_tags_gp = sample_df_data.groupby('tags').size()
        sample_tags_distribution = sample_tags_gp.reindex(tags_distribution)
        sample_tags_distribution.fillna(0, inplace=True)
        self.draw_top50_bar_graph(sample_tags_distribution, '抽样后标签分布')

        # 随机分配给工程师，数量按照name_number_list中的值

        task_dict = {}
        for name in name_list:
            task_sample = sample_df_data.sample(n=observer_dict[name], axis=0, replace=False)
            task_dict[name] = list(task_sample['id'])
            sample_df_data = sample_df_data.drop(index=task_sample.index)  # 从task pool中减去这次被抽走的任务。


        # 按照少龙的要求，打印出name-issue编号列表
        with open('data_500task_assignment_%s.txt' % now, mode='w', encoding='utf8') as f:
            for key in task_dict.keys():
                output = key+','
                for i, elements in enumerate(task_dict[key]):
                    # print(i, len(task_dict[key]))
                    if i+1 == len(task_dict[key]):
                        output = output + str(elements)
                    else:
                        output = output + str(elements) + ','
                # print(output)
                f.writelines(output+'\n')

        print('\nTotal tasks: %s; Assigned tasks: %s.\n' % (n, str(n-(len(sample_df_data)))))
        print('Create data_%stasks_assignment_%s.txt successfully!' % (n, now))



    def post_report(self):
        df = pd.read_csv('data_disengage_release.csv')

        # 统计categrized 和 uncatetorized issue的数量，计算覆盖率
        (uncategrized_count, categorized_count) = (df.groupby('category_status').size()[0], df.groupby('category_status').size()[1])
        coverying_rate = categorized_count / (uncategrized_count + categorized_count)
        print("%s 版本中的issue(有bag) 数量为: %s 条，已经处理了 %s 条， 未处理 %s条，覆盖率为 %s" % (self.release, uncategrized_count + categorized_count, categorized_count, uncategrized_count, coverying_rate))

        # 清洗掉所有"No Issue"的分类:
        exclude_list = ['No issue']
        clean_df = self.clean_data(df, 'category_name', exclude_list)

        # 根据category name进行分类统计:
        cat_name_gp = clean_df.groupby('category_name')
        cat_name_distribution = cat_name_gp.size().sort_values(ascending=False)
        # print(cat_name_gp.size())
        self.draw_top50_bar_graph(cat_name_distribution, "路测问题的分类统计")
        self.draw_top50_pie_graph(cat_name_distribution, "路测问题的分类统计")

    def observer_process(self):
        # 统计出每个人名下的event数量，已分类的数量，已关联jira id的case数量
        df = pd.read_csv('data_disengage_observer.csv')

        name_list = self.name_list
        df_out = pd.DataFrame(columns=["Name", "Total event", "Categorized", "Uncategorized", "Has Jira", "No Jira", "No Issue", "out-of-scope", "simulation-pass", "Bad bag"])

        for i,name in enumerate(name_list):
            df_name = df[df['reviewer'] == name]
            event_count = len(df_name)
            # 已分类category_status==1, 未分类==0

            bad_bag = df_name[df_name.category_name == 'bad bag']
            no_issue = df_name[df_name['category_name'].apply(lambda x: 'No issue' in str(x))]
            out_of_scope = df_name[df_name['description'].apply(lambda x: 'out-of-scope' in str(x))]
            simulation_pass = df_name[df_name['description'].apply(lambda x: 'simulation-pass' in str(x))]


            (uncategrized_count, categorized_count) \
                = (len(df_name[df_name['category_status'] < 0.5]), len(df_name[df_name['category_status'] > 0.5]))
            # 已关联Jira的 status==1， 未关联 status==2
            (hasjira_count, nojira_count) \
                = (len(df_name[df_name['status'] == 1]), len(df_name[df_name['status'] == 2]))
            # df_name.groupby()
            df_out.loc[i] = [name, event_count, categorized_count, uncategrized_count, hasjira_count, nojira_count, len(no_issue),len(out_of_scope), len(simulation_pass),len(bad_bag)]
        df_out.to_csv('data_review_process.csv', encoding='utf-8')
        print(df_out)
        print('Create data_review_process.csv successfully!')


    def observer_report(self):
        df = pd.read_csv('data_disengage_release.csv')
        df_gb_jira = df.groupby('jira').size()
        df_gb_jira.sort_values(ascending=False, inplace=True)
        print(df_gb_jira.head())

        release = self.release
        df_jira_out = pd.DataFrame(
            columns=["Jira", "Count", "New issue?", "Summary", "Status", "Priority", "Module"])
        for i,jira in enumerate(df_gb_jira.index):
            jira_list = self.get_ticket_info(str(int(jira)), release)
            df_jira_out.loc[i] = (int(jira), df_gb_jira[jira]) + jira_list[1:]
            print("jira:", int(jira))
        df_jira_out.to_csv('data_used_tickets.csv', encoding='utf-8')
        print('Create data_used_tickets.csv successfully!')
        # print(df_jira_out)


    def reviewer_task(self):

        df = pd.read_csv('data_disengage_observer.csv')
        df = df[df['category_status'] > 0.5]    # 过滤掉 uncategory 的 issue
        name_list = self.name_list
        # name_list = ['lihongyun', 'liufubo', 'lichangyuan']
        reviewer_tuple = self.reviewer_tuple

        # 获取所有的tasks
        df_reviewer = pd.DataFrame(columns=["has_jira", "jira", "number", "catagory", "observer", "issues"])
        j = 0

        # 对每个reviewer进行循环

        for i,name in enumerate(name_list):
            df_name = df[df['reviewer'] == name]
            df_name_hasjira = df_name[df_name.status == 1]  # 绑定了JIRA的所有issue
            df_name_nojira = df_name[df_name.status != 1]  # 未绑定JIRA的所有issue

            df_name_gp = df_name_hasjira.groupby('jira').size()  # 按照JIRA编号进行聚类
            for jira in df_name_gp.index:
                j += 1
                jira_name = int(jira)
                number = df_name_gp[jira]   # 每个JIRA下绑定的issue数量
                observer_name = name
                issue = str(list(df_name[df_name.jira == jira]['id'].values))
                issues = issue.strip("[]")
                issues = issues.replace(' ', '')
                df_reviewer.loc[j] = ['yes', jira_name, number, 0, observer_name, issues]


            df_name_gp = df_name_nojira.groupby('category_name').size()  # 未绑定jira的按照category进行聚类
            for categ in df_name_gp.index:
                j += 1
                category_name = str(categ)
                number = df_name_gp[categ]
                observer_name = name
                issue = str(list(df_name_nojira[df_name_nojira.category_name == categ]['id'].values))
                issues = issue.strip("[]")
                issues = issues.replace(' ', '')
                df_reviewer.loc[j] = ['no', 0, number, category_name, observer_name, issues]

        total_tasks_number = len(df_reviewer)
        # print('C5', df_reviewer.head())
        # df_reviewer.to_csv('df_reviewer.csv', encoding='utf-8')


        # 把reviewer的case分配给其他reviewer
        df_out = pd.DataFrame(columns=["has_jira", "jira", "number", "catagory", "observer", "reviewer"])
        for reviewer in reviewer_tuple:
            reviewer_inverse_list = list(reviewer_tuple)
            reviewer_inverse_list.remove(reviewer)
            df_reviewer_observer = df_reviewer[df_reviewer['observer'] == reviewer]
            total_reviewer_tasks_number = len(df_reviewer_observer)
            if total_reviewer_tasks_number == 0:
                pass
            else:
                for i, name in enumerate(reviewer_inverse_list):
                    n = min(math.ceil(len(df_reviewer_observer)/(len(reviewer_inverse_list)-i)), len(df_reviewer_observer))
                    sample_df_data = df_reviewer_observer.sample(n=n, axis=0, replace=False)
                    df_reviewer_observer = df_reviewer_observer.drop(index=sample_df_data.index)
                    sample_df_data['reviewer'] = name
                    df_out = pd.concat([df_out, sample_df_data], axis=0, sort=True)

        # 把其他observer的case平均分给reviewer
        df_tasks_wo_reviewers = df_reviewer[df_reviewer['observer'].apply(lambda x: x not in reviewer_tuple)]

        for i, name in enumerate(reviewer_tuple):
            number_per_reviwer_total = math.ceil(total_tasks_number/(len(reviewer_tuple)-i))
            total_tasks_number -= number_per_reviwer_total
            number_reviwer_already_got = len(df_out[df_out['reviewer'] == name])
            n = min(number_per_reviwer_total - number_reviwer_already_got, len(df_tasks_wo_reviewers))
            if n == 0:
                pass
            else:
                sample_df_data = df_tasks_wo_reviewers.sample(n=n, axis=0, replace=False)
                df_tasks_wo_reviewers = df_tasks_wo_reviewers.drop(index=sample_df_data.index)  # 从task pool中减去这次被抽走的任务。
                sample_df_data['reviewer'] = name
                df_out = pd.concat([df_out, sample_df_data], axis=0, sort=True)
        df_out.sort_index(inplace=True)
        # df_out.to_csv('df_out.csv', encoding='utf-8')
        print(df_out.groupby('reviewer').size())
        # print('G1', df_out)



        # 逐条创建tickets
        # for j in [6]:
        for j in range(len(df_out)):
            i = j+1

            self.create_reviewer_tickets(df_out.has_jira[i], str(df_out.jira[i]),
                                         df_out.catagory[i], df_out.observer[i],
                                         df_out.reviewer[i], str(df_out.number[i]), df_out.issues[i])



    def create_reviewer_tickets(self, has_jira, ticket_id, category, observer, reviewer, count, issues):
        username = self.username
        password = self.password
        release = self.release
        print('Z1:', ticket_id, observer, reviewer, count, issues)
        url = 'http://voyager.intra.xiaojukeji.com/static/management/#/issue/list?category_name=&page=1&currentZone=0&id='

        jira = JIRA('http://agile.intra.xiaojukeji.com/', basic_auth=(username, password))

        summary = '[Issue_review]O:{0}. R:{3}. Ticket:{1}, Count:{2}'.format(observer, ticket_id, count, reviewer)
        issue_dict = {
            'project': {'id': '12389', 'key': 'VOYTRIAGE'},
            'issuetype': {'id': '1'},
            'summary': summary,
            'labels': ['unreviewed'],
            'description': "1. Observer: " + observer + "\n"
                        "2. Reviewer: " + reviewer + "\n"
                        "3. Ticket id: [" + ticket_id + "| http://agile.intra.xiaojukeji.com/browse/VOYAGER-" + ticket_id + "]\n"
                        "4. Count: " + count + "\n"
                        "5. Event Link:\n" + url + issues +
                        "\nh3. *Reviewer's Comments:*\n",
            'assignee': {'name': reviewer},
            'reporter': {'name': observer}
            }
        # print('F2',has_jira)
        # print('F3',type(has_jira))

        if has_jira == 'no':
            summary = '[Issue_review]O:{0}. R:{3}. No_jira. {1}. Count:{2}'.format(observer, category, count, reviewer)
            issue_dict['summary'] = summary
            issue_dict['description'] = "1. Observer: " + observer + "\n" \
                        "2. Reviewer: " + reviewer + "\n"\
                        "3. Category: " + category + "\n"\
                        "4. Count: " + count + "\n"\
                        "5. Event Link:\n" + url + issues + \
                        "\nh3. *Reviewer's Comments:*\n"


        try:
            new_issue = jira.create_issue(fields=issue_dict)
        except JIRAError as e:
            print('出错啦，哈哈哈哈哈',e.status_code, e.text)

        update_issue = jira.search_issues('project = VOYTRIAGE')
        update_issue = update_issue[0]
        task_id = str(update_issue.key).split('-')[1]
        description = 'have fun'
        issueupdate = {
            'description': description,
            'labels': ['Triage', jira]
        }

        # update_issue.update(issueupdate)

        print('Reviewer ticket is created!  ID is: ' + task_id)


    def clean_data(self, df, column_name, exclude_list):
        # 清洗数据
        clean_df = df
        for exclude_tags in exclude_list:
            clean_df = clean_df[clean_df[column_name].apply(lambda x: exclude_tags not in str(x))]
        return clean_df

    def find_in_df(self,df, column_name, kwords_list):
        # 查找包含字符串
        for keywords in kwords_list:
            find_df = df[df[column_name].apply(lambda x: keywords in str(x))]

        return find_df

    def draw_top50_bar_graph(self, sample_tags_distribution, name):
        # 画柱状图
        sample_top50_tags = sample_tags_distribution.head(50)
        sample_top50_tags.plot(kind='bar', title=name,  figsize=(12, 6))

        for x, y in enumerate(sample_top50_tags.values):
            plt.text(x, y+0.2, int(y), ha='center', va='bottom', fontsize=11)
        plt.savefig('%s.png' % name)
        plt.show()

    def draw_top50_pie_graph(self, sample_tags_distribution, name):
        # 画饼图
        sample_top10_tags = sample_tags_distribution.head(9)

        # 排名靠后的都统计到other里
        count_other_tags = len(sample_tags_distribution[10:])
        sample_top10_tags.loc['other'] = count_other_tags

        sample_top10_tags.plot(kind='pie',title=name, legend=False, figsize=(12, 6))
        for x, y in enumerate(sample_top10_tags.values):
            plt.text(x, y+0.2, y, ha='center', va='bottom', fontsize=11)
        plt.savefig('%s.png' % name)
        plt.show()


    def get_ticket_info(self, jira_num, release):
        jira = JIRA('http://agile.intra.xiaojukeji.com/', basic_auth=(self.username, self.password))
        ticket = jira.issue('VOYAGER-' + jira_num)
        ticket_link = 'http://agile.intra.xiaojukeji.com/browse/VOYAGER-' + jira_num
        description = ticket.fields.description

        rule = r'release_20(\d+)'
        try:
            original_version = 'release_20' + re.findall(rule, description)[0]
            if (original_version == release):
                issue_type = 'new issue'
            else:
                issue_type = 'known issue, found version is ' + original_version
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

    def clear_all_tasks(self):
        '''
        1. get all assigned tasks ( <= 500/observer )
        2. generate clear_all_tasks_%current_time%.txt, which contains all assigned tasks, 
        with name unfilled.
        '''
        name_list = self.name_list
        task_dict = {}
        now = datetime.today().strftime('%Y-%m-%d_%H-%M')

        # get all assigned tasks ( <= 500/observer )
        for name in name_list:
            url = 'http://voyager.intra.xiaojukeji.com/daypack/disengage/query/?currentZone=0&page=1&reviewer='+name+'&size=500'
            cookies = self.cookieObj.get_cookie()
            resp = requests.get(url, cookies=cookies)
            content = eval(resp.content.decode('utf-8'))
            issue_list = content['data']['res']
            issue_id = []
            for issue in issue_list:
                issue_id.append(issue['id'])
            task_dict[name] = list(issue_id)

        # generate clear_all_tasks_%current_time%.txt, which contains all assigned tasks, 
        # with name unfilled.
        with open('clear_all_tasks_%s.txt' % now, mode='w', encoding='utf8') as f:
            for key in task_dict.keys():
                if len(task_dict[key]) == 0:
                    f.writelines('\n')
                    continue
                output = ','
                output += str(task_dict[key])[1:-1]
                f.writelines(output+'\n')
        


def main():

    disengage_issue_analysis = stasticsHelperClass('zhuzhenxia', '**', '0125', '2018-12-24', '2019-03-04')
    # disengage_issue_analysis.get_disengage_issue_by_release()
    # disengage_issue_analysis.observer_process()
    # disengage_issue_analysis.classification_statistic()
    disengage_issue_analysis.cut()
    # disengage_issue_analysis.get_disengage_issue_by_observer_task('data_500task_assignment_2019-01-13_21-57.txt')
    # disengage_issue_analysis.reviewer_task()


    # disengage_issue_analysis.sub_version_groupby()

if __name__ == '__main__':
    main()
