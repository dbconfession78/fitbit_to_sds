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
                converted_date = start_time.strftime("%Y-%m-%d_%X")
                our_list[converted_date] = num
                start_time += timedelta(hours=1)
        self.final_list = our_list
    
    def return_final_data(self, date):
        self.get_data(date)
        self.shape_data(date)
        return self.final_list
    
    def shift_date(self, date):
        new_date = datetime.strptime(date, "%Y-%m-%d")
        new_date += timedelta(days=1)
        converted_date = new_date.strftime("%Y-%m-%d")
        return converted_date
    
    def compile_lots_of_data(self, num):
        start_date = "2019-01-01"
        compiled_list = []
        for count in range(num):
            self.get_data(start_date)
            self.shape_data(start_date)
            start_date = self.shift_date(start_date)
            compiled_list.append(self.final_list)
        return compiled_list

        
