from bs4 import BeautifulSoup


def _get_apartment_contact_info(soup: BeautifulSoup) -> dict:
    """
    Get the contact information for the property.

    Returns a dictionary with the following keys:
    - phone:        The phone number of the property.
    - website:      The website of the property.
    - office_hours: A dictionary of the office hours of the property.
    """

    data = {}

    contact_container = soup.find(class_='contactInfo')
    phone             = contact_container.find(class_='phoneNumber')
    website           = contact_container.find(class_='propertyWebsiteLink')
    data['phone']     = phone.text.strip()  if phone   else None
    data['website']   = website.get('href') if website else None

    contact_hours = {}
    for hours in contact_container.find_all(class_='daysHoursContainer'):
        # This is a bit unintuitive - think of this as 2 columns...
        # The days, and the hours that are available

        # There's likely some formatting we'll need to strip away
        # These are the 'raw' entries in the list of posted hours
        days_raw  = hours.find(class_='days').text.strip(' ,\n')
        hours_raw = hours.find(class_='hours').text.strip()

        # Parse into a more standard format - this should# always return 7
        # days, no abbreviations. Apartments.com seems to start on Monday
        days_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # Parse out pairings of days, i.e. 'Monday & Tuesday'
        split_days = [x.strip() for x in days_raw.split('&')]
        if len(split_days) > 1:
            for day in split_days:
                contact_hours[day] = hours_raw
            continue

        # Parse out ranges of days, i.e. 'Monday - Friday'
        range_days = [x.strip() for x in days_raw.split('-')]
        if len(range_days) > 1:
            start_index = days_list.index(range_days[0])
            end_index   = days_list.index(range_days[1])
            
            for day in days_list[start_index : end_index + 1]:
                contact_hours[day] = hours_raw
            continue

        # If we get here, we're dealing with a single day
        contact_hours[days_raw] = hours_raw

    # This signifies a bug - tell an adult if this happens
    assert len(contact_hours) == 7, f'Failed to parse contact hours - expected 7 days, got {len(contact_hours)}.'

    # Sort the days in order
    ordered_days = {}
    for day in days_list:
        ordered_days[day] = contact_hours[day]

    data['office_hours'] = ordered_days
    return data
