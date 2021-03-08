#!usr/bin/python3
'''This module contains most of the experiments related with Selenium on Chrome
It uses the local server to run JS experiments.
You must start the server before running tests. See the server folder for more instructions.
You must first download browsers (see ./chrome/chrome_downloader.py) and drivers (see ./chrome/download_drivers.py)

It can run the following tests :
    - Testing SharedArrayBuffer availablity.
    - Testing the number of incrementation in a clock period.
    - Retrieving timings for cache hits and misses.
    - Using RDTSC to evaluate timers.
'''
# Imports :
import json
from selenium import webdriver
from selenium.common.exceptions import JavascriptException, WebDriverException
from selenium.webdriver.chrome.options import Options
import subprocess
import os
import statistics
import sys
import argparse
# Locals:
import config
import utility


def get_driver(version):
    ''' Return the path to the chromedriver associated with the version number.
    You must first download browsers and drivers (see in ./chrome).

    Parameters:
    version(int): Tested version.

    Returns:
    String: The path to the driver.
    '''
    driver_version = config.BINDINGS[str(version)]
    return config.DRIVER_DIR['chrome'] + "chromedriver_" + driver_version + "/chromedriver"


def test_sab(version, coop = True):
    ''' Perform the availablity checks for SABs for a specific version.
    Then writes in a file results: availablity and is COOP/COEP enabled.

    Parameters:
    version(int): Tested version
    coop(bool): True to activate coop/coep, False otherwise.
    '''
    print('Testing the availability of SABS in a clock period on Chrome ' + str(version))
    if coop:
        print('COOP/COEP is on.')
    else:
        print('COOP/COEP is off.')
    options = Options()
    options.binary_location = config.BROWSER_DIR['chrome'] + "chrome-" +  str(version) + "/opt/google/chrome/google-chrome"
    driver_address = get_driver(version)
    with (webdriver.Chrome(driver_address, options = options)) as driver:
        if coop:
            driver.get(config.URLS['hit_miss'] + "?coop=True")
        else:
            driver.get(config.URLS['hit_miss'])
        try:
            sab_available = (driver.execute_script("""if (SharedArrayBuffer=='undefined'){return 'False'} else{return 'True'}"""))
        except Exception as e:
            sab_available = False
        driver.close();

    stats = {'name': 'SAB availablity',
             'sab_available': sab_available,
             'coop': coop,
             'version': version,
            }
    utility.write_results(stats, version, 'chrome')
    print('SABs available: ' + str(sab_available))
    print('Done')
    print()


def test_interpolation_distribution(version, coop = True, repetitions = config.REPETITIONS):
    ''' Test repeatedly the number of maximum incrementations in a clock edge.
    This gives indication of both resolution (average number of incrementations)
    and jitter (variance of the number of ticks).
    It also allows to plot the histogram of the distribution of the number of incrementations.
    Writes the result in the folder div.

    Parameters:
    version(int): Tested version
    coop(bool): True to activate coop/coep, False otherwise.
    repetitions(int): The number of measurements. Default is set in config file.
    '''
    print('Testing the number of ticks in a clock period on Chrome ' + str(version) + ", " + str(repetitions) + ' repetitions.')
    if coop:
        print('COOP/COEP is on.')
    else:
        print('COOP/COEP is off.')
    options = Options()
    options.binary_location = config.BROWSER_DIR['chrome'] + "chrome-" +  str(version) + "/opt/google/chrome/google-chrome"
    driver_address = get_driver(version)
    timings = {'Failed'}
    try:
        with (webdriver.Chrome(driver_address, options = options)) as driver:
            if coop:
                driver.get(config.URLS['distribution'] + "?coop=True")
            else:
                driver.get(config.URLS['distribution'])
            try:
                timings = driver.execute_script("return test_clock_edges(" + str(repetitions) + ")")
            except:
                print('Failed executing script.')
            driver.close();
    except Exception as e:
        print('Something went wrong when starting the browser.')
        print(e)
    if timings != {'Failed'}:
        stats = utility.get_stats(timings)
        stats['name'] = 'Tick distibution'
        stats['version'] = version
        stats['coop'] = coop
        utility.write_results(stats, version, 'chrome')
    else:
        print('Something went wrong.')
    print('Done')
    print()

def test_hits_misses(version, clock_method, coop = True, repetitions = config.REPETITIONS):
    ''' Compute the access time of cache hits and misses for a specific clock.
    This method can take a while to run, especially with a lot of repetitions or
    a huge cache.
    Also note that running computations on the side will create a lot of noise,
    as the cache is shared by all processes.
    Timing measured by this measurement can be used to determine error rate as
    well as the impact of repetitions

    Parameters:
    version(int): Tested version
    clock_method(string): Which clock to use. Can be 'SharedArrayBuffer' or 'performance.now'.
    coop(bool): True to activate coop/coep, False otherwise.
    repetitions(int): The number of measurements. Default is set in config file.
    '''
    print('Testing hits/misses on Chrome ' + str(version) + " with " + clock_method + ", " + str(repetitions) + ' repetitions.')
    if coop:
        print('COOP/COEP is on.')
    else:
        print('COOP/COEP is off.')
    options = Options()
    options.binary_location = config.BROWSER_DIR['chrome'] + "chrome-" +  str(version) + "/opt/google/chrome/google-chrome"
    driver_address = get_driver(version)
    timings = {'Failed'}
    results = {}
    with (webdriver.Chrome(driver_address, options = options)) as driver:
        if coop:
            driver.get(config.URLS['hit_miss'] + "?coop=True")
        else:
            driver.get(config.URLS['hit_miss'])
        try:
            driver.set_script_timeout(10000000000)
            results = driver.execute_script("return getHitMiss('" + clock_method + "'," +  str(repetitions) + ")") #This might fail if SABs are unavailable so we set a try
        except Exception as e: # This exception occurs when we try to access to SABs without coop/coep on later versions.
            print(e)
            print('SABs are not available here, skipping')
            return
        driver.close();

    if results == {}:
        print('Something went wrong, skipping')
        return

    stat_hits = utility.get_stats(results['hits'])
    stat_hits['name'] = 'hit/miss'
    stat_hits['clock_method'] = clock_method
    stat_hits['hit/miss'] = 'hits'
    stat_hits['version'] = version
    stat_hits['coop'] = coop
    utility.write_results(stat_hits, version, 'chrome')

    stat_misses = utility.get_stats(results['misses'])
    stat_misses['name'] = 'hit/miss'
    stat_misses['clock_method'] = clock_method
    stat_misses['hit/miss'] = 'misses'
    stat_misses['version'] = version
    stat_misses['coop'] = coop
    utility.write_results(stat_misses, version, 'chrome')
    print('Done')
    print()




