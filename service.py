import requests 
  
# api-endpoint 
URL = "http://maps.googleapis.com/maps/api/geocode/json"
  
# location given here 
location = "delhi technological university"
  
# defining a params dict for the parameters to be sent to the API 
PARAMS = {'address':location} 
  
# sending get request and saving the response as response object 
r = requests.get(url = URL, params = PARAMS) 
  
# extracting data in json format 
data = r.json() 
  
  
formatted_address = data['results'][0]['formatted_address'] 
  
# printing the output 
print("Latitude:%s\nLongitude:%s\nFormatted Address:%s"
      %(formatted_address)) 