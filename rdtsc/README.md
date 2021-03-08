# Perfomance.rdtsc custom browsers.

In order to properly evaluate resolution and measurement time of our timers, we need a higher resolution timer.
We built a custom versions of Chromium and Firefox where we defined a new method: `performance.rdtsc`.
This method calls the native RDTSC instruction, which returns a cycle accurate timer.
To prevent Out of Order execution messing with our measurements, `performance.rdtsc` also features memory fences (`mfence` instruction) during the execution.

You can find patches to apply necessary modifications to Chromium and Firefox in the `diffs` folder. The patches were computed for Firefox 81 and Chromium 84 so they may not work for all versions as timers module have changed quite a lot, but by pasting the code to the right place you should be able to build other versions.
