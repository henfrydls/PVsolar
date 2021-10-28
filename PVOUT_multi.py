import urllib.request, urllib.parse, urllib.error
import ssl
import json
from bs4 import BeautifulSoup
from opencage.geocoder import OpenCageGeocode
from opencage.geocoder import InvalidInputError, RateLimitExceededError, UnknownError

class MTI:
    def __init__(self, location, module_wp, monthly_energy, ratio=1.25, percent=100):
        self.location = location
        self.module_wp = module_wp
        self.monthly_energy = monthly_energy
        self.ratio = ratio
        self.percent = percent/100
        self.key = '5bcb65fdf736480b8ac6a0baf16f0bec'
        self.geocoder = OpenCageGeocode(self.key)
        self.location_data, self.pv_data = {}, {}
        self.lat, self.long = map(float, self.location.split(","))

    def error_handling(self, name, target, results):
            try:
                self.location_data[name] = (results[0] ['components'][target])
            except KeyError:
                pass

    def location_name(self):
        while True:
            try:
                results = self.geocoder.reverse_geocode(self.lat, self.long, language='es', no_annotations='1')
                if results and len(results):
                    self.error_handling("Continent", 'continent', results)
                    self.error_handling("Country", 'country', results)
                    self.error_handling("State", 'state', results)
                    self.error_handling("County", 'county', results)
                    self.error_handling("Village", 'village', results)
                    self.error_handling("Town", 'town', results)
                    self.error_handling("Suburb", 'suburb', results)
                    self.error_handling("Hamlet", 'hamlet', results)
                    return(self.location_data)
            except RateLimitExceededError as ex:
                key = '08c837016a914d4a8b7db3f8d8ed1d90'
                continue
            except InvalidInputError as ex:
                return(None)

    def PVOUT_values(self):
            # Ignore SSL certificate errors
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            try:
                url = (f'https://api.globalsolaratlas.info/data/lta?loc={self.lat},{self.long}')
                html = urllib.request.urlopen(url, context=ctx).read()
            except:
                return(None)
            soup = BeautifulSoup(html, "html.parser")
            soup = json.loads(soup.text)["annual"]["data"]
            for key, value in soup.items():
                self.pv_data[key] = round(float(value), 2)
            modules = self.modules_needed()
            return(self.pv_data, modules)
        

    def modules_needed(self):
        modules = ((self.monthly_energy*self.ratio)/
    ((self.pv_data['GHI']/12)*(self.module_wp/1000)))*self.percent;
        return(round(modules))
