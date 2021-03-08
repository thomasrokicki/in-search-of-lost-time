
/*******************************************************************************
                              performance.now tests
*******************************************************************************/


/**
 * testHitPerf - Computes the access time of a cache hit using performance.now() interpolation.
 * The victim is first set in the cache by accessing it repeatedly.
 * We then wait for the next clock edge, access the victim, then interpolate it using incrementations.
 * The returned time is the time elapsed between the end of the event and the end of the clock period
 *
 * @return {Int}  The hit access time.
 */
function testHitPerf() {
	var victim = new Victim();
  var sum = 0;
  victim.setCache();
	victim.setCache();
	victim.setCache();

	waitEdge()
  victim.access()
  time = countEdge()
  return time
}

/**
 * testMissPerf - Computes the access time of a cache miss using performance.now() interpolation.
 * The victim is first evicted from the cache by using an eviction set.
 * Here the eviction set is not minimal (i.e. the approximate size of a cache set), but is a massive buffer, covering the all cache.
 * By iterating through this buffer, we make sure to evict the whole cache.
 * Make sure that the eviction set size, defined in config.js, is bigger than the actual cache size.
 *
 * We then wait for the next clock edge, access the victim, then interpolate it using incrementations.
 * The returned time is the time elapsed between the end of the event and the end of the clock period
 *
 * @param {Array} evictionSet Array larger than the cache size.
 * @return {Int}  The miss access time.
 */
function testMissPerf(evictionSet) {
	var victim = new Victim();
  var sum = 0;
	//victim.setCache();

  for (var i = 0; i < evictionSet.length; i++) {
    evictionSet[i]++;
  }
  var n = waitEdge();
	victim.access();
  time = countEdge();
  return time
}

/*******************************************************************************
                            SharedArrayBuffer tests
*******************************************************************************/

/**
 * testHitSAB - Computes the access time of a cache hit using SharedArrayBuffer.
 * The victim is first set in the cache by accessing it repeatedly.
 *
 * @param {Object} timer A SAB based timer, composed of the acutal shared array (timer.array) and a reference to the worker.
 * @return {Int}  The hit access time.
 */
function testHitSAB(timer) {
  var victim = new Victim();
  var sum = 0;
  victim.setCache();
	victim.setCache();
	victim.setCache();
  var a,b;
  a = timer.array[0];
  victim.access();
  b = timer.array[0];
  return b-a
}

/**
 * testMissSAB - Computes the access time of a cache miss using SharedArrayBuffer.
 * The victim is first evicted from the cache by using an eviction set.
 * Here the eviction set is not minimal (i.e. the approximate size of a cache set), but is a massive buffer, covering the all cache.
 * By iterating through this buffer, we make sure to evict the whole cache.
 * Make sure that the eviction set size, defined in config.js, is bigger than the actual cache size.
 *
 * We then time the event by checking the timestamp before and after.
 *
 * @param {Object} timer A SAB based timer, composed of the acutal shared array (timer.array) and a reference to the worker.
 * @param {Array} evictionSet Array larger than the cache size.
 * @return {Int}  The miss access time.
 */
function testMissSAB(evictionSet, timer) {
	var victim = new Victim();
  var sum = 0;
	//victim.setCache();

  for (var i = 0; i < evictionSet.length; i++) {
    evictionSet[i]++
  }
  var a,b;
  a = timer.array[0];
  victim.access();
  b = timer.array[0];
  return b-a
}

/*******************************************************************************
                                     Main
*******************************************************************************/


/**
 * getHitMiss - Generate timings for cache hits and misses for a specific clock.
 * This function is async to let the SAB clock initialize before starting.
 *
 * @param  {String} clockMethod A string describing which clock is used.
 * @param  {Int} repetitions The number of measurement for both hits and misses
 * @return {Object}             An object containing arrays of cache hits and misses
 */
async function getHitMiss(clockMethod, repetitions){
  console.log('Plotting hit/miss histogram');
  console.log('This can take a while, especially for huge caches');
  console.log('crossOriginIsolated: ' + String(self.crossOriginIsolated));

  if (clockMethod == 'SharedArrayBuffer'){
    var timer = await initSAB();
  }

  var hits = [];
  var misses = [];
  var evictionSet = generateRandomArray(CACHE_SIZE);

  // Get hits timings
  for (var i = 0; i < repetitions; i ++){
    if (clockMethod == 'performance.now'){
      hits.push(testHitPerf());
    }
    else if (clockMethod == 'SharedArrayBuffer') {
      hits.push(testHitSAB(timer));
    }
  }
  // Get miss timings
  for (var i = 0; i < repetitions; i ++){
    if (clockMethod == 'performance.now'){
      misses.push(testMissPerf(evictionSet));
    }
    else if (clockMethod == 'SharedArrayBuffer') {
      misses.push(testMissSAB(evictionSet,timer));
    }
  }


  if (clockMethod == 'SharedArrayBuffer') {
    killSAB(timer);
  }
  return {'hits' : hits, 'misses' : misses};
}

/**
 * plotHitMiss - Plot the cache hit/miss histogram.
 * Async because it calls an async function
 *
 * @return {Void}
 */
async function plotHitMiss(){
  let clockMethod = document.getElementById("clock").value;
  let repetitions = parseInt(document.getElementById("repetitions").value, 10);

  let {hits,misses} = await getHitMiss(clockMethod, repetitions);
  plotHist(hits,misses, clockMethod, repetitions);
}
