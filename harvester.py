from copy import deepcopy
import requests

from Omnomnomnom import mongo, app

def harvest_open_food(secure=False):

    base_api_url = "{0}www.openfood.ch/api/v1".format("http://" if not secure else "https://")
    last_page_previous_item = {"barcode": -1 }
    current_page_last_item = {"barcode": -2 }
    page = 1
    while last_page_previous_item["barcode"] != current_page_last_item["barcode"]:
        print last_page_previous_item["barcode"], current_page_last_item["barcode"], page
        last_page_previous_item = deepcopy(current_page_last_item)
        res = requests.get(base_api_url + "/products?page[number]=" + str(page)).json()
        print res["links"]
        with app.app_context():
            for r in res["data"]:
                mongo.db["item"].update( r, r, upsert=True)
        current_page_last_item = deepcopy(res["data"][-1]["attributes"])
        page += 1
        print last_page_previous_item["barcode"], current_page_last_item["barcode"], page



harvest_open_food()


