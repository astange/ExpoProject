function deleteSemester(){
    var semester = document.getElementById("delSem");
    var strSem = semester.options[semester.selectedIndex].value;
    
    var r = confirm("Are you sure you would like to delete the semester: " + strSem);

	if (r == false){
		return false;
	}
	document.location.href = "semesters/delete/" + strSem;
}

function changeSemesters(){
    var selected = document.getElementById('changeSem').selectedIndex;
    var options = document.getElementById('changeSem').options;
    
    var r = confirm("Are you sure you would like to change the semester to: " + options[selected].value);
    if(r == false){
        return false;
    }
    document.location.href = "semesters/" + options[selected].value;
}

function validateForm() {
	var semester;
	if(document.getElementById('sem_Summer').checked) {
	 	semester = "Summer";
	}else if(document.getElementById('sem_Fall').checked) {
		semester = "Fall";
	}else if(document.getElementById('sem_Spring').checked) {
		semester = "Spring";
	}else{
		alert("Please select a semester");
		return false;
	}

	var year = document.forms["semesterInput"]["year"].value;	
	var patt = new RegExp("20[0-9][0-9]");
    if (year == null || year == "" || year.length < 4 || year.length > 4 || !patt.test(year)) {
        alert("Year must be filled out and in the form 20YY");
        return false;
    }
    
    var sKey = document.forms["semesterInput"]["sKey"].value;
    if(sKey == null || sKey == "") {
        alert("Seelio Key must be filled out");
        return false;
    }

	var r = confirm("Are you sure you would like to create the new expo for semester: " + semester + " " + year +" with the key: " + sKey);

	if (r == false){
		return false;
	}
	document.location.href = "semesters/" + semester + year + "/" + sKey;
}
