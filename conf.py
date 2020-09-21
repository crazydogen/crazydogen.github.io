# -*- coding: utf-8 -*-
"""博客构建配置文件
"""

# For Maverick
site_prefix = "/"
source_dir = "../src/"
build_dir = "../dist/"
index_page_size = 10
archives_page_size = 20
# # remote template 
# template = {
#     "name": "Galileo",
#     "type": "git",
#     "url": "https://github.com/AlanDecode/Maverick-Theme-Galileo.git",
#     "branch": "latest"
# }
enable_jsdelivr = {
    "enabled": True,
    "repo": "crazydogen/crazydogen.github.io@gh-pages"
}

# 站点设置
site_name = "0x262f"
site_logo = "${static_prefix}logo.png"
site_build_date = "2020-04-19T14:51+08:00"
author = "CrazyDogen"
email = "ZVd4cE1USXhNaU52ZFhSc2IyOXJMbU52YlE9PQ=="
author_homepage = "https://github.com/crazydogen"
description = "Everything is a trade-off. Avoid useless work before enough thinking."
key_words = ['CrazyDogen','blog']
language = 'en'
external_links = [
    {
        "name": "Maverick",
        "url": "https://github.com/AlanDecode/Maverick",
        "brief": "🏄‍ Go My Own Way."
    }
]
nav = [
    {
        "name": "Home",
        "url": "${site_prefix}",
        "target": "_self"
    },
    {
        "name": "Archived",
        "url": "${site_prefix}archives/",
        "target": "_self"
    },
    {
        "name": "Thoughts",
        "url": "${site_prefix}thoughts/",
        "target": "_self"
    },
    {
        "name": "About",
        "url": "${site_prefix}about/",
        "target": "_self"
    }
]

social_links = [
    {
        "name": "GitHub",
        "url": "https://github.com/crazydogen",
        "icon": "fab fa-github"
    }
]

head_addon = r'''
<meta http-equiv="x-dns-prefetch-control" content="on">
<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.5.0/css/all.css">
<link href='https://fonts.googleapis.com/css?family=Nunito Sans' rel='stylesheet'>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<link rel="dns-prefetch" href="//cdn.jsdelivr.net" />
'''

footer_addon = ''

body_addon = ''
