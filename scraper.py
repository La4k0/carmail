import asyncio
from playwright.async_api import async_playwright, Page
import psycopg2 as pg2
import time
from datetime import datetime
import re
from colorama import init, Fore, Style
import os
from dotenv import load_dotenv

load_dotenv()

init(autoreset=True)

class CarsScraper:
    def __init__(self):
        self.home_page_url = os.getenv('PAGE_URL')

        self.filters = { "type": "//span[contains(text(),'Какво') and not(contains(@class,'hide'))]",
                         "coupe": "//span[contains(text(),'Купе') and not(contains(@class,'hide'))]",
                         "brand": "//span[contains(text(),'Марка') and not(contains(@class,'hide'))]",
                         "model": "//span[contains(text(),'Модел') and not(contains(@class,'hide'))]",
                         "fuel": "//span[contains(text(),'Гориво') and not(contains(@class,'hide'))]",
                         "gears": "//span[contains(text(),'Скорости') and not(contains(@class,'hide'))]",
                         "price": "//span[contains(text(),'Цена') and not(contains(@class,'hide'))]",
                         "year": "//span[contains(text(),'Година') and not(contains(@class,'hide'))]",
                         "location": "//span[contains(text(),'Къде') and not(contains(@class,'hide'))]",
                         "seller_type": "//span[contains(text(),'От') and not(contains(@class,'hide'))]",
                         "color": "//span[contains(text(),'Цвят') and not(contains(@class,'hide'))]",
                         "doors_count": "//span[contains(text(),'Брой врати') and not(contains(@class,'hide'))]",
                         "horse_power": "//span[contains(text(),'Мощност') and not(contains(@class,'hide'))]",
                         "features": "//span[contains(text(),'Екстри') and not(contains(@class,'hide'))]",
                         "steering_wheel": "//span[contains(text(),'Волан') and not(contains(@class,'hide'))]",
                         "listing_date": "//span[contains(text(),'Публикувани') and not(contains(@class,'hide'))]",
                         "condition": "//span[contains(text(),'Състояние') and not(contains(@class,'hide'))]", }

    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.webkit.launch(headless=True)
        context = await self.browser.new_context()
        self.page = await context.new_page()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.browser.close()
        await self.playwright.stop()

    async def wait_for_selector_and_click(self, xpath: str, timeout: int):
        element = self.page.locator(f'xpath={xpath}').first
        await element.wait_for(state="attached", timeout=timeout)
        await element.click()
        print(f"Clicked element with XPath: {xpath}")

    async def scraping_filters(self):
        await self.page.goto(self.home_page_url)

        await self.wait_for_selector_and_click(self.filters["brand"], 10 * 1000)

        all_brands_xpath = "//span[contains(text(),'Марка') and contains(@class,'title')]//following::label[contains(@for,'brand')]"

        all_brands = self.page.locator(f"xpath={all_brands_xpath}")
        all_brands_count = await all_brands.count()

        all_brands_dict = {}

        for brand in range(all_brands_count):
            await self.page.wait_for_selector(selector=f"xpath=({all_brands_xpath})[{brand+1}]", timeout=10 * 1000, state='visible')

            current_brand = self.page.locator(f"xpath=({all_brands_xpath})[{brand+1}]")
            current_brand_text = (await current_brand.text_content()).strip()

            if not re.search(r'^\W*Всички?\W*$', current_brand_text, re.I|re.U|re.S) and current_brand_text not in all_brands_dict:
                all_brands_dict[current_brand_text] = {}
                models_list = []

                await current_brand.click()
                await asyncio.sleep(1)

                await self.wait_for_selector_and_click(self.filters["model"], 10 * 1000)

                all_models_xpath = "//span[contains(text(),'Модел') and contains(@class,'title')]//following::label[contains(@for,'model')]"

                all_models = self.page.locator(f"xpath={all_models_xpath}")
                all_models_count = await all_models.count()
                print(f'All models count is {all_models_count}')

                for model in range(all_models_count):
                    await self.page.wait_for_selector(selector=f"xpath=({all_models_xpath})[{model + 1}]",timeout=10 * 1000, state='visible')
                    current_model = self.page.locator(f"xpath=({all_models_xpath})[{model + 1}]").first
                    current_model_text = (await current_model.text_content()).strip()

                    if not re.search(r'^\W*Всички?\W*$', current_model_text, re.I | re.U | re.S) and current_model_text not in all_brands_dict[current_brand_text]:
                        models_list.append(current_model_text)
                        all_brands_dict[current_brand_text] = models_list

                        await self.wait_for_selector_and_click("//span[contains(text(),'Модел') and contains(@class,'title')]//following::button[contains(.,'Потвърди')]", 10 * 1000)
                        await asyncio.sleep(1)
                        await self.wait_for_selector_and_click("//span[contains(text(),'Марка')]//following::span[contains(.,'cancel')]", 10 * 1000)
                        await asyncio.sleep(1)

                        await self.wait_for_selector_and_click(self.filters["brand"], 10 * 1000)
                        return all_brands_dict

def get_brands_dict():
    return asyncio.run(_get_brands())

async def _get_brands():
    async with CarsScraper() as scraper:
        return await scraper.scraping_filters()
