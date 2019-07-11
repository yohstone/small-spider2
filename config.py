 #-*- coding:utf-8 -*-
# /**
# * config.py 配置文件
# *
# * @version    v0.01
# * @createtime 2019/07/10
# * @updatetime 
# * @author     yjl(steve stone)
# * @copyright  Copyright (c) yjl(steve stone)
# * 配置所需爬取网页及其相应的正则表达式等
# */

# 
urls = [
	{
		'url'   			: "http://xueshu.baidu.com/s?wd=%s&pn=0&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8&sort=sc_time&sc_f_para=sc_tasktype%%3D%%7BfirstSimpleSearch%%7D&sc_hit=1",
		'page_num' 	        : 0, 										    			           # 1.抓取的页数，0表示不需要该参数
		'table_reg'   		: '<div id="content_leftrs">(.*?)<\/div>[ |\t|\r|\n]*<div id="guide-step">',    # 2.匹配整个表格的正则表达式
		'row_reg'   		: '<div class="sc_content">(.*?)<div id="[\d]*"',				   # 3.匹配表格每一行的正则表达式
		'title_reg'     	: '<h3 class="t c_font">(.*?)<\/h3>',                   		   # 4.匹配标题的正则表达式
		'pubtime_reg'   	: 'data-year="(.*?)"',										       # 5.匹配发表时间
		'type_reg'          : 'class="v_source" title="(.*?)"',  							   # 6.匹配类型/来源
		'link_reg'          : 'data-url="(.*?)"',											   # 7.匹配链接
		'cookie'            : '',                                                           	   # 8.配置固定cookie
		'reset_cookie'      : 0,                                             				   # 9.是否需要根据不同的主机设置不同的cookie，即动态cookie，若为true，抓取前会先获取适用于当前主机的动态cookie，然后拼接上方的固定cookie生成全新的cookie。
		'get_cookie_url'    : '',     															   # 10. 用于获取动态cookie的url
		'web_name'          : '百度学术'        											       # 11. 爬取的网站名称
 

	}
]


# 备用user agent，用于模拟浏览器访问
user_agent_pools = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
]