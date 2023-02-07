import json
import requests
import datetime
from datetime import datetime

# отправление ГЕТ-запроса на json сайта Go2Bus
url_170 = requests.get('https://go2bus.ru/inforoutedetails?route=170%D1%8D&vt=b&date=' + datetime.today().strftime('%Y-%m-%d') + '&srv=kem&lang=ru&timezone=0').content
url_171 = requests.get('https://go2bus.ru/inforoutedetails?route=171%D1%8D&vt=b&date=' + datetime.today().strftime('%Y-%m-%d') + '&srv=kem&lang=ru').content
url_172 = requests.get('https://go2bus.ru/inforoutedetails?route=172%D1%8D&vt=b&date=' + datetime.today().strftime('%Y-%m-%d') + '&srv=kem&lang=ru&timezone=0').content
url_173 = requests.get('https://go2bus.ru/inforoutedetails?route=173%D1%8D&vt=b&date=' + datetime.today().strftime('%Y-%m-%d') + '&srv=kem&lang=ru&timezone=0').content


# реализация функции получения ближайщего времени прибытия автобуса в город
def next_bus_on_city(inlet):
    try:
        list_bus = [url_170, url_171, url_172, url_173]
        name_bus = ['170э', '171э', '172э', '173э']
        result = ''
        for n, url in enumerate(list_bus):
            save_stop_dict = {}
            normal_time = []
            pars_json = json.loads(url)
            if url == url_171:
                stops = list(pars_json['directions'][1]['stops'])
            else:
                stops = list(pars_json['directions'][0]['stops'])

            for stop in range(len(stops)):
                name_stop = stops[stop]['zones'][0]['name']
                time_dict = stops[stop]['comings']
                for time in range(len(time_dict)):
                    save_stop_dict.setdefault(name_stop, [])
                    save_stop_dict[name_stop].append(time_dict[time]['time'])

            for stop in save_stop_dict:
                if stop == inlet:
                    for time in save_stop_dict[stop]:
                        if (datetime.strptime(time, '%Y-%m-%dT%H:%M:%S') - datetime.now()).days >= 0:
                            normal_time.append(datetime.strptime(time, '%Y-%m-%dT%H:%M:%S'))

            if normal_time == []:
                result += ''
            else:
                result += '✅'
                result += str('В ' + str(min(normal_time).time()) + ' сюда приедет автобус ' + name_bus[n])
                result += '\n'
        if result == '':
            result = '❌Похоже сегодня сюда уже никто не приедет......'
    except:
        result = 'Что-то пошло не так..... Тебе следует слушать мои просьбы, пока не я к тебе лично не приеду на 172э'
    return result

# реализация функции получения ближайщего времени прибытия автобуса на Лесную Поляну
def next_bus_on_pol(inlet):
    try:
        list_bus = [url_170, url_171, url_172, url_173]
        name_bus = ['170э', '171э', '172э', '173э']
        result = ''
        for n, url in enumerate(list_bus):
            save_stop_dict = {}
            normal_time = []
            pars_json = json.loads(url)
            if url == url_171:
                stops = list(pars_json['directions'][0]['stops'])
            else:
                stops = list(pars_json['directions'][1]['stops'])

            for stop in range(len(stops)):
                name_stop = stops[stop]['zones'][0]['name']
                time_dict = stops[stop]['comings']
                for time in range(len(time_dict)):
                    save_stop_dict.setdefault(name_stop, [])
                    save_stop_dict[name_stop].append(time_dict[time]['time'])

            for stop in save_stop_dict:
                if stop == inlet:
                    for time in save_stop_dict[stop]:
                        if (datetime.strptime(time, '%Y-%m-%dT%H:%M:%S') - datetime.now()).days >= 0:
                            normal_time.append(datetime.strptime(time, '%Y-%m-%dT%H:%M:%S'))

            if normal_time == []:
                result += ''
            else:
                result += '✅'
                result += str('В ' + str(min(normal_time).time()) + ' сюда приедет автобус ' + name_bus[n])
                result += '\n'
        if result == '':
            result = '❌Похоже сегодня сюда уже никто не приедет......'
    except:
        result = 'Что-то пошло не так..... Тебе следует слушать мои просьбы, пока не я к тебе лично не приеду на 172э'
    return result

