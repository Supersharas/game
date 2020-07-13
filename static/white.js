var height = document.getElementById('00').clientHeight;
var homeMove = true;
console.log('color', color);
console.log('move', move);
console.log(color == move);
if(color == move){
  homeMove = true;
} else {
  homeMove = false;
}
var isDraging = false;
var homeTimer = document.getElementById('homeTimer');
var awayTimer = document.getElementById('awayTimer');
var clock = {
	homeTime : '00:00',
	awayTime : '00:00'
}


function refresh(){
  fetch('/chess/move',{
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: JSON.stringify({moveNumber: parseInt(moveNumber)})
  }).then(response => response.json()).then(function(response){
    console.log('response', response);
  }).catch(function(err){
    console.log('err', err);
  })
}

function start_getNews() {
  stop_getNews();
  if(!homeMove){
    getNews = setInterval(refresh, 1000);
  }
}

function stop_getNews() {
	if(homeMove) {
		clearInterval(getNews);
	}
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
		holder.src = 'https://game.supersharas.repl.co/static/'+ boardFigures[key].pic;
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
  let figure = boardFigures[fig];
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
    time()
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
      boardFigures = response.position;
      clearBoard()
      populate()
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
        var move = {x: -Math.round((startx - e.x)/60), y: -Math.round((starty - e.y)/60)};
      } else{
        var move = {x: Math.round((startx - e.x)/60), y:Math.round((starty - e.y)/60)};
      }
			
      console.log(move);
			ifAllowed(onTheMove.id, move);
		}
		isDraging = false;
	}
});

populate();

function grab() {
  if(color == move) {
    var moving = document.querySelectorAll('.figure.' + move);
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