from lxml import html
import requests
from requests_html import HTMLSession
import json
import time



def main():
	
	#get_flight_info('A7e8f8')
	while(True):
		flights = flights_in_zone()
	
		if flights:
			for flight in flights:
				get_flight_info(flight)
		time.sleep(1)


# Appends flights ICAO present in coordinate space to list
def flights_in_zone():

	"""
	top_left = (47.528542, -122.346872)
	bottom_left = (47.525525, -122.346872)
	top_right = (47.528542, -122.278043)
	bottom_right = (47.526126,-122.278043)
	"""

	top_left = (47.541779, -122.346872)
	bottom_left = (47.538762, -122.346872)
	top_right = (47.541779, -122.278043)
	bottom_right = (47.538762,-122.278043)


	"""
	up/down, left right
	lat 	,    lon
	47.540268 -122.317177
	"""

	flights_in_zone = []

	r = requests.get('http://10.0.0.199/dump1090-fa/data/aircraft.json')
	flights_json = json.loads(r.content)
	for flight in flights_json['aircraft']:
		if 'lat' in flight and 'lon' in flight:
			if flight['lon'] > top_left[1] and flight['lon'] < top_right[1]:
				if flight['lat'] < top_left[0] and flight['lat'] > bottom_right[0]:
					flights_in_zone.append(flight['hex'])

	return flights_in_zone


# Scrapes flight info from FlightAware using ICAO
def get_flight_info(icao):

	session = HTMLSession()
	r = session.get('https://flightaware.com/live/modes/'+icao+'/redirect')

	r.html.render()

	file = open("output.html", "w")
	file.write(r.html.html)
	file.close()
	
	tree = html.fromstring(r.html.html)

	source = tree.xpath('//*[@id="flightPageTourStep1"]/div[1]/div[1]/span[2]/text()')
	destination = tree.xpath('//*[@id="flightPageTourStep1"]/div[1]/div[2]/span[2]/span/text()')
	aircraft = tree.xpath('//*[@id="slideOutPanel"]/div[1]/div[2]/div[4]/div[8]/div[1]/div/div[1]/div[2]/text()')
	flight_ident = tree.xpath('//*[@id="slideOutPanel"]/div/div/div[3]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/text()')

	cleaned_aircraft = clean_text(aircraft[0])
	cleaned_source = clean_text(source[0])
	cleaned_destination = clean_text(destination[0])
	cleaned_ident = clean_text(flight_ident[0])

	print(cleaned_ident)
	print(cleaned_source)
	print(cleaned_destination)
	print(cleaned_aircraft)
	print('\n')
	time.sleep(1)


# Cleans flight information strings
def clean_text(text):

	cleaned_text = text.replace('\n', '')
	cleaned_text = cleaned_text.replace('\t', '')

	open_paren = cleaned_text.find('(')
	close_paren = cleaned_text.find(')')
	if open_paren>0 and close_paren>0:
		cleaned_text = cleaned_text[0:open_paren]+cleaned_text[close_paren+1:len(cleaned_text)-1]
	return cleaned_text




if __name__=='__main__':
	main()