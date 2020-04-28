function changeLink(){
	var rus_to_eng = {
		"Математика": "Math",
		"Русский": "Russian",
		"Информатика": "Informatics",
		"Физика": "Physics",
		"Литература": "Literature",
		"Химия": "Chemistry",
		"Биология": "Biology"
	}

	var subject = rus_to_eng[document.getElementById("subject").value];
	var grade = document.getElementById("grade").value;
	var olimp_id = document.getElementById("olimpiad_id").textContent;
	var link = document.getElementById("load_file");
	link.href = "../static/tasks/" + olimp_id + "_" + subject + "_" + grade + ".zip";
}

