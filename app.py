from flask import Flask, render_template, jsonify, redirect, url_for, request
# from db import Brand, Model, get_column_values, get_models_by_brand

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    # brands = get_column_values(Brand, Brand.name)

    return render_template("index.html", brands=['a','b','c'])

@app.route("/submit-filter", methods=["GET", "POST"])
def submit_filter():
    data = request.form.to_dict(flat=False)
    print(data)
    return redirect(url_for("home"))

# @app.route("/models/<brand>")
# def models(brand):
#     brand_models = get_models_by_brand(brand)
#     return jsonify(brand_models)

if __name__ == "__main__":
    app.run(debug=True)
