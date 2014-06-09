refreshSectionID = null;// temporary id of expanded section
xml = null;
tableData = null;
// creates map
function loadMap(){

	// keeps track of window resolution proportion to know when to resize
	mapResProportion = window.innerHeight/window.innerWidth;

	// rain plan variable
	usingRainPlan = true;

	// main svg in map container
	var map = d3.select("#MapContainer");
	width = document.getElementById("MapContainer").clientWidth;
	height = Math.max(window.innerHeight*.8, width*.5);
	if (window.innerHeight>window.innerWidth) height = Math.max(height, width*1.5);
	var svg = map.append("svg").attr("height", height).attr("id", "MapSVG");
	svg.attr("width", width);

	// background
	svg.append("rect")
		.attr("width", width)
		.attr("height",height)
		.attr("fill","#DDDDDD")
		.attr("onclick", "revertMap()")
		.attr("id", "MapBackground");

	// Details on Demand
	var detailsHeight = 105;
	svgDetails = map.append("svg")
		.attr("id", "detailsOnDemand")
		.attr("width", width)
		.attr("height", detailsHeight);
	map.select("#MapSVG").each(function(){this.parentNode.appendChild(this);});

	svgDetails.append("rect")
		.attr("width", width)
		.attr("height", detailsHeight)
		.attr("id", "svgDetailsBackground")
		.attr("fill", "#DDDDDD");

	detailsMargin = 10;
	detailsX = detailsMargin;
	detailsY = detailsMargin;
	detailsW = width-detailsMargin*2;
	detailsH = detailsHeight-detailsMargin*2;
	detailsDY = 25;
	svgDetails.append("rect")
		.attr("x", detailsX)
		.attr("y", detailsY)
		.attr("width", detailsW)
		.attr("height", detailsH)
		.attr("fill", "white")
		.attr("stroke", "black")
		.attr("id", "svgDetailsBox")
		.attr("stroke-width", 2);

	textUnexpanded = ["Click on a zone to expand it.","This map is best viewed on:"," Chrome, Safari, or Firefox"];
	textExpanded = ["Click on a table to see team details or", "Click outside the section to unexpand"];

	// arrays of text elements in details
	detailsTitleText = [];
	detailsBodyText = [];
	detailsBodyLink = svgDetails.append("a");
	for (var i=1; i<4; i++){
		detailsTitleText.push(svgDetails.append("text")
			.attr("id", "detailsTitle"+i)
			.attr("class", "detailsTitleText")
			.attr("x", detailsX+detailsW/2)
			.attr("y", detailsY + detailsDY*i));
		detailsBodyText.push(detailsBodyLink.append("text")
			.attr("id", "detailsBody"+i)
			.attr("class", "detailsBodyText")
			.attr("x", detailsMargin+5)
			.attr("y", detailsY + detailsDY*i)
			.attr("href", "/"));
	}
	replaceDetailsText(textUnexpanded, true);
	
	// svg elements and values for section animation handling
	gMap = svg.append("g").attr("id", "gMap");
	gStadium = gMap.append("g")
		.attr("id","gStadium")
		.attr("visibility", "hidden");
	arc = d3.svg.arc();
	currGSection = null;
	currTableRect = null;
	sections = [];
	hideableElements = [];
	transCenter = "translate("+(width/2)+","+(height/2)+")";
	sectExpanded = false;
	transTime = 200;
	sectionNum=1;

	var mapFileName = "static/data/mccamish-04-23-2014.xml";
	var tablesFileName = "static/data/tables-04-23-2014.tsv";
	if (usingRainPlan){
		mapFileName = "static/data/mccamishRain-04-23-2014.xml";
		tablesFileName = "static/data/tablesRain-04-23-2014.tsv";
	}
	
	// extract table info from tables.tsv
	if (tableData==null){
		d3.tsv(tablesFileName, function(data){
			tableData = data;
		});
	}

	// create map from xml file
	if (xml==null){
		d3.xml(mapFileName, function(data){
			xml = data.documentElement;
			analyzeXML();
		});
	}
	else analyzeXML();
}

