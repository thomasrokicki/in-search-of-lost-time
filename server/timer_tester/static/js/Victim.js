
/**
 * Victim - A victim object, used for cache operations
 *
 *
 */
function Victim() {
  var _this = this;
  _this.address = [Math.floor((Math.random() * 127))];
  var sum = 0;


  /**
   * this - Set the victim in the cache by calling it repeatedly
   *
   * @param  {type} repetitions = 1000 Number of repetitions
   */
  this.setCache = function(repetitions = 1000) {
    for (var i = 0; i < repetitions; i++) {
    sum += _this.address[0];
    }
  }


  /**
   * this - Access the victim.
   *
   */
  this.access = function() {
    sum += _this.address[0]
  }

}
