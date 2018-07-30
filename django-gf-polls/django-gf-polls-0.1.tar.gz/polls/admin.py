from django.contrib import admin
from .models import Question,Choice
# Register your models here.

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
    
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date','was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']
    list_per_page =2
    #fields = [ 'question_text','pub_date']
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]

    inlines = [ChoiceInline]


admin.site.register(Question,QuestionAdmin)
admin.site.register(Choice)


