#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: giuliani
"""

import bs4, requests, schedule, time 

SEARCHED_COUNTRY = 'Italien'
REQUEST_RKI_URL = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Risikogebiete_neu.html'
REQUEST_ZDF_URL= "https://www.zdf.de/nachrichten/politik/corona-impfung-daten-100.html"
REQUEST_TELEGRAM_URL = 'https://api.telegram.org/bot_token/sendMessage?chat_id=&text={}'

CSS_SELECTOR_COUNTRIES = 'div#wrapperOuter div#wrapperInner div#wrapperDivisions div#wrapperDivisions-2 div#wrapperContent div#content div#main div.text ul' 
CSS_SELECTOR_COUNTRIES_TITLE = f'{CSS_SELECTOR_COUNTRIES} li'
NEW_LINE = '\n'

def request_rki_site():
    # download page
    rki_page = requests.get(REQUEST_RKI_URL)
    # throw an error if the page is the request failed
    rki_page.raise_for_status()
    # return parsed text from rki page 
    return bs4.BeautifulSoup(rki_page.text, 'html.parser')

def format_resultset_to_array(resultset):
    array = []
    array.extend(
        (i.text for i in resultset))
    return array

def create_covid_message(searched_country):
        result_message = 'Für dieses Land gibt es Covid Warnhinweise.' + NEW_LINE
        result_message += 'Das Land oder min. eine Region wurde als Risikogebiet deklariert:' + NEW_LINE
        result_message += f'{searched_country}'[:-1].replace(')',')' + NEW_LINE)
        return result_message

def send_message_to_telegram(result_message):
    message = result_message + '\n' + REQUEST_RKI_URL + "\n" + REQUEST_ZDF_URL
    request = requests.get(REQUEST_TELEGRAM_URL.format(f'{message}'))
    if request.status_code == 200:
       print('Message sent!')

if __name__ == "__main__":
    rki_text = request_rki_site()

    # get countries and regions by css selector
    countries_resultset = rki_text.select(CSS_SELECTOR_COUNTRIES_TITLE)
    # result set to arrays  
    countries = format_resultset_to_array(countries_resultset)

    # get italy element from countries
    filtered_countries = list(filter(lambda country: SEARCHED_COUNTRY in country, countries))

    if len(filtered_countries) > 0:
        # get first value
        searched_country = filtered_countries[0]
        # create message
        result_message = create_covid_message(searched_country)
        # send message
        send_message_to_telegram(result_message)
    else:
        # create message
        result_message = f'{SEARCHED_COUNTRY} ist kein Risikogebiet.'
        # send message
        send_message_to_telegram(result_message)
