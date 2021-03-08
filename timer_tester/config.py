#!usr/bin/python3


from os import listdir


REPETITIONS = 1000

BASE_URL = 'http://localhost:8000'

URLS = {'hit_miss': BASE_URL + '/hit_miss',
        'distribution': BASE_URL + '/distribution',
        'rdtsc': BASE_URL + '/rdtsc',
        }

BROWSER_DIR = {'firefox' : './firefox/browsers/',
               'chrome' : './chrome/browsers/',
              }


RESULTS_DIR = {'firefox' : './firefox/results/',
               'chrome' : './chrome/results/',
              }

CSV_DIR = {'firefox' : './firefox/csv/',
               'chrome' : './chrome/csv/',
              }


DRIVER_DIR = {'chrome': './chrome/chromedrivers/'}

FIREFOX_DRIVER = './firefox/driver/'

SUPPORTED_BROWSERS = ['firefox','chrome','tor']

RDTSC_EXEC = {'firefox': '',
              'chrome': ''}

ALL_VERSIONS = {'firefox': [int(folder[-2:]) for folder in listdir(BROWSER_DIR['firefox'])],
                'chrome': [int(folder[-2:]) for folder in listdir(BROWSER_DIR['chrome'])]}

BINDINGS = {'48': '2.24', '49': '2.24', '50': '2.24', '51': '2.24', '52': '2.24', '53': '2.26', '54': '2.27', '55': '2.28', '56': '2.29', '57': '2.29', '58': '2.31', '59': '2.32', '60': '2.33', '61': '2.34', '62': '2.35', '63': '2.36', '64': '2.37', '65': '2.38', '66': '2.40', '67': '2.41', '68': '2.42', '69': '2.44', '70': '2.45', '71': '2.46', '72': '2.46', '73': '73.0.3683.68', '74': '74.0.3729.6', '75': '75.0.3770.140', '76': '76.0.3809.126', '77': '77.0.3865.40', '78': '78.0.3904.105', '79': '79.0.3945.36', '80': '80.0.3987.106', '81': '81.0.4044.138', '83': '83.0.4103.39', '84': '84.0.4147.30', '85': '85.0.4183.87', '86': '86.0.4240.22', 'rdtsc':'84.0.4147.30'}

BUGGY = {'chrome' : [61,65,66,67,68,72,73,77]}
