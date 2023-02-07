from bs4 import BeautifulSoup


def _get_google_review(soup: BeautifulSoup) -> dict:
    """
    Gets the Google maps review data for the apartment.

    In general, this seems to be much saner than Apartments.com's review
    system and this provides an easy way to "sanity check" the data.
    I have found glowing reviews on their website and horror shows on
    Google, so do with it as you will.
    """

    data = {}

    # Google names are hideous
    google_reviews = soup.select('div[data-attrid*="kc:/collection/knowledge_panels/local_reviewable:star_score"]')
    if len(google_reviews) > 0:
        # These classes make me awfully suspicious, no idea if they'll change
        google_rating       = google_reviews[0].find('span', class_='Aq14fc')
        google_review_count = google_reviews[0].find('span', class_='hqzQac')

        data['google_rating']       = float(google_rating.text)                if google_rating       else None
        data['google_review_count'] = int(google_review_count.text.split()[0]) if google_review_count else None

    return data
