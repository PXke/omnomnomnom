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
    limit = int(limit)
    if limit > 1000:
        limit = 1000
    regex = re.compile(".*{0}.*".format(search_term))
    results = mongo.db["item"].find({"attributes.name": {"$regex": regex}})
    results = results[:limit]
    results = [res["attributes"] for res in results]
    return json.dumps({"results": results})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
