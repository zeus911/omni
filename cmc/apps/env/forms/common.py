# -*- coding:utf8 -*-
"""
Created on 15-6-4 下午5:13
@author: FMC
"""
from django.forms import ModelForm

from cmc.apps.env.models import EnvInfoModel
from omni.libs.django.form import bootstrap


@bootstrap.bootstrap_form_decorator
class EnvInfoForm(bootstrap.BootstrapFormStyles, ModelForm):

    class Meta:
        fields = ['name', 'visible_name', 'description']
        model = EnvInfoModel
