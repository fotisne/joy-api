from woocommerce import API

# Σύνδεση με WooCommerce
wcapi = API(
    url="https://www.joyfashionhouse.com",
    consumer_key="ck_d4c3aab55f4192ff737a1cac745c70db1fa8451c",
    consumer_secret="cs_7b88b5452edea933245a96a456814c1471202b65",
    version="wc/v3"
)

# Ανάκτηση μόνο των δημοσιευμένων προϊόντων
products = wcapi.get("products", params={"per_page": 70, "status": "publish"}).json()

for product in products:
    print(f"\n🔹 {product['name']} | ID: {product['id']}")

    # Μικρή Περιγραφή (short description)
    short_desc = product.get("short_description", "")
    print("📝 Μικρή Περιγραφή:", short_desc.strip() if short_desc.strip() else "—")

    # Περιγραφή
    desc = product.get("description", "")
    print("📄 Περιγραφή:", desc.strip() if desc.strip() else "—")

    # Τιμή  ---- Se epipedo proiontos exei mono price, oi kanonikes times einai se epipedo parallagis
    #price = product.get("price", "")
    #print("💶 Τιμή:", f"{price}€" if price else "—")

    #price = product.get("regular_price", "")
    #print("💶 Τιμή:", f"{price}€" if price else "—")
    price = 0.0
    regular_price = 0.0
    sale_price = 0.0
    sizes = []
    color = '-'

    # Διαθεσιμότητα και μέγεθος
    if product["type"] == "variable":
        variations = wcapi.get(f"products/{product['id']}/variations").json()
        for v in variations:
            price = v.get("price", "—")
            regular_price = v.get("regular_price", "—")
            sale_price = v.get("sale_price", "—")      
            #print("💶 Τιμή (Συνολική):", v.get("price", "—"))
            #print("💶 Κανονική Τιμή:", v.get("regular_price", "—"))
            #print("💶 Τιμή Προσφοράς:", v.get("sale_price", "—"))
            available = "Ναι" if v.get("stock_status") == "instock" else "Όχι"
            #print(f"- Διαθέσιμο: {available}")
            for attr in v["attributes"]:
                #print(attr["name"])
                if attr["name"] == "Μέγεθος":
                    #available = "Ναι" if v.get("stock_status") == "instock"
                    if v.get("stock_status") == "instock":
                        sizes.append(attr['option'])
                if attr["name"] == "Χρώμα":
                    color = attr['option']
                
                    

#                    else "Όχι"
                    print(f"- Μέγεθος: {attr['option']} | Διαθέσιμο: {available}")
    else:
        διαθέσιμο = "Ναι" if product.get("stock_status") == "instock" else "Όχι"
        print(f"- Μέγεθος: ONE SIZE | Διαθέσιμο: {διαθέσιμο}")


    print("💶 Τιμή (Συνολική):", price)
    print("💶 Κανονική Τιμή:", regular_price)
    print("💶 Τιμή Προσφοράς:", sale_price)
    print("💶 Color:", color)
    print("💶 Available Sizes:", ' - '.join(sizes))
    



    # Εικόνα
    if product["images"]:
        print("🖼️ Εικόνα:", product["images"][0]["src"])
    else:
        print("🖼️ Δεν υπάρχει εικόνα.")

    # Κατηγορίες
    if product["categories"]:
        categories = [cat["name"] for cat in product["categories"]]
        print("🏷️ Κατηγορίες:", ", ".join(categories))
    else:
        print("🏷️ Κατηγορίες: —")

    print("—" * 60)