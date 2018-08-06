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
project_api_key = '6e764740-cb49-40ed-8a1a-1331b1d87ed2'
# paste your model api key
project_customized_key = '8d0aa6f4-50c3-4471-84e6-9bd4877ed19a'
model_api_key = "4976b57c-cb94-4b94-8cc3-f90d38ef03bb"

bsh = bshapi.BuildSimHubAPIClient(base_url='http://develop.buildsim.io:8080/IDFVersionControl/')
model = bsh.model_results(project_api_key, model_api_key)
wwr = bshapi.measures.WindowWallRatio()
wwr.set_data(0.4)

wue = bshapi.measures.WindowUValue(orientation='E')
wue.set_data(1.6)

wushgc = bshapi.measures.WindowSHGC(orientation='E')
wushgc.set_data(0.4)

overhang = bshapi.measures.ShadeOverhang(orientation='E')
overhang.set_data(1.0)

daylit = bshapi.measures.DaylightingSensor()

measure_list = list()
measure_list.append(wwr)
measure_list.append(overhang)
measure_list.append(daylit)
measure_list.append(wue)
measure_list.append(wushgc)

new_api = model.apply_measures(measure_list)
new_sj = bsh.new_simulation_job(project_api_key)
new_sj.run_model_simulation(track_token=new_api, track=True)



