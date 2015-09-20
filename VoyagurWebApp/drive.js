// The Browser API key obtained from the Google Developers Console.
var developerKey = 'AIzaSyCyeXft5v3Bkt9J-Loq3Lzz9bgDPapqHNo';

// The Client ID obtained from the Google Developers Console. Replace with your own Client ID.
var clientId = "186158066963-05merjcea3mio8kcajk0sg72kq8mrchh.apps.googleusercontent.com"

// Scope to use to access user's photos.
var scope = ['https://www.googleapis.com/auth/drive.photos.readonly'];

var pickerApiLoaded = false;
var oauthToken;

var tripName;

var tripID2;

function uploadPhotos(){
  if(document.getElementById("tripSelect").options.length == 0) {
    alert("Please select a trip, or create a new trip.");
    return;
  }
  $(".drawer").drawer("close");
  tripName = $("#tripSelect option:selected").text();
  onApiLoad();
}

// Use the API Loader script to load google.picker and gapi.auth.
function onApiLoad() {
  gapi.load('auth', {'callback': onAuthApiLoad});
  gapi.load('picker', {'callback': onPickerApiLoad});
}

function onAuthApiLoad() {
  window.gapi.auth.authorize(
      {
        'client_id': clientId,
        'scope': scope,
        'immediate': false
      },
      handleAuthResult);
}

function onPickerApiLoad() {
  pickerApiLoaded = true;
  createPicker();
}

function handleAuthResult(authResult) {
  if (authResult && !authResult.error) {
    oauthToken = authResult.access_token;
    createPicker();
  }
}

// Create and render a Picker object for picking user Photos.
function createPicker() {
  if (pickerApiLoaded && oauthToken) {
    var picker = new google.picker.PickerBuilder().
        addView(google.picker.ViewId.DOCS_IMAGES).
        enableFeature(google.picker.Feature.MULTISELECT_ENABLED).
        setOAuthToken(oauthToken).
        setDeveloperKey(developerKey).
        setCallback(pickerCallback).
        build();
    picker.setVisible(true);
  }
}

// A simple callback implementation.
function pickerCallback(data) {
  var fileIDs = [];
  var fileIDsObject = {};
  if (data[google.picker.Response.ACTION] == google.picker.Action.PICKED) {
    for(var i = 0; i < data[google.picker.Response.DOCUMENTS].length; i++)
    {
      var doc = data[google.picker.Response.DOCUMENTS][i];
      fileIDs[i] = doc[google.picker.Document.ID];
    }

    fileIDsObject["name"] = tripName;
    fileIDsObject["email"] = userEmail;
    fileIDsObject["access_token"] = oauthToken;
    fileIDsObject["file_ids"] = fileIDs;
    var pickerJson = JSON.stringify(fileIDsObject);
    console.log(fileIDsObject);
    console.log(pickerJson);

    //send file ids to server
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://gcp-hackthenorth-3108.appspot.com/trip');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function() {
      var responseJson = xhr.responseText;
      console.log(responseJson);
      responseJson = responseJson.replace(/'/g, '"');
      responseJson = responseJson.replace(/ u/g, ' ');
      responseJson = responseJson.replace(/\{u"/g, '{ "');
      console.log(responseJson);
      var responseObject = jQuery.parseJSON(responseJson);
      console.log(responseObject);
      tripID2 = responseObject["trip_id"];
      addPhotos(responseObject);
    };
    xhr.send(pickerJson);

  }

}