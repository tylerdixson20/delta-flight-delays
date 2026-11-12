# This script builds delta_slc_flights_2025.csv from the raw BTS files.
# The raw files are too big for GitHub (about 300 MB per month), so we
# downloaded the 12 monthly zip files for 2025 from
# https://transtats.bts.gov/PREZIP/ and kept only Delta flights into SLC.

import pandas as pd
import zipfile

keep_cols = ['FlightDate', 'Month', 'DayofMonth', 'DayOfWeek', 'Marketing_Airline_Network',
             'Operating_Airline ', 'Origin', 'OriginCityName', 'Dest', 'CRSDepTime', 'CRSArrTime',
             'DepDelay', 'ArrDelay', 'ArrDel15', 'Cancelled', 'Diverted', 'CRSElapsedTime', 'Distance',
             'CarrierDelay', 'WeatherDelay', 'NASDelay', 'SecurityDelay', 'LateAircraftDelay']

months = []
for month in range(1, 13):
    name = 'On_Time_Marketing_Carrier_On_Time_Performance_Beginning_January_2018_2025_' + str(month) + '.zip'
    zip_file = zipfile.ZipFile(name)
    csv_name = zip_file.namelist()[0]
    data = pd.read_csv(zip_file.open(csv_name), usecols=keep_cols, low_memory=False)
    data = data[(data['Marketing_Airline_Network'] == 'DL') & (data['Dest'] == 'SLC')]
    months.append(data)

flights = pd.concat(months)
flights = flights.rename(columns={'Operating_Airline ': 'Operating_Airline'})
final_cols = ['FlightDate', 'Month', 'DayofMonth', 'DayOfWeek', 'Operating_Airline', 'Origin', 'OriginCityName',
              'Dest', 'CRSDepTime', 'CRSArrTime', 'DepDelay', 'ArrDelay', 'ArrDel15', 'Cancelled', 'Diverted',
              'CRSElapsedTime', 'Distance', 'CarrierDelay', 'WeatherDelay', 'NASDelay', 'SecurityDelay',
              'LateAircraftDelay']
flights = flights[final_cols]
flights = flights.sort_values(['FlightDate', 'CRSDepTime', 'Origin'])
flights.to_csv('delta_slc_flights_2025.csv', index=False)

# The weather file came from the NOAA data service for the Salt Lake City airport station:
# https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&stations=USW00024127&startDate=2025-01-01&endDate=2025-12-31&format=csv&units=standard&dataTypes=PRCP,SNOW,TMAX,TMIN,AWND,WSF2