// analyze each line of the XML file and populate SVG elements
function analyzeXML(){
	// value for positioning text in stadium
	var textOffsetY = window.getComputedStyle(document.getElementById("gStadium")).getPropertyValue("font-size");
	var textOffsetY = (+textOffsetY.substring(0,textOffsetY.length-2))/3;
	
	// values for positioning and sizing table
	textOffsetYTable = window.getComputedStyle(document.getElementById("gMap")).getPropertyValue("font-size");
	textOffsetYTable = (+textOffsetYTable.substring(0,textOffsetYTable.length-2))/3;
	tableWidth = 30;
	tableHeight = 25;
	
	// Polygons
	var arr = xmlTag(xml, "polygon");
	for (var i=0; i<arr.length; i++){
		var arrPoints = xmlTag(arr[i], "point");
		var pts = [];
		var color = xmlAttr(arr[i], "color");
		for (var j=0; j<arrPoints.length; j++){
			pts.push(new Point(xmlAttr(arrPoints[j], "x"),xmlAttr(arrPoints[j], "y")));
		}
		var poly = new Polygon(pts, color);
		poly.drawPolygon(gStadium);
	}

	// Text
	arr = xmlTag(xml, "text");
	for (var i=0; i<arr.length; i++){
		gStadium.append("text")
			.attr("x", xmlAttr(arr[i], "x"))
			.attr("y", +xmlAttr(arr[i], "y")+textOffsetY)
			.attr("class", "mapStadiumText")
			.text(arr[i].textContent);
	}

	// sectionArc
	arr = xmlTag(xml, "sectionArc");
	for (var i=0; i<arr.length; i++){
		var currGSection = createSection(arr[i]);

		// Outdoor areas of the section
		arrOutdoor  = xmlTag(arr[i], "sectionArcOutdoor");
		for (var j=0; j<arrOutdoor.length; j++){

			var iRadius = +xmlAttr(arrOutdoor[j], "innerRadius");
			var oRadius = +xmlAttr(arrOutdoor[j], "outerRadius");
			var sAngle = radToAngle(xmlAttr(arrOutdoor[j], "startAngle"));
			var eAngle = radToAngle(xmlAttr(arrOutdoor[j], "endAngle"));
			
			// outdoor arc
			var outside = currGSection.append("path")
				.attr("fill", "white")
				.attr("stroke-width","10px")
				.attr("class", "mapSectionOutside")
				.datum({
					outerRadius: oRadius,
					innerRadius: iRadius,
					startAngle: sAngle,
					endAngle: eAngle,
				})
				.attr("d",arc);
		}
		// put main arc on top of outdoor section to prevent edge overlap
		currGSection.select(".mapSectionPath").each(function(){this.parentNode.appendChild(this);});
		

		// Extensions to indoor sections beyond the main arc
		var arrExtensions = xmlTag(arr[i], "sectionArcExtension");
		var iRadius = +xmlAttr(arr[i], "outerRadius");
		var color = xmlAttr(arr[i], "color");
		for (var j=0; j<arrExtensions.length; j++){
			var oRadius = iRadius+ (+xmlAttr(arrExtensions[j], "dRadius"));
			var sAngle = radToAngle(xmlAttr(arrExtensions[j], "startAngle"));
			var eAngle = radToAngle(xmlAttr(arrExtensions[j], "endAngle"));
			
			// extension arc
			currGSection.append("path")
				.attr("fill", "white")
				.attr("stroke", color)
				.attr("stroke-width","10px")
				.datum({
					outerRadius: oRadius,
					innerRadius: iRadius,
					startAngle: sAngle,
					endAngle: eAngle,
				})
				.attr("d",arc);

			// covers up the color outline between the section and extension
			currGSection.append("path")
				.attr("fill", "white")
				.attr("stroke", "white")
				.attr("stroke-width","12px")
				.datum({
					outerRadius: iRadius+1,
					innerRadius: iRadius,
					startAngle: sAngle+.0218,// might be incorrect for some radii
					endAngle: eAngle-.0218,// might be incorrect for some radii
				})
				.attr("d",arc);
		}

		// Section Doors
		var arrDoors = xmlTag(arr[i], "sectionDoor"); 
		for (var j=0; j<arrDoors.length; j++){
			var iRadius = (+xmlAttr(arrDoors[j], "radius"));
			var oRadius = iRadius+1;
			var sAngle = radToAngle(xmlAttr(arrDoors[j], "startAngle"));
			var eAngle = radToAngle(xmlAttr(arrDoors[j], "endAngle"));

			currGSection.append("path")
				.attr("fill", "white")
				.attr("stroke", "#DDDDDD")
				.attr("stroke-width","12px")
				.attr("class", "mapSectionDoor")
				.datum({
					outerRadius: iRadius,
					innerRadius: iRadius,
					startAngle: sAngle,
					endAngle: eAngle
				})
				.attr("d",arc);
		}

		// Tables inside section
		var gTableCollection = currGSection.append("g").attr("class", "gTableCollection");
		var arrTables = xmlTag(arr[i], "tableArc");
		for (var j=0; j<arrTables.length; j++){
			var angle = radToAngle(xmlAttr(arrTables[j],"angle"));
			var radius = xmlAttr(arrTables[j],"radius");
			var x = Math.sin(angle)*radius-tableWidth/2;
			var y = -Math.cos(angle)*radius-tableHeight/2;
			var tableText = arrTables[j].textContent;
			
			// g for table
			var gTable = gTableCollection.append("g")
				.attr("info", tableText)
				.attr("class", "mapTable");
			// table rectangle
			var table = gTable.append("rect")
				.attr("x", x)
				.attr("y", y)
				.attr("width", tableWidth)
				.attr("height", tableHeight)
				.attr("class", "mapTableRect");
			// table rectangle rotation
			table.attr("transform", "rotate("+xmlAttr(arrTables[j],"angle")+" "+(x+tableWidth/2)+" "+(y+tableHeight/2)+")");

			// table text
			var text = gTable.append("text")
				.attr("x", +x+tableWidth/2)
				.attr("y", +y+tableHeight/2+textOffsetYTable)
				.attr("class", "mapTableText")
				.text(tableText);
			// onclick: details on demand
			[gTable].forEach(function(d){
				d.on("click", function(){
					if (this.parentNode.__data__.expanded){
						highlightTable(d);
						setTableDetails(d.attr("info"));
					}
				});
			});

		}

		// Arc Text inside section
		var arrText = xmlTag(arr[i], "sectionTextArc");
		for (var j=0; j<arrText.length; j++){
			var angle = radToAngle(xmlAttr(arrText[j],"angle"));
			var radius = xmlAttr(arrText[j],"radius");
			var x = Math.sin(angle)*radius;
			var y = -Math.cos(angle)*radius;

			var text = currGSection.append("text")
				.attr("x", x)
				.attr("y", y)
				.attr("font-size", "16px")
				.attr("class", "mapStadiumText")
				.text(arrText[j].textContent);

			text.attr("transform", "rotate("+xmlAttr(arrText[j],"angle")+" "+(x)+" "+(y)+")");
		}

		// Text inside section
		var arrText = xmlTag(arr[i], "sectionText");
		for (var j=0; j<arrText.length; j++){
			currGSection.append("text")
				.attr("x", xmlAttr(arrText[j], "x"))
				.attr("y", +xmlAttr(arrText[j], "y")+textOffsetY)
				.attr("font-size", xmlAttr(arrText[j], "font-size"))
				.attr("class", "mapStadiumText")
				.text(arrText[j].textContent);
		}

		// Section Strips on expand
		var stadiumSections = currGSection.append("g")
			.attr("class", "sectionStadiumStrips");
		var arrStadium = xmlTag(arr[i], "stadiumSection");
		var oRadius = +xmlAttr(arr[i], "innerRadius");
		var iRadius = oRadius-30;
		for (var j=0; j<arrStadium.length; j++){
			var sAngle = radToAngle(xmlAttr(arrStadium[j], "startAngle"));
			var eAngle = radToAngle(xmlAttr(arrStadium[j], "endAngle"));
			var angle = (sAngle+eAngle)/2;
			var radius = iRadius+(oRadius-iRadius)*.1;
			var x = Math.sin(angle)*radius;
			var y = -Math.cos(angle)*radius;
			angle = ((+xmlAttr(arrStadium[j], "startAngle"))+(+xmlAttr(arrStadium[j], "endAngle")))/2;

			// section strip path
			stadiumSections.append("path")
				.attr("fill", "white")
				.attr("stroke", color)
				.attr("stroke-width",5)
				.datum({
					outerRadius: oRadius,
					innerRadius: iRadius,
					startAngle: sAngle,
					endAngle: eAngle,
				})
				.attr("d",arc);

			// section strip text
			stadiumSections.append("text")
				.attr("x",x)
				.attr("y",y)
				.text(arrStadium[j].textContent)
				.attr("transform", "rotate("+angle+" "+x+" "+y+")");
		}

		// add to sections array
		if (xmlAttr(arr[i],"expandable")==="true") sections.push(currGSection);
		hideableElements.push(currGSection);
	}

	// sectionRect
	arr = xmlTag(xml, "sectionRect");
	for (var i=0; i<arr.length; i++){
		var x = +xmlAttr(arr[i], "x");
		var y = +xmlAttr(arr[i], "y");

		var currGSection = createSectionRect(
			xmlAttr(arr[i], "color"),
			x, y,
			+xmlAttr(arr[i], "width"),
			+xmlAttr(arr[i], "height"));
		if (xmlAttr(arr[i],"expandable")==="true") sections.push(currGSection);
		hideableElements.push(currGSection);

		// tables in rectangle section
		var gTableCollection = currGSection.append("g").attr("class", "gTableCollection");
		var arrTables = xmlTag(arr[i], "tableRect");
		for (var j=0; j<arrTables.length; j++){
			var dx = +xmlAttr(arrTables[j], "dx");
			var dy = +xmlAttr(arrTables[j], "dy");
			var tableText = arrTables[j].textContent;
			// g for table
			var gTable = gTableCollection.append("g")
				.attr("info", tableText)
				.attr("class", "mapTable");
			// table rectangle
			var table = gTable.append("rect")
				.attr("x", dx+x)
				.attr("y", dy+y)
				.attr("width", tableHeight)
				.attr("height", tableWidth)
				.attr("class", "mapTableRect");

			// table text
			var text = gTable.append("text")
				.attr("x", dx+x+tableHeight/2+textOffsetYTable/2)
				.attr("y", dy+y+tableWidth/2)
				.attr("class", "mapTableText")
				.text(tableText);

			// onclick: details on demand
			[gTable].forEach(function(d){
				d.on("click", function(){
					if (this.parentNode.__data__.expanded){
						highlightTable(d);
						setTableDetails(d.attr("info"));
					}
				});
			});

		}

		// Text inside section
		var arrText = xmlTag(arr[i], "sectionText");
		for (var j=0; j<arrText.length; j++){
			currGSection.append("text")
				.attr("x", xmlAttr(arrText[j], "x"))
				.attr("y", +xmlAttr(arrText[j], "y")+textOffsetY)
				.attr("font-size", xmlAttr(arrText[j], "font-size"))
				.attr("class", "mapStadiumText")
				.text(arrText[j].textContent);
		}

	}

	// create onclick action for each section
	hideableElements.push(gStadium);
	centerMap();
	applySectionsOnClick();

	if (refreshSectionID!=null) reexpandSection();

}

