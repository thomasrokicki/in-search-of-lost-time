# In Search Of Lost Time : Local Server

This folder contains the code used for client side experiments of the paper.
It is initially meant to work in pair with python scripts and selenium webdriver, but can be used alone for quick graphical results.

## How to run
You need Docker to run the server.
To run it, run in this folder:
```Bash
docker-compose up
```

Depending on your docker installation, you might need to run it with sudo. If the docker daemon is not running, you can start it with ``` systemctl start docker ```. 
You can then access the server at http://localhost:8000.

## Content
The server contains 3 distinct pages. For each page, you can add `?coop=True` in order to enable COOP/COEP. Activating it changes the resolution of performance.now and enables SharedArrayBuffer on Firefox79 and later.

### Cache hit/miss histogram
This page contains functions to create cache hits and cache miss and time them, using different timers. It can also plot the cache/hit miss histogram.
The code is also the basis for error rate computation for repetitions. However, we used Python to compute these so the code is not available directly on the local server.

### Distribution of ticks in a clock period
This page contains functions to count the maximum number of incrementations in a period of performance.now. It is an important tool to evaluate the jitter, as it gives indication on its range as well as distribution. You can plot a histogram chart of this distribution.

### RDTSC measurements
This page uses a custom version of the browser where performance.rdtsc is defined. It returns a cycle accurate timestamp. We use it to precisely measure resolution and overhead of our functions.
All the functions on this page are not available if you have the release version of your browser. The code of performance.rdtsc for Chromium and Firefox is available in the paper
