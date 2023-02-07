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
    containers    = soup.find(class_='amenitiesSection')
    section_names = containers.find_all(class_='sectionTitle') if containers else None
    section_data  = containers.find_all(class_='spec')         if containers else None
    assert len(section_names) == len(section_data)

    # These sections may not exist
    index = 0
    for i in range(len(section_names)):
        # I considered parsing out the sections, but they're not consistant across
        # listings, so it seems like more trouble than it's worth. These bullet
        # points, on the other hand, will almost always be there.
        name       = section_names[i].text.lower().replace(' ', '_')
        data[name] = [x.text.strip() for x in section_data[i].find_all(class_='specInfo') if x]

    return data