// returns array of elements in xml with tag name
function xmlTag(xml, tag){
	return xml.getElementsByTagName(tag);
}

// returns attribute value of xml element
function xmlAttr(xml, attr){
	return xml.attributes.getNamedItem(attr).nodeValue;
}

function radToAngle(angle){
	return (angle)*Math.PI/180.
}

// scale and center map appropriately
function centerMap(){
	// margin rectangle
	var box = document.getElementById("gMap").getBBox();
	var margin = 30;
	box.x-=margin/2;
	box.y-=margin/2;
	box.width+=margin;
	box.height+=margin;
	var scale = Math.min(height/(box.height), width/(box.width));
	transX = width/2-(box.x+box.width/2)*scale;
	transY = height/2-(box.y+box.height/2)*scale;
	
	gMap.transition()
		.duration(0)
		.each("end", function(){gStadium.attr("visibility", "visible");});
	gMap.attr("transform", "translate("+transX+","+transY+") scale("+scale+")");

}

// converts parallel x and y value lists into a Polygon
function polyFromVals(xVals, yVals, color){
	points = [];
	for (i=0; i<xVals.length; i++) points.push(new Point(xVals[i], yVals[i]));
	return new Polygon(points, color);
}

// class structure for single (x,y) coordinate
function Point(x,y){
	this.x = +x;
	this.y = +y;
}