# реализация функции получения расписания на сегодняшний день с этого момента времени
def timetable_today(stop, line):
    try:
        list_bus = [url_170, url_171, url_172, url_173]
        result = '🗣В течение этого дня здесь будут такие автобусы:'
        result += '\n'*2
        for bus in list_bus:
            pars = json.loads(bus)
            if bus == url_171:
                if line == 'в город':
                    stops = pars['directions'][1]['stops']
                else:
                    stops = pars['directions'][0]['stops']
            else:
                if line == 'в город':
                    stops = pars['directions'][0]['stops']
                else:
                    stops = pars['directions'][1]['stops']
            list_time = []
            for n, i in enumerate(stops):
                name = stops[n]['zones'][0]['name']
                times = stops[n]['comings']
                if name == stop:
                    for m in range(len(times)):
                        time = times[m]['time']
                        now = datetime.now()
                        hour = now.hour
                        minutes = now.minute
                        sec = now.second
                        list_hour = int(time[11:13])
                        list_minutes = int(time[14:16])
                        list_sec = int(time[17:19])

                        all_sec_now = (hour*60*60) + (minutes*60) + sec
                        all_sec_list = (list_hour*60*60) + (list_minutes*60) + list_sec
                        if all_sec_list > all_sec_now:
                            list_time.append(time)
            if bus == url_170:
                name_bus = '170э'
            elif bus == url_171:
                name_bus = '171э'
            elif bus == url_172:
                name_bus = '172э'
            elif bus == url_173:
                name_bus = '173э'

            if list_time == []:
                result += 'Автобус ' + name_bus + ' сегодня здесь проезжать не будет'
                result += '\n'*2
            else:
                result += '🚎Aвтобус ' + name_bus + ':'
                result += '\n'
                for i in list_time:
                    result += '--> '
                    result += str(i[11:16])
                    result += '\n'
                result += '\n'
    except:
        result = 'Что-то пошло не так..... Тебе следует слушать мои просьбы, пока не я к тебе лично не приеду на 172э'
    return result

# реализация функции получения расписания на любой выбранный день
def timetable(stop, data, line):
    try:
        new_url_170 = requests.get('https://go2bus.ru/inforoutedetails?route=170%D1%8D&vt=b&date=' + data + '&srv=kem&lang=ru&timezone=0').content
        new_url_171 = requests.get('https://go2bus.ru/inforoutedetails?route=171%D1%8D&vt=b&date=' + data + '&srv=kem&lang=ru').content
        new_url_172 = requests.get('https://go2bus.ru/inforoutedetails?route=172%D1%8D&vt=b&date=' + data + '&srv=kem&lang=ru&timezone=0').content
        new_url_173 = requests.get('https://go2bus.ru/inforoutedetails?route=173%D1%8D&vt=b&date=' + data + '&srv=kem&lang=ru&timezone=0').content
        list_bus = [new_url_170, new_url_171, new_url_172, new_url_173]
        result = '🗣В течение твоего дня здесь будут такие автобусы:'
        result += '\n'
        for bus in list_bus:
            pars = json.loads(bus)
            if bus == new_url_171:
                if line == 'в город':
                    stops = pars['directions'][1]['stops']
                else:
                    stops = pars['directions'][0]['stops']
            else:
                if line == 'в город':
                    stops = pars['directions'][0]['stops']
                else:
                    stops = pars['directions'][1]['stops']
            list_time = []
            for n, i in enumerate(stops):
                name = stops[n]['zones'][0]['name']
                times = stops[n]['comings']
                if name == stop:
                    for m in range(len(times)):
                        time = times[m]['time']
                        list_time.append(time)
            if bus == new_url_170:
                name_bus = '170э'
            elif bus == new_url_171:
                name_bus = '171э'
            elif bus == new_url_172:
                name_bus = '172э'
            elif bus == new_url_173:
                name_bus = '173э'

            if list_time == []:
                result += '\n'
                result += '❌Автобус ' + name_bus + ' здесь проезжать не будет'
                result += '\n'
            else:
                result += '\n'
                result += '🚎Aвтобус ' + name_bus + ':'
                result += '\n'
                for i in list_time:
                    result += '--> '
                    result += str(i[11:16])
                    result += '\n'
    except Exception:
        result = 'Что-то пошло не так..... Тебе следует слушать мои просьбы, пока не я к тебе лично не приеду на 172э'
    return result

# функция для выборки всех остановок, через которые проезжают все автобусы (для отображения списка остановок в процессе выбора нужной остановки)
def create_all_stops():
    new_url_170 = json.loads(url_170)
    new_url_171 = json.loads(url_171)
    new_url_172 = json.loads(url_172)
    new_url_173 = json.loads(url_173)
    stops_170 = new_url_170['directions'][0]['stops']
    stops_171 = new_url_171['directions'][0]['stops']
    stops_172 = new_url_172['directions'][0]['stops']
    stops_173 = new_url_173['directions'][0]['stops']
    list_stops = []

    for n, i in enumerate(stops_170):
        list_stops.append(stops_170[n]['zones'][0]['name'])

    for n, i in enumerate(stops_171):
        stop = stops_171[n]['zones'][0]['name']
        c = 0
        for k in list_stops:
            if k == stop:
                c += 1
        if c == 0:
            list_stops.append(stop)

    for n, i in enumerate(stops_172):
        stop = stops_172[n]['zones'][0]['name']
        c = 0
        for k in list_stops:
            if k == stop:
                c += 1
        if c == 0:
            list_stops.append(stop)

    for n, i in enumerate(stops_173):
        stop = stops_173[n]['zones'][0]['name']
        c = 0
        for k in list_stops:
            if k == stop:
                c += 1
        if c == 0:
            list_stops.append(stop)
    return list_stops