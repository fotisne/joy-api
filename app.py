from flask import Flask, request, jsonify
from woocommerce import API

app = Flask(__name__)

wcapi = API(
    url="https://www.joyfashionhouse.com",
    consumer_key="ck_d4c3aab55f4192ff737a1cac745c70db1fa8451c",
    consumer_secret="cs_7b88b5452edea933245a96a456814c1471202b65",
    version="wc/v3"
)

@app.route("/")
def home():
    return "JOY API is running!"

@app.route("/product")
def get_product():
    query = request.args.get("name", "").lower()
    if not query:
        return jsonify({"error": "No product name given"}), 400

    results = []
    page = 1
    while True:
        products = wcapi.get("products", params={"per_page": 100, "status": "publish", "page": page}).json()
        if not products:
            break
        for p in products:
            if query in p["name"].lower():
                results.append({
                    "name": p["name"],
                    "short_description": p.get("short_description", ""),
                    "description": p.get("description", ""),
                    "price": p.get("price"),
                    "image": p["images"][0]["src"] if p["images"] else None,
                    "categories": [c["name"] for c in p["categories"]],
                    "id": p["id"]
                })
        page += 1

    if not results:
        return jsonify({"message": "Δεν βρέθηκε προϊόν"}), 404

    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
