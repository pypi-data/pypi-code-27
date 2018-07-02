# encoding: utf-8
# std
# thd
from datetime import datetime
# app
from pyfi import WindHelper


def case1():
    """测试getMultiTimeSeriesDataFrame"""
    pass


def case2():
    """测试getTimeseriesdataframe"""
    begin_date = "20160101"
    end_date = "20180110"
    print(WindHelper.wsd(code='204007.SH', paras=["vwap"], begin_date=begin_date, end_date=end_date))


def case3():
    begin_date = datetime(2017, 10, 1)
    end_date = datetime(2017, 12, 30)
    print(WindHelper.edb(codes=["gkz10y"], begin_date=begin_date, end_date=end_date))


def case4():
    begin_date = "2016-01-04"
    end_date = "2018-01-15"
    WindHelper.tdays(begin_date, end_date)


def case5():
    target_date = "20170105"

    code = ["160025.IB", "160017.IB"]
    code = u"110003.IB,080205.IB,050012.IB,060019.IB,070406.IB,050001.IB,030006.IB,130317.IB,130431.IB,060417.IB,060017.IB,130334.IB,130325.IB,130333.IB,9026.IB,140423.IB,010005.IB,130239.IB,130240.IB,060010.IB,139108.IB,139107.IB,050004.IB,070006.IB,130416.IB,140305.IB,140303.IB,140304.IB,130024.IB,110413.IB,110314.IB,060201.IB,070225.IB,130016.IB,110016.IB,080013.IB,9029.IB,100012.IB,070206.IB,130019.IB,140001.IB,140003.IB,050901.IB,140311.IB,130017.IB,140302.IB,140206.IB,100304.IB,050214.IB,100002.IB,080020.IB,100034.IB,090203.IB,130322.IB,130323.IB,090017.IB,110014.IB,100010.IB,110226.IB,030009.IB,010214.IB,130434.IB,130246.IB,130247.IB,070018.IB,130023.IB,110220.IB,130342.IB,140403.IB,010212.IB,0982023.IB,140202.IB,100008.IB,130018.IB,140201.IB,100005.IB,110212.IB,100236.IB,130318.IB,0700002.IB,090023.IB,1001069N.IB,100410.IB,100009.IB,100412.IB,100040.IB,100301.IB,060801.IB,140205.IB,080023.IB,070208.IB,090027.IB,060016.IB,140422.IB,090006.IB,110008.IB,020203.IB,070010.IB,100019.IB,0801095.IB,070003.IB,110204.IB,1082107.IB,100303.IB,140203.IB,100225.IB,110013.IB,1001079N.IB,100014.IB,090202.IB,092003.IB,110240.IB,100020.IB,110221.IB,090012.IB,110306.IB,110004.IB,070408.IB,130427.IB,070014.IB,110407.IB,110412.IB,110015.IB,090410.IB,090024.IB,110411.IB,1180130.IB,0700008.IB,110311.IB,130328.IB,090026.IB,100202.IB,110019.IB,110315.IB,1182257.IB,100041.IB,080018.IB,110010.IB,100026.IB,090002.IB,130238.IB,130237.IB,080003.IB,090205.IB,070203.IB,1182097.IB,110309.IB,090007.IB,070229.IB,100031.IB,060020.IB,080309.IB,140004.IB,140317.IB,100407.IB,110002.IB,050203.IB,100038.IB,140421.IB,100306.IB,100003.IB,070310.IB,080006.IB,110211.IB,080004.IB,0700005.IB,110415.IB,110214.IB,110218.IB,110304.IB,0801035.IB,110405.IB,088048.IB,100022.IB,100029.IB,090221.IB,110316.IB,110402.IB,090016.IB,130340.IB,100218.IB,120408.IB,120201.IB,070215.IB,120309.IB,110005.IB,100208.IB,100039.IB,080214.IB,100204.IB,060018.IB,110024.IB,130423.IB,090003.IB,110235.IB,110210.IB,130425.IB,120203.IB,120221.IB,120222.IB,080310.IB,080022.IB,080312.IB,080218.IB,110216.IB,100007.IB,060003.IB,090031.IB,120233.IB,120234.IB,110201.IB,100032.IB,120006.IB,110317.IB,110006.IB,110410.IB,1082086.IB,1082087.IB,120232.IB,120230.IB,120231.IB,100203.IB,140407.IB,140408.IB,100033.IB,130433.IB,100027.IB,1080109.IB,100307.IB,120010.IB,129106.IB,090201.IB,120411.IB,100013.IB,110419.IB,120227.IB,120016.IB,120214.IB,080014.IB,130244.IB,1282227.IB,120307.IB,130245.IB,110017.IB,130429.IB,130006.IB,100028.IB,120003.IB,120229.IB,120206.IB,120224.IB,130321.IB,130421.IB,120407.IB,130020.IB,130243.IB,030201.IB,070013.IB,120007.IB,130402.IB,139103.IB,1382114.IB,120207.IB,120301.IB,090212.IB,140409.IB,120413.IB,100312.IB,120009.IB,120021.IB,130209.IB,130208.IB,130207.IB,120017.IB,140418.IB,080216.IB,120217.IB,130312.IB,130313.IB,1182311.IB,1182347.IB,120235.IB,1280003.IB,120208.IB,120306.IB,120410.IB,070218.IB,120015.IB,0801017.IB,110205.IB,120414.IB,1280399.IB,100411.IB,100415.IB,130413.IB,1382074.IB,120005.IB,120404.IB,140402.IB,110420.IB,129109.IB,130202.IB,150215.IB,140401.IB,130305.IB,120220.IB,120416.IB,120013.IB,130004.IB,130009.IB,120004.IB,1280102.IB,130013.IB,100416.IB,150013.IB,140439.IB,140438.IB,090001.IB,110021.IB,120020.IB,1282156.IB,130412.IB,130411.IB,120312.IB,110257.IB,130408.IB,1282501.IB,130001.IB,130211.IB,130212.IB,120304.IB,120303.IB,150213.IB,1280043.IB,110022.IB,130022.IB,1280002.IB,129104.IB,130015.IB,130406.IB,130219.IB,130409.IB,120322.IB,120323.IB,120326.IB,120237.IB,130021.IB,130008.IB,130011.IB,140218.IB,140347.IB,1576008.IB,140006.IB,120014.IB,1280372.IB,120242.IB,130432.IB,110417.IB,150212.IB,120243.IB,130221.IB,120018.IB,130003.IB,159906.IB,130222.IB,130220.IB,130201.IB,130330.IB,130012.IB,1382275.IB,130007.IB,140431.IB,130010.IB,130306.IB,140020.IB,150406.IB,150309.IB,140432.IB,140214.IB,130225.IB,130223.IB,130224.IB,130014.IB,150004.IB,150416.IB,150313.IB,150007.IB,140373.IB,120316.IB,130231.IB,130230.IB,150407.IB,150306.IB,140433.IB,130302.IB,130301.IB,140435.IB,140434.IB,150014.IB,150303.IB,150304.IB,150202.IB,120325.IB,1561006.IB,150012.IB,1561005.IB,1561023.IB,1561022.IB,140322.IB,140323.IB,140424.IB,140208.IB,140019.IB,140025.IB,140027.IB,150015.IB,150308.IB,130229.IB,140440.IB,140441.IB,120246.IB,120247.IB,140015.IB,140443.IB,130227.IB,130228.IB,130405.IB,130310.IB,130205.IB,130203.IB,140009.IB,140210.IB,140209.IB,140211.IB,140430.IB,150016.IB,140224.IB,150005.IB,140216.IB,1480411.IB,140220.IB,140219.IB,140331.IB,140332.IB,150201.IB,140378.IB,150003.IB,140005.IB,130005.IB,130303.IB,130304.IB,150305.IB,150404.IB,150405.IB,150001.IB,150410.IB,150211.IB,140221.IB,150210.IB,150209.IB,150208.IB,140358.IB,140230.IB,150204.IB,150203.IB,150205.IB,150307.IB,140428.IB,150315.IB,140225.IB,150302.IB,140023.IB,150402.IB,140014.IB,150311.IB,140215.IB,140024.IB,140223.IB,150412.IB,150002.IB,140446.IB,140445.IB,140028.IB,150207.IB,140013.IB,140016.IB,150401.IB,1480317.IB,140212.IB,1480556.IB,140368.IB,140369.IB,140029.IB,140026.IB,150008.IB,140437.IB,140350.IB,140228.IB,140227.IB,140229.IB,150415.IB,140012.IB,140008.IB,140222.IB,1480457.IB,140021.IB,130309.IB,1382060.IB,150011.IB,1561002.IB,150413.IB,150414.IB,1568019.IB,150218.IB,1580220.IB,150023.IB,150026.IB,150419.IB,1561025.IB,1561027.IB,150022.IB,150018.IB,1580253.IB,150019.IB"
    print(WindHelper.wsi(code, "matu_cnbd", target_date))


