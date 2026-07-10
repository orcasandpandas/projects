
import openmeteo_requests

import pandas as pd
import requests_cache
import httpx

from retry_requests import retry

URL = "https://archive-api.open-meteo.com/v1/archive"


def main():
    print("Weather!")    

