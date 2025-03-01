#Showing a image with a layer of text (the weather forcast)
import datetime
import os
import imageio
import numpy as np
import night_day_time
from the_gui import start_gui


global img
path = r"/home/heidi/PycharmProjects/Python/weather_app/build/assets/frame0/"
path_refresh_icon = '/home/heidi/refresh.png'
city = ''


def is_img_light(img, thrshld):
    """returns True if overal color of image is light"""
    return np.mean(img) > thrshld



def get_text_color(plaatje):
    """returns textcolor depending on the overal light in an image"""
    f = imageio.v2.imread(plaatje, mode=False)
    print(is_img_light(f, 127))
    if (is_img_light(f, 127)) == 'dark':
        return 'white'
    else:
        return 'black'


def get_text_for_ui(weer_data):
    theta = '\N{DEGREE SIGN}'
    #weer_data['verw'] + '\n\n' + 'Windkracht: ' + weer_data[
                  # 'wind'] + '\n' + 'Temperatuur: ' + weer_data['temp'] + theta + '\n\n' + 'Zonsopkomst: ' + weer_data[
                  # 'zonop'] +
               #'\n' + 'Zonsondergang: ' + weer_data['zononder'])
    weer = (f"{weer_data['samenv']}\n\nVerwachting:\n{weer_data['verw']}\n\nWindkracht: {weer_data['wind']}\n"
            f"Temperatuur: {weer_data['temp']}{theta}\n\nZonsopkomst: {weer_data['zonop']}\nZonsondergang: {weer_data['zononder']}")
    return weer


def create_ui( weer_data):
    """
    gets image depending on the weather
    gets the forecast to show in UI
    gets the textcolor for text printed on the image. If image is light textcolor is dark and visa versa
    calls the method to build the GUI with all this data
    :param background_img: background image depending on the weather
    :param weer_data: the weather dict received from weerlive API call
    :returns:
    """
    background_img = choose_weather_img(weer_data['samenv'].lower(), weer_data['zonop'], weer_data['zononder'])
    weer = get_text_for_ui(weer_data)
    color_text = get_text_color(background_img)
    datum = night_day_time.get_time_values(weer_data['zonop'], weer_data['zononder'])
    start_gui(weer_data['plaats'], weer, color_text, background_img, datum)


def choose_weather_img(samenv, zonop, zononder):
    """
    returns a image of clouds, sun, rain ect ect depending on the forecast and if it is day or night.
    :param samenv: summary of the weather on that moment
    :param zonop: time the sun goes up
    :param zononder: time the sun goes down
    :return: weather image
    """
    #TODO: Change to regex searching (re.findall(pattern))
    if 'onweer' in samenv:
        image = 'onweer_regen'
    elif 'bewolkt' in samenv and 'regen' in samenv:
        image = 'regen'
    elif 'zon' in samenv or 'zonnig' in samenv or 'helder' in samenv and not 'wolken' in samenv and not 'bewolkt' in samenv:
        image = 'zonnig'
    elif 'licht bewolkt' in samenv or 'droog na regen' in samenv:
        image = 'licht_bewolkt'
    elif 'geheel bewolkt' in samenv or 'zwaar bewolkt' in samenv:
        image = 'zwaar_bewolkt'
    elif 'wolken' in samenv and 'zon' in samenv:
        image = 'licht_bewolkt'
    elif 'motregen' in samenv or 'regen' in samenv:
        image = 'regen'
    else:
        image = 'licht_bewolkt'
    #check if sun is under and add _nacht to path
    if not night_day_time.is_time_in_range(zonop, zononder):
        return path + image + '_nacht' + '.png'
    return path + image + '.png'