// class structure containing a polygon as list of points, a color, and the function to draw that polygon
function Polygon(points, color){
	this.points = points;
	this.color = color;
	this.drawPolygon = drawPolygon;
}

// draws a Polygon
function drawPolygon(g){
	pointString = "";
	for (i=0; i<this.points.length; i++){
		p = this.points[i];
		pointString += p.x.toString()+","+p.y.toString()+" ";
	}
	poly = g.append("polygon")		
		.attr("points", pointString)
		.attr("fill", this.color)
		.attr("col", this.color)
}

// creates a section with onclick transition
function createSection(xmlSection){
	var color = xmlAttr(xmlSection, "color");
	var sExpandable = xmlAttr(xmlSection, "expandable")==="true";
	var sInnerRadius = +xmlAttr(xmlSection, "innerRadius");
	var sOuterRadius = +xmlAttr(xmlSection, "outerRadius");
	var sStartAngle = radToAngle(xmlAttr(xmlSection, "startAngle"));
	var sEndAngle = radToAngle(xmlAttr(xmlSection, "endAngle"));

	// create g element to contain section
	var gSection = gMap.append("g")
		.attr("id", "section"+sectionNum)
		.attr("class", "gSection")
		.datum({
			expanded:false,
			startAngle: sStartAngle,
			endAngle: sEndAngle
		});

	// create section
	gSection.append("path")
		.attr("fill","white")
		.attr("stroke", color)
		.attr("stroke-width", "10px")
		.attr("class", "mapSectionPath")

		.datum({
			outerRadius: sOuterRadius,
			innerRadius: sInnerRadius,
			startAngle: sStartAngle,
			endAngle: sEndAngle,
		})
		.attr("d",arc);

	sectionNum+=1;
	return gSection;
}

