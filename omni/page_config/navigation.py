# -*- coding:utf8 -*-
"""
Created on 15-6-2 下午3:20
@author: FMC

侧边栏菜单字段说明:
    name: 菜单名称
    value: 具体的显示内容
    title: 提示
    url: 超链接
    bg_img: 菜单背景图片
    before_icon: 菜单value之前的图标
    after_icon: 菜单value之后的图标
    badge: 徽章数据,父级菜单没有徽章
"""
# 样式声明
fa_angle_left = 'fa fa-angle-left pull-right'


# 仪表盘
dashboard = {'name': 'Dashboard', 'value': 'Dashboard', 'title': 'Dashboard', 'url': '/index.html',
             'bg_img': None, 'before_icon': 'fa fa-dashboard', 'after_icon': None, 'badge': None,
             'sub__': None}

# 服务器
server_menu = {'name': 'host', 'value': '服务器', 'title': '服务器', 'url': None, 'bg_img': None,
               'before_icon': 'fa fa-dashboard fa-fw', 'after_icon': fa_angle_left, 'badge': None, 'sub__': list()}

server_menu['sub__'].append({'name': 'node_list', 'value': '主机列表', 'title': '主机列表', 'url': '/host/',
                             'bg_img': None, 'before_icon': 'fa fa-dashboard', 'after_icon': None, 'badge': None,
                             'sub__': None})

# SaltStack
salt_menu = {'name': 'host', 'value': 'SaltStack', 'title': 'SaltStack', 'url': None, 'bg_img': None,
             'before_icon': 'fa fa-dashboard fa-fw', 'after_icon': fa_angle_left, 'badge': None, 'sub__': list()}

salt_menu['sub__'].append({'name': 'salt_state_list', 'value': 'State列表', 'title': 'State列表', 'url': '/salt/',
                           'bg_img': None, 'before_icon': 'fa fa-dashboard', 'after_icon': None, 'badge': None,
                           'sub__': None})


aside_menu_data = [dashboard, server_menu, salt_menu]
