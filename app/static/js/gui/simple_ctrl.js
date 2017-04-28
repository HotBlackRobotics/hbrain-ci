var ros = new ROSLIB.Ros({
  url : 'ws://'+ master_url +':9090'
});

var request = new ROSLIB.ServiceRequest({
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

var send_command_pub = new ROSLIB.Topic({
  ros : ros,
  name : dotbot_name + '/simple_ctrl',
  messageType : 'std_msgs/UInt8'
});




var send_command = function (ind) {
  var move = new ROSLIB.Message({
    data: ind
  });
  send_command_pub.publish(move);
};
