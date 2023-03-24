import haversine as hs
from collections import OrderedDict
import numpy as np
from parsel import Selector 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.google.com")


def find_coord(location):
    url = "https://www.google.com/search?q=" + location + "+coordinates&oq=" +location + "+coordinates"
    driver.get(url)
    page_content = driver.page_source
    response = Selector(page_content)
    for el in response.xpath('//*[@id="rso"]/div[1]/div/block-component/div/div[1]/div[1]/div/div/div[1]/div/div/div[2]/div/div/div'):
        content = el.xpath('./div[1]').extract_first('')
        start = content.index(">") + 1
        end = content[start:].index("<")
        lat, long = content[start:start + end].split(", ")
        lat = lat[:lat.index("°")]
        long = long[:long.index("°")]
    
    return (float(lat), float(long))


def find_dist(coord1, coord2):
    dist = hs.haversine(coord1, coord2)
    return dist

def find_3_min_distance(coords):
    dist = {}
    for loc1 in coords:
        for loc2 in coords:
            if loc1 == loc2 or (loc2, loc1) in dist:
                continue
            distance = find_dist(coords[loc1], coords[loc2])
            dist[(loc1, loc2)] = distance
    sorted_dist = dict(sorted(dist.items(), key=lambda item: item[1]))
    i = 0
    for locations in sorted_dist:
        print(locations)
        i += 1
        if i == 3:
            break
    # print(sorted_dist)

def all_locations(location):
    coords = {}
    for loc in location:
        coord = find_coord(location= loc)
        coords[loc] = coord
    find_3_min_distance(coords= coords)
    

locations = ["lt+williams+hall+of+residence", "sengupta+hall", "macdonald+hall+iiest+shibpur", "pandya+hall+iiest+shibpur"]
all_locations(locations)