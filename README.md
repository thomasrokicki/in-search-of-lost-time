# In Search Of Lost Time - Code

## Project description

This repository contains all code associated with the paper : _SoK: In Search of Lost Time: A Review of JavaScript Timers_, as well as data used in the paper.

The code is composed of several components:

- `server/`: The code for a local Django server. It is used to run client-side experiments in JavaScript. You can find more info on how to run it in the [server's README](server/README.md)

- `timer_tester`: This folder contains all python code used in our experiments, mainly :
  - Tools to download all required versions of browsers.
  - Scripts using Selenium WebDriver used to automate tests on all browsers.
  - Scripts to parse raw data, plot graphs and export csv files.

  You can find more info on how to run it in the [timer_tester's README](timer_tester/README.md)

- `rdtsc`: In order to evaluate timers' resolution and measurement overhead with precision, we built custom versions of Firefox and Chromium containing `performance.rdtsc`, a method calling the native `RDTSC` instruction to retrieve a high resolution timer. This directory contains patches to apply the changes to the source code of both browsers. You can find more info in [RDTSC's README](rdtsc/README.md). You can also find pre-built versions of Chromium 81 and Firefox 84 for Linux-x86_64 [here](https://github.com/thomasrokicki/in-search-of-lost-time/releases/tag/1.0)

- `data`: All the csv files used in the paper for results and graphs. These files were generated using the code in this repository.


## Quickstart

To run the code, you must first run the local server. To do so, you need Docker on your system. Please run:

```Bash
cd server/
docker-compose up
```
Depending on your docker installation, you might need to run it with sudo. If the docker daemon is not running, you can start it with ``` systemctl start docker ```
More details on the server can be found [here](server/README.md).

From now on, you can either access the server directly with your browser at http://localhost:8000 or you can use automated tests.

To run automated tests, you must first install requirements with
```Bash
cd timer_tester
pip3 install -r requirements.txt
```

To run tests on Firefox, you must also download GeckoDriver [here](https://github.com/mozilla/geckodriver/releases/tag/v0.29.0) and set it in your path.

You can then download different browser versions. To download all available versions on both Firefox and Chrome you can run:

```Bash
cd firefox
python3 ff_downloader.py

cd ../chrome
python3 chrome_downloader.py
python3 download_drivers.py # As ChromeDrivers work only for a few versions, we must download them automatically.
```
The downloaded versions are now set in the `browser` folders. You can also use the downloaders to download only specific versions.

Next, you can run tests with Selenium. For instance, to run all tests on all available Firefox browsers, you can run

```Bash
python3 ff_tester.py
```

In a similar way, to test in Chrome you can run
```Bash
python3 chrome_tester.py
```

More information on tests can be found [here](timer_tester/README.md)

Finally, after computing the raw data, you can use scripts to plot graphs used in the paper.

```Bash
# Plots the hit/miss histogram for a certain version of a browser.
python3 hit_miss.py --plot -b $your_browser -v $your_version --clock performance.now()

# Plots the evolution of the error rate in function of repetitions
python3 error_rate_repetitions.py --plot -b $your_browser -v $your_version --clock performance.now

# Plots the evolution of the number of ticks in a clock period - This shows the changes on jitter and resolution.
python3 jitter_boxplot.py -b $your_browser


```