function createSectionRect(color, x, y, w, h){
	// create g element to contain section
	gSection = gMap.append("g")
		.attr("id", "section"+sectionNum)
		.datum({expanded:false});
	
	section = gSection.append("rect")
		.attr("fill", color)
		.attr("class", "mapSectionRect")
		.attr("x",x)
		.attr("y",y)
		.attr("width",w)
		.attr("height",h)
		.attr("stroke-width", "5px")
		.attr("stroke", "black");
	
	sectionNum+=1;
	return gSection;		
}

// create onclick event for each section
function applySectionsOnClick(){
	
	var box = document.getElementById("gMap").getBBox();
	mapScale = Math.min(height/box.height, width/box.width);
	var rect = document.getElementById("MapBackground").getBBox();
	rotSideways = rect.height>rect.width;

	// create onclick transition
	sections.forEach(function(d){
		
		// determine transform parameters
		var box = document.getElementById(d.attr("id")).getBBox();
		var data = d.datum();

		// calculate new scale by looking at bounding rectangle of section when expanded
		var x = box.x+box.width/2;
		var y = box.y+box.height/2;
		var rotAngle = 0;
		if (data.startAngle!=null) rotAngle = -(data.startAngle+data.endAngle)/2*180/Math.PI;
		else if (box.height>box.width) rotAngle = -90;
		if (rotSideways){
			if (rotAngle>-180) rotAngle += 90;
			else rotAngle -= 90;
		}
		var trans = "rotate("+rotAngle+","+x+","+y+")";
		d.attr("transform", trans);

		var tableCollection = document.getElementById(d.attr("id"))
			.getElementsByClassName("gTableCollection")[0]
			.getElementsByClassName("mapTable");

		// Compute width and height of section using the section table positions
		var currTableBox = tableCollection[0].getBoundingClientRect();
		var minTableX = currTableBox.left;
		var maxTableX = currTableBox.left;
		var minTableY = currTableBox.top;
		var maxTableY = currTableBox.top;
		for (var i=0; i<tableCollection.length; i++){
			var currTableBox = tableCollection[i].getBoundingClientRect();
			minTableX = Math.min(minTableX, currTableBox.left);
			maxTableX = Math.max(maxTableX, currTableBox.left);
			minTableY = Math.min(minTableY, currTableBox.top);
			maxTableY = Math.max(maxTableY, currTableBox.top);
		}
		var sectionWidth = maxTableX-minTableX;
		var sectionHeight = maxTableY-minTableY;

		data.scale=Math.min(height/sectionHeight*.8, width/sectionWidth*.8);
		data.bigX = -x;
		if (!rotSideways === box.height>box.width) data.bigX += (width/2-transX);
		data.bigY = -y;
		d.attr("transform", "");

		d.on("click", function(){
			data = d.datum();
			if (!sectExpanded && !data.expanded){
				refreshSectionID = d.attr("id");

				// update details on demand
				replaceDetailsText(textExpanded, true);

				this.parentNode.appendChild(this);// move section to top
				data.expanded = true;
				sectExpanded = true;
				var rotAngle = 0;
				if (data.startAngle!=null) rotAngle = -(data.startAngle+data.endAngle)/2*180/Math.PI;
				else if (box.height>box.width) rotAngle = -90;
				if (rotSideways){
					if (rotAngle>-180) rotAngle += 90;
					else rotAngle -= 90;
				}
				var x = box.x+box.width/2;
				var y = box.y+box.height/2;
				var trans = "scale("+data.scale+") translate("+data.bigX+","+data.bigY+") rotate("+rotAngle+","+x+","+y+")";
				d.transition()
					.duration(transTime)
					.ease("linear")
					.attr("transform", trans);
				
				d.selectAll(".mapTableText").call(function(tables){
					var tables = tables[0];
					for (var i=0; i<tables.length; i++){						
						var x = (+tables[i].attributes.getNamedItem("x").value);
						var y = (+tables[i].attributes.getNamedItem("y").value)-textOffsetYTable;
						var tr = "rotate("+(-rotAngle)+","+x+","+y+")";
						tables[i].setAttribute("transform", tr);
					}
				})

				d.selectAll(".sectionStadiumStrips").attr("style", "opacity:1");

				for (var i=0; i<hideableElements.length; i++){
					if (hideableElements[i]!==d){
						hideableElements[i].attr("display", "none");
					}
				};
			}
			else if (sectExpanded && !data.expanded) revertMap();
		});
	});
}

