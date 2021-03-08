
/**
 * getLayout - Creates a layout and data traces for plotly histograms.
 * It takes into account the different resolutions and versions in order to adjust parameters.
 *
 * @param  {Array[Int]} hits        hit timings
 * @param  {Array[Int]} misses      Miss timings
 * @param  {String} clockMethod     String describing the clock
 * @param  {Int} repetitions        Number of repetitions (for title)
 * @return {Object}                 hit and miss data traces and the layout.
 */
function getLayout(hits, misses, clockMethod, repetitions) {
  browser = getBrowser();
  var hitTrace = {
    x: hits,
    type: 'histogram',
    name: "hit",
    xbins: {
      start: 0,
      size: 0,
      end: 0
    }
  };
  var missTrace = {
    x: misses,
    type: 'histogram',
    name: "miss",
    xbins: {
      start: 0,
      size: 0,
      end: 0
    }
  };
  var layout = {
    title: "Hit / Miss histogram using " + clockMethod + " with " + parseInt(repetitions,10) + " repetition(s) on " + browser.name + " " + browser.version,
    xaxis: {
      range: [0, 0]
    }
  };
  switch (clockMethod) {
    case 'SharedArrayBuffer' :
      hitTrace.xbins.start = 0;
      hitTrace.xbins.size = 1;
      hitTrace.xbins.end = 300;
      missTrace.xbins.start = 0;
      missTrace.xbins.size = 1;
      missTrace.xbins.end = 300;
      layout.xaxis.range = [0,300];
      break;

    case 'performance.now' :
      if (browser.name == "Chrome") {
        hitTrace.xbins.start = 0;
        hitTrace.xbins.size = 1;
        hitTrace.xbins.end = 40;
        missTrace.xbins.start = 0;
        missTrace.xbins.size = 1;
        missTrace.xbins.end = 40;
        layout.xaxis.range = [0,40];
      }
      else if (browser.name == 'Firefox') {
        if (parseInt(browser.version, 10) >= 79 && self.crossOriginIsolated) {
          layout.title += " with COOP/COEP"
          hitTrace.xbins.start = 0;
          hitTrace.xbins.size = 10;
          hitTrace.xbins.end = 300;
          missTrace.xbins.start = 0;
          missTrace.xbins.size = 10;
          missTrace.xbins.end = 300;
          layout.xaxis.range = [0,300];
        }
        else {
          layout.title += " without COOP/COEP"
          hitTrace.xbins.start = 0;
          hitTrace.xbins.size = 100;
          hitTrace.xbins.end = 10000;
          missTrace.xbins.start = 0;
          missTrace.xbins.size = 100;
          missTrace.xbins.end = 10000;
          layout.xaxis.range = [0,10000];

        }
      }
      break;
    default :
      console.log("Please enter a proper timing method");
  };
  data = [hitTrace,missTrace];
  return {data: data, layout: layout}
}


/**
 * plotHist - Plot a hit miss histogram on the page.
 *
 * @param  {Array[Int]} hits        hit timings
 * @param  {Array[Int]} misses      Miss timings
 * @param  {String} clockMethod     String describing the clock
 * @param  {Int} repetitions        Number of repetitions (for title)
 */
function plotHist(hits, misses, clockMethod, repetitions){
  var {data, layout} = getLayout(hits, misses, clockMethod, repetitions);
  var name = "hist_div";
  var div = document.createElement('div');
  div.setAttribute('id', name);
  document.body.appendChild(div);

  //Add the graph to it
  Plotly.newPlot(name, data, layout);
}


/**
 * plotDist - Plot the distribution histogram of ticks per clock period
 *
 * @param  {Array[int]} data
 */
function plotDist(data) {
  browser = getBrowser();
  var trace = {
      x: data,
      type: 'histogram',
      name: 'Proportion of ticks'
    };
  var layout = {title : "Distibution of ticks per clock period using " + browser.name + " " + browser.version}
  if (self.crossOriginIsolated) {
    layout.title += " with COOP/COEP"
  }
  else {
    layout.title += " without COOP/COEP"
  }
  layout.title += " and " + String(data.length) + " repetitions";
  var data = [trace];
  var name = "hist_div";
  var div = document.createElement('div');
  div.setAttribute('id', name);
  document.body.appendChild(div);
  Plotly.newPlot(name, data, layout);
}
