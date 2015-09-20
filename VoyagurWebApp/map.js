//access token
L.mapbox.accessToken = 'pk.eyJ1IjoibHVveWFuZzkiLCJhIjoiY2llbm5nd3ExMGhtdHNzbTJtOXU0NzgwOSJ9.J8foZzRMoJhim7PslJlO5w';

//create map, set view
var mapGeo = L.mapbox.map('map_geo', 'mapbox.streets').setView([43.8, -79.8], 8);

//get geocoder object for geocoding (transforming strings to latlng)
var geocoder = L.mapbox.geocoder('mapbox.places');

var existingContainer = document.getElementById("existing-posts");

var allTrips = [];
var tripIDs = [];
updateTripSelect();

function newTrip(tripName){
  if(tripName == "") {
    alert("Please enter a trip name!"); 
    return;
  }
  //create feature layer, add to map
  var tripLayer = L.mapbox.featureLayer().addTo(mapGeo);
  allTrips.push(tripLayer);
  tripIDs.push(tripName);
  updateTripSelect();
}

function updateTripSelect(){
  $("#tripSelect").empty();
  for(var i = 0; i < tripIDs.length; i++){
    var option = document.createElement("option");
    option.text = tripIDs[i];
    option.value = i;
    document.getElementById("tripSelect").add(option);
  }
}



//add post with create new post form
function addPost(){
  var tripSelect = document.getElementById("tripSelect");

  if(tripSelect.options.length == 0) {
    alert("Please select a trip, or create a new trip.");
    return;
  }

  var tripID = tripSelect.options[tripSelect.selectedIndex].value;

	var location = document.getElementById("location").value;
	var title = document.getElementById("title").value;
	var description = document.getElementById("description").value;
  var imageArray = $("#postImages img").map(function() {
    return this.src;
  });
	geocoder.query(location, function(err, data){
	    mapGeo.fitBounds(data.lbounds);
	    addMarker(data.latlng[0], data.latlng[1], title, description, imageArray, tripID);
	});
}

//add marker to feature layer
function addMarker(x, y, title, description, images, tripID){
  var marker = L.marker([x, y], {
  	icon: L.mapbox.marker.icon({
    	"marker-color": "#3bb2d0",
    	"marker-symbol": "star",
    	"marker-size": "medium",
  	})
  });
  var popupContent = "<h1>" + title + "</h1><p>" + description + "</p>";
  for(var i = 0; i < images.length; i++){
    popupContent += "<img src='" + images[i] + "' width=100% /><br/>"
  }
  marker.bindPopup(popupContent);
  console.log(allTrips);
  console.log(tripID);
  allTrips[tripID].addLayer(marker);
  marker.openPopup();

  var line = [];

  allTrips[tripID].eachLayer(function(marker) {
    line.push(marker.getLatLng());
  });

  var polyline_options = {
    color: '#000'
  };

  if(line.length > 1)
  var polyline = L.polyline(line, polyline_options).addTo(mapGeo);



  addPostSidebar(marker, title, description);
}

//add post to sidebar
function addPostSidebar(marker, title, description){
  var link = existingContainer.appendChild(document.createElement('div'));
  link.className = 'navItem';

  // Populate content from each markers object.
  link.innerHTML =  "<h2>" + title + "</h2><p>" + description.substring(0, 50) + "...</p>";
  link.onclick = function() {

    mapGeo.panTo(marker.getLatLng());
    marker.openPopup();
  }
}
