var map = L.map('map').setView([53.299697,-4.387321], 10);

osm = L.tileLayer('https://api.maptiler.com/maps/basic/{z}/{x}/{y}.png?key=LHlqrAvd3VUM4yZjqFDy', {
attribution: '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',
});
osm.addTo(map);

fetch('https://api.maptiler.com/data/b92719af-8d5b-4006-9631-3d8b13eaa1c6/features.json?key=g9ErshPDnj0LYYtEd10o')
	.then(function (responce) {
	return responce.json();
	})
	.then(function (data) {
      L.geoJSON(data).addTo(map);
	});
  