# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings


# Create your models here.
# 周报
class ClassWeek(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='classWeek_student', verbose_name='学生', null=True)
    class_id = models.IntegerField("班级id", null=True)
    year = models.IntegerField()  # 年
    week = models.IntegerField(null=True)  # 第几周
    type_int = models.IntegerField(default=0)  # 1-班级总数记录 2-平均数记录 3-班级学生的记录 -9:班级老师的记录
    start_date = models.DateField()  # 开始日期
    end_date = models.DateField()
    mentor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='classWeek_mentor',null=True,on_delete=models.SET_NULL)  # 助教
    live_mins = models.IntegerField()  # 练习时长
    feed_count = models.IntegerField()  # 发表日志数
    live_days = models.IntegerField()  # 练习天数
    live_count = models.IntegerField()  # 练习次数
    # watched_count = models.IntegerField(null=True)  # 被助教观看的次数
    # watched_days = models.IntegerField(null=True)  # 被助教观看的天数
    # commented_count = models.IntegerField(null=True)  # 被助教评论的次数
    last_user_section_id = models.IntegerField(null=True)  # 最后一个学习的课件
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'bee_django_report_class_week'
        app_label = 'bee_django_report'
        ordering = ['created_at']
        # permissions = (
        #     ('can_view_mission', '可以进入mission管理页'),
        # )

    def __str__(self):
        return self.id.__str__()

    def __unicode__(self):
        return self.id.__str__()



# 报表 助教分数报表
class mentorScore(models.Model):
    mentor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    year = models.IntegerField()  # 年
    week = models.IntegerField(null=True)  # 第几周
    score = models.FloatField(null=True)  # 分数
    rank = models.IntegerField(null=True)  # 排名
    level = models.IntegerField(null=True)  # 等级，1优10中20差
    info = models.TextField(null=True)  # 备注
    created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

    class Meta:
        db_table = 'bee_django_report_montor_score'
        app_label = 'bee_django_report'
        ordering = ['created_at']

    def __unicode__(self):
        return (
            "mentorScore->week:" + self.week.__str__() + ",mentor:" + self.mentor.__str__() + ",score:" + self.score.__str__())

    def __str__(self):
        return (
            "mentorScore->week:" + self.week.__str__() + ",mentor:" + self.mentor.__str__() + ",score:" + self.score.__str__())
