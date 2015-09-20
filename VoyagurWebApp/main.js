var check = false;
(function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4)))check = true})(navigator.userAgent||navigator.vendor||window.opera);
if(check) window.location.replace("http://www.myvoyagr.co/mobile");

$("document").ready(function(){

  //google autocomplete
  var autocomplete = new google.maps.places.Autocomplete( (document.getElementById('location')), { types: ['geocode'] });
  google.maps.event.addListener(autocomplete, 'place_changed', function() {});

  //start drawer
  $(".drawer").drawer();

  //load google photos
  onApiLoad();
  autoUploadGooglePhotos();

  //drawer img dragging
  $( ".drawerImg" ).draggable({
      appendTo: "#addPostContainer",
      cursor: "move",
      cursorAt: {left:0, top:0},
      helper: 'clone',
      revert: "valid",
      zIndex: 9998,
      start: function(e, ui) {
        ui.helper.animate({
            width: 100,
            height: 100
          });
      }
    });


  $("#postImages").droppable({
      tolerance: "pointer",
      accept: ".drawerImg",
      activeClass: "ui-state-default",
      hoverClass: "ui-state-hover",
      drop: function(event, ui) {   
          $("#postImages").css("height", "auto"); 
          ui.draggable.animate({
            width: "25%"
          });    
          $(this).append($(ui.draggable));
      }
  });
});


var userEmail;
function onSignIn(googleUser) {
  // Useful data for your client-side scripts:
  var profile = googleUser.getBasicProfile();

  console.log("ID: " + profile.getId()); // Don't send this directly to your server!
  console.log("Name: " + profile.getName());
  console.log("Image URL: " + profile.getImageUrl());
  console.log("Email: " + profile.getEmail());
  userEmail = profile.getEmail();



  // The ID token you need to pass to your backend:
  var id_token = googleUser.getAuthResponse().id_token;
  console.log("ID Token: " + id_token);

  //send token to backend server
  
  var xhr = new XMLHttpRequest();
  xhr.open('POST', 'http://gcp-hackthenorth-3108.appspot.com/user');
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onload = function() {
    console.log('Signed in as: ' + xhr.responseText);
  };
  xhr.send(JSON.stringify({token:id_token}));

  
  $("#fadeBackground").fadeOut();
};

function logOut() {
   var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
  $("#fadeBackground").fadeIn();
    });
}

/**
 * Load the Drive API client.
 * @param {Function} callback Function to call when the client is loaded.
 */
function loadClient(callback) {
  gapi.client.load('drive', 'v2', callback);
}

function getGooglePhotos(fileId) {
  var request = gapi.client.drive.files.get({
      'fileId': fileId
  });
  request.execute(function(resp) {
    if (!resp.error) {
      console.log('Title: ' + resp.title);
      console.log('Description: ' + resp.description);
      console.log('MIME type: ' + resp.mimeType);
    } else if (resp.error.code == 401) {
      // Access token might have expired.
      checkAuth();
    } else {
      console.log('An error occured: ' + resp.error.message);
    }
  });
}




function showAddPost() {
  $("#addPostContainer").fadeIn();
}

function hideAddPost() {
  $("#addPostContainer").fadeOut();
}

function first(obj) {
    for (var a in obj) return a;
}

function addPhotos(photoObject) {
  var photo = "";
  for(var i=0; i < photoObject["entities"].length; i++){

    var url = photoObject["entities"][i][first(photoObject["entities"][i])]["thumbnail_link"];

    photo +=  '<li class="drawer-submenu-item"><img src="' 
                + url + '" width="100%" class="drawerImg ui-widget ui-widget-content"/></li>';
  }

  $("#currTrip").append(photo);

  $(".drawerImg").draggable({
      appendTo: "#addPostContainer",
      cursor: "move",
      cursorAt: {left:0, top:0},
      helper: 'clone',
      revert: "valid",
      zIndex: 9998,
      start: function(e, ui) {
        ui.helper.animate({
            width: 100,
            height: 100
          });
      }
    });
}