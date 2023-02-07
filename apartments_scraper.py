from bs4 import BeautifulSoup
from _get_apartment_amenities       import _get_apartment_amenities
from _get_apartment_contact_info    import _get_apartment_contact_info
from _get_apartment_models          import _get_apartment_models
from _get_apartment_property_info   import _get_apartment_property_info
from _get_apartment_reviews         import _get_apartment_reviews
from _get_apartment_transportation  import _get_apartment_transportation
from _get_google_review             import _get_google_review
import util


class ApartmentsScraper:
    def __init__(self):
        self._driver = util._create_selenium_webdriver()


    def get_apartment_data(self, listing_url: str) -> dict:
        source = util._get_parseable_page_source(listing_url, self._driver)
        soup   = BeautifulSoup(source, features='html.parser')
        
        amalgamation  = {}
        to_amalgamate = [
            _get_apartment_amenities(soup),
            _get_apartment_contact_info(soup),
            _get_apartment_models(soup),            
            _get_apartment_property_info(soup),
            _get_apartment_reviews(soup),
            #_get_apartment_transportation(soup)
        ]

        for i in to_amalgamate:
            amalgamation.update(i)


        # Try to scrape reviews off Google by just searching the name and address
        # Simple, but thankfully works in most cases
        search = f'https://www.google.com/search?q={amalgamation["property_name"]} {amalgamation["address"]}'
        source = util._get_parseable_page_source(search, self._driver)
        soup   = BeautifulSoup(source, features='html.parser')

        amalgamation.update(_get_google_review(soup))

        return amalgamation
