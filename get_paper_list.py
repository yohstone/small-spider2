 #-*- coding:utf-8 -*-
# /**
# * get_paper_list.py 爬虫运行文件，
# *
# * @version    v0.01
# * @createtime 2019/07/10
# * @updatetime 
# * @author     yjl(steve stone)
# * @copyright  Copyright (c) yjl(steve stone)
# * 循环爬取config文件中，urls列表里配置好的网页并解析内容
# * 默认设置为1天爬取一次，查看页面数据是否更新
# * 教程请参考：https://steve.blog.csdn.net/article/details/95526888
# */
import config
import function
import json
import time

while(1):
	keyword = "protocol"
	i = 0
	for url_info in config.urls:
		is_new = False
		# -- 设置爬取url
		url = url_info['url'] % (keyword)

		# -- 爬取源码并保存到文件中备用
		html_res  = function.get_html(url)
		html_file = open("./%d.html" % (i), "wb")
		html_file.write(html_res.encode('utf-8'))
		html_file.close()

		# -- 解析内容
		new_content_list = function.get_content(html_res, config.urls[0])

		# -- 获取数据库文件中已存在的数据
		db_file = open("./newest_paper_%d.json" % (i), "w+")
		db_content_json = db_file.read()

		# -- 遍历新解析出的内容，检查是否有新数据
		for paper_info in new_content_list:
			# --- 使用名称的唯一性判断是否是新数据
			if db_content_json.find(paper_info['title']) == -1:
				mail_content = """
					<p>你好啊...</p><br/>
					<p>有个事需要和你说一下</p><br/>
					<p>有新论文出现了！</p><br/>
					<p>名称：%s</p><br/>
					<p>发布时间：%s</p><br/>
					<p>来源/类型：%s</p><br/>
					<p>链接：%s</p><br/>
					<p>来自：%s</p><br/>
					""" % (paper_info['title'], paper_info['pubtime'], paper_info['type'], paper_info['link'], paper_info['web_name'])
				#function.send_mail(mail_content)
				is_new = True
				break

		# -- 检查是否需要更新数据库文件
		new_content_json = json.dumps(new_content_list)  # 将列表转换成json字符串
		if is_new or not db_content_json:
			#db_file = open("./newest_paper_%d.json" % (i), "w")
			db_file.write(new_content_json)
			function.write_log("更新数据库文件\r\n")               # 保存日志
		else:
			function.write_log("尚未发现新论文，数据依旧\r\n")      # 保存日志

		db_file.close()
		i = i + 1

	# - 间隔一天爬一次
	break  # 挂后台运行时记得把break注释掉
	time.sleep(24*3600)

