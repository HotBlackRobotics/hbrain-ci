
var editor;

$(window).keypress(function(event) {
    if (!(event.which == 115 && event.ctrlKey) && !(event.which == 19)) return true;
    event.preventDefault();
    return false;
});

$(function() {
  editor = CodeMirror.fromTextArea(document.getElementById('code'), {
    lineNumbers: true,
    styleActiveLine: true,
    mode: "text/x-c++src",
  });
});


var save = function(id) {
  var sketch = { code: editor.getDoc().getValue() };
    $.ajax({
    url: '/api/v1.0/files/' + id + '/',
    type: 'PUT',
    contentType: "application/json",
    data: JSON.stringify(sketch),
    success: function(result) {
        console.log("uploaded");
    }
  });
}

var shell = function() {
  $('#shellModal').modal('show');
}

var download = function (id) {
  save(id)
  $.ajax({
    url: '/api/v1.0/sketches/download/' + id ,
    type: 'GET',
    success: function(result) {
        console.log("downloaded");
    }
  });
}

var Console = function() {
  this.log = function(data) {
    $("#my_console").append(data +'<br>');
    $("#my_console").scrollTop($("#my_console")[0].scrollHeight);
  };
  this.empty = function() {
    $("#my_console").empty();
  }
}


var compile =  function(id) {
  shell();
  $("#shellLabel").html("Compiling...")
  my_console.empty();
  var valeur = 0;
  // $("#devprogress").attr('transition', 'none');
  $("#devprogress").css('width', valeur+'%').attr('aria-valuenow', valeur);

  id = id || 1
  $("#devprogress").css('width', valeur+'%').attr('aria-valuenow', valeur);
  var url =  '/api/v1.0/nodes/'+ id + '/build';
  var evtSrc = new EventSource(url);

  /*
    To close the connection if error occurs:
    otherwise it continues tu push
  */
  evtSrc.onerror = function(e) {
    console.log(e);
    e.target.close();
  }

  evtSrc.onmessage = function(e) {
    if (e.data === 'STOP'){
      console.log("STOP");
      e.target.close();
      valeur = 100;
      $("#devprogress").css('width', valeur+'%').attr('aria-valuenow', valeur);
      $("#shellLabel").html("Shell");

    } else {
      my_console.log(e.data);
      console.log(e.data);
      valeur = valeur+0.1;
      $("#devprogress").css('width', valeur+'%').attr('aria-valuenow', valeur);
    }
  };
  return false;
}

var kill = function(ed) {
    $.ajax({
    url: '/api/v1.0/kill',
    type: 'GET',
    success: function(result) {
        console.log("killed");
    }
  });
}

var run =  function(id) {
  shell();
  my_console.empty();
  var valeur = 0;
  id = id || 1
  var url =  '/api/v1.0/nodes/'+ id + '/run';
  var evtSrc = new EventSource(url);
  $("#shellLabel").html("Node Running..." )

  /*
    To close the connection if error occurs:
    otherwise it continues tu push
  */
  evtSrc.onerror = function(e) {
    console.log(e);
    e.target.close();
  }

  evtSrc.onmessage = function(e) {
    if (e.data === 'STOP'){
      console.log("STOP");
      e.target.close();
      $("#closeShell").attr("disabled", false);
    } else {
      my_console.log(e.data);
      console.log(e.data);
    }
  };
  return false;
}



var my_console = new Console()

var Buffer = function() {
  this.cnt = 0;
  this.str = "";
  this.addline = function(line) {
    this.str += line+'\n';
    if (this.cnt >= 100) {
      console.log(this.cnt, this.str.indexOf('\n'))
      this.str = this.str.substr(this.str.indexOf('\n')+1, this.str.length);
    } else {
      this.cnt+=1;
      console.log(this.cnt)
    }
    return this.str
  };
}
