from apartments_scraper import ApartmentsScraper

scraper  = ApartmentsScraper()
listings = [
    'https://www.apartments.com/lyra-new-york-ny/jjl8rp5/',
    'https://www.apartments.com/park-towers-south-new-york-ny/xc7j4tn/',
    'https://www.apartments.com/8-spruce-new-york-ny/1l3y464/',
    'https://www.apartments.com/eos-new-york-ny/zls36xz/',
    'https://www.apartments.com/via-57-west-new-york-ny/7tc4rkx/',
    'https://www.apartments.com/70-w-45th-st-new-york-ny/dxtefkl/',
    'https://www.apartments.com/frank-57-west-new-york-ny/yh2kx5r/',
    'https://www.apartments.com/10-hanover-square-new-york-ny/1wxy6j5/'
]

scraped_listings = []
for listing in listings:
    print(f'Scraping {listing}')
    data = scraper.get_apartment_data(listing)
    scraped_listings.append(data)

def filter_properties(prop: dict):
    try:
        truthiness = [
            prop['google_rating'] > 4.0        
        ]        
        return all(truthiness)

    except:
        # Something can't be compared, treat it as false
        return False

def filter_models(model: dict):
    try:
        truthiness = [
            model['is_available'] == True,
            model['bedrooms']     >= 1,
            model['rent_low']     <  6900,
            model['sqft']         >  600,
        ]
        return all(truthiness)

    except:
        return False    
    

viable_listings   = []
filtered_listings = list(filter(filter_properties, scraped_listings))
for listing in filtered_listings:
    temp           = listing.copy()
    temp['models'] = list(filter(filter_models, listing['models']))
    if len(temp['models']) > 0:
        viable_listings.append(temp)

_breakpoint = 1
