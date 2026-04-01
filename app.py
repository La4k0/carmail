from flask import Flask, render_template, jsonify, redirect, url_for, request
from db import Brand, Model, get_column_values, get_models_by_brand
from add_ons import random_select_from_list, random_select_between_numbers, available_prices
from datetime import datetime
from scraper import CarsScraper
import asyncio

CURRENT_YEAR = datetime.now().year

app = Flask(__name__)

car_scraper = CarsScraper()

@app.route("/", methods=["GET", "POST"])
def home():
    brands = get_column_values(Brand, Brand.name)
    example_brand = random_select_from_list(['Mercedes-Benz','Audi','BMW','Ford','Toyota','Porsche','Fiat','Kia','Nissan','Peugeot','Skoda','Honda','Suzuki','Volvo','Hyundai','Opel','Dacia'])
    example_model = random_select_from_list(get_models_by_brand(example_brand))
    example_start_year = random_select_between_numbers(1990,CURRENT_YEAR-1)
    example_end_year = random_select_between_numbers(example_start_year,CURRENT_YEAR)
    example_price = random_select_from_list(available_prices())
    example_hour = random_select_between_numbers(0,23)
    if example_hour < 10:
        example_hour = f'0{example_hour}'

    return render_template("index.html", brands=brands, example_brand=example_brand, example_model=example_model, example_start_year=example_start_year, example_end_year=example_end_year, example_price=example_price, example_hour=example_hour)

@app.route("/submit-filter", methods=["GET", "POST"])
async def submit_filter():
    # TO DO
    data = request.form.to_dict(flat=False)
    d = car_scraper.scrape_data(data)

    print(d)

    return redirect(url_for("home"))

@app.route("/models/<brand>")
def models(brand):
    brand_models = get_models_by_brand(brand)
    return jsonify(brand_models)

if __name__ == "__main__":
    app.run(debug=True)
