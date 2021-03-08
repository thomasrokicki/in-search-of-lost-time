/* Don't forget to document callback - must be instanciated before, or in a promise*/

/**
 * initSAB - Initializate a SAB based clock.
 * Creates a webWorker than increments an array on a loop.
 * The array is shared between the main thread and the web worker.
 * By checking the array value, the user can retrieve a timestamp.
 *
 * As postMessage is a callback, this function must be resolved before being able to use the timer.
 * This means that the user must use the await keyword in an async function, or call it and letting the callback finish.
 *
 * Also note that this is very performance consuming.
 * Don't forget to kill the worker afterwards with killSAB.
 *
 * @return {Object}  The shared array and a reference to the worker.
 */
function initSAB(){
  console.log("Initializing SAB.")
  return new Promise((resolve,reject) => {
    const code = `onmessage = function(event) {
        var buffer=event.data;
        var arr = new Uint32Array(buffer);
        postMessage("done");
        while(1) {
          Atomics.add(arr,0,1);
       }
    }`;
    let buffer = new SharedArrayBuffer(BUFFER_ELEMENT_SIZE);
    const blob = new Blob([code], { "type": 'application/javascript' });
    const url = window.URL || window.webkitURL;
    const blobUrl = url.createObjectURL(blob);
    const counter = new Worker(blobUrl);
    counter.onmessage = e => {
      const res = new Uint32Array(buffer);
      window.setTimeout(() => {
        resolve({
            array: res,
            worker: counter
        });
      },10);
    };
    counter.onerror = reject;
    counter.postMessage(buffer);
    //console.log("Done.")
  });
}


/**
 * killSAB - Terminate a SAB based clock
 *
 * @param  {type} timer The shared array and a reference to the worker.
 */
function killSAB(timer){
  console.log("Stopping clock.")
  timer.worker.terminate();
}
