# -*- coding:utf8 -*-
"""
Created on 2014年12月24日
    运行环境相关数据表
@author: FMC
"""
from __future__ import print_function, unicode_literals, division, absolute_import

from django.db import models
from omni.libs.django.field import list_fields


class EnvInfoModel(models.Model):
    name = models.CharField(max_length=20, unique=True, help_text='运行环境名称,例如: test; prod')
    visible_name = models.CharField(blank=True, null=True, max_length=30, help_text='显示名称,例如: 测试环境; 生产环境')
    description = models.CharField(blank=True, null=True, max_length=512, help_text='详细描述、说明')

    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    class Meta:
        db_table = 'env_info'

    def get_absolute_url(self):
        """
        返回访问对象的URI地址
        :return:
        """
        return '/env/detail/{0}'.format(self.name)


class ProductRelateEnvModel(models.Model):
    env = models.SmallIntegerField(help_text='运行环境ID')
    product = models.SmallIntegerField(help_text='产品ID')
    description = models.CharField(max_length=50, help_text='描述信息')

    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    class Meta:
        db_table = 'product_relate_env'


class ClusterRelateEnvModel(models.Model):
    env = models.SmallIntegerField(help_text='运行环境ID')
    cluster = models.SmallIntegerField(help_text='集群ID')
    description = models.CharField(max_length=50, help_text='描述信息')

    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    class Meta:
        db_table = 'cluster_relate_env'


class HostNodeRelateEnvModel(models.Model):
    env = models.SmallIntegerField(help_text='运行环境ID')
    host_node = models.SmallIntegerField(help_text='主机节点ID')
    is_manager_node = models.BooleanField(help_text='是否为管理节点')
    description = models.CharField(max_length=50, help_text='描述信息')

    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    class Meta:
        db_table = 'host_node_relate_env'


class HostGroupRelateEnvModel(models.Model):
    env = models.SmallIntegerField(help_text='运行环境ID')
    host_group = models.SmallIntegerField(help_text='主机组ID')
    description = models.CharField(max_length=50, help_text='描述信息')

    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    class Meta:
        db_table = 'host_group_relate_env'


class ProjectRelateClusterModel(models.Model):
    env = models.SmallIntegerField(help_text='所属运行环境')
    subproject = models.SmallIntegerField(help_text='项目id,与subproject表关联')
    version_list = list_fields.ListCommaSeparatedIntegerField(blank=True, null=True, max_length=300,
                                                              help_text='与之关联的版本,值为空则表示所有版本')
    cluster = models.SmallIntegerField(help_text='集群,与cluster表id关联')
    description = models.CharField(max_length=1024, help_text='详细描述')

    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    class Meta:
        db_table = 'project_relate_cluster'
