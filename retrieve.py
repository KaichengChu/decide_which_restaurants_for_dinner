from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from typing import Dict, Any
import logging

logging.basicConfig(filename='data.log', level=logging.ERROR, filemode='w')

BRUIN_PLATE_URL = "https://dining.ucla.edu/bruin-plate/"
DE_NEVE_URL = "https://dining.ucla.edu/de-neve-dining/"
EPICURIA_URL = "https://dining.ucla.edu/epicuria-at-covel/"

def get_menu_info(url:str) -> Dict[str, Any]:
    '''
    Description:
        Fetches and parses menu information from a given restaurant URL.
    Arguments:
        url: str : URL of the restaurant's menu page
    Returns: 
        list : a List of menu items
    '''
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    if "bruin-plate" in url:
        stations = ['Freshly Bowled', 'Harvest', 'Stone Fired', 'Stone Fired']
    elif "de-neve" in url:
        stations = ["The Front Burner", "The Kitchen", "The Grill", "Seasonal Sides"]
    else:
        stations = ["Psistaris", "Alimenti", "Mezze"]

    logging.info(f"Stations are {stations}")

    try:
        driver.get(url)
        time.sleep(3)

        # For retrieve the page information.
        # with open("bruin_plate_source.html", "w", encoding="utf-8") as f:
        #     f.write(driver.page_source)
        # print("Successfully saved page source to bruin_plate_source.html")

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract the restaurant name
        restaurant_name = soup.select_one('h1.wp-block-heading strong')

        if not restaurant_name:
            restaurant_name = soup.select_one('h1.wp-block-heading')

        # Extract activity level
        activity_level = None
        activity_level = soup.select_one('span#activity-level').get_text(strip=True)

        # Extract menu items: 1. find the correct div by id, then loop through the dishes.
        dinner_menu = {}
        for station in stations:
            station_id = f"dinner-{station.replace(' ', '-')}"
            station_div = soup.find('div', id=station_id)
            if station_div:
                items = station_div.select('.ucla-prose h3')
                item_list = [item.get_text(strip=True) for item in items]

                if station in dinner_menu:
                    dinner_menu[station].extend(item_list)
                else:
                    dinner_menu[station] = item_list
            else:
                logging.warning(f"Station {station} not found on the page.")
        return {
            "restaurant_name": restaurant_name.get_text(strip=True) if restaurant_name else "Unknown",
            "activity_level": activity_level if activity_level else "Unknown",
            "dinner_menu": dinner_menu
        }               
    except Exception as e:
        logging.error(f"Error retrieving menu info: {e}")
        return {}
    finally:
        driver.quit()

if __name__ == "__main__":
    bruinfood = get_menu_info(EPICURIA_URL)
    
    for key, value in bruinfood.items():
        print(f"{key}: {value}")