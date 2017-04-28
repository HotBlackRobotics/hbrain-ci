var ros = new ROSLIB.Ros({
  url : 'ws://'+ master_url +':9090'
});



ros.on('error', function(error) {
  console.log('Error connecting to websocket server: ', error);
  $("#roscore-alert").show();
});

ros.on('close', function() {
  console.log('Connection to websocket server closed.');
});


ros.on('connection', function() {
  console.log('Connected to websocket server.');
});

var cmdLed = new ROSLIB.Topic({
  ros : ros,
  name : '/' + dotbot_name + '/led',
  messageType : 'dotbot_msgs/Led'
});

var led = new ROSLIB.Message({
});

var cmdMotor = new ROSLIB.Topic({
  ros : ros,
  name : '/' + dotbot_name + '/speed',
  messageType : 'dotbot_msgs/Speed'
});





var check_click = function(element, num) {
  console.log("Led" + num + " ", element.checked);
  led["led" + num] = element.checked;
  cmdLed.publish(led);
};

var read_value = function(v) {
  if (isNaN(v)) return 0;
  else if (v > 255) return 255;
  else if (v < -255) return -255;
  return v;
};

var setMotors = function(element, num) {
  console.log("Motor 1", Number($("#Motor1").val()));
  console.log("Motor 2", document.getElementById("Motor2").value);

  var speed = new ROSLIB.Message({
    dx: read_value(Number($("#Motor2").val())),
    sx: read_value(Number($("#Motor1").val()))
  });
  console.log(speed);
  cmdMotor.publish(speed);
};
