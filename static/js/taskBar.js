
function barLen(taskLength, taskStartAbs, goalLength, id){
	
	margin_left = Math.round(taskStartAbs/goalLength*100);
	margin_right = Math.round((goalLength-taskLength-taskStartAbs)/goalLength*100);
	// alert(taskLength+","+margin_right);
	
	document.getElementById(id).style.marginLeft = margin_left+"%";
	document.getElementById(id).style.marginRight = margin_right+"%";
	document.getElementById(id).style.backgroundColor = "#23A651";
}