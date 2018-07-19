# coding: utf-8
# 'ascii'
from dianping.client import Client
from dianping.request.poi import QueryCategoriesRequest
from dianping.request.poi import QueryCitiesByProvinceNameRequest
from dianping.request.poi import QueryCitysRequest
from dianping.request.poi import QueryHomeProvincesRequest
from dianping.request.poi import QueryOpenCategoryNameRequest
from dianping.request.poi import QueryOverSeasCitiesRequest
from dianping.request.poi import QueryOverseasProvinces
from dianping.request.poi import QueryPoiBusinessDistrictRequest
from dianping.request.poi import QueryRegionsRequest
from dianping.request.poi import QueryShopPoiDetailRequest
from dianping.request.poi import QueryCityByCoordinate
from dianping.request.poi import QueryShopSearchUrl
from dianping.request.poi import BatchQueryPoiDetailRequest
from dianping.request.poi import PoiDetailRequest
from dianping.request.poi import QueryPoiRequest

# 分类元数据查询
def querycategorietest():
    categoriesrequest = QueryCategoriesRequest(1000069, '6862bd6012020b0fd385652905db18d4c9eaa835',
                                               '24b4e5e0e94119930686399d02439415013ab013',
                                               '上海')
    client = Client(categoriesrequest)
    response = client.invoke()
    print(response)
    assert (response is not None)


# 城市元数据查询
def querycitytest():
    querycity = QueryCitysRequest(1000069, '6862bd6012020b0fd385652905db18d4c9eaa835',
                                  '24b4e5e0e94119930686399d02439415013ab013')
    client = Client(querycity)
    response = client.invoke()
    print(response)
    assert (response is not None)


# 省份下所有城市信息查询
def querycitybyprovincenametest():
    querycitybyprovicerequest = QueryCitiesByProvinceNameRequest(1000069, '6862bd6012020b0fd385652905db18d4c9eaa835',
                                                                 '24b4e5e0e94119930686399d02439415013ab013',
                                                                 '上海')
    client = Client(querycitybyprovicerequest)
    response = client.invoke()
    print(response)
    assert (response is not None)


# 国内省份元数据查询
def queryhomeprovincenametest():
    queryhomeprovicerequest = QueryHomeProvincesRequest(1000069, '6862bd6012020b0fd385652905db18d4c9eaa835',
                                                        '24b4e5e0e94119930686399d02439415013ab013')
    client = Client(queryhomeprovicerequest)
    response = client.invoke()
    print(response)
    assert (response is not None)


# 类目（分级）元数据查询
def queryopencategorynametest():
    opencategoryname = QueryOpenCategoryNameRequest(1000069, '6862bd6012020b0fd385652905db18d4c9eaa835',
                                                    '24b4e5e0e94119930686399d02439415013ab013', '上海')
    client = Client(opencategoryname)
    response = client.invoke()
    print(response)
    assert (response is not None)


# 海外城市元数据查询
def queryoverseacitytest():
    queryoverseacity = QueryOverSeasCitiesRequest(1000069, '6862bd6012020b0fd385652905db18d4c9eaa835',
                                                  '24b4e5e0e94119930686399d02439415013ab013')
    client = Client(queryoverseacity)
    response = client.invoke()
    print(response)
    assert (response is not None)


# 海外国家元数据查询
def queryoverseaprovincetest():
    queryoverseaprivince = QueryOverseasProvinces(1000069, '6862bd6012020b0fd385652905db18d4c9eaa835',
                                                  '24b4e5e0e94119930686399d02439415013ab013')
    client = Client(queryoverseaprivince)
    response = client.invoke()
    print(response)
    assert (response is not None)


# 行政区、商区元数据查询
def querypoibusinessdistricttest():
    querypoibusinessdistrict = QueryPoiBusinessDistrictRequest(1000069, '6862bd6012020b0fd385652905db18d4c9eaa835',
                                                               '24b4e5e0e94119930686399d02439415013ab013', '上海')
    client = Client(querypoibusinessdistrict)
    response = client.invoke()
    print(response)
    assert (response is not None)


# 区域元数据查询
def queryregionstest():
    queryregions = QueryRegionsRequest(1000069, '6862bd6012020b0fd385652905db18d4c9eaa835',
                                       '24b4e5e0e94119930686399d02439415013ab013', '上海')
    client = Client(queryregions)
    response = client.invoke()
    print(response)
    assert (response is not None)


# 店铺详情查询
def queryshoppoidetailstest():
    queryshoppoidetail = QueryShopPoiDetailRequest(1000069, '6862bd6012020b0fd385652905db18d4c9eaa835',
                                                   '24b4e5e0e94119930686399d02439415013ab013', '123', '12', '', '', '',
                                                   '')
    client = Client(queryshoppoidetail)
    response = client.invoke()
    print(response)
    assert (response is not None)


# 城市名称查询
def querycitybycoordinatetest():
    querycitybycoordinate = QueryCityByCoordinate(1000175, '344b3d8c4d2c7f3e0e17d3239c35566244a5b71e',
                                                   '886a3d83067b0aeb68abf6ae30582c2d9fd7f9fd', 31.22, 121.48, 0)
    client = Client(querycitybycoordinate)
    response = client.invoke()
    print(response)
    assert (response is not None)


# 店铺信息搜索
def querypoitest():
    querypoi = QueryPoiRequest(1000175, '344b3d8c4d2c7f3e0e17d3239c35566244a5b71e',
                                            '886a3d83067b0aeb68abf6ae30582c2d9fd7f9fd', 'JH-289', '', '上海')
    client = Client(querypoi)
    response = client.invoke()
    print(response)
    assert (response is not None)


# 店铺搜索url列表查询
def queryshopsearchurltest():
    queryshopsearchurl = QueryShopSearchUrl(1000175, '344b3d8c4d2c7f3e0e17d3239c35566244a5b71e',
                                                  '886a3d83067b0aeb68abf6ae30582c2d9fd7f9fd', '上海')
    client = Client(queryshopsearchurl)
    response = client.invoke()
    print(response)
    assert (response is not None)


# 批量店铺详情查询
def batchquerypoidetailtest():
    batchquerypoidetail = BatchQueryPoiDetailRequest(1000175, '344b3d8c4d2c7f3e0e17d3239c35566244a5b71e',
                                            '886a3d83067b0aeb68abf6ae30582c2d9fd7f9fd', 'JH-289', '', '', '', '', '',
                                            'SvSpAmuxkrkYwcwfOA5-dg,D4txAit9MLtHy3yFL5lRnQ')
    client = Client(batchquerypoidetail)
    response = client.invoke()
    print(response)
    assert (response is not None)


# 店铺详情查询(新)
def poidetailtest():
    poidetail = PoiDetailRequest(1000175, '344b3d8c4d2c7f3e0e17d3239c35566244a5b71e',
                                 '886a3d83067b0aeb68abf6ae30582c2d9fd7f9fd', 'JH-289', '', '', '', '', '',
                                 'SvSpAmuxkrkYwcwfOA5-dg')
    client = Client(poidetail)
    response = client.invoke()
    print(response)
    assert (response is not None)

if __name__ == '__main__':
    querycategorietest()
    querycitybyprovincenametest()
    querycitytest()
    queryhomeprovincenametest()
    queryopencategorynametest()
    queryoverseacitytest()
    queryoverseaprovincetest()
    querypoibusinessdistricttest
    queryregionstest()
    queryshoppoidetailstest()
    querycitybycoordinatetest()
    querypoitest()
    queryshopsearchurltest()
    batchquerypoidetailtest()
    poidetailtest()