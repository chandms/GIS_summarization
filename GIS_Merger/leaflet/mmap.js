// Setup the map
var map = L.map('map', {drawControl: true}).fitWorld();

//create the tile layer with correct attribution
// var osmUrl='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
var osmUrl='tiles_kgp_nit/{z}/{x}/{y}.png';
var osmAttrib='Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors';
var osm = new L.TileLayer(osmUrl, {minZoom: 15, maxZoom: 18, attribution: osmAttrib});

// start the map in NIT Dgp
map.addLayer(osm);

// var gl = L.mapboxGL({
//         attribution: '<a href="https://www.maptiler.com/license/maps/" target="_blank">© MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">© OpenStreetMap contributors</a>',
//         accessToken: 'not-needed',
//         style: 'https://maps.tilehosting.com/c/0aab4c7d-013b-4f10-ab29-8e438f06ec1b/styles/basic/style.json?key=urAR9j6VqdctDxrgbJcr'
//       }).addTo(map);


// +++++ CHANGE THIS VIEW FOR NIT AND KGP +++++++++++++++++++++++++++++

// NIT:
map.setView(new L.LatLng(23.5499538, 87.2856928),15);

// KGP SALTLAKE:
//map.setView(new L.LatLng(22.57381,88.41790),18);

var contact_list =[];

contact_map = new Map();



try{
readCounter("counter.json","personified.json");
}
catch(err){
    console.log("counter file "+err);
}

try{
readCluster("clustermap.geojson");
}
catch(err){
    console.log("cluester file" + err);
}



function clearMap() {
    for (i in map._layers) {
    if (map._layers[i].options.format == undefined) {
        try {
            map.removeLayer(map._layers[i]);
        } catch (e) {
            console.log("problem with " + e + map._layers[i]);
        }
    }
}

// start the map in NIT Dgp
map.addLayer(osm);

// var gl = L.mapboxGL({
//         attribution: '<a href="https://www.maptiler.com/license/maps/" target="_blank">© MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">© OpenStreetMap contributors</a>',
//         accessToken: 'not-needed',
//         style: 'https://maps.tilehosting.com/c/0aab4c7d-013b-4f10-ab29-8e438f06ec1b/styles/basic/style.json?key=urAR9j6VqdctDxrgbJcr'
//       }).addTo(map);


// +++++ CHANGE THIS VIEW FOR NIT AND KGP +++++++++++++++++++++++++++++

// NIT:
map.setView(new L.LatLng(23.5499538, 87.2856928),15);
}

function getRandomColor() {
  var letters = '0123456789ABCDEF';
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

//////////////////////////

function readVideo(file)
{
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    var res=0;
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                var allText = rawFile.responseText;
               // console.log("chandrika  "+allText);
                var obj = JSON.parse(allText);
                res= obj['video'];
                
               // alert(allText);
            }
        }
    }
    rawFile.send(null);
    return res;
}
function readAudio(file)
{
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    var res=0;
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                var allText = rawFile.responseText;
                //console.log("chandrika  "+allText);
                var obj = JSON.parse(allText);
                res= obj['audio'];
                
               // alert(allText);
            }
        }
    }
    rawFile.send(null);
    return res;
}
function readImage(file)
{
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    var res=0;
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                var allText = rawFile.responseText;
                //console.log("chandrika  "+allText);
                var obj = JSON.parse(allText);
                res= obj['image'];
                
               // alert(allText);
            }
        }
    }
    rawFile.send(null);
    return res;
}
function readMap(file)
{
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    var res=0;
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                var allText = rawFile.responseText;
                //console.log("chandrika  "+allText);
                var obj = JSON.parse(allText);
                res= obj['sum'];
                
               // alert(allText);
            }
        }
    }
    rawFile.send(null);
    return res;
}
function readText(file)
{
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    var res=0;
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                var allText = rawFile.responseText;
                //console.log("chandrika  "+allText);
                var obj = JSON.parse(allText);
                res= obj['text'];
                
               // alert(allText);
            }
        }
    }
    rawFile.send(null);
    return res;
}

function readContact(file)
{
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    var res=0;
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                var allText = rawFile.responseText;
                //console.log("chandrika  "+allText);
                var obj = JSON.parse(allText);
                res= obj['pgp'].length;
                
               // alert(allText);
            }
        }
    }
    rawFile.send(null);
    return res;
}









