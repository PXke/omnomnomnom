import json
import re
from flask import Flask, request
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)


@app.route('/search')
def search():
    search_term = request.args.get("searchparam")
    limit = request.args.get("limit", 10)
    try:
        limit = int(limit)
    except:
        limit = 10

    if limit > 1000:
        limit = 1000
    regex = re.compile(".*{0}.*".format(search_term))
    results = mongo.db["item"].find({"attributes.name": {"$regex": regex}})
    results = results[:limit]
    results = [change_keys(res["attributes"]) for res in results]
    return json.dumps({"results": results})


@app.route('/insert', methods=["POST"])
def insert():
    try:
        content = request.get_json(silent=True)
        mongo.db["item"].update(content, content, upsert=True)
        return json.dumps({"code": 0, "message": "Insertion succeed"})
    except:
        return json.dumps({"code": 1, "message": "Insertion failed"})


def change_keys(obj):
    """
    Recursivly goes through the dictionnary obj and replaces keys with the convert function.
    """
    if isinstance(obj, dict):
        new = {}
        for k, v in obj.iteritems():
            new[k.replace("-","_")] = change_keys(v)
    elif isinstance(obj, list):
        new = []
        for v in obj:
            new.append(change_keys(v))
    else:
        return obj
    return new


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