#                                 RDTSC                                        #

def test_rdtsc(coop = True, repetitions = config.REPETITIONS):
    ''' Measure the execution time of our timers.
    This needs a custom version of Chromium where performance.rdtsc is implemented.
    Reference the executable in the config file.
    Writes the output in a different file than the other experiments.

    Parameters:
    coop(bool): True to activate coop/coep, False otherwise.
    repetitions(int): The number of measurements. Default is set in config file.
    '''
    print('Testing RDTSC')
    if not config.RDTSC_EXEC['chrome']:
        print('You have not defined the path to custom rdtsc Chrome.')
        print('Please set it up properly in the config file.')
        print('Also set the adequate binding to the chromedriver.')
        print('Skipping...')
        return
    results = {}
    options = Options()
    options.binary_location = config.RDTSC_EXEC['chrome']
    driver_address = get_driver('rdtsc')
    with (webdriver.Chrome(driver_address, options = options)) as driver:
        if coop:
            driver.get(config.URLS['rdtsc'] + "?coop=True")
        else:
            driver.get(config.URLS['rdtsc'])
        results = driver.execute_script("return getTimerMeasurements("+ str(repetitions) + ")")
        driver.close();
    results['name'] = 'rdtsc'
    results['coop'] = coop
    utility.write_results(results, 'rdtsc', 'chrome')
    print('Done')
    print()


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', help='Use a specific version. By default, runs all versions available. Some of them do not run.', type=int)
    parser.add_argument('-r', '--repetitions', help='Number of measurements for hit/miss, distribution and rdtsc.', type=int)
    parser.add_argument('-c', '--coop', help = 'Enables COOP and COEP. Default is off.', action='store_true',default=False)
    parser.add_argument('--sab', help='Run the availablity tests for SharedArrayBuffer.', action='store_true',default=False)
    parser.add_argument('--distribution', help='Evaluates the number of incrementation per clock period.', action='store_true',default=False)
    parser.add_argument('--hit_miss', help='Evalueate timings for cache hits and misses. This can take a while.', action='store_true',default=False)
    parser.add_argument('--rdtsc', help='Run performance.rdtsc tests. You need to set the path of you custom chrome in the config file.', action='store_true',default=False)

    #parser.add_argument('--clean', help='Delete former result files. Default is false')
    args = parser.parse_args()
    return args

def main(args):
    #clean = args.clean
    if args.repetitions:
        repetitions = args.repetitions
    else:
        print('You have not specified a number of repetitions. Using config.')
        repetitions = config.REPETITIONS
    print('Number of measurements : '+str(repetitions))

    if args.version:
        if args.version in config.ALL_VERSIONS['chrome'] and args.version not in config.BUGGY['chrome']:
            versions = [args.version]
        else:
            print('Only support versions later than 57')
            sys.exit(1)
    else:
        print('Running tests on all available versions.')
        versions = []
        for version in config.ALL_VERSIONS['chrome']:
            if version not in config.BUGGY['chrome']:
                versions.append(version)

    if args.coop:
        print('Using coop for tests.')
        coop = True
    else:
        print('Not using coop for tests.')
        coop = False

    if args.rdtsc:
        test_rdtsc(coop = coop, repetitions = repetitions) # Since rdtsc does not require a version, we treat it differently - you can't run rdtsc and the others in the same run.
        #TODO: Maybe improve the CLI.
    else:

        if ( not (args.sab) or (args.hit_miss=='False') or (args.distribution=='False')):
            print("You have not specified tests, running sab availability, distribution and hit_miss")
            for version in versions:
                print("Evaluating version " + str(version))
                test_sab(version, coop)
                test_interpolation_distribution(version, coop, repetitions)
                test_hits_misses(version, 'SharedArrayBuffer', coop , repetitions)
                test_hits_misses(version, 'performance.now', coop , repetitions)
        else:
            print(args)
            if args.sab:
                for version in versions:
                    test_sab(version, coop)
            if args.distribution:
                for version in versions:
                    test_interpolation_distribution(version, coop, repetitions)
            if args.hit_miss:
                for version in versions:
                    test_hits_misses(version, 'SharedArrayBuffer', coop , repetitions)
                    test_hits_misses(version, 'performance.now', coop , repetitions)

if __name__ == '__main__':
    if sys.version_info < (3, 0):
        sys.stdout.write("Sorry, requires Python 3.x, not Python 2.x\n")
        sys.exit(1)
    args = parse_arguments()
    main(args)
