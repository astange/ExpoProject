// Used for menu icon matrix adjustment on window size change
function check(){
	var isMobile = Math.max(screen.width, screen.height) < 1024;
	var content = document.getElementById("content");
	var vertical = content.offsetWidth<795;
	
	if (isMobile){
		document.getElementById("projects").src = "/static/img/Projects_m.png";
		document.getElementById("map").src = "/static/img/Map_m.png";
		document.getElementById("tips").src = "/static/img/Tips_m.png";
		document.getElementById("events").src = "/static/img/Schedule_m.png";
		document.getElementById("seelio").src = "/static/img/Seelio_m.png";
		document.getElementById("social").src = "/static/img/Social_m.png";
		console.log(content.offsetWidth);
		$("#icons").css("margin","0%");
		if (content.offsetWidth<600){
			$(".icon").css("width","48%");
		}
		else{
			$(".icon").css("width","32%");
		}
	}
	else{
		document.getElementById("projects").src = "/static/img/Projects.png";
		document.getElementById("map").src = "/static/img/Map.png";
		document.getElementById("tips").src = "/static/img/Tips.png";
		document.getElementById("events").src = "/static/img/Schedule.png";
		document.getElementById("seelio").src = "/static/img/Seelio.png";
		document.getElementById("social").src = "/static/img/Social.png";
		if (vertical){
			$(".icon").css("width","90%");
			$("#icons").css("margin","2%");
		}
		else{
			$(".icon").css("width","48%");
			$("#icons").css("margin","2%");
		}
	}

}