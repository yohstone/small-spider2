 #-*- coding:utf-8 -*-
# /**
# * function.py 爬虫所使用到的各类函数
# *
# * @version    v0.01
# * @createtime 2019/07/10
# * @updatetime 
# * @author     yjl(steve stone)
# * @copyright  Copyright (c) yjl(steve stone)
# *
# */

import requests
import re
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from requests.exceptions import RequestException

# /* 爬取网站的html源码
#  * url        : 网站链接
#  * cookie     : 请求头部中的cookie值，即header中的cookie值
#  * proxy      : 代理ip，默认为空（若爬取源码失败，可能是主机ip被封，此时可以使用已有的代理再次尝试获取）
#  * proxy_port : 代理端口号，默认为空
#  * referer    : 来源地址，有些网站需要有该参数才能爬取到源码
#  * return     : 返回$url对应的网站源码
#  */
def get_html(url, cookie='', proxy='', proxy_port='', referer=''):
	try:
		# 添加头部信息
		header_dict = {
			'User-Agent'   : 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
			'Content-Type' : 'application/json',
		}
		if cookie:
			header_dict['Cookie']  = cookie
		if referer:
			header_dict['Referer'] = referer 
		if proxy:
			proxies = {
				'http'  : proxy + ':' + proxy_port,
				'https' : proxy + ':' + proxy_port
			}
			response = requests.get(url, headers=header_dict, proxies=proxies)
		else:
			response = requests.get(url, headers=header_dict)

		# 进行状态码判断，是否正确读取到网页
		if response.status_code == 200:
			write_log(url + " 爬取完成\r\n")
			return response.text
		return None
	except RequestException:
		return None



# /* 解析指定网站源码的内容
#  * html_code : 网页源码
#  * url_info  : 源码网站的相关信息，其中包含了需要匹配内容的正则表达式
#  * return    : 返回网站内容解析结果
#  */
def get_content(html_code, url_info):
	# 匹配整个列表
	table_res = re.search(url_info['table_reg'], html_code, re.S)
	if not table_res:
		write_log("匹配列表失败！\r\n")

	# 匹配列表中每一项
	row_res  = re.findall(url_info['row_reg'], table_res.group(), re.S)
	if not row_res:
		write_log("匹配单项失败！\r\n")

	# 遍历每一项
	content_list = []
	for row in row_res:
		# - html标签正则模式，用于去掉结果中多余的标签
		html_pattern = re.compile(r'<[^>]+>',re.S)

		# - 匹配标题
		title_res = re.search(url_info['title_reg'], row, re.S)
		if not title_res:
			write_log("匹配标题失败！\r\n")

		# - 匹配发布时间
		pubtime_res = re.search(url_info['pubtime_reg'], row, re.S)
		if not pubtime_res:
			write_log("匹配发布时间失败！\r\n")
		
		# - 匹配数据类型/来源
		type_res = re.search(url_info['type_reg'], row, re.S)
		if not type_res:
			write_log("匹配数据类型失败！\r\n")
		
		# - 匹配数据链接
		link_res = re.search(url_info['link_reg'], row, re.S)
		if not link_res:
			write_log("匹配链接失败！\r\n")
		
		# - 匹配结果放入字典
		content_res   = {
			'title'   : html_pattern.sub('', title_res.group(1)).strip(),   # 去除多余的空格、标签与换行符
	        'pubtime' : html_pattern.sub('', pubtime_res.group(1)).strip(), # 去除多余的空格、标签与换行符
	        'type'    : html_pattern.sub('', type_res.group(1)).strip(),  	# 去除多余的空格、标签与换行符
	        'link'    : link_res.group(1),                                  # 链接里不会有多余空格等
	        'web_name' : url_info['web_name'],                              # 爬取的网站名称，当爬取的网站多时可用来区分数据来源
		}

	 	# -拼接每一项的结果
		content_list.append(content_res)

	if content_list:
		write_log( " 解析完成\r\n")
	else:
		write_log( " 解析失败！\r\n")
	return content_list



# /* 将日志数据写入文件中，记录下来
#  * log_info : 需要写入日志文件的数据
#  */
def write_log(log_info):
	# 获取当前时间的时间戳，转换成指定格式
	now_time = time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime(int( time.time() ) ) )
	log_file = open('./spider.log', "a")
	log_file.write(now_time + log_info)
	log_file.close()



# /* 发送邮件
#  * mail_content : 邮件内容
#  */
def send_mail(mail_content):
	# 第三方 SMTP 服务
	mail_host="smtp.126.com"           # 设置邮箱服务器
	mail_user="steve_stone"    		   # 邮箱账号
	mail_pass="xxxxxxxxx"              # 授权密码
	
	sender = 'steve_stone@126.com'
	receivers = ['stone_movies@126.com']   # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

	message = MIMEText(mail_content, 'plain', 'utf-8')       # 设置邮件内容 
	message['From'] = Header("论文爱好者425dds342", 'utf-8')  # 设置发件人名称
	message['To'] =  Header("steve123s123", 'utf-8')		 # 设置收件人名称
	
	subject = '来自新论文的问候......75345df'
	message['Subject'] = Header(subject, 'utf-8')       # 设置邮件标题
	
	try:
		smtpObj = smtplib.SMTP() 
		smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
		smtpObj.set_debuglevel(1)         # 打印出和SMTP服务器交互的所有信息
		smtpObj.login(mail_user, mail_pass)  
		res = smtpObj.sendmail(sender, receivers, message.as_string())
		write_log("邮件发送成功\r\n")
	except smtplib.SMTPException:
		write_log("Error: 无法发送邮件\r\n")
