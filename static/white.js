var height = document.getElementById('00').clientHeight;
var homeMove = true;
var isDraging = false;
var homeTimer = document.getElementById('homeTimer');
var awayTimer = document.getElementById('awayTimer');
var clock = {
	homeTime : '00:00',
	awayTime : '00:00'
}
var crazyTime = false;
homeTimer.innerText = clock.homeTime;
awayTimer.innerText = clock.awayTime;

function timer(someTime, someTimer, other) {
  someTimer.style.backgroundColor = "red";
	let minutes = parseInt(clock[someTime].slice(0,2));
	let seconds = parseInt(clock[someTime].slice(3,5));
	seconds += 1;
	if (seconds == 60){
		minutes += 1;
		seconds = 0;
	}
	minutes = minutes.toString();
	seconds = seconds.toString();
	if (minutes.length == 1) {
		minutes = '0' + minutes;
	}
	if (seconds.length == 1) {
		seconds = '0' + seconds;
	}
	clock[someTime] = minutes + ':' + seconds;
	someTimer.innerText = minutes + ':' + seconds;
	other.style.backgroundColor = "white";
}

function time() {
	stop();
	if(homeMove){
		crazyTime = setInterval(timer, 1000, 'homeTime', homeTimer, awayTimer);
	} else {
		crazyTime = setInterval(timer, 1000, 'awayTime', awayTimer, homeTimer);
	}
}

function stop() {
	if(crazyTime) {
		clearInterval(crazyTime);
	}
}

// GET  
console.log(boardFigures);

function populate() {
  console.log('populating');
  document.getElementById('awayCheck').style.visibility = 'hidden';
  document.getElementById('homeCheck').style.visibility = 'hidden';
	for (key in boardFigures){
		let holder = document.createElement("img");
		//holder.src = {{ url_for('/static', filename = boardFigures[key].pic) }};
    holder.alt = boardFigures[key].name;
		holder.src = 'http://game.supersharas.repl.co/static/'+ boardFigures[key].pic;
		holder.setAttribute("class", 'figure ' + boardFigures[key].color);
		holder.setAttribute("id", boardFigures[key].name);
		if(boardFigures[key].location == 'homeHolder' || boardFigures[key].location == 'awayHolder') {
			holder.style.height = height - (height / 100 * 53);
			holder.style.width = height - (height / 100 * 53);
		} else {
			holder.style.height = height - (height / 100 * 20);
			holder.style.width = height - (height / 100 * 20);
		}
		document.getElementById(boardFigures[key].location).appendChild(holder);
	};
}

window.addEventListener('mouseup', e => {
	if (isDraging === true) {
		if (onTheMove) {
			var move = {x: Math.round((startx - e.x)/60), y:Math.round((starty - e.y)/60)};
			ifAllowed(onTheMove.id, move);
		}
		isDraging = false;
	}
});

populate();

function grab() {
	var moving = document.querySelectorAll('.figure.white');
	moving.forEach(function(move) {
		move.addEventListener('mousedown', e => {
			e.preventDefault();
			startx = e.x;
			starty = e.y;
			isDraging = true;
			onTheMove = e.target;
			onTheMove.style.position = 'absolute';
			onTheMove.style.left = e.clientX - (height/2.5);
			onTheMove.style.top = e.clientY - (height/2.5);
		});
	});
}

window.addEventListener('mousemove', e => {
	if (isDraging === true) {
		e.preventDefault();
		onTheMove.style.left = e.clientX - (height/2.5);
		onTheMove.style.top = e.clientY - (height/2.5);
	}
});

grab();
time();