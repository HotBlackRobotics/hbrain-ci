var ros = new ROSLIB.Ros({
  url : 'ws://'+ master_url +':9090'
});

var getMovesClient = new ROSLIB.Service({
  ros : ros,
  name : '/' + dotbot_name + '/services/get_moves',
  serviceType : 'dotbot_msgs/GetMoves'
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
  getMovesClient.callService(request, function(result) {
    console.log(result);
    $("#btnMove1").html(result.move1);
    $("#btnMove2").html(result.move2);
    $("#btnMove3").html(result.move3);
    $("#btnMove4").html(result.move4);
  });
});

var send_move_pub = new ROSLIB.Topic({
  ros : ros,
  name : dotbot_name + '/move',
  messageType : 'std_msgs/UInt8'
});




var send_move = function (ind) {
  var move = new ROSLIB.Message({
    data: ind
  });
  send_move_pub.publish(move);
};


var hp_sub = new ROSLIB.Topic({
  ros : ros,
  name : dotbot_name + '/hp',
  messageType : 'std_msgs/UInt8'
});

hp_sub.subscribe(function(message) {
  var hp = message.data;
  console.log('Received message on ' + hp_sub.name + ': ' + message.data);
  $('#hpBar').css('width', hp+'%').attr('aria-valuenow', hp).html(hp);
  if (hp > 50) $('#hpBar').attr('class', 'progress-bar progress-bar-success');
  else if (hp > 20) $('#hpBar').attr('class', 'progress-bar progress-bar-warning');
  else $('#hpBar').attr('class', 'progress-bar progress-bar-danger');

});
