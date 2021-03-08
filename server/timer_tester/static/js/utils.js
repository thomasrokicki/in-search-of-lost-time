

/**
 * average - Computes the average of an array.
 *
 * @param  {Array[Int]} array
 * @return {Int}   The average value.
 */
function average(array) {
  return array.reduce((a, b) => a + b) / array.length
}


/**
 * variance - Computes the average of an array.
 *
 * @param  {Array[Int]} arr
 * @return {type} The variance.
 */
function variance(arr)
{
    var len = 0;
    var sum=0;
    for(var i=0;i<arr.length;i++)
    {
        if (arr[i] == ""){}
        else
        {
            len = len + 1;
            sum = sum + parseFloat(arr[i]);
        }
    }
    var v = 0;
    if (len > 1)
    {
        var mean = sum / len;
        for(var i=0;i<arr.length;i++)
        {
            if (arr[i] == ""){}
            else { v = v + (arr[i] - mean) * (arr[i] - mean); }
        }
        return v / len;
    }
    else { return 0; }
}



/**
 * median - Computes the median of an int array
 *
 * @param  {Array[Int]} array
 * @return {Int}        The median
 */
function median (array) {
  array.sort(function(a, b) {
    return a - b;
  });
  var mid = array.length / 2;
  return mid % 1 ? array[mid - 0.5] : (array[mid - 1] + array[mid]) / 2;
}



/**
 * Number.prototype.mod - Computes the modulo of two numbers.
 * Must be used as Number.modulo(Int).
 *
 * @param  {Int} n The modulus
 * @return {Int}   The remainder
 */
Number.prototype.mod = function(n) {
	var m = (( this % n) + n) % n;
	return m < 0 ? m + Math.abs(n) : m;
};



/**
 * generateRandomArray - Generate a random array of given size filled with random integers.
 *
 * @param  {Int} size description
 * @return {Array[int]}      description
 */
function generateRandomArray(size) {
	array = [];
	for (var i = 0; i < size; i++) {
		array.push(Math.floor(Math.random()*127));
	}
	return array;
};



/**
 * getBrowser - Get browser information
 *
 * @return {Object[String]}  The name and version of the browser as strings
 */
function getBrowser() {
    var ua=navigator.userAgent,tem,M=ua.match(/(opera|chrome|safari|firefox|msie|trident(?=\/))\/?\s*(\d+)/i) || [];
    if(/trident/i.test(M[1])){
        tem=/\brv[ :]+(\d+)/g.exec(ua) || [];
        return {name:'IE',version:(tem[1]||'')};
        }
    if(M[1]==='Chrome'){
        tem=ua.match(/\bOPR|Edge\/(\d+)/)
        if(tem!=null)   {return {name:'Opera', version:tem[1]};}
        }
    M=M[2]? [M[1], M[2]]: [navigator.appName, navigator.appVersion, '-?'];
    if((tem=ua.match(/version\/(\d+)/i))!=null) {M.splice(1,1,tem[1]);}
    return {
      name: M[0],
      version: M[1]
    };
 }
