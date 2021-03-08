# In Search Of Lost Time - Code

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
