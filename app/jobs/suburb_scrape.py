from selenium import webdriver
from bs4 import BeautifulSoup
from app import models
import logging
from time import sleep
from sqlalchemy.exc import IntegrityError

logging_format = '%(asctime)s: %(levelname)s - %(message)s'
logging.basicConfig(level = logging.INFO, format=logging_format)

class FlatmatesSuburbScrapper:
    BASE_URL = 'https://flatmates.com.au/rooms/'

    def __init__(self):
        self.web = webdriver.Chrome()
        self._enabled_cookies = False
    
    def scrape_suburb(self, suburb):
        self.suburb_name = suburb.name
        try:
            self._get_page_info_for(suburb.name, suburb.postcode)
            while self.next_page_clickable:
                self.process_page()
                self.get_next_page()
        except Exception as ex:
            raise ex
        finally:
            self.web.close()
    
    def get_next_page(self):
        if self.enabled_cookies:
            logging.info("Clicking Next Page")
            self.next_page_button.click()
            sleep(5)
            
    def process_page(self):
        raw_page_data = BeautifulSoup(self.web.page_source)
        processed_listings = self._process_page_data(raw_page_data)
        for listing in processed_listings:
            self._save_listing(listing)

    def _save_listing(self, listing_url):
        try:
            sess = models.Session()
            sess.add(models.Listing(listing_url, self.suburb_name))
            sess.commit()
        except IntegrityError:
            pass
        
    def _process_page_data(self, raw_page_data):
        listings = [self._process_listing(raw_listing) for raw_listing in raw_page_data.find_all('div', {'class' : 'content-column'})]
        logging.info(f"Found {len(listings)} listings")
        return listings
            
    def _process_listing(self, raw_listing):
        return raw_listing.div.a['href']
    
    def _get_page_info_for(self, suburb, postcode):
        logging.info(f"Getting Page Info for {self._transform_url(suburb, postcode)}")
        self.web.get(self._transform_url(suburb, postcode))
        
    def _transform_url(self, suburb, postcode):
        suburb_proper = '-'.join(suburb.split()).lower()
        return self.BASE_URL + f'{suburb_proper}-{postcode}'
    
    def _enable_cookies(self):
        logging.info("Enabling Cookies")
        self.web.find_element_by_class_name('gdpr-consent-element-button').click()

    @property
    def next_page_button(self):
        return self.web.find_element_by_class_name('styles__nextLink___2xdE0')
    
    @property
    def next_page_clickable(self):
        logging.info(f"Next Page Button Text: {self.next_page_button.text}")
        return self.next_page_button.text == 'Next'
    
    @property
    def enabled_cookies(self):
        if self._enabled_cookies:
            return True
        else:
            self._enable_cookies()
            self._enabled_cookies = True
            return True
