import json, requests
from datetime import datetime, timedelta

class AQI_API:
    # Set the Base URL and Token for the AQI Stuff
    token = ''
    aqi_url = ''
    aqi_list = []
    final_list = {}
    
    # Actually obtain the token (open the JSON file)
    with open('config.json') as config_file:
        token = json.load(config_file)['AQI_Token']

    with open('config.json') as config_file:
        aqi_url = json.load(config_file)['AQI_URL']

    # Should be in the form of "2019-01-01" (as an example)
    def get_data(self, date):
        data = "{'parameterId': '59','dataType': 'aqi','dataView': 'daily','startDate': '" + date + "'}"
        response = requests.post(
            url = self.aqi_url,
            data = data,
            headers = {
                'Content-type': 'application/json'
            }
        )
        json_response = response.json()
        for result in json_response['results']:
            if result['Zone Name'] == "South Central Bay":
                for station in result['Stations']:
                    if 'data' in station:
                        now_current = station['data']
                        self.aqi_list.append(now_current)
        
    def shape_data(self, date):
        our_list = {}
        for data in self.aqi_list:
            start_time = datetime.strptime(date, "%Y-%m-%d")
            for num in data:
                our_list[start_time] = num
                start_time += timedelta(hours=1)
        self.final_list = our_list



# Example code for how it works!
# x = AQI_API()
# x.get_data("2019-01-01")
# x.shape_data("2019-01-01")


        
