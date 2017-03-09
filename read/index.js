var Gpio = require('pigpio').Gpio,
  echo = new Gpio(18, {mode: Gpio.INPUT, alert: true});

(function () {

  var prevTick;

  echo.on('alert', function (level, tick) {

    if(prevTick) {

        var pulse = tick - prevTick;

        var state = level ? 0 : 1;

        console.log(state + ': ' + pulse);

    }

    prevTick = tick;

  });
}());