def case6():
    print(WindHelper.all_tf_codes(begin_date="2013-09-01", end_date="2018-01-23", contract_type="T"))


def case7():
    target_date = "20170105"
    print(WindHelper.t_days_offset(offset=2, cur_date=target_date))


def case8():
    code = "TF1803.CFE"
    paras = "lasttrade_date,lastdelivery_date"
    df = WindHelper.wss(code, paras)
    print(df)


def case9():
    from windhelper import WindHelper
    import numpy as np
    import pandas as pd
    import math
    begin_date = "20131216"
    end_date = "20180101"
    WindHelper.all_tf_codes(contract_type="T", begin_date=begin_date, end_date=end_date)


def case10():
    from windhelper import WindHelper as w
    end_date = w.get_end_date()
    begin_date = w.t_days_offset(offset=22, cur_date=end_date)
    w.edb(begin_date=begin_date, end_date=end_date, codes=["brent"])


def case11():
    from windhelper import WindHelper as w
    begin_date = datetime(2018, 3, 13)
    end_date = datetime(2018, 3, 14)
    code = "050004.IB"
    paras = ['windcode', 'yield_cnbd', 'net_cnbd', 'dirty_cnbd', 'modidura_cnbd', 'matu_cnbd', 'vobp_cnbd', 'cnvxty_cnbd', 'accrueddays', 'nxcupn', 'accruedinterest', 'day', 'volume', 'dealnum']
    # wind_data = w.wsd(code, paras, begin_date, end_date, options)


