var height = document.getElementById('00').clientHeight;
var homeMove = true;
console.log('color', color);
console.log('move', data.move);
console.log(color == data.move);
console.log(data);

var isDraging = false;

function startFun(){
	if(color == data.move){
	  homeMove = true;
	} else {
	  homeMove = false;
	}
	populate();
	grab();
	time();
	start_getNews();
}

startFun();

function start_getNews() {
    getNews = setInterval(refresh, 1000);
}

function refresh(){
  fetch('/chess/move',{
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: JSON.stringify({moveNumber: parseInt(data.move_number)})
  }).then(response => response.json()).then(function(response){
    console.log('response', response);
    if (response){
    	data = response;
      clearBoard();
      startFun();
    }
  }).catch(function(err){
    console.log('err', err);
  })
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

var homeTimer = document.getElementById('homeTimer');
var awayTimer = document.getElementById('awayTimer');
var clock = {
	homeTime : '00:00',
	awayTime : '00:00'
}

function time() {
	stop();

	whiteSec = data.white_time % 60
	whiteMin = (data.white_time - whiteSec) / 60
	let wminutes = parseInt(whiteMin);
	let wseconds = parseInt(whiteSec);
	if (wminutes.length == 1) {
		wminutes = '0' + wminutes;
	}
	if (wseconds.length == 1) {
		wseconds = '0' + wseconds;
	}
	blackSec = data.black_time % 60
	blackMin = (data.black_time - blackSec) / 60
	let bminutes = parseInt(blackMin);
	let bseconds = parseInt(blackSec);
	if (bminutes.length == 1) {
		bminutes = '0' + bminutes;
	}
	if (bseconds.length == 1) {
		bseconds = '0' + bseconds;
	}
	if(data.color == 'white'){
		clock.homeTime = wminutes + ':' + wseconds
		clock.awayTime = bminutes + ':' + bseconds
	} else {
		clock.homeTime = bminutes + ':' + bseconds
		clock.awayTime = wminutes + ':' + wseconds
	}
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
console.log(data.boardFigures);

function populate() {
	var boardFigures = data.position
  console.log('populating');
  document.getElementById('awayCheck').style.visibility = 'hidden';
  document.getElementById('homeCheck').style.visibility = 'hidden';
	for (key in boardFigures){
		let holder = document.createElement("img");
		//holder.src = {{ url_for('/static', filename = boardFigures[key].pic) }};
    	holder.alt = boardFigures[key].name;
		//holder.src = 'https://game.supersharas.repl.co/static/'+ boardFigures[key].pic;
		holder.src = '/static/'+ boardFigures[key].pic;
		holder.setAttribute("class", 'figure ' + boardFigures[key].color);
		holder.setAttribute("id", boardFigures[key].name);
		if(boardFigures[key].location == 'whiteHolder' || boardFigures[key].location == 'blackHolder') {
			holder.style.height = height - (height / 100 * 53);
			holder.style.width = height - (height / 100 * 53);
		} else {
			holder.style.height = height - (height / 100 * 20);
			holder.style.width = height - (height / 100 * 20);
		}
		//console.log('loc', boardFigures[key].location);
		document.getElementById(boardFigures[key].location).appendChild(holder);
	};
}

function clearBoard() {
	var toDestroy = document.getElementsByClassName("figure");
	var len = toDestroy.length;
	var list = [];
	for(x = 0; x < len; x += 1) {
		list.push(toDestroy[x].id)
	};
	list.forEach(function(node) {
		kid = document.getElementById(node);
		kid.parentNode.removeChild(kid);
	});
}

function getBack() {
	onTheMove.style.position = 'relative';
	onTheMove.style.left = 0;
	onTheMove.style.top = 0;
	return;
}

function ifAllowed(fig, move){
  let figure = data.position[fig];
	var posx = parseInt(figure.location[0]);
	var posy = parseInt(figure.location[1]);
	var desx = posx + move.x;
	var desy = posy + move.y;
	var destination = desx.toString() + desy.toString();
	if(figure.moves.includes(destination)) {
    document.getElementById(destination).appendChild(onTheMove);
    onTheMove.style.position = 'relative';
    onTheMove.style.left = '0';
    onTheMove.style.top = '0';
    homeMove = false;
		console.log('HITT');
    fetch('/chess/move',{
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: JSON.stringify({'figure': figure.name, 'move': destination})
    }).then(response => response.json()).then(function(response){
      console.log('response', response);
      data = response;
      moveNumber = response.move_number;
      clearBoard();
      startFun();
    }).catch(function(err){
      console.log('err', err);
    })
	} else {
		return getBack();
	}
}

window.addEventListener('mouseup', e => {
	if (isDraging === true) {
		if (onTheMove) {
	      if(color == 'black'){
	        //var move = {x: -Math.round((startx - e.x)/60), y: -Math.round((starty - e.y)/60)};
	        var move = {x: -Math.round((startx - e.pageX)/60), y: -Math.round((starty - e.pageY)/60)};
	      } else{
	        //var move = {x: Math.round((startx - e.x)/60), y:Math.round((starty - e.y)/60)};
	        var move = {x: Math.round((startx - e.pageX)/60), y: Math.round((starty - e.pageY)/60)};
	      }
		ifAllowed(onTheMove.id, move);
		}
		isDraging = false;
	}
});

function grab() {
  if(color == data.move) {
    var moving = document.querySelectorAll('.figure.' + data.move);
    moving.forEach(function(move) {
      move.addEventListener('mousedown', e => {
        e.preventDefault();
        console.log('e', e);
        //startx = e.x;
        //starty = e.y;
        startx = e.pageX;
        starty = e.pageY;
        isDraging = true;
        onTheMove = e.target;
        onTheMove.style.position = 'absolute';
        //onTheMove.style.left = e.clientX - (height/2.5);
        //onTheMove.style.top = e.clientY - (height/2.5);
        onTheMove.style.left = e.pageX - (height/2.5);
        onTheMove.style.top = e.pageY - (height/2.5);
      });
    });
  }
}

window.addEventListener('mousemove', e => {
	if (isDraging === true) {
		e.preventDefault();
		onTheMove.style.left = e.pageX - (height/2.5);
		onTheMove.style.top = e.pageY - (height/2.5);
	}
});

