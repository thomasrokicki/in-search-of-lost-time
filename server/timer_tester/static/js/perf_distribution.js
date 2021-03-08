
/**
 * test_clock_edge - Computes the number of incrementations in a given clock period.
 *
 * Wait for a clock edge, then increments a variable until the end of the clock period.
 * This is equivalent to using clock interpolation without an event to time.
 *
 * @return {Int}  The number of incrementation in a single clock period.
 */
function test_clock_edge() {
  waitEdge();
  ticks = countEdge();
  return ticks;
}



/**
 * test_clock_edges - Computes repeatedly the number of incrementations in a clock period
 *
 * @param  {Int} repetitions        The number of measurements
 * @return {Array[Int]}             An array containing, the number of incrementations for different clock periods.
 */
function test_clock_edges(repetitions) {
  tickNumber = []
  for (var i = 0; i < repetitions; i++) {
    tickNumber.push(test_clock_edge());
  }
  return tickNumber;
}


/**
 * distribution - Computes the distribution of the number of incrementations per clock period.
 * Plot the histogram of the distribution.
 *
 */
function distribution(){
  console.log("go");
  var repetitions = parseInt(document.getElementById("repetitions").value, 10);

  results = test_clock_edges(repetitions);

  console.log(average(results));
  console.log(Math.sqrt(variance(results)));

  plotDist(results);
}
