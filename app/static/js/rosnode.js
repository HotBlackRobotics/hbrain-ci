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


var ros_nodes = [];


var show_nodes = function(nodes) {
  $('#nodesList').empty();
  for ( i = 0; i < nodes.length; i+=1) {
    s = nodes[i];
    console.log(s);
    var btn_class = 'btn btn-xs btn-danger';
    if (s == 'rosout') {
      btn_class = btn_class + ' disabled';
    }
    $('#nodesList').append(
      '<tr>' +
      '<td>' + s + '</td>' +
      '<td>'+
      '<div class="btn-group" role="group">'+
      '<button class="' + btn_class + '" type="button" onclick="deleteNode(\'' + s + '\')">kill node</button> </div></td>'+
      '</tr>'
    );
  }
};

var load_nodes = function () {
    all_nodes = [];
    ros.getNodes(function (tt) {
      console.log(tt);
      (function(ns) {all_nodes = ns;})(tt);
      show_nodes(all_nodes);
    });
};

var deleteNode = function(node) {
  $.ajax({
    url: '/api/v1.0/rosnode' + node + '/',
    type: 'DELETE',
    success: function(result) {
      console.log("deleted");
    }
  });
};

$(document).ready(function () {
  load_nodes();
  var myVar = setInterval(load_nodes, 1000);
});
