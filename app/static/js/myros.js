console.log(document.URL);

var ros = new ROSLIB.Ros({
  url : 'ws://'+ master_url +':9090'
});


ros.on('error', function(error) {
  console.log('Error connecting to websocket server: ', error);
});

ros.on('close', function() {
  console.log('Connection to websocket server closed.');
});


ros.on('connection', function() {
  console.log('Connected to websocket server.');
});




  var lis = new ROSLIB.Topic({
    ros : ros,
    name : '/test',
    messageType : 'std_msgs/String'
  });

  lis.subscribe(function(message) {
    console.log('Received message on ' + lis.name + ': ' + message.data);
    $("#console-echo").append("<br> [" + lis.name + '] ' + message.data);
  });
