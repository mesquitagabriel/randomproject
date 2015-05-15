# coding=utf-8
from django import template

register = template.Library()

@register.inclusion_tag("tags/barchart.html")
def barchart(data, label, chartname=""):
    return {"data": '/static/data/' + data,
            "name": chartname,
            "label": label
    }

@register.inclusion_tag("tags/wordcloud.html")
def wordcloud(data, chartname=""):
    return {"data": data,
            "name": chartname
    }
