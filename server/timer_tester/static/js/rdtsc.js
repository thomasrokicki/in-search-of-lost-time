
/**
 * measureOverhead - Measure the overhead of performance.rdtsc.
 * This is achieved by calling performance.rdtsc twice in a row.
 *
 * @return {Int}  The overhead (pseudo-cycles)
 */
function measureOverhead() {
  let begin,end;
  begin = performance.rdtsc();
  end = performance.rdtsc();
  return end - begin;
}


/**
 * measurePerf - Measure the measurement time of performance.now interpolation.
 *
 * @return {Int}  Measurement time (pseudo-cycles)
 */
function measurePerf() {
  let begin,end;
  waitEdge();
  begin = performance.rdtsc();
  countEdge();
  end = performance.rdtsc();
  return end - begin;
}


/**
 * measureSABRead - Measure the execution time of a read in a SAB.
 *
 * @param  {type} clock The shared array and the worker
 * @return {Int}        Read time (pseudo-cycles)
 */
function measureSABRead(clock) {
  let begin,end, tmp;
  begin = performance.rdtsc();
  tmp = clock.array[0];
  end = performance.rdtsc();
  return end - begin;
}



/**
 * measureSABIncr - Measure the execution time of a write in a SAB.
 *
 * @param  {type} clock The shared array and the worker
 * @return {Int}        Write time (pseudo-cycles)
 */
function measureSABIncr(clock) {
  let begin,end, tmp;
  begin = performance.rdtsc();
  tmp = clock.array[0];
  end = performance.rdtsc();
  return end - begin;
}


/**
 * getTimerMeasurements - Get measurements for overhead, performance.now and SAB
 * Async because we may initialize a SAB clock.
 *
 * @param  {Int} repetitions The number of measurements
 * @return {Object}          Object of arrays containing results for each measurements
 */
async function getTimerMeasurements(repetitions) {
  results = {};

  //Overhead
  console.log("measuring overhead");
  results['overhead'] = [];
  for (let i = 0; i < repetitions; i++) {
    results['overhead'].push(measureOverhead());
  }

  // Clock period
  console.log("measuring performance.now");
  results['perf'] = [];
  for (let i = 0; i < repetitions; i++) {
    console.log("measuring performance.now");
    results['perf'].push(measurePerf());
  }

  if (typeof(SharedArrayBuffer) != "undefined") {
    // SAB read
    var clock = await initSAB();

    console.log("measuring SAB read");
    results['sab_read'] = [];
    for (let i = 0; i < repetitions; i++) {
      results['sab_read'].push(measureSABRead(clock));
    }

    // SAB incrementation
    console.log("measuring SAB incr");
    results['sab_incr'] = [];
    var clock = await initSAB();
    for (let i = 0; i < repetitions; i++) {
      results['sab_incr'].push(measureSABIncr(clock));
    }
    killSAB(clock);
  }
  console.log("Done measuring!");
  return results;
}


/**
 * displayMeasurements - Display the average of each measurement on the HTML page
 *
 */
async function displayMeasurements() {
  console.log("go !")
  repetitions = parseInt(document.getElementById("repetitions").value, 10);
  var results = await getTimerMeasurements(repetitions);

  var resultsDiv = document.getElementById("results");
  divValue = "";
  overhead = average(results.overhead);
  divValue += "Average overhead of performance.rdtsc(): " + overhead;
  divValue += "</br>";

  var perf = average(results.perf) - overhead
  divValue += "Average performance.now measurement time: " + perf;
  divValue += "</br>";

  if (typeof(SharedArrayBuffer) != "undefined") {
    var SABRead = average(results.sab_read) - overhead
    divValue += "Average SAB read time: " + SABRead;
    divValue += "</br>";

    var SABIncr = average(results.sab_incr) - overhead
    divValue += "Average SAB increment time: " + SABIncr;
    divValue += "</br>";
  }
  else {
    divValue += "Average SAB read time: SABs are unavailable here"
    divValue += "</br>";
    divValue += "Average SAB increment time: SABs are unavailable here"
    divValue += "</br>";
  }
  resultsDiv.innerHTML = divValue;
}
