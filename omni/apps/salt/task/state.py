# -*- coding:utf8 -*-
"""
Created on 15-11-21 下午12:49
@author: FMC

"""
from __future__ import nested_scopes, generators, division, with_statement, print_function

from celery import Celery
from ..libs.common import get_salt_master

celery_app = Celery('omni.salt')
celery_app.config_from_object('django.conf:settings')

salt_master = get_salt_master()


@celery_app.task()
def state_sls(tgt, sls, expr_form='nodegroup', timeout=60):
    """
    执行saltstack state
    :param tgt: 执行目标
    :param sls: state 名称
    :param timeout: 超时时间
    :param expr_form: 目标匹配方式, node和nodegroups两种
    :return:
    """
    return salt_master.cmd(tgt=tgt, fun='state.sls', arg=[sls], expr_form=expr_form, timeout=timeout)


