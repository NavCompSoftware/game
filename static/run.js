function orientate(){
  if (navigator.geolocation){
    navigator.geolocation.getCurrentPosition(go_to_me);
  }
}

function go_to_me(position){
  map.panTo(new L.LatLng(position.coords.latitude, position.coords.longitude));
}

function update() {
  console.log("updating");
  const message = document.getElementById("state_message");
  const link = document.getElementById("register_catch_button");
  cookie = document.cookie;
  
  if (navigator.geolocation && cookie != ""){
    navigator.geolocation.getCurrentPosition(communicate);
    link.innerHTML = "I got caught.";
  } else if (navigator.geolocation) { 
    console.warn("user not yet logged in");
    message.innerHTML = "Unfortunately we could not find your log in details.";
    link.style.display = "none";
  } else{
    console.warn("nav unavaliable");
    message.innerHTML = "Navigation is unavaliable.";
    link.innerHTML = "";
  }
}

function communicate(position){
  let my_id = get_id();
  
  var my_lat = position.coords.latitude;
  var my_long = position.coords.longitude;
  const my_data = [my_lat,my_long,my_id];

  const req = new XMLHttpRequest();
  req.open("POST","/update_state");
  req.onreadystatechange = function(res){
    if (req.readyState == 4 && req.status == 200){
      var data = req.response;
      return(data);
    }
  }
  req.send(my_data);
}

function clear_map(){
  markers.clearLayers();
}

function register_catch(){
  console.log("registering catch");
  let my_id = get_id();
  console.log("id: " + my_id);
  
  const req = new XMLHttpRequest();
  req.open("POST","/register_catch");
  req.onreadystatechange = function(res){
    if (req.readyState == 4 && req.status == 200){
      console.log(req.response);
    }
  }
  req.send(my_id);
}

function get_id(){  
  let cookie = document.cookie;
  let stage1 = cookie.split(":")[1];
  let my_id = stage1.substr(0,stage1.length);
  return(my_id);
}
