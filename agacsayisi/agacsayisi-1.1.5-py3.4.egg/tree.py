

def numberOfTrees(co2_amount):        #ağaç sayısını bulan fonksiyon

    tree = (co2_amount/11.7934016)    #verilen karbondioksit miktarına(kg) göre ağaç sayısının bulunması.
                                      #Genç bir ağacın bir senede emdiği karbondioksit miktarı 11.7934016 kg.
    return tree


def multiplier(energy=23844012, coeff=0.45110999999999996):     #katsayıyla verilen enerjiyi çarpan fonksiyon. Enerji kWh olarak girilmeli.
                                                                
    result = coeff*energy                                       #katsayıyla girilen verinin çarpılması
                                                                #bu katsayıyı 2018 nisan ayı verilerine göre manuel olarak buldum
    return result


def coefficient(energy=23844012, nat_gas=28, imp_coal=16, lignite=15, coal=1, wind_power=5, geothermal_energy=3, solar_energy=3):     #katsayıyı hesaplayan fonksiyon.

        #Katsayıyı hesaplamak için gerekli olan iki veri var biri elemanlara göre üretim yüzdeleri, diğeri ise toplam enerji miktarı.

        #2018 Nisan ayı verileri varsayılmıştır.
        #6 ayda bir varsayılan veriler güncellenecek.

    ton1 = (energy*nat_gas/100)*499/1000          #Kaynakta her elemanın oluşturduğu emisyon değerleri var. Doğalgaz için 499 ton/GWh, ithal kömür için 888 ton/GWh vs vs. 
    ton2 = (energy*imp_coal/100)*888/1000         #Bu değerleri kg/kWh a çevirip ve basit oran orantıyla formülize ediyoruz.
    ton3 = (energy*lignite/100)*1054/1000         #Linyitin değeri: 1054 ton/GWh
    ton4 = (energy*coal/100)*888/1000             #Taş kömürünün değeri: 888 ton/GWh
    ton5 = (energy*wind_power/100)*10/1000        #rüzgar enerjisinin değeri: 10 ton/GWh
    ton6 = (energy*geothermal_energy/100)*38/1000 #jeotermal enerji için : 38 ton/GWh
    ton7 = (energy*solar_energy/100)*23/1000      #güneş enerjisi içinse : 23 ton/GWh



    summation = ton1+ton2+ton3+ton4+ton5+ton6+ton7     #katsayıyı bulmak için toplam karbon dioksit miktarı gerektiğinden topluyoruz. 
    coeff = summation/energy                           #toplam karbon dioksit miktarını girilen enerjiye böldüğümüz zaman katsayıyı bulmuş oluyoruz.
        
    return coeff


