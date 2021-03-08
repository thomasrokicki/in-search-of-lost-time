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

- `rdtsc`: In order to evaluate timers' resolution and measurement overhead with precision, we built custom versions of Firefox and Chromium containing `performance.rdtsc`, a method calling the native `RDTSC` instruction to retrieve a high resolution timer. This directory contains patches to apply the changes to the source code of both browsers. You can find more info in [RDTSC's README](rdtsc/README.md)

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
```
The downloaded versions are now set in the `browser` folders.

Next, you can run tests with Selenium. For instance, to test timers on all available Firefox browsers and visualize the jitter's evolution, you can run

```Bash
python3 ff_tester.py --distribution
python3 jitter_boxplot -b firefox
```

More information on tests and plots can be found [here](timer_tester/README.md)