// revert to original map
function revertMap(){
	if (sectExpanded){
		sectExpanded = false;
		replaceDetailsText(textUnexpanded, true);
		highlightTable(null);

		// unhide everything
		for (var i=0; i<hideableElements.length; i++){
			hideableElements[i].attr("display", "");
		};

		// revert expanded section
		sections.forEach(function(d){
			
			if (d.datum().expanded){
				refreshSectionID = null;
				d.selectAll(".sectionStadiumStrips").attr("style", "");
				d.datum().expanded = false;
				d.transition()
					.duration(transTime)
					.ease("linear")
					.attr("transform", "");
				gStadium.transition().attr("transform", "");
				
				d.selectAll(".mapTableText").call(function(tables){
					var tables = tables[0];
					for (var i=0; i<tables.length; i++){						
						tables[i].setAttribute("transform", null);
					}
				})
				
			}
		});
	}
}


// Replace the details on demand text
// if true, text goes in title; if false, text goes in body
// removes the text in the other
function replaceDetailsText(arrText, isTitle){
	var detailsWrite = detailsBodyText;
	var detailsDelete = detailsTitleText;
	var detailsBoxWidth = d3.select("#svgDetailsBox").attr("width");

	if (isTitle){
		detailsWrite = detailsTitleText;
		detailsDelete = detailsBodyText;
	}
	for (var i=0; i<3; i++){
		detailsWrite[i].text("");
	}
	for (var i=0; i<Math.min(arrText.length,detailsWrite.length); i++){
		var text = arrText[i];
		detailsWrite[i].text(arrText[i]);
		var element = document.getElementById(detailsWrite[i].attr("id"));
		var textWidth = element.getComputedTextLength();
		//alert(detailsBoxWidth+", "+textWidth);
		if (textWidth > detailsBoxWidth){
			while (textWidth > detailsBoxWidth){
				text = text.substring(0,text.length-1);
				detailsWrite[i].text(text);
				element = document.getElementById(detailsWrite[i].attr("id"));
				textWidth = element.getComputedTextLength();
			}
			text = text.substring(0,text.length-4)+"...";
			detailsWrite[i].text(text);
		}
		
		
	}
	for (var i=0; i<3; i++){
		detailsDelete[i].text("");
	}
}

