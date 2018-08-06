"""

"""
import BuildSimHubAPI as bshapi
import BuildSimHubAPI.postprocess as pp
import pandas as pd


file_dir = "/Users/weilixu/Desktop/data/outpatient.idf"
wea_dir = "/Users/weilixu/Desktop/data/UnitTest/in.epw"
wea_dir_sf = "/Users/weilixu/Desktop/data/UnitTest/insf.epw"
temp_dir = "/Users/weilixu/Desktop/data/"

# model_key can be found in each model information bar
# paste your project api key
project_api_key = '74139f64-eb54-4f6c-90e7-8bf583d5a930'
# paste your model api key
project_customized_key = '8d0aa6f4-50c3-4471-84e6-9bd4877ed19a'
model_api_key = "e5d343bf-b08c-40f9-a0aa-ee353a1b15c5"

bsh = bshapi.BuildSimHubAPIClient()
model = bsh.model_results(project_api_key, model_api_key)
wwr = bshapi.measures.WindowWallRatio()
wwr.set_data(0.4)

wue = bshapi.measures.WindowUValue(unit='ip', orientation='E')
wue.set_data(0.4)

wushgc = bshapi.measures.WindowSHGC(orientation='E')
wushgc.set_data(0.4)

overhang = bshapi.measures.ShadeOverhang(orientation='E')
overhang.set_data(0.11)

daylit = bshapi.measures.DaylightingSensor()
daylit.set_data(0)

bldg_orient = bshapi.measures.BuildingOrientation()
bldg_orient.set_data(0)

measure_list = list()
measure_list.append(wwr)
measure_list.append(overhang)
measure_list.append(daylit)
measure_list.append(wue)
measure_list.append(wushgc)
measure_list.append(bldg_orient)

new_api = model.apply_measures(measure_list)