def case12():
    begin_date = datetime(2008, 12, 1)
    end_date = datetime(2017, 8, 30)
    # df = WindHelper.getEDBTimeSeriesDataFrame(["S0059749"], begin_date=begin_date, end_date=end_date)
    codeList = ["T1612.CFE", "T1703.CFE"]
    para = "settle"
    df = WindHelper.getMultiTimeSeriesDataFrame(codeList=codeList, beginDate=datetime(2016, 5, 1),
                                                endDate=datetime(2016, 12, 11), para=para)
    print(df)


def case13():
    from pyfi import WindHelper
    begin_date = datetime(2011, 1, 1)
    end_date = datetime(2017, 1, 1)
    base = WindHelper.wsd(code="gz10yind", begin_date=begin_date, end_date=end_date, paras=["close"])
    print(base)


def case14():
    from pyfi import WindHelper
    begin_date = datetime(2011, 1, 1)
    end_date = datetime(2017, 1, 1)
    WindHelper.edb(codes=["环渤海动力煤指数"], begin_date=begin_date, end_date=end_date)


def case15():
    begin_date = datetime(2007, 1, 1)
    end_date = datetime(2007, 5, 1)
    ip = WindHelper.edb(codes=["ip_yoy", "ip_cyoy"],
                        begin_date=begin_date,
                        end_date=end_date, shift=1)
    print(ip)


def case16():
    from pyfi import WindHelper
    import pandas as pd
    begin_date = "2009-01-01"
    end_date = "2018-06-04"
    df = WindHelper.edb(codes=["环渤海动力煤指数"],
                        begin_date=begin_date,
                        end_date=end_date)
    print(df)


def case17():
    from pyfi import hbhdlm
    begin_date = "2009-01-01"
    end_date = "2018-06-04"
    print(hbhdlm(begin_date=begin_date, end_date=end_date))


def case18():
    from pyfi import WindHelper, ds_ip_idx
    from datetime import datetime
    import matplotlib.pylab as plt
    import matplotlib as mpl
    import pandas as pd
    mpl.rcParams["axes.unicode_minus"] = False
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams["axes.unicode_minus"] = False
    begin_date = datetime(2004, 1, 1)
    end_date = datetime(2018, 4, 1)
    df = WindHelper.edb(codes=['ip_yoy'], begin_date=begin_date, end_date=end_date)
    # base_ind = WindHelper.edb(codes=["M5567963"], begin_date=begin_date, end_date=end_date)
    yoy_Deseason = ds_ip_idx(begin_date, end_date)

    op = pd.DataFrame(index=pd.date_range(yoy_Deseason.index[0], yoy_Deseason.index[-1], freq='M'))
    op['季调工业增加值当月同比'] = yoy_Deseason
    op['工业增加值当月同比'] = df.iloc[:, 0]/100.0
    op.plot()
    plt.show()


def case_wsd():
    from pyfi import WindHelper
    WindHelper.wsd(code=["TF1406.CFE"], begin_date="20131216", end_date="20140101", paras=["settle"], options=None)


if __name__ == "__main__":
    case18()
