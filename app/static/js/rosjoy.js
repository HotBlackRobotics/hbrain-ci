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

var cmdJoy = new ROSLIB.Topic({
  ros : ros,
  name : '/' + dotbot_name + '/joy',
  messageType : 'geometry_msgs/Vector3'
});



console.log("touchscreen is", VirtualJoystick.touchScreenAvailable() ? "available" : "not available");

var joystick	= new VirtualJoystick({
  container	: document.getElementById('joypad'),
  mouseSupport	: true,
});

setInterval(function(){
  var outputEl	= document.getElementById('result');
  var joy = new ROSLIB.Message({
    x: joystick.deltaX(),
    y: joystick.deltaY()
  });
  cmdJoy.publish(joy);
}, 1/10 * 1000);
