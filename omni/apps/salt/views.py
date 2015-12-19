# -*- coding:utf8 -*-
"""
Created on 15-11-22 下午11:31
@author: FMC

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

from omni.libs.django.view.base import CommonTemplateView
from .config import salt_state_list


class NodeGroupListView(CommonTemplateView):
    """
    主机组列表视图
    """
    template_name = 'salt/index.html'

    def get_context_data(self, **kwargs):
        context = {
            'salt_state_list': salt_state_list
        }
        kwargs.update(context)
        return super(NodeGroupListView, self).get_context_data(**kwargs)
