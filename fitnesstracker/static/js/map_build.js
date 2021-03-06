var map = L.map("map").setView([53.299697,-4.387321], 10);

osm = L.tileLayer('https://api.maptiler.com/maps/basic/{z}/{x}/{y}.png?key=LHlqrAvd3VUM4yZjqFDy', {
attribution: '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>'
});
osm.addTo(map);

// Add the route to the map
fetch("https://api.maptiler.com/data/b92719af-8d5b-4006-9631-3d8b13eaa1c6/features.json?key=g9ErshPDnj0LYYtEd10o")
.then(function (responce) {
return responce.json();
})
.then(function (data) {
L.geoJSON(data).addTo(map);
});

// Add the start / lap checkered flag
var checkerd = L.icon ({
    iconAnchor: [5, 60],
    iconSize: [60, 60],
    iconUrl: "static/images/markers/checkered-flag.png"
     });

var start = L.marker([53.3219, -4.2259],{icon:checkerd}).addTo(map);

// Add unique markers for each group member
// Would like to get this into a loop but Leaflet.js is beyound the scope
// of this project. The for this will be classed as future development
var mapMarkers = [
    L.icon({
            iconAnchor: [15, 15],
            iconSize: [30, 30],
            iconUrl: "static/images/markers/runner-yellow.png",
            popupAnchor: [5, 5]
            }),
    L.icon({
            iconAnchor: [15, 15],
            iconSize: [30, 30],
            iconUrl: "static/images/markers/runner-green.png",
            popupAnchor: [5, 5]
            }),
    L.icon({
            iconAnchor: [15, 15],
            iconSize: [30, 30],
            iconUrl: "static/images/markers/runner-red.png",
            popupAnchor: [5, 5]
            }),
    L.icon({
            iconAnchor: [15, 15],
            iconSize: [30, 30],
            iconUrl: "static/images/markers/runner-pink.png",
            popupAnchor: [5, 5]
            }),
    L.icon({
            iconAnchor: [15, 15],
            iconSize: [30, 30],
            iconUrl: "static/images/markers/runner-blue.png",
            popupAnchor: [5, 5]
            }),
    L.icon({
            iconAnchor: [15, 15],
            iconSize: [30, 30],
            iconUrl: "static/images/markers/runner-orange.png",
            popupAnchor: [5, 5]
            }),
    L.icon({
            iconAnchor: [15, 15],
            iconSize: [30, 30],
            iconUrl: "static/images/markers/runner-d-blue.png",
            popupAnchor: [5, 5]
            }),
    L.icon({
            iconAnchor: [15, 15],
            iconSize: [30, 30],
            iconUrl: "static/images/markers/runner-lime.png",
            popupAnchor: [5, 5]
            }),
    L.icon({
            iconAnchor: [15, 15],
            iconSize: [30, 30],
            iconUrl: "static/images/markers/runner-l-blue.png",
            popupAnchor: [5, 5]
            }),
    L.icon({
            iconAnchor: [15, 15],
            iconSize: [30, 30],
            iconUrl: "static/images/markers/runner-purple.png",
            popupAnchor: [5, 5]
            }),
    L.icon({
            iconAnchor: [15, 15],
            iconSize: [30, 30],
            iconUrl: "static/images/markers/runner-navy.png",
            popupAnchor: [5, 5]
            }),
    L.icon({
            iconAnchor: [15, 15],
            iconSize: [30, 30],
            iconUrl: "static/images/markers/runner-rose.png",
            popupAnchor: [5, 5]
            }),
    L.icon({
            iconAnchor: [15, 15],
            iconSize: [30, 30],
            iconUrl: "static/images/markers/runner-slate.png",
            popupAnchor: [5, 5]
            }),
    L.icon({
            iconAnchor: [15, 15],
            iconSize: [30, 30],
            iconUrl: "static/images/markers/runner-brown.png",
            popupAnchor: [5, 5]
            }),
    L.icon({
            iconAnchor: [15, 15],
            iconSize: [30, 30],
            iconUrl: "static/images/markers/runner-white.png",
            popupAnchor: [5, 5]
            })
];


async function getUsers() {
  // load users JSON File
    const response = await fetch("static/json/user_data.json");
    const user_data = await response.json();

  // Loop JSON to get users data
    for (item of user_data) {
      for( var i = 0;  i < mapMarkers.length;  i++ ) {
   if(item.icon_num == i){
  var marker = L.marker(
      [ item.latitude, item.longitude ],
      { icon: mapMarkers[i] }
  ).addTo( map );
const txt = `${item.first} ${item.last}: Your Total Distance is
${item.total} miles. You have completed ${item.laps} laps and
have covered ${item.current} miles on your current lap.`;
      marker.bindPopup(txt);
}}
}
}

getUsers();

var LandmarkIcon = L.Icon.extend({
        options: {
        iconSize: [60, 60],
        iconAnchor: [5, 60],
        popupAnchor: [5, -60]
}
});


var icon_landmark = new LandmarkIcon({
    iconUrl: "static/images/markers/a-red-flag.png" });

let obj = JSON.parse(unlocked);

async function getLandmarks() {
// load JSON File
const response = await fetch("static/json/landmark_data.json");
const landmark_data = await response.json();
// Loop JSON to get landmark data
for (item of landmark_data) {
const marker = L.marker([item.latitude, item.longitude], {
    icon: icon_landmark }).addTo(map);
let txt = "";
Object.keys(obj).forEach(key => {
let value = obj[key];

if (item.modal_link == key){
if(value == "yes"){
txt = `<button type="button" class="btn btn-warning btn-sm"
data-bs-toggle="modal"data-bs-target="#${item.modal_link}"
> ${item.modal_link} ${item.landmark_name} </button>`;
}

else{
txt = `<button type="button" class="btn btn-secondary btn-sm"
>${item.modal_link} ${item.landmark_name} </button>`;
}
}
});
marker.bindPopup(txt);
}
}
getLandmarks();