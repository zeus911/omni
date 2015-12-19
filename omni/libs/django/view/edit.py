# -*- coding:utf8 -*-
"""
    FMC 创建于 2014年10月10日
    自定义编辑视图
"""
import logging

log = logging.getLogger(__name__)

# 导入内置库
from django.views.generic.edit import FormMixin, ModelFormMixin, ProcessFormView, DeletionMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic.detail import SingleObjectTemplateResponseMixin, BaseDetailView
from django.core.exceptions import ImproperlyConfigured
from django.views.generic.base import TemplateResponseMixin
# 导入自定义模块
from .base import CommonExtMixin
from .list import MultipleObjectFilterMixin
from omni.libs.django.form.bootstrap import BootstrapErrorList


class CommonExtFormMixin(CommonExtMixin):
    """
    FormMixin的通用扩展
    """
    fields_default = {}

    def get_fields_default(self):
        """
        设置Form中未包含字段的默认值
        """
        return self.fields_default

    def ajax_form_invalid(self, form):
        """
        ajax对不合法请求参数的处理
        """
        context = {}
        context['fieldErrors'] = form.errors
        return context

    def form_save(self, form):
        """
        保存form数据，并写入数据库
        """
        return form.save(commit=True)

    def get_result_comment(self):
        """
        返回视图的执行结果描述信息
        """
        comment = {
            'success': '执行成功!! 注: 该信息为默认描述信息,可能不够清晰,请自行扩展更为详细的描述信息!!',
            'failure': '执行失败!! 注: 该信息为默认描述信息,可能不够清晰,请自行扩展更为详细的描述信息!!'
        }
        return comment

    def get_form_kwargs(self):
        """
        为form指定ErrorList类,用于格式化错误错误输出
        """
        kwargs = super(CommonExtFormMixin, self).get_form_kwargs()
        kwargs.update({'error_class': BootstrapErrorList})
        return kwargs


class CommonFormMixin(CommonExtFormMixin, FormMixin):
    """
    用于处理Ajax响应的Mixin
    """
    def form_invalid(self, form):
        response = super(CommonFormMixin, self).form_invalid(form)
        if self.request.is_ajax():
            context = self.ajax_form_invalid(form)
            return JsonResponse(context)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(CommonFormMixin, self).form_valid(form)
        if self.request.is_ajax():
            self.object.__dict__.pop('_state')
            context_data = {
                'model': self.object_meta._meta.__str__(),
                'pk': self.object.pk,
                'fields': self.object.__dict__
            }
            context = self.get_response_data(context_data)
            context['pk'] = self.object.pk
            return JsonResponse(context)
        else:
            return response


class CommonModelMixin(CommonExtFormMixin, ModelFormMixin):
    """
    对ModelFormMixin类的扩展，使其更为通用，并支持Ajax
    """
    def form_invalid(self, form):
        response = super(CommonModelMixin, self).form_invalid(form)
        if self.request.is_ajax():
            context = self.ajax_form_invalid(form)
            return JsonResponse(context)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        self.object = self.form_save(form)
        response = super(ModelFormMixin, self).form_valid(form)
        if self.request.is_ajax():
            self.object.__dict__.pop('_state')
            context_data = {
                'model': self.object._meta.__str__(),
                'pk': self.object.pk,
                'fields': self.object.__dict__
            }
            context = self.get_response_data(context_data)
            context['pk'] = self.object.pk
            return JsonResponse(context)
        else:
            return response

    def get_model_instance(self):
        """
        创建用于实例化Form的model实例的object变量
        """
        if self.fields_default:
            form_class = self.get_form_class()
            model_class = form_class._meta.model
            self.object = model_class(**self.get_fields_default())

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        # 创建model实例
        self.get_model_instance()
        kwargs = super(CommonModelMixin, self).get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs


class AjaxableProcessFormView(CommonExtFormMixin, ProcessFormView):
    """
    Ajax类型请求直接返回用户，其他请求则由模版渲染页面，并返回用户
    """
    def get(self, request, *args, **kwargs):
        """
        当get请求为ajax时,直接返回用户数据,当不是ajax时,通过模版生成页面响应用户
        """
        if self.request.is_ajax():
            context = self.get_context_data()
            return JsonResponse(context)
        else:
            form_class = self.get_form_class()
            kwargs['form'] = self.get_form(form_class)
            return self.render_to_response(self.get_context_data(**kwargs))


class CreateView(TemplateResponseMixin, CommonModelMixin, AjaxableProcessFormView):
    """
    新增数据的通用视图
    """
    template_name_suffix = '_form'

    def get(self, request, *args, **kwargs):
        self.object = None
        return super(CreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        return super(CreateView, self).post(request, *args, **kwargs)


class UpdateView(SingleObjectTemplateResponseMixin,  CommonModelMixin, AjaxableProcessFormView):
    """
    View for updating an object,
    with a response rendered by template.
    """
    template_name_suffix = '_form'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(UpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(UpdateView, self).post(request, *args, **kwargs)

    def get_fields_default(self, **kwargs):
        """
        赋予默认值，当值为'__default__'时,则不更改字段
        """
        for key in self.fields_default.keys():
            if self.fields_default[key] == '__default__':
                kwargs[key] = self.object.__getattribute__(key)
                continue
            if key in kwargs.keys() and kwargs[key]:
                continue
            kwargs[key] = self.fields_default[key]
        return kwargs


class AjaxableDeletionMixin(DeletionMixin):
    """
    支持Ajax的删除mixin
    """
    def delete(self, request, *args, **kwargs):
        """
        当请求是ajax时，返回json格式的数据
        """
        response = super(AjaxableDeletionMixin, self).delete(request, *args, **kwargs)
        if request.is_ajax():
            return JsonResponse({})
        else:
            return response


class MultipleObjectDeletionMixin(DeletionMixin):
    """
    支持多对象删除操作
    """
    status = {
        'result': True,
        'comment': '',
        'data': {}
    }

    def delete(self, request, *args, **kwargs):
        """
        调用delete()，可批量删除多个对象，并重定向至success_url
        """

        self.object_list = self.get_queryset()
        success_url = self.get_success_url()

        comment = self.get_result_comment()

        try:
            self.object_list.delete()
        except:
            self.status['result'] = False
            self.status['comment'] = comment['failure']
        else:
            self.status['result'] = True
            self.status['comment'] = comment['success']

        if self.request.is_ajax():
            return JsonResponse(self.status)
        else:
            return HttpResponseRedirect(success_url)

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")


class DeleteView(CommonExtFormMixin, MultipleObjectFilterMixin, MultipleObjectDeletionMixin, BaseDetailView):
    """
    接收来自url的pk关键字参数，并通过self.get_queryset()方法获取相应的数据列表，最后调用self.delete批量删除相关记录
    """
    template_name_suffix = '_confirm_delete'


class FormView(TemplateResponseMixin, CommonFormMixin, AjaxableProcessFormView):
    """
    A view for displaying a form, and rendering a template response.
    """