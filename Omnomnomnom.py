import json
import re
import traceback
from geopy.distance import vincenty
from geopy.geocoders import Nominatim
from flask import Flask, request
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)


@app.route('/search')
def search():
    search_term = request.args.get("searchparam")
    limit = request.args.get("limit", 10)
    country = request.args.get("country", "Switzerland")

    try:
        int(search_term)
        # We have a barcode
        regex = re.compile(u".*{0}.*".format(search_term), re.IGNORECASE)
        results = mongo.db["item"].find({"attributes.barcode": {"$regex": regex}})
    except:
        regex = re.compile(u".*{0}.*".format(search_term), re.IGNORECASE)
        results = mongo.db["item"].find({"attributes.name": {"$regex": regex}})


    try:
        limit = int(limit)
    except ValueError:
        limit = 10

    if limit > 1000:
        limit = 1000


    results = results[:limit]
    results = [change_keys(res["attributes"]) for res in results]

    for res in results:
        if "estimated_CO2" not in res and "origins" in res and res["origins"]:
            try:
                traject = mongo.db["traject"].find({"from": res["origins"][0], "to": country}).next()
                co2 = traject["co2"]
                res["estimated_co2"] = co2
            except Exception:
                g = Nominatim()
                try:
                    d1 = g.geocode(country)
                    d2 = g.geocode(res["origins"][0])
                    co2 = compute_co2(vincenty(d1.point, d2.point).kilometers)
                    res["estimated_co2"] = co2
                    mongo.db["traject"].insert({"from": res["origins"][0], "to": country, "co2": co2})
                except AttributeError:
                    mongo.db["to_correct"].insert({"barcode": res["barcode"]})
    try:
        return json.dumps({"results": results})
    except Exception as e:
        traceback.print_exc()
        print(results)
        return json.dumps({})


@app.route('/insert', methods=["POST"])
def insert():
    try:
        content = request.get_json(silent=True)
        mongo.db["item"].update(content, content, upsert=True)
        return json.dumps({"code": 0, "message": "Insertion succeed"})
    except:
        return json.dumps({"code": 1, "message": "Insertion failed"})


def compute_co2(distance):
    if distance > 1000:
        return distance * 500
    else:
        return distance * 105


def change_keys(obj):
    """
    Recursivly goes through the dictionnary obj and replaces keys with the convert function.
    """
    if isinstance(obj, dict):
        new = {}
        for k, v in obj.iteritems():
            new[k.replace("-", "_")] = change_keys(v)
    elif isinstance(obj, list):
        new = []
        for v in obj:
            new.append(change_keys(v))
    else:
        return obj
    return new


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
