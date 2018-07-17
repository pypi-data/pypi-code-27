"""

"""
import BuildSimHubAPI as bshapi
import BuildSimHubAPI.postprocess as pp
import pandas as pd


file_dir = "/Users/weilixu/Desktop/data/UnitTest/5ZoneAirCooled.idf"
wea_dir = "/Users/weilixu/Desktop/data/UnitTest/in.epw"
wea_dir_sf = "/Users/weilixu/Desktop/data/UnitTest/insf.epw"
temp_dir = "/Users/weilixu/Desktop/data/"

# model_key can be found in each model information bar
# paste your project api key
project_api_key = 'f98aadb3-254f-428d-a321-82a6e4b9424c'
# paste your model api key
project_customized_key = '8d0aa6f4-50c3-4471-84e6-9bd4877ed19a'
model_api_key = 'f10f9365-ad6f-4f34-b4d8-e598d89af953'

bsh = bshapi.BuildSimHubAPIClient(base_url='http://develop.buildsim.io:8080/IDFVersionControl/')

new_sj = bsh.new_simulation_job(project_api_key)
new_sj.run(file_dir, wea_dir, track=True)