function setTableDetails(tableName){
	var text = [];
	text.push("Table:               "+tableName)
	tableName = tableName.toLocaleLowerCase();
	for (var i=0; i<tableData.length; i++){
		if (tableData[i]["table"]===tableName){
			text.push("Team Name:    "+tableData[i]["team"])
			text.push("Project Name:  "+tableData[i]["project"])
			detailsBodyLink.attr("xlink:href", "/projectdetails/"+tableData[i]["submission"]);
			replaceDetailsText(text, false);
			return;
		}
	}

}

// unhighlights the current highlighted table and highlights the given table
function highlightTable(table){
	if (currTableRect!=null) currTableRect.attr("style", null);
	if (table!=null){
		currTableRect = d3.select("[info='"+table.attr("info")+"']").select("rect");
		currTableRect.attr("style", "fill:#ffff99");
	}
}

// if map was reloaded while expanded, reexpand the previously expanded section
function reexpandSection(){
	d = d3.select("#"+refreshSectionID);
	var data = d.datum();
	var box = document.getElementById(d.attr("id")).getBBox();
	data.expanded = true;
	sectExpanded = true;
	var rotAngle = 0;
	if (data.startAngle!=null) rotAngle = -(data.startAngle+data.endAngle)/2*180/Math.PI;
	else if (box.height>box.width) rotAngle = -90;
	if (rotSideways){
		if (rotAngle>-180) rotAngle += 90;
		else rotAngle -= 90;
	}
	var x = box.x+box.width/2;
	var y = box.y+box.height/2;
	var trans = "scale("+data.scale+") translate("+data.bigX+","+data.bigY+") rotate("+rotAngle+","+x+","+y+")";
	d.attr("transform", trans);
	d.selectAll(".mapTableText").call(function(tables){
		var tables = tables[0];
		for (var i=0; i<tables.length; i++){						
			var x = (+tables[i].attributes.getNamedItem("x").value);
			var y = (+tables[i].attributes.getNamedItem("y").value)-textOffsetYTable;
			var tr = "rotate("+(-rotAngle)+","+x+","+y+")";
			tables[i].setAttribute("transform", tr);
		}
	})
	d.selectAll(".sectionStadiumStrips").attr("style", "opacity:1");
	for (var i=0; i<hideableElements.length; i++){
		if (hideableElements[i].attr("id")!==refreshSectionID){
			hideableElements[i].attr("display", "none");
		}
	};
}

// redraws map on resize
window.onresize = function(){
	var currMapResProportion = window.innerHeight/window.innerWidth;
	if (Math.abs(mapResProportion-currMapResProportion)>0.02){
		document.getElementById("MapContainer").innerHTML="";
		loadMap();
	}
};
