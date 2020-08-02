class PreText:
    TITLE = r'''
   _____           _     _ ____        _   
  / ____|         (_)   | |  _ \      | |  
 | |     _____   ___  __| | |_) | ___ | |_ 
 | |    / _ \ \ / / |/ _` |  _ < / _ \| __|
 | |___| (_) \ V /| | (_| | |_) | (_) | |_ 
  \_____\___/ \_/ |_|\__,_|____/ \___/ \__|
'''

    MENU = '''
    1) Run default mode
    2) Search by country
    3) Headless option

    If you're having a hard time with the options, just write 'help'
    If you wanna exit, just write 'exit'
    '''

    HELP = '''
    Default mode -> The tracker'll run with the standard configuration:
                    * Return the global situation;
                    * Top 5 countries.

    Search by country -> The tracker'll run the optimized configuration:
                         * Return the specific country.
    
    Headless option -> Headless is a mode that the browser will be hidden or not.
                       If you active the headless mode you'll not see the browser running, otherwise you will.
    '''

    COUNTRIES_MENU = '''
    Select one of the countries below:

    1) Brasil
    2) USA
    3) China
    4) Russia
    5) Italy
    6) India
    7) Canada
    8) Portugal
    9) Australia
    10) UK

    If you wanna exit, just write 'exit'
    '''

    HEADLESS_MENU = '''
    Headless mode?
    
    1) Yes
    2) No
    
    If you wanna exit, just write 'exit'
    '''

    ERROR_MESSAGE = '''
    Error: Parameter not found. Please check the input.
    '''
