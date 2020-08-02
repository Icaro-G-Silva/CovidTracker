from CovidTracker import CovidTracker
from PreText import PreText

class interface:
    def __init__(self, headless = False):
        self.headless = headless
        self.headlessMenu = PreText.HEADLESS_MENU
        self.title = PreText.TITLE
        self.menuBot = PreText.MENU
        self.help = PreText.HELP
        self.countriesMenu = PreText.COUNTRIES_MENU
        self.error = PreText.ERROR_MESSAGE
    
    def run(self, url = None):
        try:
            if url == None:
                self.tracker = CovidTracker(self.headless)
            else:
                self.tracker = CovidTracker(self.headless, url)
            self.tracker.fetch()
        except Exception as error:
            print(f'An error has been ocurred -> {error}')
        finally:
            self.tracker.getOffline()
    
    def menu(self):
        choosing = True
        while choosing:
            print(self.title)
            print(self.menuBot)
            option = input('->').strip().lower()
            if option == '1':
                choosing = False
                self.run()
            elif option == '2':
                baseURL = 'https://covid19.who.int/region/'
                choosingCountry = True
                while choosingCountry:
                    print(self.countriesMenu)
                    option = input('->').strip().lower()
                    if option == '1': self.run(baseURL + 'amro/country/br')
                    elif option == '2': self.run(baseURL + 'amro/country/us')
                    elif option == '3': self.run(baseURL + 'wpro/country/cn')
                    elif option == '4': self.run(baseURL + 'euro/country/ru')
                    elif option == '5': self.run(baseURL + 'euro/country/it')
                    elif option == '6': self.run(baseURL + 'searo/country/in')
                    elif option == '7': self.run(baseURL + 'amro/country/ca')
                    elif option == '8': self.run(baseURL + 'euro/country/pt')
                    elif option == '9': self.run(baseURL + 'wpro/country/au')
                    elif option == '10': self.run(baseURL + 'euro/country/gb')
                    elif option == 'exit':
                        choosingCountry = False
                        continue
                    else:
                        print(self.error)
                        continue
                    choosingCountry = False
                    choosing = False
            elif option == '3':
                choosingHead = True
                while choosingHead:
                    print(self.headlessMenu)
                    option = input('->').strip().lower()
                    if option == '1':
                        self.headless = True
                        print('headless mode activated')
                    elif option == '2':
                        self.headless = False
                        print('headless mode disabled')
                    elif option == 'exit':
                        choosingHead = False
                        continue
                    else:
                        print(self.error)
                        continue
                    choosingHead = False
            elif option == 'help':
                print(self.help)
                continue
            elif option == 'exit':
                choosing = False
                continue
            else:
                print(self.error)
                continue
        print('All Done!')
