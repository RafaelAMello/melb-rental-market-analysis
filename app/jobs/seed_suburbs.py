from app import models
import logging

logging_format = '%(asctime)s: %(levelname)s - %(message)s'
logging.basicConfig(level = logging.INFO, format=logging_format)


class SeedDatabase:
    ALLOWABLE_SUBURBS = {
        'Melbourne' : 3000,
        'Southbank' : 3006,
        'St Kilda' : 3182,
        'North Melbourne' : 3051,
        'Fitztoy' : 3065,
        'South Melbourne' : 3205,
        'Hawthorn' : 3122,
        'Richmond' : 3121,
        'Carlton' : 3053,
        'Docklands' : 3008
    }

    def __init__(self):
        self.session = models.Session()
        self.seed_suburbs()
        self.session.commit()

    def seed_suburbs(self):
        for suburb_name, postcode in self.ALLOWABLE_SUBURBS.items():
            self.session.add(models.Suburb(suburb_name, postcode))
