// puts each tip in the correct bulleted list
function populateTips(){
	appendJudgeTipList(document.getElementById("tipsJudges"), judgeTips, judgeSubTips);
	appendStudentTipList(document.getElementById("tipsStudents"), studentTips, studentSubTips);
	appendVisitorTipList(document.getElementById("tipsVisitors"), visitorTips, visitorSubTips);
	document.getElementById("divJudges").style.height="auto";
	document.getElementById("divStudents").style.height="auto";
	document.getElementById("divVisitors").style.height="auto";
}


function appendJudgeTipList(element, mainlist, sublist){
	for (var i=0; i<mainlist.length; i++){
		var tip = document.createElement("li");
		var text = document.createTextNode(mainlist[i]);
		var subtiplist = document.createElement("ul");
		var subtip = document.createElement("li");
		if(i==1){
			var link = document.createElement("a");
			link.textContent = "Click here";
			link.setAttribute('href', "https://docs.google.com/forms/d/1Oqnsv87GCAP0cHEvTLoT4c774xj-NfbL1CDf5IFPUeQ/viewform");
			link.target = "_blank";
			subtip.appendChild(link);
		}
		var subtext = document.createTextNode(sublist[i]);
		subtip.appendChild(subtext);
		if(i==3){
			var subSubtiplist = document.createElement("ul");
			for(var j = 0; j<judgeSubTipsThird.length; j++){
				var subSubtip = document.createElement("li");
				var subSubtext = document.createTextNode(judgeSubTipsThird[j]);
				subSubtip.appendChild(subSubtext);
				subSubtiplist.appendChild(subSubtip);
			}
			subtip.appendChild(subSubtiplist);
		}
		subtiplist.appendChild(subtip);
		tip.appendChild(text);
		tip.appendChild(subtiplist);
		element.appendChild(tip);
		
	}
}

function appendStudentTipList(element, mainlist, sublist){
	for (var i=0; i<mainlist.length; i++){
		var tip = document.createElement("li");
		var text = document.createTextNode(mainlist[i]);
		var subtiplist = document.createElement("ul");
		var subtip = document.createElement("li");
		if(i==0){
			var subtext = document.createTextNode(sublist[i]);
			var link = document.createElement("a");
			link.textContent = "use this link.";
			link.setAttribute('href', "https://seelio.com/register?gCode=gatech1");
			link.target = "_blank";
			subtip.appendChild(subtext);
			subtip.appendChild(link);
		}
		else{
			var subtext = document.createTextNode(sublist[i]);
			subtip.appendChild(subtext);
		}
		
		subtiplist.appendChild(subtip);
		//subtiplist.insertBefore(li, tip);
		tip.appendChild(text);
		tip.appendChild(subtiplist);
		element.appendChild(tip);
	}
}

function appendVisitorTipList(element, mainlist, sublist){
	for (var i=0; i<mainlist.length; i++){
		var tip = document.createElement("li");
		var text = document.createTextNode(mainlist[i]);
		var subtiplist = document.createElement("ul");
		var subtip = document.createElement("li");
		if(i==1){
			var subtext = document.createTextNode(sublist[i]);
			var link = document.createElement("a");
			link.textContent = "on this map.";
			link.setAttribute('href', "http://pts.gatech.edu/PublishingImages/ParkingZones1314.jpg");
			link.target = "_blank";
			subtip.appendChild(subtext);
			subtip.appendChild(link);
		}
		else if(i==3){
			var subtext = document.createTextNode(sublist[i]);
			var link = document.createElement("a");
			link.textContent = "using this link.";
			link.setAttribute('href', "https://docs.google.com/forms/d/1Oqnsv87GCAP0cHEvTLoT4c774xj-NfbL1CDf5IFPUeQ/viewform");
			link.target = "_blank";
			subtip.appendChild(subtext);
			subtip.appendChild(link);

		}
		else{
			var subtext = document.createTextNode(sublist[i]);
			subtip.appendChild(subtext);
		}
		
		subtiplist.appendChild(subtip);
		//subtiplist.insertBefore(li, tip);
		tip.appendChild(text);
		tip.appendChild(subtiplist);
		element.appendChild(tip);
	}
}

judgeTips = [
"Can I be a judge?",
"How do I RSVP?",
"Do I need to select which teams I judge?",
"What criteria are used to judge the teams?",
"What is the dress code?",
"Where is the nearest parking?"
];

judgeSubTips=[
"Judges are either faculty, alumni and/or industry professionals and can be from any discipline or area of expertise.",
" to fill in your details.",
"No. On the day of the expo, you will receive a unique link in your email which will show which teams to judge and their table numbers.",
"Each team will be judged on a 1 to 5 scale, 5 being the best, in the following categories:",
"Anything comfortable for you is fine. However, business casual will be most common at the expo.",
"The nearest parking will be at the visitors and family housing on 10th street.  Address is: 251 10th Street NW, Atlanta, GA 30318-0475"
];

judgeSubTipsThird=[
"Creativity and innovation",
"Utility",
"Quality of analysis",
"Proof of function",
"Good communication"
];

studentTips = [
"Is my team eligible to win the Seelio Award?",
"What is the dress code?",
"By when should our team be ready to present?",
"Do we get free food?"
];

studentSubTips=[
"Yes, only if you have created your project page on Seelio.com by April 16th. To signup, ",
"Wear whatever you need to be successful. Most teams will be in business attires, but few also wear custom/themed attires including custom t-shirts. Your team will be judged by industry experts, alumni, faculty and sponsors. Dress to impress!",
"4:30pm sharp!",
"Yes. Students will be given food vouchers at the time of check in and will begin being able to receive food from the concession stands at the McCamish Pavilion starting at 3pm."
];

visitorTips = [
"Is the event open for public?",
"Where is the nearest parking?",
"Do I have to stay for the entire event?",
"Do I have to RSVP?"
];

visitorSubTips=[
"Absolutely! It will be free and open from 4:30pm to 8:00pm for anyone and everyone! Feel free to bring your colleagues, friends and family to witness what GT graduating seniors are doing to change the world.",
"There are several visitor parking areas around the Pavilion.  The closest visitor parking is at the 4th and Fowler Street parking garage. This is a paid parking garage. Marked E52 center right location ",
"No. However, we are sure you will leave wishing the event was open for longer.",
"No. However, if you wish to judge then you have to RSVP by the 15th of April, 2014 "
];
