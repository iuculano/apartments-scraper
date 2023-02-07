from bs4 import BeautifulSoup
import re
import util


def _get_apartment_models(soup: BeautifulSoup) -> dict:
    """
    Get a list of nearby apartments by scraping... the nearyby apartments
    section of the page, unsurprisingly.

    Returns a list of dicts, each dict containing the following keys:
    - name:         The name of the model.
    - rent_low:     The low end of the rent range.
    - rent_high:    The high end of the rent range.
    - bedrooms:     The number of bedrooms. 0 for studio.
    - bathrooms:    The number of bathrooms.
    - sqft:         The square footage of the model.
    - deposit:      The required deposit for the lease agreement.
    - availability: The text describing the availability of the model.
    - is_available: Boolean of whether the model is available.
    - units:        A list of units for the model.

    Each unit is a dict with the following keys:
    - name:         The name of the unit.
    - rent:         The rent for the unit.
    - sqft:         The square footage of the unit.
    - availability: Availability date of the unit.
    """

    data = {
        'models':  []
    }

    # This will grab both available and unavailable models at the same time by
    # basically walking the list of models when the 'All' tab is selected
    container = soup.find(id='pricingView')
    container = container.find(class_='active', attrs={'data-tab-content-id': 'all'})
    models    = container.find_all(class_='pricingGridItem')

    for model in models:
        model_data = {}
        
        # The model's name, this always exists
        model_data['name'] = model.find(class_='modelName').text

        # This is the rent range, ie. $1,700 - $2,100. We want to parse it out
        # into the low and high number. Numerical strings will be converted to
        # numbers so they can be used more easily for comparisons/filtering.
        rent_text  = model.find(class_='rentLabel').text.strip()
        rent_match = re.search(r'^(\$[\d,]+)[-–\s]{0,3}(\$[\d,]+)?$', rent_text)
        if not rent_match:
            # Currently, None is used as a placeholder for a non-numeric value
            model_data['rent_low']  = None
            model_data['rent_high'] = None

        else:
            # Not always guaranteed to be a range - single numbers are valid
            # In this case, the high end is the same as the low end
            model_data['rent_low']  = int(util._strip_numerical_formatting(rent_match.group(1)))
            model_data['rent_high'] = int(util._strip_numerical_formatting(rent_match.group(2))) if rent_match.group(2) else model_data['rent_low']


        # Details should have the bedrooms, baths, sqft, and possibly deposit
        # These are stored in a few spans
        # Just split on all these characters and take the first element - it's
        # the number we want. For example: '1 bath' -> 1
        details                 = model.find(class_='detailsTextWrapper').find_all('span')
        model_data['bedrooms']  = 0 if details[0].text == 'Studio' else int(details[0].text.split()[0]) # Transform '1 bed'  to 1
        model_data['bathrooms'] = float(details[1].text.split()[0])
        model_data['sqft']      = int(util._strip_numerical_formatting(details[2].text.split()[0])) if details[2].text else None

        # May not always exist
        lease_deposit     = model.find(class_='leaseDepositLabel')
        #data['deposit']   = int(util._strip_currency_formatting(lease_deposit.text.split()[0])) if len(lease_deposit) > 0 else 0

        # Availability can seemingly show up in 2 different spans for some
        # reason I don't really understand.
        # Just checking that it isn't 'Not Available' appears sufficient...
        availability = model.find(class_=['availability', 'availabilityInfo'])
        if availability:
            model_data['availability'] = availability.text
            model_data['is_available'] = True if availability.text != 'Not Available' else False
        else:
            model_data['availability'] = 'Unknown'
            model_data['is_available'] = False



        # Try to walk the list of containers for units if it's available
        # This doesn't always exist
        units               = model.find_all(class_='unitContainer')
        model_data['units'] = []
        for unit in units:
            # This occasionally gets empty strings for some reason...
            # Just skipping them seems sufficient
            if unit.text == '':
                continue

            # Yeahhh some of this is gross
            model_data['units'].append({
                'name':         unit.find(class_='unitColumn').text.strip(),
                'rent':         int(util._strip_numerical_formatting(unit.find(class_='pricingColumn').find_all('span', class_=None)[0].text.strip())),
                'sqft':         unit.find(class_='sqftColumn').find_all('span', class_=None)[0].text,
                'availability': [x.strip() for x in unit.find(class_='dateAvailable').text.split('\n') if x.strip()][1] # WTF
            })

        data['models'].append(model_data)

    return data
