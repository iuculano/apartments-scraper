from bs4 import BeautifulSoup
import re


def _get_apartment_reviews(soup: BeautifulSoup) -> dict:
    """
    Get information about the apartment's reviews.

    Sometimes these appear beyond earthly logic, don't put too much stock in
    what's returned here.

    Returns a dictionary with the following keys:
    - rating:       The average rating of the apartment, on a scale of 1 to 5
    - review_count: The number of reviews the apartment has
    """

    data = {}

    # The parent div always exists, but these 2 are conditional
    rating               = soup.find(class_='reviewRating')
    review_count         = soup.find(class_='reviewCount')
    data['rating']       = float(rating.text) if rating else None    
    data['review_count'] = int(re.findall(r'(\d+)', review_count.text)[0]) if review_count else None

    return data
