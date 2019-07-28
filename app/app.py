import config
import models
from jobs.seed_suburbs import SeedDatabase

def run():
    if config.SEED_DATABASE:
        SeedDatabase()
