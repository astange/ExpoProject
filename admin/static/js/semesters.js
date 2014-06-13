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
	
    if (year == null || year == "" || year.length < 4 || year.length > 4) {
        alert("Year must be filled out and in the form YYYY");
        return false;
    }

	var r = confirm("Are you sure you would like to create the new expo for semester: " + semester + " " + year);

	if (r == false){
		return false;
	}
	document.location.href = "semesters/" + semester + year;
}


function deleteSemester(){
    return false;
}
