from CovidTracker import CovidTracker

class interface:
    def __init__(self, headless = False):
        self.tracker = CovidTracker(headless)
    
    def run(self):
        try:
            self.tracker.fetch()
        except Exception as error:
            print(f'An error has been ocurred -> {error}')
        finally:
            self.tracker.getOffline()
