var update = function() {
  $("#update-btn").text("updating...");
  $.get( "/api/v1.0/bin/update", function( data ) {
    location.reload();
  });
};


var set_ros = function() {
  console.log({
      master: $("#master_text").val(),
      ip: $("#ip_text").val(),
      namespace: $("#namespace_text").val()
    }
  );

  data = {
    master: $("#master_text").val(),
    ip: $("#ip_text").val(),
    namespace: $("#namespace_text").val()
  };
  $.ajax({
    type: "PUT",
    url: "/api/v1.0/ros/rosconfig",
    data: JSON.stringify(data, null, '\t'),
    contentType: 'application/json;charset=UTF-8',
    success: function (data) {console.log(data);}
  });
};
