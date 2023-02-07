from bs4 import BeautifulSoup
import util


def _get_apartment_transportation(soup: BeautifulSoup) -> dict:
    """
    Gets a list of available transportation options near the apartment.

    Returns a dict containing a list of nearby apartments:
    - <the name of the transportation type>: 
    """

    data = {}

    # This section may or may not exist
    container = soup.find(class_='profileV2TransportationSection')
    if not container:
        return data

    # These are basically a set of tables, need to grab the first header
    # for the name of the table we're dealing with - for example:
    # - Transit / Subway
    # - Commuter Rail
    # - Airports
    for table in container.find_all(class_='transportationDetail'):
        # Try to grab the name out of the header, this will be the key
        # of the object we create - if we can't parse this, consider it
        # a failed attempt and skip
        header = table.find(class_='longLabel')
        if not header:
            continue
        
        # Finally iterate over the rows of the table and grab the data
        name       = header.find(class_='headerCol1').text.lower().replace('/', '_').replace(' ', '')
        data[name] = []
        for row in table.find_all('tr'):
            temp = {
                'name':     row.find(class_='transportationName').text,
                'type':     row.find(class_='commute-type-data').text,
                'time':     row.find(class_='left-align-data').text,
                'distance': row.find(class_='right-align-data').text
            }

            # Some rows link to their spot on the map, grab that if it exists
            link = row.find(class_='transportationName').find('a').get('href')
            if link:
                temp['link'] = link

            data[name].append(temp)
    
    transportation_score_card = soup.find(class_='transportationScoreCard')
    for card in transportation_score_card.find_all(class_='score-card'):
        # Transform name like "Walk Score" -> "walk_score"
        name       = card.find(class_='bodyTextLine').text.lower().replace(' ', '_')
        data[name] = {
            'title':       card.find(class_='title').text,
            'score':       int(card.find(class_='score').text),
            'description': card.find(class_='generatedText').text
        }

    return data
