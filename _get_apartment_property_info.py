from bs4 import BeautifulSoup


def _get_apartment_property_info(soup: BeautifulSoup) -> dict:
    """
    Get the apartment's property information, such as its address.

    Returns a dictionary with the following keys:
    - property_name:       The name of the property.
    - street:              The street address of the apartment.
    - city:                The city the apartment is in.
    - state:               The state the apartment is in.
    - zip:                 The zip code of the apartment.
    - address:             The full address of the apartment.
    - neighborhood_link:   The link to the neighborhood page.
    - is_verified_listing: Whether or not the listing is verified.
    - description:         The description of the property.
    - blurb:               The blurb of the property.
    - features:            The features of the property.
    """

    data = {}


    # This should always be present
    data['property_name'] = soup.find(class_='propertyName', id='propertyName').text.strip()

    # This feels a little fragile, but is hopefully fine...
    address                   = [x.strip(',') for x in soup.find(class_='propertyAddressContainer').text.split('\n') if x.strip()]
    data['street']            = address[0]
    data['city']              = address[1] 
    data['state']             = address[2]
    data['zip']               = address[3]
    data['address']           = f'{data["street"]} {data["city"]} {data["state"]} {data["zip"]}'
    data['neighborhood_link'] = soup.find('a', class_='neighborhood').get('href')

    # Might as well
    is_verified                 = soup.find(class_='verifedText')
    data['is_verified_listing'] = True if is_verified else False


    description_container = soup.find(class_='descriptionSection')
    data['description']   = description_container.find('p').text
    data['blurb']         = description_container.find(class_='propertyBlurbContent').text
    data['features']      = [feature.text.strip() for feature in description_container.find_all('li')]

    return data