///////////////////////////
function readCounter(file,file2)
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
                //console.log("chandrika  "+allText);
                
                var obj = JSON.parse(allText);
                //console.log(obj['video']);
                document.getElementById('videoCount').textContent="Videos : "+obj['video'];
                document.getElementById('imageCount').textContent="Images : "+obj['image'];
                document.getElementById('audioCount').textContent="Audios : "+obj['audio'];
                document.getElementById('contactCount').textContent="Contacts : "+obj['pgp'].length;
                document.getElementById('mapCount').textContent="Maps : "+obj['sum'];
                document.getElementById('textCount').textContent="Texts : "+obj['text'];
                
                contact_list=obj['pgp'];
                console.log(contact_list);

                var rfile = new XMLHttpRequest();
                rfile.open("GET",file2,false);
                rfile.onreadystatechange = function()
                {
                    if(rfile.readyState == 4)
                    {
                        if(rfile.status == 200 || rfile.status==0)
                        {
                            var content = rfile.responseText;
                            var ob= JSON.parse(content);
                            for(var con in contact_list)
                            {
                                var st= contact_list[con];
                                contact_map[st]=ob[st][0]+" "+ob[st][1]+" "+ob[st][2]+" "+ob[st][3];
                            }
                        }
                    }
                }
                rfile.send(null);
               
               
               
            }
        }
    }
    rawFile.send(null);
    
}

/// Summary per person
function information()
{
    var contact_no= document.getElementById('myContactNo').value;
    var res="";
    console.log("pupul My contact = ",contact_no);
    console.log(typeof(contact_no),contact_no);
    for (var k in contact_map)
    {
        if(contact_no==k)
            console.log("true");
        console.log(k,contact_map[k]);
    }
    if(contact_no!= "")
    {
        res=contact_map[contact_no];

    }
    else
        console.log("No given value");
    return res;
}
function getCurrentVersion(file)
{
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    var val=0;
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                var allText = rawFile.responseText;
                var lines = allText.split('\n');
                var len=lines.length-2;
                var vers = JSON.parse(lines[len]);
                val = vers.version;
                
            }
        }
    }
    rawFile.send(null); 
    return val;
}
function getTime(file,ind)
{
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    var val="";
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                var allText = rawFile.responseText;
                var lines = allText.split('\n');
                var real_index = ind -1;
                val = lines[real_index].split('%')[0];
                
            }
        }
    }
    rawFile.send(null); 
    return val;
}

