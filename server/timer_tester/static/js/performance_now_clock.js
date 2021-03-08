
/**
 * waitEdge - Wait for the next clock edge.
 *
 * @author Michael Schwarz
 * @return {type}  description
 */
function waitEdge() {
    var next, last = performance.now();
    // Do nothing until next tick
    while ( performance.now() == last){}
    return next ;
}


/**
 * countEdge - Interpolate the time between the start of the function and the next clock edge
 * using performance.now and incrementations.
 *
 * @author Michael Schwarz
 * @return {Int}  The interpolated time
 */
function countEdge() {
    var last = performance.now();
    var count = 0;
    while (performance.now() == last) {
      count++
    }
    return count;
}
