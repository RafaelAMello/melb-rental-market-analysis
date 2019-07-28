import multiprocessing as mp

import config
import models
from jobs.seed_suburbs import SeedDatabase
from jobs.suburb_scrape import FlatmatesSuburbScrapper

def scrape_suburb(suburb):
    scraper = FlatmatesSuburbScrapper()
    scraper.scrape_suburb(suburb)

def get_all_suburbs():
    pool = mp.Pool(1)
    suburbs = models.Session().query(models.Suburb).all()
    pool.map(scrape_suburb, suburbs)

def run():
    if config.SEED_DATABASE:
        SeedDatabase()
    get_all_suburbs()
