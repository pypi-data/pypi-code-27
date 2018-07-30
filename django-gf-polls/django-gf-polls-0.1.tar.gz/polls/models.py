from django.db import models
import datetime
from django.utils import timezone

# Create your models here.
#在 Django 里写一个数据库驱动的 Web 应用的第一步是定义模型 - 也就是数据库结构设计和附加的其它元数据。

#投票问题
class Question(models.Model):
    question_text = models.CharField(max_length=200)   
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):  #问题是否近期发布，是否大于 当前日期-1天
        now = timezone.now()
        return  (now - datetime.timedelta(days=1)) <=self.pub_date <=now

#对投票问题的投票
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)   #默认的在数据库中，Django 会在外键字段名后追加字符串 "_id"
    choice_text = models.CharField(max_length=200)   #一个问题有几个选项，针对每个选项的投票
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text