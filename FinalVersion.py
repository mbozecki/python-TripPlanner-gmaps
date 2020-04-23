from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'fullscreen', '0')
Config.set('graphics', 'width', '648')
Config.set('graphics', 'height', '1152')
Config.write()
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.core.text import FontContextManager as FCM
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button  # przyciski
from kivy.uix.image import Image
from kivy.graphics import *
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
import gmaps
import googlemaps
import sys
import datetime
from datetime import timedelta
import requests

gmaps.configure(api_key="AIzaSyCANn6wVutvF2Ul8CJoTCTa4oIWMMDm2DM")
GoogleMaps=googlemaps.Client(key="AIzaSyCANn6wVutvF2Ul8CJoTCTa4oIWMMDm2DM") #dla skrócenia komend

class LoginScreen(FloatLayout):  # ekran nr 1

    def __init__(self, **var_args):

        super(LoginScreen, self).__init__(**var_args)
        now = datetime.datetime.now()
        hour = str(now.hour)
        if hour == "0":
            hour = "00"
        minuta = str(now.minute)

        #tlo
        self.tlo = Image(source='Tloo1.png')
        self.tlo.opacity = 0.75
        self.tlo.size_hint_x = 1
        self.tlo.size_hint_y = 1
        self.tlo.pos_hint = {"x": 0, "top": 1}
        self.add_widget(self.tlo)

        self.skad = TextInput(multiline=False, size_hint=(0.45, 0.1), font_size=20, pos_hint={"x": 0.28, "top": 0.7},
                              text='            Skąd wychodzisz?')
        self.add_widget(self.skad)

        self.dokad = TextInput(multiline=False, size_hint=(0.45, 0.1), font_size=20, pos_hint={"x": 0.28, "top": 0.5},
                               text='       Dokąd chcesz dojechać?')
        self.add_widget(self.dokad)

        self.godzina = TextInput(multiline=False, size_hint=(0.05, 0.04), font_size=15, pos_hint={"x": 0.4, "top": 0.3},
                              text=hour)

        self.minuta = TextInput(multiline=False, size_hint=(0.05, 0.04), font_size=15, pos_hint={"x": 0.5, "top": 0.3},
                                 text=minuta)
        self.add_widget(self.godzina)
        self.add_widget(self.minuta)

        przycisk = Button(text='Wyszukaj!')
        przycisk.bind(on_press=self.clkfunc)
        przycisk.opacity = 0.9
        self.add_widget(przycisk)


        # logo na gorze
        self.img = Image(source='2019.png')
        self.img.opacity = 0.9
        self.img.size_hint_x = 1
        self.img.size_hint_y = 0.26
        self.img.pos_hint = {"x": 0, "top": 0.98}
        self.add_widget(self.img)

        # obrazek skad
        self.img1 = Image(source='skad2.png')
        self.img1.opacity = 0.9
        self.img1.size_hint_x = 0.1
        self.img1.size_hint_y = 0.05
        self.img1.pos_hint = {"x": 0.18, "top": 0.7}
        self.add_widget(self.img1)

        # obrazek dokad
        self.img2 = Image(source='skad3.png')
        self.img2.opacity = 0.9
        self.img2.size_hint_x = 0.1
        self.img2.size_hint_y = 0.05
        self.img2.pos_hint = {"x": 0.18, "top": 0.5}
        self.add_widget(self.img2)


        # obrazek zegara
        self.img3 = Image(source='clocku.png')
        self.img3.opacity = 0.9
        self.img3.size_hint_x = 0.1
        self.img3.size_hint_y = 0.05
        self.img3.pos_hint = {"x": 0.18, "top": 0.31}
        self.add_widget(self.img3)





    def clkfunc(self, event): # przycisk ktory odpowiada za zebranie danych + nowy ekran

        adres1 = self.skad.text + "Łódź"
        adres2 = self.dokad.text+ "Łódź"

        now=datetime.datetime.now()
        now-= timedelta(hours=(now.hour),minutes=now.minute)
        now+= timedelta(hours=int(self.godzina.text),minutes=int(self.minuta.text))

        #adres1 = "Piotrkowska cetnurm łódź"
        #adres2 = "Mikołaja Kopernika 76/78"

        self.clear_widgets()

        while True:
            try:
                geocode1 = GoogleMaps.geocode(adres1)
                geocode2 = GoogleMaps.geocode(adres2)
                for x, y in geocode1[0].items():  # wyciganiecie szerokosci geograf z pierwszej lokalizacji
                    if (x == "geometry"):
                        for i, j in y.items():
                            if (i == "location"):
                                lat1 = list(j.values())[0]
                                lng1 = list(j.values())[1]
                                lokacja1 = []
                                lokacja1.append(lat1)
                                lokacja1.append(lng1)

                for xx, yy in geocode2[0].items():  # wyciganiecie szerokosci geograf z 2 lokalizacji
                    if (xx == "geometry"):
                        for ii, jj in yy.items():
                            if (ii == "location"):
                                lat2 = list(jj.values())[0]
                                lng2 = list(jj.values())[1]
                                lokacja2 = []
                                lokacja2.append(lat2)
                                lokacja2.append(lng2)
                break
            except:
                print("Błedne lokacje lub brak przejazdów")
                sys.exit()

        POMIN = False
        przesiadka = False
        wskazowki = (GoogleMaps.directions(lokacja1, lokacja2, mode="transit", departure_time=now))
        direkcje = (GoogleMaps.distance_matrix(adres1, adres2, mode='transit'))

        odlegloscD = (direkcje['rows'][0]['elements'][0]['distance']['text'])  # odleglosc całej drogi od A do B
        czasD = (direkcje['rows'][0]['elements'][0]['duration']['text'])

        if 'Walk' in (wskazowki[0]['legs'][0]['steps'][0]['html_instructions']) and len(wskazowki[0]['legs'][0]['steps'])<2:
            POMIN = True
        try:
            nazwatramwaju = (wskazowki[0]['legs'][0]['steps'][0]['transit_details']['headsign'])
            nrtramwaju = (wskazowki[0]['legs'][0]['steps'][0]['transit_details']['line']['short_name'])
            godzinawyjazdutram = (wskazowki[0]['legs'][0]['steps'][0]['transit_details']['departure_time']['text'])
            godzinadojazdu = (wskazowki[0]['legs'][0]['steps'][0]['transit_details']['arrival_time']['text'])
            gdziewsiadasz = (wskazowki[0]['legs'][0]['steps'][0]['transit_details']['departure_stop']['name'])
            lprzystankow = (wskazowki[0]['legs'][0]['steps'][0]['transit_details']['num_stops'])
        except:
            try:
                nazwatramwaju = (wskazowki[0]['legs'][0]['steps'][1]['transit_details']['headsign'])
                lprzystankow = (wskazowki[0]['legs'][0]['steps'][1]['transit_details']['num_stops'])
                nrtramwaju = (wskazowki[0]['legs'][0]['steps'][1]['transit_details']['line']['short_name'])
                godzinawyjazdutram = (wskazowki[0]['legs'][0]['steps'][1]['transit_details']['departure_time']['text'])
                godzinadojazdu = (wskazowki[0]['legs'][0]['steps'][1]['transit_details']['arrival_time']['text'])
                gdziewsiadasz = (wskazowki[0]['legs'][0]['steps'][1]['transit_details']['departure_stop']['name'])
            except:
                lprzystankow = ""
                nrtramwaju = ""
                godzinawyjazdutram = ""
                godzinadojazdu = ""
                gdziewsiadasz = ""
                nazwatramwaju = ""

        try:
            nazwatramwaju2 = (wskazowki[0]['legs'][0]['steps'][2]['transit_details']['headsign'])
            nrtramwaju2 = (wskazowki[0]['legs'][0]['steps'][2]['transit_details']['line']['short_name'])
            lprzystankow2 = (wskazowki[0]['legs'][0]['steps'][2]['transit_details']['num_stops'])
            godzinawyjazdutram2 = (wskazowki[0]['legs'][0]['steps'][2]['transit_details']['departure_time']['text'])
            godzinadojazdu2 = (wskazowki[0]['legs'][0]['steps'][2]['transit_details']['arrival_time']['text'])
            gdziewsiadasz2 = (wskazowki[0]['legs'][0]['steps'][2]['transit_details']['departure_stop']['name'])
        except:
            try:
                gdziewsiadasz2 = (wskazowki[0]['legs'][0]['steps'][3]['transit_details']['departure_stop']['name'])
                godzinadojazdu2 = (wskazowki[0]['legs'][0]['steps'][3]['transit_details']['arrival_time']['text'])
                godzinawyjazdutram2 = (wskazowki[0]['legs'][0]['steps'][3]['transit_details']['departure_time']['text'])
                lprzystankow2 = (wskazowki[0]['legs'][0]['steps'][3]['transit_details']['num_stops'])
                nrtramwaju2 = (wskazowki[0]['legs'][0]['steps'][3]['transit_details']['line']['short_name'])
                nazwatramwaju2 = (wskazowki[0]['legs'][0]['steps'][3]['transit_details']['headsign'])
            except:
                nazwatramwaju2 = ""
                nrtramwaju2 = ""
                lprzystankow2 = ""
                godzinawyjazdutram2 = ""
                godzinadojazdu2 = ""
                gdziewsiadasz2 = ""

        if not POMIN:

            if nazwatramwaju2!="":
                droga=(
                    "\nWyjazd: " + godzinawyjazdutram + "\nze stacji: \n"+gdziewsiadasz2+ "\n\nWsiądź do: \n     [" + str(
                        nrtramwaju) + "] " + str(nazwatramwaju) + "\nPrzejedź " + str(
                        lprzystankow)+ " przystanków " + "\n\nWsiądź do: \n     [" + str(
                        nrtramwaju2) + "] " + str(nazwatramwaju2) + "\nPrzejedź " + str(
                        lprzystankow2)+  "przystanków\n\n\nOdległość: " + odlegloscD)
            else:
                droga=("\nWyjazd: " + godzinawyjazdutram + "\nze stacji: \n"+gdziewsiadasz+ "\nWsiądź do: [" +str(nrtramwaju) +"] "+ str(
                    nazwatramwaju) + "\nLiczba przystanków: " + str(lprzystankow)+"\nOdległość: " + odlegloscD  +"\nDojedziesz o: " +godzinadojazdu)

        else:

            if (len(wskazowki[0]['legs'][0]['steps'])) == 1 and godzinawyjazdutram!="" :
                droga=("\nWyjazd o:\n" + godzinawyjazdutram + "\n\n" + wskazowki[0]['legs'][0]['steps'][0][
                'html_instructions'] + "\nNazwa tramwaju:\n" + str(nazwatramwaju) + "\nNr: " + str(nrtramwaju))

            elif (len(wskazowki[0]['legs'][0]['steps'])) == 2:
                droga=(wskazowki[0]['legs'][0]['steps'][0][
                'html_instructions'] + "\nWyjedź o: " + godzinawyjazdutram + "\nOdległoość: " + odlegloscD + "\nCzas: " + czasD + "\nNazwa pierwszego tramwaju: " + str(
                nazwatramwaju) + "\nNr: " + str(nrtramwaju) + "\nLiczba przystanków: " + str(
                lprzystankow) + "\nNazwa drugiego tramwaju: " + str(nazwatramwaju2) + " Nr: " + str(
                nrtramwaju2) + "\nLiczba przystanków: " + str(lprzystankow2))
            else:
                droga=("Przejdź się!\n"+wskazowki[0]['legs'][0]['steps'][0]['html_instructions'])



        self.add_widget(Button(text=droga,pos_hint = {"x": 0, "top": 1},size_hint=(1.1, 1)))
        self.tlo = Image(source='Tloo1.png')
        self.tlo.opacity = 0.2
        self.tlo.size_hint_x = 1
        self.tlo.size_hint_y = 1
        self.tlo.pos_hint = {"x": 0, "top": 1}
        self.add_widget(self.tlo)

        self.canvas.add(Color(72/255, 19/255, 91/255))
        self.canvas.add(Rectangle(pos=(0, 730), size=(1000, 130)))

        print(len(wskazowki[0]['legs'][0]['steps']))

        self.two = Image(source='twopts.png')
        self.two.opacity = 0.9
        self.two.size_hint_x = 0.2
        self.two.size_hint_y = 0.1
        self.two.pos_hint = {"x": 0.4, "top": 0.98}
        self.add_widget(self.two)
        #user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        #map.map_source = source
        #MapView().map_source = "osm"
        #mapview = MapView(zoom=11, lat=50.6394, lon=3.057)
        #self.add_widget(mapview)

class MyApi(App):
    def build(self):
        self.title = 'Trip Planner- Mikolaj Bozecki'
        return LoginScreen()


if __name__ == '__main__':
    MyApi().run()