function readTextFile(file,version)
{
    console.log("got = ",version);
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    clearMap();
    var MyMap = new Map();
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                var allText = rawFile.responseText;
                var lines = allText.split('\n');
                var real_index = version-1;
                var jsobj = lines[real_index];
                var object = JSON.parse(jsobj);

                var no_of_obj = object.jsonObjects.length;
                for (var id = 0;id<no_of_obj;id ++)
                {
                    var flag = object.jsonObjects[id].flag;
                    if (flag == "map")
                    {
                        var metadata = object.jsonObjects[id].metadata;
                        var pos = object.jsonObjects[id].position.split(',');
                        if (pos in MyMap)
                            MyMap[pos] = MyMap[pos]+"<br>"+"map"+" = "+ "<a target='_blank' href='viewer.html?file_name=" + metadata + "' >"  + "<img src='"+"./sync/SurakshitMap/"+metadata+"'>" + "</a>";
                        else
                            MyMap[pos] = "map"+" = "+ "<a target='_blank' href='viewer.html?file_name=" + metadata + "' >"  + "<img src='"+"./sync/SurakshitMap/"+metadata+"'>" + "</a>";

                        var array = [];
                        var cord = object.jsonObjects[id].coordinates.split(',');
                        for(var ln=0;ln<cord.length;ln++)
                        {
                            latlong = cord[ln].split(' ');
                            var sarray=[];
                            sarray.push(latlong[0]);
                            sarray.push(latlong[1]);
                            array.push(sarray);

                        }
                        var polygon = L.polygon(array, {color: 'red'}).addTo(map);
                    }
                    else if(flag == "normal")
                    {
                        var media_type= "";
                        var metadata = object.jsonObjects[id].metadata;
                        if(metadata.endsWith('.mp4'))
                            media_type="video";
                        else if(metadata.endsWith('.jpeg'))
                            media_type="image";
                        else
                            media_type="audio";

                        letter = object.jsonObjects[id].position.split(',');
                        if(letter in MyMap)
                        {
                            if(media_type=='image')
                                MyMap[letter]=MyMap[letter]+"<br>"+media_type+" = "+ "<a target='_blank' href='viewer.html?file_name=" + metadata + "' >"  + "<img src='"+"./sync/SurakshitImages/"+metadata+"'>" + "</a>";
                            else if(media_type=='video')
                                MyMap[letter]=MyMap[letter]+"<br>"+media_type+" = "+ "<video width='160' height='120' controls='controls' poster='back_ground.jpeg'> <source src='"+"./sync/SurakshitVideos/"+metadata+"' type='video/mp4'>Bummer, your  browser does not support the video tag.</video>";
                            else
                                MyMap[letter]=MyMap[letter]+"<br>"+media_type+" = "+ "<audio  controls='controls' autoplay > <source src='"+"./sync/SurakshitAudio/"+metadata+"' type='audio/3gp'>Bummer, your  browser does not support the audio tag.</audio>";
                        }
                        else
                        {
                            if(media_type=='image')
                                MyMap[letter]=media_type+" = "+ "<a target='_blank' href='viewer.html?file_name=" + metadata + "' >"  + "<img src='"+"./sync/SurakshitImages/"+metadata+"'>" + "</a>";
                            else if(media_type=='video')
                                MyMap[letter]=media_type+" = "+ "<video width='160' height='120' controls='controls' poster='back_ground.jpeg'> <source src='"+"./sync/SurakshitVideos/"+metadata+"' type='video/mp4'>Bummer, your  browser does not support the video tag.</video>";
                            else
                                MyMap[letter]=media_type+" = "+ "<audio controls='controls' autoplay > <source src='"+"./sync/SurakshitAudio/"+metadata+"' type='audio/3gp'>Bummer, your  browser does not support the audio tag.</audio>";
                        }
                    }
                    else if (flag == "cluster")
                    {
                        metadata = object.jsonObjects[id].metadata;
                        pos = object.jsonObjects[id].position.split(',');
                        if(pos in MyMap)
                            MyMap[pos]=MyMap[pos]+"<br>"+"map"+" = "+ "<a target='_blank' href='viewer.html?file_name=" + metadata + "' >"  + "<img src='"+"./sync/SurakshitMap/"+metadata+"'>" + "</a>";
                        else
                            MyMap[pos]="map"+" = "+ "<a target='_blank' href='viewer.html?file_name=" + metadata + "' >"  + "<img src='"+"./sync/SurakshitMap/"+metadata+"'>" + "</a>";

                        var array = [];
                        var cord = object.jsonObjects[id].coordinates.split(',');
                        for(var ln=0;ln<cord.length;ln++)
                        {
                            latlong = cord[ln].split(' ');
                            var sarray=[];
                            sarray.push(latlong[0]);
                            sarray.push(latlong[1]);
                            array.push(sarray);

                        }
                        var pops="";
                        var my_text="";
                        var txt=0,vd=0,im=0,ad=0;
                        var polygon = L.polygon(array, {color: 'green'}).addTo(map);
                        var media = object.jsonObjects[id].clusterString;
                        var len_med = object.jsonObjects[id].clusterString.length;
                        for (var ii= 0 ;ii<len_med;ii++)
                        {
                            if(media[ii].endsWith('.3gp'))
                                {
                                    ad++;
                                    pops=pops+"<audio controls='controls' autoplay > <source src='"+"./sync/SurakshitAudio/"+media[ii]+"' type='audio/3gp'>Bummer, your  browser does not support the audio tag.</audio>";
                                }
                            else if(media[ii].endsWith('.mp4'))
                                {
                                    if (ad>0)
                                    {
                                        pops=pops+"<br><br>";
                                        ad=0
                                    }
                                    vd++;
                                    pops=pops+ "<video width='160' height='120' controls='controls' poster='back_ground.jpeg'> <source src='"+"./sync/SurakshitVideos/"+media[ii]+"' type='video/mp4'>Bummer, your  browser does not support the video tag.</video>";
                                }
                            else if(media[ii].endsWith('.jpeg'))
                                {
                                    if (vd>0)
                                    {
                                        pops=pops+"<br><br>";
                                        vd=0
                                    }
                                    im++;
                                    pops=pops+"<a target='_blank' href='viewer.html?file_name=" + media[ii] + "' >" + "<img src='"+"./sync/SurakshitImages/"+media[ii]+"'>"+ "</a>";

                                }
                            else
                                {
                                    txt++;
                                    my_text=my_text+media[ii]+"<br>";
                                }
                        
                        }
                        if(txt!=0)
                            {
                                pops=pops+"<br>"+'<a  target="_blank" href="textTab.html?text='+my_text+'">TEXT SUMMARY</a>'+"<br>";
                            }
                        polygon.bindPopup(pops);


                    }
                
                }

                for(latlon in MyMap)
                {
                    var plot = L.marker([latlon[0],latlon[1]]).addTo(map);
                    plot.bindPopup(MyMap[kt]);
                }
            }
        }
    }
    rawFile.send(null); 
}
function readCluster(file)
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
                var col=getRandomColor();
                for(var i = 0;i < lines.length;i++){
                      if(lines[i]!="")
                      {
                      word= lines[i].split('%');
                        var er=word[3];
                        var op=0.5;
                        if(word[3]>=50)
                        {
                           er=word[3]*2;
                           op=0.1;
                           
                        }
                        console.log(word[0],word[1],word[3]);
                        var circle = L.circle([word[0],word[1]], {
                            color: col,
                            fillColor: col,
                            fillOpacity: op,
                            radius: er
                        }).addTo(map);
                        circle.bindPopup(word[2]);
                        if(word[3]>=50)
                        {
                           col=getRandomColor();
                           
                        }

                    }
                      
                    }
               // alert(allText);
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
