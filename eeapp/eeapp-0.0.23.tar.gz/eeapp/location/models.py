# Create your models here.
from django.db import models
from django.contrib import admin


class Province(models.Model):
    province_id = models.CharField(
        max_length=6, default=None, verbose_name='省份编号')
    province = models.CharField(max_length=40, default=None, verbose_name='省份')
    order = models.IntegerField(verbose_name="排序", default=0)

    def __str__(self):
        print("this is province")
        return self.province


class City(models.Model):
    city_id = models.CharField(max_length=6, default=None, verbose_name='城市编号')
    city = models.CharField(max_length=50, default=None, verbose_name='市/县')
    father = models.ForeignKey(
        Province, on_delete=models.DO_NOTHING, related_name='cities', default=None, verbose_name='所属省份')
    order = models.IntegerField(verbose_name="排序", default=0)

    def __str__(self):
        return self.father.province+self.city


class Area(models.Model):
    area_id = models.CharField(
        max_length=50, default=None, verbose_name='地区编号')
    area = models.CharField(max_length=60, default=None, verbose_name='区')
    father = models.ForeignKey(
        City, on_delete=models.DO_NOTHING, related_name='areas', default=None, verbose_name='所属城市')
    order = models.IntegerField(verbose_name="排序", default=0)

    def __str__(self):
        return self.father.city+self.area


class Address(models.Model):
    order = models.IntegerField(verbose_name="排序", default=0)
    area = models.ForeignKey(Area, on_delete=models.DO_NOTHING)
    street = models.CharField(max_length=300, default='')
    address = models.CharField(max_length=300, default='')
    post_code = models.CharField(max_length=10, default='')


class CityInline(admin.TabularInline):
    model = City
    list = ['city', 'city_id']


class AreaInline(admin.TabularInline):
    model = Area
    list = ['area', 'area_id']


class ProvinceAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None,               {'widget': ['question_text']}),
    #     ('Date information', {'widget': ['pub_date'], 'classes': ['collapse']}),
    # ]
    inlines = [CityInline]
    list_display = ('province', 'province_id')
    # list_filter = ['pub_date']
    # search_fields =


class CityAdmin(admin.ModelAdmin):
    inlines = [AreaInline]
    list_display = ('city', 'city_id')


class AreaAdmin(admin.ModelAdmin):
    list_display = ('area', 'area_id')


admin.site.register(Province, ProvinceAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Area, AreaAdmin)
