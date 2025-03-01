#is current time between two given timemoments? In my case sun up sun under?
# using datetime module
import datetime
import locale


def get_time_values(sun_up, sun_under):
    locale.setlocale(locale.LC_ALL, "")#needed to get my locale dutch
    ct = datetime.datetime.now()
    print()
    try:
        time_dict = {'curr_hour': int(ct.hour),
                     'curr_minute': int(ct.minute),
                     'sun_up_hour': int(sun_up[0:2]),
                     'sun_under_hour':int(sun_under[0:2]),
                     'sun_up_minute': int(sun_up[3:5]),
                     'sun_under_minute': int(sun_under[3:5]),
                     'date_string':ct.strftime('%d %B %Y'),#23 januari 2044
                     'time_string': ct.strftime('%H:%M uur')}#12:05 uur
    except ValueError:
        print('ValueError')
    return time_dict


#veranderen met dateTime math methodes
def is_time_in_range(sun_up, sun_under):
   time_dict = get_time_values(sun_up, sun_under)
   if time_dict['curr_hour'] == time_dict['sun_up_hour'] and time_dict['curr_minute'] > time_dict['sun_up_minute']:
       return True
   elif time_dict['curr_hour'] == time_dict['sun_under_hour'] and time_dict['curr_minute'] < time_dict['sun_under_minute']:
       return True
   elif time_dict['sun_up_hour'] < time_dict['curr_hour'] < time_dict['sun_under_hour']:
       return True
   else:
       return False

