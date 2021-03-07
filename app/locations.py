# Locations to measure actual and to create forecasts for

# Llanfairfechen = microclimate - side of mountain and presumably quite wet
# Fastnet Rock : stormy weather
# for free tier of 1000 api calls per day I can have 6 locations
# FIXME - there may be a utf-8 issue with llanfaifechen - needs more investigation - caused exception
# FIXME : add location_code to this structure for now - see https://weather.codes/united-kingdom/

import get_env

stage = get_env.get_stage()

# Need two locations for testing as a minimum
if stage == 'DEV' or stage == 'IDE':
    locations = [
        {"location": "Stockcross, UK", "lat": "51.41460037", "lon": "-1.37486378"},
        {"location": "Chamonix, FR", "lat": "45.9237", "lon": "6.8694"},
    ]
elif stage == 'PRD':    # 5 locations = 720 api calls per day
    locations = [
        {"location": "Stockcross, UK", "lat": "51.41460037", "lon": "-1.37486378"},
        {"location": "Yarmouth Harbour, UK", "lat": "50.7051", "lon": "-1.5027"},
        {"location": "Lymington Harbour, UK", "lat": "50.7535", "lon": "-1.5283"},
        {"location": "Portsmouth, UK", "lat": "50.8198", "lon": "-1.0880"},
        {"location": "Cowes, UK", "lat": "50.7628", "lon": "-1.3005"}
    ]
else:   # indicates a probable error
    locations = [
        {"location": "Bay of Biscay, Portugal", "lat": "45.5570", "lon": "-3.1632"}
    ]

# {"location": "Lymington Harbour, UK", "lat": "50.7535", "lon": "-1.5283"},
# {"location": "Fastnet Rock, Ireland", "lat": "51.3889", "lon": "-9.6036"},
# {"location": "Bay of Biscay, Portugal", "lat": "45.5570", "lon": "-3.1632"},
# {"location": "Mercury Marina, Hamble, UK", "lat": "50.8708", "lon": "-1.3129"},
# {"location": "Portsmouth, UK", "lat": "50.8198", "lon": "-1.0880"},
# {"location": "Cowes, UK", "lat": "50.7628", "lon": "-1.3005"},
# {"location": "Snake Pass, UK", "lat": "53.4326", "lon": "-1.8673"}
# {"location": "Beaulieu, UK", "lat": "50.8156", "lon": "-1.4532"},
# {"location": "Lymington Harbour, UK", "lat": "50.7535", "lon": "-1.5283"},
# {"location": "Llanfairfechen, UK", "lat": "53.2528", "lon": "-3.9751"},
# {"location": "Yarmouth Harbour, UK", "lat": "50.7051", "lon": "-1.5027"}
# {"location": "Llanfairfechen, UK", "lat": "53.2528", "lon": "-3.9751"}
# {"location": "Norwich, UK", "lat": "52.6310", "lon": "1.2970"},
# {"location": "New York City, US", "lat": "40.7125", "lon": "-74.0060"},
# {"location": "Chamonix, FR", "lat": "45.9237", "lon": "6.8694"},
# {"location": "San Francisco, US", "lat": "37.7749", "lon": "-122.4194"}