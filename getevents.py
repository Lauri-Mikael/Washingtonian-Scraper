from bs4 import BeautifulSoup
from image_down import image_down
from datetime import datetime, timedelta
from selenium import webdriver
import time

def get_events():

    # Create an empty list to store the event data
    event_data = []

    number = 1

    # URL to SOUP
    url = 'https://calendar.washingtonian.com/calendars/all-events?proxy_host=calendar.washingtonian.com&proxy_slug=washingtonian'
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all the event listings on the page
    day_events = soup.find_all('div', class_=["css-card js-card day-card type-smad",
                                    "css-card js-card day-card type-smad expandable",
                                    "css-card js-card day-card type-smad expandable ongoing"])
    
    for day_event in day_events:

        if 'css-card js-card day-card type-smad expandable ongoing' in str(day_event):

            eventdate = day_event.find('div', class_='day-card__header day-card__header--ongoing').text.strip()
        
        else:

            eventdate = day_event.find('div', class_='day-card__header day-card__header--daily').text.strip()

            if eventdate == 'Today':
                # Get today's date
                today = datetime.today()
                # Format the date
                eventdate = today.strftime('%A, %B %d')

            if eventdate == 'Tomorrow':
                # Get today's date
                today = datetime.today()
                # Get tomorrow's date
                tomorrow = today + timedelta(days=1)
                # Format tomorrow's date as 'Thursday, September 8'
                eventdate = tomorrow.strftime('%A, %B %d')

        event_listings = day_event.find_all('li', class_='card-listings-item event-element')

        # Loop through each event listing and extract the event data
        
        for event in event_listings:

            print("Still Running")

            # Extract the event title and link
            title = event.find('div', class_='card-listing-item-title')
            link = 'https://calendar.washingtonian.com/calendars/all-events/' + event['data-event']

            # Extract date and place
            eventtime = event.find('span', class_='card-listing-item-time')

            place = event.find('span', class_='card-listing-item-location')

            # Extract image
            image = event.find('img')

            if image == None or place == None or title == None or link == None:
                continue

            eventtime = eventtime.text.strip()[:-2]
            place = place.text.strip()
            title = title.text.strip()

            if 'src' not in str(image):
                continue
            image_url = image['src']
            image_name = image_down(image_url, number)

            if image_down == 0:
                continue
            
            number += 1
            final_data = [title, link, eventdate, eventtime, place, image_name]

            event_data.append(final_data)

    return event_data
