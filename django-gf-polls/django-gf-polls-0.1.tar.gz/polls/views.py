from django.shortcuts import render, get_object_or_404 #快捷函数
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.urls import reverse   #路径解析 ，避免了我们在视图函数中硬编码 URL
from django.views import generic  #通过视图
from .models import Question,Choice
from django.utils import timezone
# Create your views here.
#每个视图必须要做的只有两件事：返回一个包含被请求页面内容的 HttpResponse 对象，或者抛出一个异常，比如 Http404 。
#使用通用视图：代码还是少点好
#一般来说，当编写Django 应用时，应先评估一下通用视图是否可以解决你的问题，你应该在一开始使用它，而不是进行到一半时重构代码。

'''
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    return render(request,"polls/index.html",{"latest_question_list":latest_question_list})
'''
class IndexView(generic.ListView):
    template_name= 'polls/index.html'
    context_object_name='latest_question_list'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

'''
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
'''
#DetailView 期望从 URL 中捕获名为 "pk" 的主键值
class DetailView(generic.DeleteView):
    model = Question
    template_name='polls/detail.html'

'''
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
'''
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        #所选的投票次数+1
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


