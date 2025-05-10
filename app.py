from flask import Flask, jsonify, request
from woocommerce import API

app = Flask(__name__)

# WooCommerce API σύνδεση
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
        for product in products:
            if query in product["name"].lower():
                # Πιθανόν να έχει παραλλαγές
                sizes = []
                color = "-"
                price = product.get("price", "-")
                regular_price = "-"
                sale_price = "-"
                if product["type"] == "variable":
                    variations = wcapi.get(f"products/{product['id']}/variations").json()
                    for v in variations:
                        price = v.get("price", "-")
                        regular_price = v.get("regular_price", "-")
                        sale_price = v.get("sale_price", "-")
                        for attr in v["attributes"]:
                            if attr["name"] == "Μέγεθος":
                                sizes.append(attr["option"])
                            if attr["name"] == "Χρώμα":
                                color = attr["option"]
                
                results.append({
                    "name": product["name"],
                    "short_description": product.get("short_description", ""),
                    "description": product.get("description", ""),
                    "price": price,
                    "regular_price": regular_price,
                    "sale_price": sale_price,
                    "available_sizes": sizes,
                    "color": color,
                    "image": product["images"][0]["src"] if product["images"] else None,
                    "categories": [c["name"] for c in product["categories"]],
                    "id": product["id"]
                })
        page += 1

    if not results:
        return jsonify({"message": "Δεν βρέθηκε προϊόν"}), 404

    return jsonify(results)
