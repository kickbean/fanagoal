

function render(unit){
	document.getElementById("frq_unit").innerHTML = " "+unit;
	if(unit=='days' || unit=='months'){
		document.getElementById('weeklyOnly').style.display = 'none';
	}else{
				document.getElementById('weeklyOnly').style.display = '';

	}
}