import json
import os

from appdirs import user_config_dir
import arrow
import colored
from colored import stylize
import click
import requests


SUN_FACE = "\U0001f31e"
BAR_CHART = "\U0001f4ca"


class UVForecast:
    def __init__(self, epa_resp):
        self.today = self._lookup_time()
        self.readings = self._interpret(epa_resp)
        self.max = self._max()

    def _lookup_time(self):
        return arrow.utcnow()

    def _interpret(self, epa_data):
        today = []
        for hour in epa_data:
            # TODO: map zipcode to timezone for storage later
            normalized_datetime = arrow.get(hour["DATE_TIME"], "MMM/DD/YYYY HH A")
            order = hour["ORDER"]
            uv = hour["UV_VALUE"]
            today.append(
                {"order": order, "datetime": normalized_datetime, "uv_value": uv}
            )
        return today

    def _max(self):
        return max(a["uv_value"] for a in self.readings)


class ConfigFileHandler:
    def __init__(self):
        self.cfg_dir = user_config_dir(appname="sunscreen", appauthor=False)
        os.makedirs(self.cfg_dir, exist_ok=True)
        self.cfg_path = os.path.join(self.cfg_dir, "sunscreen.cfg")

    def save_zip_to_file(self, zipcode):
        config = {"zipcode": zipcode}
        with open(self.cfg_path, "w") as f:
            json.dump(config, f)

    def get_zip_from_file(self):
        if os.path.isfile(self.cfg_path):
            with open(self.cfg_path) as f:
                config = json.load(f)
                return config.get("zipcode", None)
        else:
            return None


def get_local_zip():
    cfg_handler = ConfigFileHandler()
    saved_zipcode = cfg_handler.get_zip_from_file() or None
    zipcode = click.prompt("Enter US zipcode", default=saved_zipcode, type=str)
    # TODO: ensure zipcode is legit
    if saved_zipcode is None:
        cfg_handler.save_zip_to_file(zipcode)
    return zipcode


def get_todays_uv_data(zipcode):
    click.echo("Retrieving today's UV data...")
    epa_url = (
        "https://iaspub.epa.gov/enviro/efservice/"
        f"getEnvirofactsUVHOURLY/ZIP/{zipcode}/json"
    )
    # TODO: handle network problems
    req = requests.get(epa_url)
    uv = UVForecast(req.json())
    return uv


def graph_uv_data(uv_forecast):
    # print legend
    print("Time ", end="")
    max_uv = uv_forecast.max
    SPACE = " "
    for val in range(1, max_uv + 1):
        if val < 3:
            print(stylize(SPACE, colored.bg("chartreuse_3b")), end="")  # green
        elif val < 6:
            print(stylize(SPACE, colored.bg("yellow_1")), end="")  # yellow
        elif val < 8:
            print(stylize(SPACE, colored.bg("orange_1")), end="")  # orange
        elif val < 10:
            print(stylize(SPACE, colored.bg("red")), end="")  # red
        else:
            print(stylize(SPACE, colored.bg("purple_1b")), end="")  # purple

    # UV values header, also adds newline
    print(" UV level")

    # TODO: use the colors above as background for the chart below

    # print each hour's time + UV in chart if there's any UV
    for hour in uv_forecast.readings:
        uv = hour["uv_value"]
        if uv > 0:
            print(hour["datetime"].format("HHmm"), end=" ")
            print(pad(data="*" * uv, limit=max_uv + 1) + f"{uv}")


def pad(data, limit):
    """Pad a given string `data` by spaces to length `limit`."""
    if len(data) > limit:
        raise Exception(
            f"length of string {data} is higher than your requested limit, {limit}"
        )
    return data + (limit - len(data)) * " "


@click.command()
def main():
    """example"""
    click.echo(f"Welcome to sunscreen! {SUN_FACE} {BAR_CHART}")
    # TODO: add option to specify a new zip code as arg
    zipcode = get_local_zip()
    uv_data = get_todays_uv_data(zipcode)
    graph_uv_data(uv_data)
