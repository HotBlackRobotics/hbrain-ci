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



function syntaxHighlight(json) {
    if (typeof json != 'string') {
         json = JSON.stringify(json, undefined, 2);
    }
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
        var cls = 'number';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = 'key';
            } else {
                cls = 'string';
            }
        } else if (/true|false/.test(match)) {
            cls = 'boolean';
        } else if (/null/.test(match)) {
            cls = 'null';
        }
        return '<span class="' + cls + '">' + match + '</span>';
    });
}

function TopicHandler(name, type) {
  var that = this;
  that.name = name;
  that.type = type;
  that.listener = new ROSLIB.Topic({
      ros : ros,
      name : that.name,
      messageType : that.type
    });

  that.div = document.createElement("div");
  $("#rostopic-echo-div").append(that.div);
  $(that.div).hide();

  that.unlisten = function() {
      this.onclick = that.listen;
      that.listener.unsubscribe();
      this.className = 'btn btn-xs btn-success';
      this.innerHTML = "Echo";
      $(that.div).hide();
  };

  that.listen = function() {
    this.onclick = that.unlisten;
    this.innerHTML = "Close";
    this.className = 'btn btn-xs btn-danger';
    that.div.innerHTML = '<div class="col-md-6"><div class="panel panel-success"><div class="panel-heading">' + that.name + '</div><div class="panel-body"><pre class="rostopic_pre"></pre></div></div></div>';
    $(that.div).show();
    var pre = that.div.getElementsByTagName("pre")[0];
    that.listener.subscribe(function (msg) {
      pre.innerHTML = syntaxHighlight(msg);
    });
  };

}



var ros_topics = [];
var show_topics = function(topics) {
  $('#topics-list').empty();
  var t_lists = document.createElement("div");
  for ( i = 0; i < topics.length; i+=1) {
    console.log(topics[i])
    ros_topics[i] = new TopicHandler(topics[i][0], topics[i][1]);
    var btn_class = 'btn btn-xs btn-success';
    var tr = document.createElement("tr");
    tr.innerHTML ='<td>' + ros_topics[i].name + '</td>' +
      '<td>' + ros_topics[i].type + '</td>' +
      '<td>'+
      '<div class="btn-group" role="group">'+
      '<button class="' + btn_class + '" type="button">Echo</button> </div></td>';
      tr.getElementsByTagName("button")[0].onclick = ros_topics[i].listen;
    $('#topics-list').append(tr);
  }
}

var load_topics = function () {

    all_topics = [];

    ros.getTopics(function (tt) {
      console.log(tt)
      for (t in tt) {
        console.log(tt[t]);
        (function (top) {
        ros.getTopicType(tt[t], function(ty) {
          console.log(top, ty);
          all_topics.push([top, ty]);
          show_topics(all_topics);
        });})(tt[t]);
      }
    });
}

$(document).ready(function () {
  load_topics();
});
