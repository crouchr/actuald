# free tier is 1000 calls per day - has this changed recently ?
# make a call every 10 minutes = 600 seconds
# num locations = 6
num_locations = 10
days_in_month = 31

api_calls_per_month = days_in_month * num_locations * (24 * 60 * 60) / 600

print('Monthly number of API calls : ' + str(api_calls_per_month))
