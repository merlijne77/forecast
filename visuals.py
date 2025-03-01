#Showing a image with a layer of text (the weather forcast)
import datetime
import os
import imageio
import numpy as np
import night_day_time
from the_gui import start_gui


#TODO: tijd 2 decimalen terughalen uit git nieuwe versies
#TODO: Check if image is dark terughalen uit git nieuwe versies textcolor veranderen
#TODO: Bij een refresh de city even bewaren
global img
path = r"/home/heidi/PycharmProjects/Python/weather_app/build/assets/frame0/"
path_refresh_icon = '/home/heidi/refresh.png'
city = ''


def is_img_light(img, thrshld):
    is_light = np.mean(img) > thrshld
    return 'light' if is_light else 'dark'


def get_text_color(plaatje):
    f = imageio.v2.imread(plaatje, mode=False)
    print(is_img_light(f, 127))
    if (is_img_light(f, 127)) == 'dark':
        return 'white'
    else:
        return 'black'


def process_images_from_directory(weer_data):
    files = os.listdir(path)

    for file in files:
        print(file)
    print(weer_data['samenv'].lower())

    #get picture depending on the weather
    plaatje = choose_weather_img(weer_data['samenv'].lower(), weer_data['zonop'], weer_data['zononder'])
    create_ui(plaatje, weer_data)


def get_text_for_ui(weer_data):
    theta = '\N{DEGREE SIGN}'
    weer = str(weer_data['samenv'] + '\n\n' + 'Verwachting: ' + '\n' +
               weer_data['verw'] + '\n\n' + 'Windkracht: ' + weer_data[
                   'wind'] + '\n' + 'Temperatuur: ' + weer_data['temp'] + theta + '\n\n' + 'Zonsopkomst: ' + weer_data[
                   'zonop'] +
               '\n' + 'Zonsondergang: ' + weer_data['zononder'])
    return weer


def create_ui(background_img, weer_data):
    ct = datetime.datetime.now()
    weer = get_text_for_ui(weer_data)
    color_text = get_text_color(background_img)
    print(background_img)
    datum = night_day_time.get_time_values(weer_data['zonop'], weer_data['zononder'])
    start_gui(weer_data['plaats'], weer, color_text, background_img, datum)


def choose_weather_img(samenv, zonop, zononder):
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
