# In Search Of Lost Time : Timer Tester


## Requirements
To install needed libraries, please run:
```Bash
pip3 install -r requirements.txt
```


To retrieve client-side results, we use Selenium WebDriver to automate the use of browsers. Selenium requires to have a webdriver for each type of browsers. For Chrome, as a driver generally works for only one browser, a file allowing to download drivers for available versions is given in /chrome. However, we let the user download the GeckoDriver (for Firefox) [here](https://github.com/mozilla/geckodriver/releases/tag/v0.29.0) and set it in the path.

You also need to run the local server to run client-side experiments.
To see more information on that, please see the server folder.
_____
## Step by step
The following section describe a quickstart guide to use our code.
For more detailed instructions on all modules, such as arguments description, please refer to next section.

### Download browsers.
The first step to test browsers is to download them. `./chome` and `./firefox` contain scripts allowing to download and extract recent versions of browsers for linux 64 bits. The extracted browsers will be placed in `browsers` folders.


#### Firefox
To download versions of firefox, you can run `./firefox/ff_downloader.py`.
Running the following command will download and extract all versions of firefox for linux 64 bits starting from 57:

```Bash
cd firefox
python3 ff_downloader.py
```

We only download versions starting from 57 as previous versions require another version of the GeckoDriver.

To download only a specific version of Firefox for quick tests, you can run the following commands:

```Bash
cd firefox
python3 ff_downloader.py -v $your_version
```

The browsers will be extracted in the `./firefox/browsers`, under the naming convention `firefox-version`. The executable file for the browser is set at `./firefox/browsers/firefox-version/firefox`.

The downloader automatically removes the uploader, however you may still need to change settings at the first start - otherwise the browser may automatically updates to the latest version.
If you wish to use the browser by hand, you can directly run the executable.
You may have to close other firefox processes, or run it with a different user.


#### Chrome

##### Browsers
We have not found an official release channel for Chrome releases.
Instead, we download from [here](https://www.slimjet.com/chrome/google-chrome-old-version.php). All the versions are not available, and some do not run on our system.

To download available versions (mainly versions 48-latest), you can run the following commands:
```Bash
cd chrome
python3 chrome_downloader.py
```

The browsers will be extracted in the `./chrome/browsers`, under the naming convention `chrome-version`. The executable file for the browser is set at `./chrome/browsers/chrome-version/opt/google/chrome/google-chrome`.

The downloader automatically removes the uploader, however you may still need to change settings at the first start - otherwise the browser may automatically updates to the latest version.
If you wish to use the browser by hand, you can directly run the executable.
You may have to close other Chrome processes.

##### ChromeDrivers
As opposed to GeckoDrivers, ChromeDrivers only often works with one or two Chrome versions.
We logically need to download all the ChromeDrivers required to use our browsers with Selenium.
To do so, run the following commands:

```Bash
cd chrome
python3 download_drivers.py
```

The script downloads all required ChromeDrivers in the `./chrome/chromedrivers` folder.
To know which ChromeDriver is associated with which Chrome version, we use the `./chrome/bindings.json`.
The bindings currently only is described until version 86, and new versions must be added by hand.

### Get results.

This section presents the Selenium scripts.
They use the local server to run client-side JavaScript experiments and write results.
The results returned by these scripts are used in our paper.

The different tests are:
- `SharedArrayBuffer` availablity.
- Cache Hit/Miss timings (with various clocks).
- Distribution on the number of incrementation in a performance.now period.
- Measurements using `performance.rdtsc`. This requires a custom version of browsers where `performance.rdtsc` is defined, and add the executable path to `config.py`. Please see the rdtsc folder for more information.

The results are stored in the results folder of the associated browser.
It is important to note that you need to have previously downloaded browsers in order to run these tests.
You must also have started the local server.

#### Firefox
`ff_tester.py` contains all the scripts to run client-side tests for firefox.

To run non-rdtsc experiments on all available versions _without_ COOP/COEP, run the following command:

```Bash
python3 ff_tester.py
```

If you wish to test with COOP/COEP enabled, you can add the `-c` flag:

```Bash
python3 ff_tester.py -c
```

If you wish to test for a single version, you can use the `-v` parameter:

```Bash
python3 ff_tester.py -v $your_version
```

To run experiments with `performance.rdtsc`, you must first have a custom version of Firefox.
You need to add the executable path in `config.py` in the RDTSC_EXEC dict.
If you wish to run rdtsc tests, you can add the `--rdtsc` flag:

```Bash
python3 ff_tester.py --rdtsc
```

If you wish to run only certain non-rdtsc experiments, you can use one of the following flags:

```Bash
python3 ff_tester.py --sab --distribution --hit_miss
```

For more detail on this module, refer to the argument list [here](#ff_tester)


#### Chrome

`chrome_tester.py` contains all the scripts to run client-side tests for chrome.

To run non-rdtsc experiments on all available versions _without_ COOP/COEP, run the following command:

```Bash
python3 chrome_tester.py
```

If you wish to test with COOP/COEP enabled, you can add the `-c` flag:

```Bash
python3 chrome_tester.py -c
```

If you wish to test for a single version, you can use the `-v` parameter:

```Bash
python3 chrome_tester.py -v $your_version
```

To run experiments with `performance.rdtsc`, you must first have a custom version of Chromium.
You need to add the executable path in `config.py` in the RDTSC_EXEC dict.
If you wish to run rdtsc tests, you can add the `--rdtsc` flag:

```Bash
python3 chrome_tester.py --rdtsc
```

If you wish to run only certain non-rdtsc experiments, you can use one of the following flags:

```Bash
python3 chrome_tester.py --sab --distribution --hit_miss
```

The results are stored in the `chrome/results/` folder. A json file by version is created, and results are added to that file. This means that different experiments on the same version write to the same file. This allow a user to split long computations in shorter experiments.
For more detail on this module, refer to the argument list [here](#chrome_tester)


### Plot / Further analysis

Once you have run the experiments, results are stored as json files in the appropriate folders.
This section offer a few tools in order to analyze these results.
These tests run the same for Chrome and Firefox.

#### Hit/Miss histogram
A powerful metric to check the efficiency of a timer on cache attacks is to plot the timings of hits and timings of misses.
To do so, we use the result from the hit-miss test on the local server and create a histogram.

To directly plot the histogram, run :

```Bash
python3 hit_miss.py --plot -b $your_browser -v $your_version --clock $your_clock
```

The clock parameter can be either `SharedArrayBuffer` or `performance.now` for interpolation.
You can add the `-c` flag to plot the same histogram for results with COOP/COEP set.
You can adjust the parameters of the histogram using the `--min, --max, --step` flags.

A timer is efficient when the two distributions are clearly separated.
Typically, a cache miss being slower than a cache hit, the miss distribution is situated to the right of the histogram.
However, as `performance.now` interpolation measures the time between the end of the operation and the end of the clock period, a slower operation will have a shorter interpolated time.
This means that for interpolated clock, misses must be on the left side of the graph.


#### Error rate and repetitions
To minimize the effect of the jitter, an attacker can repeat the experiments.
As the jitter is often a triangle distribution, with the middle value being the real value, an attacker can retrieve more information on the real timing by averaging timings from various measurements.


We define the error rate as the average of false hits (misses evaluated as hits) and false misses (hits evaluated as misses).
In a real world scenario, where the attacker does not know whether an access is a hit or a miss, the error rate would be the proportion of false guesses.

The `error_rate_repetitions.py` module allow the user to see the impact of repetitions on the cache hit/miss exercise.
By using hit/miss timings computed before, we can evaluate this error rate.
In particular, to show the impact of repetitions on the efficiency of jitter, we plot the evolution of the cache error rate when we increase the number of repetitions by running the following command:

```Bash
python3 error_rate_repetitions.py --plot -b $your_browser -v $your_version --clock $your_clock
```

The clock parameter can be either `SharedArrayBuffer` or `performance.now` for interpolation.
You can add the `-c` flag to plot the same histogram for results with COOP/COEP set.

#### Evolution of resolution and jitter
This module plots the evolution of the number of ticks in a clock period for all available versions.
This allows to illustrate the evolution of resolution/jitter through time.
You must have run the distribution tests before, for all versions you wish to evaluate.

You can plot the graph with:
```Bash
python3 jitter_boxplot.py -b $your_browser
```

You can plot the graph for browsers with COOP/COEP enabled by adding the `-c` flag.
_____

## More details on modules.


### ff_downloader.py


| short  | long    | help                  | values | default |
| :----: |:-------:| :--------------------:|:------:| :-----: |
| -d     | --debug | Activate debug prints |    -   | False   |
| -v     | --version | Set this if you need a single version. |    int>57   | all versions from 57 to latest   |
| -z     | --zips | Keep compressed browser files |    -   | False   |




### ff_tester.py
<a name="ff_tester"></a>
If no specific tests are set, default will run SharedArrayBuffer availablity, distribution of incrementation per clock period of performance.now and hit/miss tests for SharedArrayBuffer and performance.now interpolation.

As rdtsc requires a specific browser, it is not possible to run it with other tests.
Calling --rdtsc flag will disable the other tests.


| short  | long    | help                  | values | default |
| :----: |:-------:| :--------------------:|:------:| :-----: |
| -v     | --version | Use a specific version, that must be in firefox/browsers | int | all versions in firefox/browsers |
| -r     | --repetitions | Number of measurements for hit/miss, distribution and rdtsc. | int | 1000 |
| -c     | --coop | Enables COOP and COEP. | - | False |
| -     | --sab | Run the availablity tests for SharedArrayBuffer | - | False |
| -     | --distribution | Evaluates the number of incrementation per clock period. | - | False |
| -     | --hit_miss | Evaluates timings for cache hits and misses. This can take a while. | - | False |
| -     | --rdtsc | Run performance.rdtsc tests. You need to set the path of you custom firefox in the config file. | - | False |



### chrome_tester.py
<a name="chrome_tester"></a>

If no specific tests are set, default will run `SharedArrayBuffer` availablity, distribution of incrementation per clock period of performance.now and hit/miss tests for `SharedArrayBuffer` and performance.now interpolation.

As `performance.rdtsc` requires a specific browser (here chromium), it is not possible to run it with other tests.
Calling --rdtsc flag will disable the other tests.





| short  | long    | help                  | values | default |
| :----: |:-------:| :--------------------:|:------:| :-----: |
| -v     | --version | Use a specific version, that must be in chrome/browsers. Some versions do not work, need to figure out why. | int | all versions in chrome/browsers |
| -r     | --repetitions | Number of measurements for hit/miss, distribution and rdtsc. | int | 1000 |
| -c     | --coop | Enables COOP and COEP. | - | False |
| -     | --sab | Run the availablity tests for SharedArrayBuffer | - | False |
| -     | --distribution | Evaluates the number of incrementation per clock period. | - | False |
| -     | --hit_miss | Evaluates timings for cache hits and misses. This can take a while. | - | False |
| -     | --rdtsc | Run performance.rdtsc tests. You need to set the path of you custom firefox in the config file. | - | False |

### hit_miss.py

| short  | long    | help                  | values | default |
| :----: |:-------:| :--------------------:|:------:| :-----: |
| -b | --browser | Use a specific browser. | firefox or chrome | firefox |
| -v | --version | Use a specific version | int | 81 |
| - | --clock | Use a specific clock method | SharedArrayBuffer of performance.now | performance.now |
| -c     | --coop | Use results with COOP and COEP. | - | False |
| -p | --plot | Plot hit/miss histogram | - | False |
| - | --csv | Create csv file containing the histogram (for latex or others) | - | False |
| - | --step |Bin size of the histogram | int | 1 |
| - | --min | Min value of the histogram | int | 0 |
| - | --max | Max value of the histogram | int | max timing |


### get_error_repetition.py

| short  | long    | help                  | values | default |
| :----: |:-------:| :--------------------:|:------:| :-----: |
| -b | --browser | Use a specific browser. | firefox or chrome | firefox |
| -v | --version | Use a specific version | int | 81 |
| - | --clock | Use a specific clock method | SharedArrayBuffer of performance.now | performance.now |
| -c     | --coop | Use results with COOP and COEP. | - | False |
| -p | --plot | Plot error rate repetitions graph | - | False |
| - | --csv | Create csv file containing the error rate for different repetitions (for latex or others) | - | False |

### jitter_boxplot.py
| short  | long    | help                  | values | default |
| :----: |:-------:| :--------------------:|:------:| :-----: |
| -b     | --browser | Use a specific browser. | firefox or chrome | firefox |
| -c     | --coop | Use results with COOP and COEP. | - | False |
