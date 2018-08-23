// Setup the map
var map = L.map('map', {drawControl: true}).fitWorld();

// create the tile layer with correct attribution
// var osmUrl='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
// var osmAttrib='Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors';
// var osm = new L.TileLayer(osmUrl, {minZoom: 2, maxZoom: 18, attribution: osmAttrib});       

// // start the map in NIT Dgp
// map.setView(new L.LatLng(23.5499538, 87.2856928),15);
// map.addLayer(osm);

var gl = L.mapboxGL({
        attribution: '<a href="https://www.maptiler.com/license/maps/" target="_blank">© MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">© OpenStreetMap contributors</a>',
        accessToken: 'not-needed',
        style: 'https://maps.tilehosting.com/c/0aab4c7d-013b-4f10-ab29-8e438f06ec1b/styles/basic/style.json?key=urAR9j6VqdctDxrgbJcr'
      }).addTo(map);
map.setView(new L.LatLng(23.5499538, 87.2856928),15);

readTextFile("./../merged.geojson");

function readTextFile(file)
{
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                var allText = rawFile.responseText;
                var lines = allText.split('\n');
                for(var i = 0;i < lines.length;i++){
                      word= lines[i].split(',');
                      var array=[];
                      for(var t = 0;t < word.length;t++)
                      {
                        latlong=word[t].split(' ');
                        //var marker = L.marker([word[0],word[1]]).addTo(map); 
                        var sarray=[];
                        sarray.push(latlong[0]);
                        sarray.push(latlong[1]);
                        array.push(sarray); 
                      }
                      var polygon = L.polygon(array, {color: 'red'}).addTo(map);
                     //console.log(word[0]);
                      
                    }
                alert(allText);
            }
        }
    }
    rawFile.send(null);
}
function onLocationFound(e) {
    var radius = e.accuracy / 2;

    L.marker(e.latlng).addTo(map)
    .bindPopup("You are within " + radius + " meters from this point").openPopup();

    L.circle(e.latlng, radius).addTo(map);
}

map.on('locationfound', onLocationFound);


var ourCustomControl = L.Control.extend({ 
    options: {
        position: 'topright' 
//control position - allowed: 'topleft', 'topright', 'bottomleft', 'bottomright'
},
onAdd: function (map) {
    var container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom');
    container.style.backgroundColor = '#8a8a8a';
    container.style.backgroundImage = "url('images/marker-icon.png')";
    container.style.backgroundSize = "30px";
    container.style.width = '30px';
    container.style.height = '30px';
    container.onclick = function(){
        console.log('goTolocation');
        map.locate({setView: true, maxZoom: 18});
    }
    return container;
},

});
map.addControl(new ourCustomControl());



// Plot Existing Data
// db.collection("gisObjects").get().then(function(querySnapshot) {
//     querySnapshot.forEach(function(doc) {
//         // doc.data() is never undefined for query doc snapshots
//         // console.log(doc.id, " => ", doc.data());
//         // console.log(doc.data().GeoJSON);
//         // L.geoJSON(JSON.parse(doc.data().GeoJSON)).addTo(map);
//         var GeoJSON = JSON.parse(doc.data().GeoJSON);
//         drawGeoJSON(GeoJSON);
// });
// });

// GeoJSON Drawer
function drawGeoJSON(GeoJSON){
    var thisLayer = L.geoJSON(GeoJSON, {});
    thisLayer.addTo(map);
    thisLayer.bindPopup(
            function (layer) {
            return GeoJSON.properties.description;
        })
    thisLayer.bindTooltip(GeoJSON.properties.description, {
        permanent: true,
        opacity: 0.9,
        direction: 'top'
    }).openTooltip();
}



// Draw Event
var geojsondrawn;
map.on(L.Draw.Event.CREATED, function (e) {
    var type = e.layerType,
    layer = e.layer;
//     if (type === 'marker') {
// // Do marker specific actions
// }

    geojsondrawn = e.layer.toGeoJSON();
    geojsondrawn.properties.type = type;
//  Do whatever else you need to. (save to db; add to map etc)
    openDescriptionInputModal();

});


// Save GIS
// function saveGIS(geojson, date, type, description_input){
//     db.collection("gisObjects").add({
//         GeoJSON: JSON.stringify(geojson),
//         timestamp: date,
//         type: type,
//         description: description_input
//     })
//     .then(function(docRef) {
//         console.log("Document written with ID: ", docRef.id);
//         alert("data saved successfully..");
//         drawGeoJSON(geojson);
//         closeModal();
//     })
//     .catch(function(error) {
//         console.error("Error adding document: ", error);
//         closeModal();
//     });
// }



// Description Inpur Modal
var modal = document.getElementById('descriptionInputModal');
var saveButton = document.getElementById('save-button');
var cancelButton = document.getElementById('cancel-button');
var descriptionTextArea = document.getElementById('description-input');

function openDescriptionInputModal(){
    console.log("Here");
    modal.style.display = "block";
}


// When user clicks save
saveButton.onclick = function(){
    console.log("SAVEEE!!");
    description_input = descriptionTextArea.value;
    if(description_input == ""){
        alert("Enter valid description");
    }else{
        geojsondrawn.properties.description = description_input;
        console.log("saving.." + description_input + geojsondrawn);
        console.log(geojsondrawn);
        var date = Date().toString();
        saveGIS(geojsondrawn, date, geojsondrawn.properties.type, description_input);
    }

}

// When user clicks cancel
cancelButton.onclick = function(){
    console.log("CANCEL!!");
    closeModal();
}



// Close Modal
function closeModal(){
    descriptionTextArea.value = "";
    geojsondrawn = "";
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        closeModal();
    }
}




//var marker = L.marker([23.54471714689103 , 87.29008785958843]).addTo(map);
// When the user clicks on <span> (x), close the modal
var span = document.getElementsByClassName("close")[0];
span.onclick = function() {
    closeModal();
}
