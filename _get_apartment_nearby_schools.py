from bs4 import BeautifulSoup


def _get_apartment_amenities(soup: BeautifulSoup) -> dict:
    """
    Get information about the both the property's amenities and features
    of the apartments themselves.

    Returns a dictionary with the following keys:
    - community_amenities: The community amenities available withing the property.
    - apartment_features:  The features of the apartment itself.
    """

    data = {}

    # Always split into 2 sections as far as I can tell
    containers          = soup.find(class_='schoolsSection').find_all(class_='spec')
    community_amenities = containers[0]
    apartment_features  = containers[1]

    # I considered parsing out the sections, but they're not consistant across
    # listings, so it seems like more trouble than it's worth. These bullet
    # points, on the other hand, will almost always be there.
    data['community_amenities'] = [x.text.strip() for x in community_amenities.find_all(class_='specInfo')]
    data['apartment_features']  = [x.text.strip() for x in apartment_features.find_all(class_='specInfo')]

    return data
