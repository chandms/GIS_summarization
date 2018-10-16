

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
                for(var i = 0;i < lines.length;i++)
                {
                	if(lines[i]!="")
                	{
                		word= lines[i].split('%');
                		if(word[1]==version)
                		{

                			if(word[2]=="map")
                			{
                				letter = word[4].split(',');
                            	if(letter in MyMap)
                                	MyMap[letter]=MyMap[letter]+"<br>"+"map"+" = "+ "<a target='_blank' href='viewer.html?file_name=" + word[3] + "' >"  + "<img src='"+"./sync/SurakshitMap/"+word[3]+"'>" + "</a>";
                            	else
                                	MyMap[letter]="map"+" = "+ "<a target='_blank' href='viewer.html?file_name=" + word[3] + "' >"  + "<img src='"+"./sync/SurakshitMap/"+word[3]+"'>" + "</a>";
	                            var array = [];
	                            cord = word[0].split(',');
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
                			else if(word[2]=="normal")
                			{
                				var media_type= "";
		                        if(word[3].endsWith('.mp4'))
		                            media_type="video";
		                        else if(word[3].endsWith('.jpeg'))
		                            media_type="image";
		                        else
		                            media_type="audio";
		                        console.log("media type = ",media_type);
		                        letter = word[0].split(' ');
		                        if(letter in MyMap)
		                        {
		                            if(media_type=='image')
		                                MyMap[letter]=MyMap[letter]+"<br>"+media_type+" = "+ "<a target='_blank' href='viewer.html?file_name=" + word[3] + "' >"  + "<img src='"+"./sync/SurakshitImages/"+word[3]+"'>" + "</a>";
		                            else
		                                MyMap[letter]=MyMap[letter]+"<br>"+media_type+" = "+ "<a target='_blank' href='viewer.html?file_name=" + word[3] + "' >"  + word[3] + "</a>";
		                                

		                        }
		                        else
		                        {
		                            if(media_type=='image')
		                                MyMap[letter]=media_type+" = "+ "<a target='_blank' href='viewer.html?file_name=" + word[3] + "' >"  + "<img src='"+"./sync/SurakshitImages/"+word[3]+"'>" + "</a>";
		                            else
		                                MyMap[letter]=media_type+" = "+ "<a target='_blank' href='viewer.html?file_name=" + word[3] + "' >"  + word[3] + "</a>";
		                        }
                			}
                			else if(word[2]=="cluster")
                			{
                				letter = word[4].split(',');
		                        if(letter in MyMap)
		                            MyMap[letter]=MyMap[letter]+"<br>"+"map"+" = "+ "<a target='_blank' href='viewer.html?file_name=" + word[3] + "' >"  + "<img src='"+"./sync/SurakshitMap/"+word[3]+"'>" + "</a>";
		                        else
		                            MyMap[letter]="map"+" = "+ "<a target='_blank' href='viewer.html?file_name=" + word[3] + "' >"  + "<img src='"+"./sync/SurakshitMap/"+word[3]+"'>" + "</a>";
		                        console.log("got map ",word[3]);

		                        var array = [];
		                        cord = word[0].split(',');
		                        var maxLat=-90,maxLon=-180,minLat=90,minLon=180;
		                        for(var ln=0;ln<cord.length;ln++)
		                        {
		                            latlong = cord[ln].split(' ');
		                            var sarray=[];
		                            sarray.push(latlong[0]);
		                            sarray.push(latlong[1]);
		                            array.push(sarray);
		                            maxLat=Math.max(maxLat,latlong[0]);
		                            maxLon=Math.max(maxLon,latlong[1]);
		                            minLat = Math.min(minLat,latlong[0]);
		                            minLon= Math.min(minLon,latlong[1]);

		                        }
		                        var centLat=(maxLat+minLat)/2;
		                        var centLon=(minLon+maxLon)/2;
		                        var polygon = L.polygon(array, {color: 'green'}).addTo(map);
		                        var media = word[5].split('::');

		                        var pops="";
		                        for(var jt=0;jt<media.length;jt++)
		                        {
		                            if(media[jt].endsWith('.mp4'))
		                            {
		                                pops=pops+"video = "+ "<a target='_blank' href='viewer.html?file_name=" + media[jt] + "' >"  + media[jt] + "</a>";
		                                pops=pops+"<br>";
		                            }
		                            else if(media[jt].endsWith('.jpeg'))
		                            {
		                                pops=pops+"image = "+ "<a target='_blank' href='viewer.html?file_name=" + media[jt] + "' >" + "<img src='"+"./sync/SurakshitImages/"+media[jt]+"'>"+ "</a>";
		                                pops=pops+"<br>";
		                            }

		                            else if(media[jt].endsWith('.3gp'))
		                            {
		                                pops=pops+"audio = "+ "<a target='_blank' href='viewer.html?file_name=" + media[jt] + "' >"  + media[jt] + "</a>";
		                                pops=pops+"<br>";
		                            }
		                            else
		                            {
		                                pops=pops+"text = "+media[jt]+"<br>";
		                            }
		                        }
		                        console.log(maxLat,maxLon,minLat,minLon);
		                        console.log("centre", centLat, centLon);
		                        var mark = cord[0].split(' ');
		                        var media_plot = L.circle([mark[0],mark[1]],{color:'black',radius:2}).addTo(map);
		                        media_plot.bindPopup(pops);
                			}
                		}
                		else if(word[1]>version)
                			break;
                	}
                }

                for(kt in MyMap)
                {
                        
                    latlon=kt.split(',');
                    var plot = L.marker([latlon[0],latlon[1]]).addTo(map);
                    plot.bindPopup(MyMap[kt]);

                }
                
            }
        }
    }
    rawFile.send(null); 
    return val;
}