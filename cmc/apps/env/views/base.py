# -*- coding:utf8 -*-
"""
Created on 15-6-4 下午5:10
@author: FMC
"""
import datetime

from omni.libs.django.view.edit import CreateView
from ..forms.common import EnvInfoForm


class EnvInfoCreateView(CreateView):

    form_class = EnvInfoForm
    template_name = 'env/index.html'
    context_object_name = 'env_object'

    fields_default = dict()
    fields_default['create_time'] = datetime.datetime.now()
    fields_default['update_time'] = datetime.datetime.now()
