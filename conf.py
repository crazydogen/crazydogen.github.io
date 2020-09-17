# -*- coding: utf-8 -*-
"""博客构建配置文件
"""

# For Maverick
site_prefix = "/Blog/"
source_dir = "../src/"
build_dir = "../dist/"
index_page_size = 10
archives_page_size = 20
template = {
    "name": "Galileo",
    "type": "local",
    "path": "../Galileo"
}
enable_jsdelivr = {
    "enabled": True,
    "repo": "crazydogen/Blog@gh-pages"
}

# 站点设置
site_name = "0x262f"
site_logo = "${static_prefix}logo.png"
site_build_date = "2020-04-19T14:51+08:00"
author = "Crazydogen"
email = "ZVd4cE1USXhNaU52ZFhSc2IyOXJMbU52YlE9PQ=="
author_homepage = "https://crazydogen.github.io/Blog/"
description = "Stay Hungry. Stay Foolish"
key_words = ['Crazydogen','blog']
language = 'zh-CN'
external_links = [
    {
        "name": "Maverick",
        "url": "https://github.com/AlanDecode/Maverick",
        "brief": "🏄‍ Go My Own Way."
    }
]
nav = [
    {
        "name": "首页",
        "url": "${site_prefix}",
        "target": "_self"
    },
    {
        "name": "归档",
        "url": "${site_prefix}archives/",
        "target": "_self"
    },
    {
        "name": "杂",
        "url": "${site_prefix}sundries/",
        "target": "_self"
    },
    {
        "name": "关于",
        "url": "${site_prefix}about/",
        "target": "_self"
    }
]

social_links = [
#     {
#         "name": "Twitter",
#         "url": "https://twitter.com/AlanDecode",
#         "icon": "gi gi-twitter"
#     },
    {
        "name": "GitHub",
        "url": "https://github.com/crazydogen",
        "icon": "gi gi-github"
    },
#     {
#         "name": "Weibo",
#         "url": "https://weibo.com/5245109677/",
#         "icon": "gi gi-weibo"
#     }
]

head_addon = r'''
<meta http-equiv="x-dns-prefetch-control" content="on">
<link rel="dns-prefetch" href="//cdn.jsdelivr.net" />
'''

footer_addon = ''

body_addon = ''
