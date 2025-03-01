import json
import requests
import visuals


weer = ' '


def getKey():
    file_path = "/home/heidi/PycharmProjects/Python/weather_app/build/assets/info.txt"
    with open(file_path, 'r') as file:
        file_content = file.read()

    return file_content


def forcast(city):
    """
    calls the weather Api from liveweer.nl with the forecast from a village or city in the Netherlands
    :param city: village or city in the netherlands
    :return: json with the forecast
    """
    link = "https://weerlive.nl/api/json-data-10min.php?key=6afe9341be&locatie=Rotterdam"
    key = getKey()
    link_with_cor = f"https://weerlive.nl/api/json-data-10min.php?key={key}&locatie=" + city
    # Request data from link as 'str'
    data = requests.get(link_with_cor).text
    # convert 'str' to Json
    return json.loads(data)  #dict


def process_data(city='Rotterdam'):
    """
    puts the json data in to a dict
    :param city:
    :return: weer_data dict with all the forecast data
    """
    data = forcast(city)
    verw = data['liveweer'][0]['verw']
    verw = newline_str(verw)

    weer_data = {'zonop': data['liveweer'][0]['sup'],
                 'zononder': data['liveweer'][0]['sunder'],
                 'verw': verw,
                 'wind': data['liveweer'][0]['winds'],
                 'temp': data['liveweer'][0]['temp'],
                 'plaats': data['liveweer'][0]['plaats'],
                 'samenv': data['liveweer'][0]['samenv']}

    visuals.create_ui(weer_data)


def newline_str(text):
    """creates a newline with every dot or comma in the text"""
    text = text.replace('.','.\n').replace(',',',\n')
    return text

#TODO: New API link (LIVEWEER) Available. Implement before december 2025