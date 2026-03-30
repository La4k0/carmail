from flask import Flask, render_template, jsonify
from db import Brand, Model, get_column_values, get_models_by_brand

app = Flask(__name__)

@app.route("/")
def home():
    brands = get_column_values(Brand, Brand.name)
    return render_template("index.html", brands=brands)

@app.route("/models/<brand>")
def models(brand):
    brand_models = get_models_by_brand(brand)
    return jsonify(brand_models)

if __name__ == "__main__":
    app.run(debug=True)
