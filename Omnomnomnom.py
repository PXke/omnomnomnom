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
    results = [correct_dict(res["attributes"]) for res in results]
    return json.dumps({"results": results})


@app.route('/insert', methods=["POST"])
def insert():
    try:
        content = request.get_json(silent=True)
        mongo.db["item"].update(content, content, upsert=True)
        return json.dumps({"code": 0, "message": "Insertion succeed"})
    except:
        return json.dumps({"code": 1, "message": "Insertion failed"})


def correct_dict(d):
    new = {}
    for k, v in d.iteritems():
        if isinstance(v, dict):
            v = correct_dict(v)
        new[k.replace('-', '_')] = v
    return new


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
