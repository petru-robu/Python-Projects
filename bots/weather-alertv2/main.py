import os, json, requests, time
import datetime as dt
import pyautogui as pt

TODAY = dt.datetime.today().date()
CITY = 'bucharest'
WHATSAPP_PATH =  "C:\\Users\\petru\\AppData\\Local\\WhatsApp\\WhatsApp.exe"

api_key = '602e20addbb81c5663dd395860b660eb'
forecast_request_url = f'https://api.openweathermap.org/data/2.5/forecast?q={CITY},ro&units=metric&appid={api_key}&lang=ro'
current_request_url = f'https://api.openweathermap.org/data/2.5/weather?q={CITY},ro&units=metric&appid={api_key}&lang=ro'


class Weather_data:
    def __init__(self):
        res = requests.get(forecast_request_url)
        self.forecast_data = json.loads(res.text)
        res = requests.get(current_request_url)
        self.curr_data = json.loads(res.text)

    def get_forecast_data(self):
        return self.forecast_data

    def get_current_data(self):
        return self.curr_data
    
    def forecast_info(self):
        ret = ""
        maxTemp, minTemp = 0, 99
        for d in self.forecast_data['list']:
            temp_dt = dt.datetime.fromtimestamp(d['dt'])
            weather_state = d['weather'][0]['main']
            weather_state_desc = d['weather'][0]['description']
            temp = d['main']['temp']
            
            if temp_dt.day == TODAY.day:
                maxTemp = max(maxTemp, temp)
                minTemp = min(minTemp, temp)
                ret += f"La ora {temp_dt} va fi: {weather_state}({weather_state_desc})\n"
                ret += f"Temperatura este: {temp}°C\n\n"
        ret += f"Maxima: {maxTemp}°C, Minima: {minTemp}°C"
        return ret
    
    def current_info(self):
        res =""
        temp_dt = dt.datetime.fromtimestamp(self.curr_data['dt'])
        temp = self.curr_data['main']['temp']
        weather_state = self.curr_data['weather'][0]['main']
        weather_state_desc = self.curr_data['weather'][0]['description']
        sunset  = dt.datetime.fromtimestamp(self.curr_data['sys']['sunset'])
        sunrise = dt.datetime.fromtimestamp(self.curr_data['sys']['sunrise'])

        res += f"Astazi este {temp_dt.date()}\n"
        res += f"La ora {temp_dt.time()} este: {weather_state}({weather_state_desc})\n"
        res += f"Temperatura este: {temp} °C\n"
        res += f"Sunrise: {sunrise.time()} | Sunset: {sunset.time()}"
        return res
    
class Spammer:
    def __init__(self):
        self.toSend = ""
        os.startfile(WHATSAPP_PATH)
        time.sleep(20)
        pt.moveTo(165, 274)
        pt.click()
        time.sleep(2)
        pt.moveTo(795, 966)
        time.sleep(5)
    
    def parse_for_whatsapp(self, text):
        res = "```"
        res += text
        res += "```"
        return res

    def load(self, text):
        text = self.parse_for_whatsapp(text)
        self.toSend = text

    def send(self):
        for line in self.toSend.splitlines():
            pt.typewrite(line)
            pt.hotkey('shift', 'enter')   
         
        pt.press("enter")

    def start(self):
        i = 0
        if pt.confirm("Incepe spamul? (5sec)") == "OK":
            i = 5
            while i:
                print(i)
                i-=1
                time.sleep(1)
            while True:
                self.send()

info = Weather_data()
print(info.current_info())

sp = Spammer()
sp.load(info.current_info())
sp.send()
