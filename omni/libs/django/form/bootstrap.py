# -*- coding:utf8 -*-
"""
Created on 15-6-4 下午4:23
@author: FMC
"""

from django.utils import six
from django.utils.encoding import force_text
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.forms.utils import ErrorList
from django.utils.html import format_html, format_html_join


class BootstrapFormStyles(object):
    """
    Form的公共样式类
    """

    def as_bootstrap(self):
        """
        支持bootstrap样式
        """
        return self._html_output(
            normal_row='<div%(html_class_attr)s>%(label)s<div class="col-sm-8 col-md-8 col-lg-6">%(errors)s%(field)s%(help_text)s</div>'
                       '</div>',
            error_row='%s',
            row_ender='</div>',
            help_text_html=' <p class="help-block">%s</p>',
            errors_on_separate_row=False)

    def _html_output(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row):
        """
        覆盖默认的_html_output方法,增加对bootstrap样式的支持
        """
        top_errors = self.non_field_errors()  # Errors that should be displayed above all fields.
        output, hidden_fields = [], []

        for name, field in self.fields.items():
            html_class_attr = ''
            bf = self[name]
            # Escape and cache in local variable.
            bf_errors = self.error_class([conditional_escape(error) for error in bf.errors])
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend(
                        [_('(Hidden field %(name)s) %(error)s') % {'name': name, 'error': force_text(e)}
                         for e in bf_errors])
                hidden_fields.append(six.text_type(bf))
            else:
                # Create a 'class="..."' attribute if the row should have any
                # CSS classes applied.                      增加form-group类
                css_classes = bf.css_classes(extra_classes='form-group')
                if css_classes:
                    html_class_attr = ' class="%s"' % css_classes

                if errors_on_separate_row and bf_errors:
                    output.append(error_row % force_text(bf_errors))
                if bf_errors:
                    html_class_attr = html_class_attr[:-1] + ' has-error"'

                if bf.label:
                    label = conditional_escape(force_text(bf.label))
                    label = bf.label_tag(label, attrs={'class': 'col-sm-2 col-md-2 col-lg-1 control-label'}) or ''
                else:
                    label = ''

                if field.help_text:
                    help_text = help_text_html % force_text(field.help_text)
                else:
                    help_text = ''

                output.append(normal_row % {
                    'errors': force_text(bf_errors),
                    'label': force_text(label),
                    'field': six.text_type(bf),
                    'help_text': help_text,
                    'html_class_attr': html_class_attr,
                    'field_name': bf.html_name,
                })

        if top_errors:
            output.insert(0, error_row % force_text(top_errors))

        if hidden_fields:  # Insert any hidden fields in the last row.
            str_hidden = ''.join(hidden_fields)
            if output:
                last_row = output[-1]
                # Chop off the trailing row_ender (e.g. '</td></tr>') and
                # insert the hidden fields.
                if not last_row.endswith(row_ender):
                    # This can happen in the as_p() case (and possibly others
                    # that users write): if there are only top errors, we may
                    # not be able to conscript the last row for our purposes,
                    # so insert a new, empty row.
                    last_row = (normal_row % {
                        'errors': '',
                        'label': '',
                        'field': '',
                        'help_text': '',
                        'html_class_attr': html_class_attr,
                        'field_name': '',
                    })
                    output.append(last_row)
                output[-1] = last_row[:-len(row_ender)] + str_hidden + row_ender
            else:
                # If there aren't any rows in the output, just append the
                # hidden fields.
                output.append(str_hidden)
        return mark_safe('\n'.join(output))


def bootstrap_form_decorator(form_class):
    """
    修改form的所有field的widget的属性,增加widget的"class"属性值"form-control",以支持bootstrap样式.
    :param form_class:
    :return:
    """
    for field_name in form_class.base_fields:
        form_class.base_fields[field_name].widget.attrs.update({
            'class': 'form-control ' + form_class.base_fields[field_name].widget.attrs.get('class', '')
        })
    return form_class


class BootstrapErrorList(ErrorList):
    """
    扩展ErrorList,增加适用于bootstrap风格的格式化方法
    """
    def as_bootstrap_ul(self):
        if not self.data:
            return ''

        return format_html(
            '<ul class="{}">{}</ul>',
            'list-unstyled help-block',
            format_html_join('',
                             '<li><span class="fa fa-times-circle-o" style="padding-right: 0.5em;"></span>{}</li>',
                             ((force_text(e),) for e in self))
        )

    def __str__(self):
        return self.as_bootstrap_ul()
