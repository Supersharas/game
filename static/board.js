var height = document.getElementById('00').clientHeight;
var homeMove = true;
var whiteLocations = [];
var blackLocations = [];
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
  console.log('this', this);
  console.log('crazyTime', crazyTime);
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
var boardFigures = {
	WP8: {name: 'WP8', color: 'white', location: '01', pic:'WP.png', notMoved: true},
	WP7: {name: 'WP7', color: 'white', location: '11', pic:'WP.png', notMoved: true},
	WP6: {name: 'WP6', color: 'white', location: '21', pic:'WP.png', notMoved: true},
	WP5: {name: 'WP5', color: 'white', location: '31', pic:'WP.png', notMoved: true},
	WP4: {name: 'WP4', color: 'white', location: '41', pic:'WP.png', notMoved: true},
	WP3: {name: 'WP3', color: 'white', location: '51', pic:'WP.png', notMoved: true},
	WP2: {name: 'WP2', color: 'white', location: '61', pic:'WP.png', notMoved: true},
	WP1: {name: 'WP1', color: 'white', location: '71', pic:'WP.png', notMoved: true},
	BP8: {name: 'BP8', color: 'black', location: '06', pic:'BP.png', notMoved: true},
	BP1: {name: 'BP1', color: 'black', location: '16', pic:'BP.png', notMoved: true},
	BP2: {name: 'BP2', color: 'black', location: '26', pic:'BP.png', notMoved: true},
	BP3: {name: 'BP3', color: 'black', location: '36', pic:'BP.png', notMoved: true},
	BP4: {name: 'BP4', color: 'black', location: '46', pic:'BP.png', notMoved: true},
	BP5: {name: 'BP5', color: 'black', location: '56', pic:'BP.png', notMoved: true},
	BP6: {name: 'BP6', color: 'black', location: '66', pic:'BP.png', notMoved: true},
	BP7: {name: 'BP7', color: 'black', location: '76', pic:'BP.png', notMoved: true},
	WR1: {name: 'WR1', color: 'white', location: '00', pic:'WR.png', notMoved: true},
	WR2: {name: 'WR2', color: 'white', location: '70', pic:'WR.png', notMoved: true},
	BR1: {name: 'BR1', color: 'black', location: '07', pic:'BR.png', notMoved: true},
	BR2: {name: 'BR2', color: 'black', location: '77', pic:'BR.png', notMoved: true},
  WB1: {name: 'WB1', color: 'white', location: '10', pic:'WB.png', notMoved: true},
  WB2: {name: 'WB2', color: 'white', location: '60', pic:'WB.png', notMoved: true},
  BB1: {name: 'BB1', color: 'black', location: '17', pic:'BB.png', notMoved: true},
  BB2: {name: 'BB2', color: 'black', location: '67', pic:'BB.png', notMoved: true},
  WKN1: {name: 'WKN1', color: 'white', location: '20', pic:'WK.png', notMoved: true},
  WKN2: {name: 'WKN2', color: 'white', location: '50', pic:'WK.png', notMoved: true},
  BKN1: {name: 'BKN1', color: 'black', location: '27', pic:'BK.png', notMoved: true},
  BKN2: {name: 'BKN2', color: 'black', location: '57', pic:'BK.png', notMoved: true},
  WQ: {name: 'WQ', color: 'white', location: '30', pic:'WQ.png', notMoved: true},
  BQ: {name: 'BQ', color: 'black', location: '37', pic:'BQ.png', notMoved: true},
  BKing: {name: 'BKing', color: 'black', location: '47', pic:'BKing.png', notMoved: true, check: false},
  WKing: {name: 'WKing', color: 'white', location: '40', pic:'WKing.png', notMoved: true, check: false}
};

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
//HELPER FUNCTION TO CANCELL A MOVE
function getBack() {
	onTheMove.style.position = 'relative';
	onTheMove.style.left = 0;
	onTheMove.style.top = 0;
	return;
}
//HELPER FUNCTION TO MAKE A MOVE
function moved(figure, destination, strike=false) {
	figure.notMoved = false;
	figure.location = destination;
	homeMove = !homeMove;
	if(strike){
		let battle = document.getElementById(destination);
		let fallen = battle.firstChild.id;
		if(figure.color == 'white'){
			strike = 'homeHolder';
		} else {
			strike = 'awayHolder';
		}
		boardFigures[fallen].location = strike;
	}
	clearBoard();
	populate();
  boardFigures = calculateMoves(boardFigures);
  check();
	grab();
	time();
	return;
}
//HELPER FUNCTION TO FIND WHAT FIGURE IN LOCATION
function who(location) {
	if(location){
		if(whiteLocations.includes(location)){
      return 'W';
		}else if(blackLocations.includes(location)){
      return 'B';
    } else {
			return false;
		}
	}
	return false;
}
//HELPER FUNCTION TO GET STRING DESTINATION IF IT EXISTS ON THE BOARD
function loc(desx, desy){
	if((desx >= 0 && desx <= 7) && (desy >= 0 && desy <= 7)){ 
		return desx.toString() + desy.toString();
	} else{
		return false;
	}
}
//HELPER FUNCTION FOR ROOK AND QUEEN
function moveStright(figure) {
	let x = parseInt(figure.location[0]);
	let y = parseInt(figure.location[1]);
	for(i = y + 1; i < 8; i++){
		if(!who(loc(x,i))){
			figure.moves.push(loc(x,i));
		} else {
			if((figure.name.slice(0,1) == 'W' && who(loc(x,i)) == 'B') || (figure.name.slice(0,1) == 'B' && who(loc(x,i)) == 'W')){
				figure.strikes.push(loc(x,i));
			}
			break;
		}
	};
	for(i = y - 1; i >= 0; i--){
		if(!who(loc(x,i))){
			figure.moves.push(loc(x,i));
      console.log('move pushed', figure, loc(x,i), who(loc(x,i)));
		} else {
			if((figure.name.slice(0,1) == 'W' && who(loc(x,i)) == 'B') || (figure.name.slice(0,1) == 'B' && who(loc(x,i)) == 'W')){
				figure.strikes.push(loc(x,i));
			}
		  break;
		}
	};
	for(i = x + 1; i < 8; i++){
		if(!who(loc(i,y))){
			figure.moves.push(loc(i,y));
		} else {
			if((figure.name.slice(0,1) == 'W' && who(loc(i,y)) == 'B') || (figure.name.slice(0,1) == 'B' && who(loc(i,y)) == 'W')){
				figure.strikes.push(loc(i,y));
			}
		  break;
		}
	};
	for(i = x - 1; i >= 0; i--){
		if(!who(loc(i,y))){
			figure.moves.push(loc(i,y));
		} else {
			if((figure.name.slice(0,1) == 'W' && who(loc(i,y)) == 'B') || (figure.name.slice(0,1) == 'B' && who(loc(i,y)) == 'W')){
				figure.strikes.push(loc(i,y));
			}	
		  break;
		}
	};
	return figure;
}

function moveSlope(figure){
	let x = parseInt(figure.location[0]);
  let originalx = x;
	let y = parseInt(figure.location[1]);
  for(i = y + 1; i < 8; i++){
    x++;
		if(!who(loc(x,i))){
			figure.moves.push(loc(x,i));
		} else {
			if((figure.name.slice(0,1) == 'W' && who(loc(x,i)) == 'B') || (figure.name.slice(0,1) == 'B' && who(loc(x,i)) == 'W')){
				figure.strikes.push(loc(x,i));
			}
			break;
		}
	};
  x = originalx;
  for(i = y - 1; i >= 0; i--){
    x--;
		if(!who(loc(x,i))){
			figure.moves.push(loc(x,i));
		} else {
			if((figure.name.slice(0,1) == 'W' && who(loc(x,i)) == 'B') || (figure.name.slice(0,1) == 'B' && who(loc(x,i)) == 'W')){
				figure.strikes.push(loc(x,i));
			}
			break;
		}
	};
  x = originalx;
  for(i = y - 1; i >= 0; i--){
    x++;
		if(!who(loc(x,i))){
			figure.moves.push(loc(x,i));
		} else {
			if((figure.name.slice(0,1) == 'W' && who(loc(x,i)) == 'B') || (figure.name.slice(0,1) == 'B' && who(loc(x,i)) == 'W')){
				figure.strikes.push(loc(x,i));
			}
			break;
		}
	};
  x = originalx;
  for(i = y + 1; i < 8; i++){
    x--;
		if(!who(loc(x,i))){
			figure.moves.push(loc(x,i));
		} else {
			if((figure.name.slice(0,1) == 'W' && who(loc(x,i)) == 'B') || (figure.name.slice(0,1) == 'B' && who(loc(x,i)) == 'W')){
				figure.strikes.push(loc(x,i));
			}
			break;
		}
	};
  x = originalx;
  return figure;
}

//PLACE FIGURES ON THE BOARD
function populate() {
  whiteLocations = [];
  blackLocations = [];
  document.getElementById('awayCheck').style.visibility = 'hidden';
  document.getElementById('homeCheck').style.visibility = 'hidden';
	for (key in boardFigures){
		let holder = document.createElement("img");
		//holder.src = {{ url_for('static', filename = boardFigures[key].pic) }};
		holder.src = 'static/'+ boardFigures[key].pic;
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
    if(boardFigures[key].color == 'white'){
      whiteLocations.push(boardFigures[key].location);
    } else {
      blackLocations.push(boardFigures[key].location);
    }
	};
  console.log('locations', whiteLocations, blackLocations);
}

function calculateMoves(figures){
  console.log('calculating');
  console.log( 'whiteLocations', whiteLocations )
  figures.WKing.check = false;
  console.log('figures in action', figures, figures.WKing.check);
  figures.BKing.check = false;
	for (key in figures) {
		let figure = figures[key];
		figure.moves = [];
		figure.strikes = [];
		let x = parseInt(figure.location[0]);
		let y = parseInt(figure.location[1]);
		//WHITE POWN
		if(figure.name.slice(0,2) == 'WP') {
      figure.pownStrikes = [];
			if(!who(loc(x, y+1))){
				figure.moves.push(loc(x, y+1));
				if(figure.notMoved){
					if(!who(loc(x, y+2))){
						figure.moves.push(loc(x, y+2));
					}
				}
			}
			if(who(loc(x+1,y+1))){
				if(who(loc(x+1,y+1)) == 'B'){
					figure.strikes.push(loc(x+1,y+1));
				 }
			}
      figure.pownStrikes.push(loc(x+1,y+1));
			if(who(loc(x-1,y+1))){
				if(who(loc(x-1,y+1)) == 'B'){
					figure.strikes.push(loc(x-1,y+1));
				}
			}
      figure.pownStrikes.push(loc(x-1,y+1));
		} else if(figure.name.slice(0,2) == 'BP') {  //BLACK POWN
      figure.pownStrikes = [];
			if(!who(loc(x, y-1))){
				figure.moves.push(loc(x, y-1));
				if(figure.notMoved){
					if(!who(loc(x, y-2))){
						figure.moves.push(loc(x, y-2));
					}
				}
			}
			if(who(loc(x+1,y-1))){
				if(who(loc(x+1,y-1)) == 'W'){
					figure.strikes.push(loc(x+1,y-1));
				}
			}
      figure.pownStrikes.push(loc(x+1,y-1));
			if(who(loc(x-1,y-1))){
				if(who(loc(x-1,y-1)) == 'W'){
					figure.strikes.push(loc(x-1,y-1));
				}
			}
      figure.pownStrikes.push(loc(x-1,y-1));
		} else if(figure.name.slice(1,2) == 'R'){  //ROOK
			figure = moveStright(figure);
		} else if(figure.name.slice(1,2) == 'B'){  //BISHOP
      figure = moveSlope(figure);
    } else if(figure.name.slice(1,3) == 'KN'){   //KNIGHT
      if(!who(loc(x+1,y+2))){
        figure.moves.push(loc(x+1, y+2));
      } else if((figure.name.slice(0,1) == 'W' && who(loc(x+1,y+2)) == 'B') || (figure.name.slice(0,1) == 'B' && who(loc(x+1,y+2)) == 'W')){
        figure.strikes.push(loc(x+1, y+2));
      }
      if(!who(loc(x+1,y-2))){
        figure.moves.push(loc(x+1, y-2));
      } else if((figure.name.slice(0,1) == 'W' && who(loc(x+1,y-2)) == 'B') || (figure.name.slice(0,1) == 'B' && who(loc(x+1,y-2)) == 'W')){
        figure.strikes.push(loc(x+1, y-2));
      }
      if(!who(loc(x-1,y+2))){
        figure.moves.push(loc(x-1, y+2));
      } else if((figure.name.slice(0,1) == 'W' && who(loc(x-1,y+2)) == 'B') || (figure.name.slice(0,1) == 'B' && who(loc(x-1,y+2)) == 'W')){
        figure.strikes.push(loc(x-1, y+2));
      }
      if(!who(loc(x-1,y-2))){
        figure.moves.push(loc(x-1, y-2));
      } else if((figure.name.slice(0,1) == 'W' && who(loc(x-1,y-2)) == 'B') || (figure.name.slice(0,1) == 'B' && who(loc(x-1,y-2)) == 'W')){
        figure.strikes.push(loc(x-1, y-2));
      }

      if(!who(loc(x+2,y+1))){
        figure.moves.push(loc(x+2, y+1));
      } else if((figure.name.slice(0,1) == 'W' && who(loc(x+2,y+1)) == 'B') || (figure.name.slice(0,1) == 'B' && who(loc(x+2,y+1)) == 'W')){
        figure.strikes.push(loc(x+2, y+1));
      }
      if(!who(loc(x+1,y-2))){
        figure.moves.push(loc(x+2, y-1));
      } else if((figure.name.slice(0,1) == 'W' && who(loc(x+2,y-1)) == 'B') || (figure.name.slice(0,1) == 'B' && who(loc(x+2,y-1)) == 'W')){
        figure.strikes.push(loc(x+2, y-1));
      }
      if(!who(loc(x-2,y+1))){
        figure.moves.push(loc(x-2, y+1));
      } else if((figure.name.slice(0,1) == 'W' && who(loc(x-2,y+1)) == 'B') || (figure.name.slice(0,1) == 'B' && who(loc(x-2,y+1)) == 'W')){
        figure.strikes.push(loc(x-2, y+1));
      }
      if(!who(loc(x-2,y-1))){
        figure.moves.push(loc(x-2, y-1));
      } else if((figure.name.slice(0,1) == 'W' && who(loc(x-2,y-1)) == 'B') || (figure.name.slice(0,1) == 'B' && who(loc(x-2,y-1)) == 'W')){
        figure.strikes.push(loc(x-2, y-1));
      }
    } else if(figure.name.slice(1,2) == 'Q'){  //QUEEN
      figure = moveStright(figure);
      figure = moveSlope(figure);
    } else if(figure.name.slice(1) == 'King'){
      if(!who(loc(x, y-1))){
				figure.moves.push(loc(x, y-1));
			} else if(figure.name.slice(0,1) != who(loc(x, y-1))){
				figure.strikes.push(loc(x, y-1));
			}
      if(!who(loc(x, y+1))){
				figure.moves.push(loc(x, y+1));
			} else if(figure.name.slice(0,1) != who(loc(x, y+1))){
				figure.strikes.push(loc(x, y+1));
			}
      if(!who(loc(x+1, y-1))){
				figure.moves.push(loc(x+1, y-1));
			} else if(figure.name.slice(0,1) != who(loc(x+1, y-1))){
				figure.strikes.push(loc(x+1, y-1));
			}
      if(!who(loc(x+1, y+1))){
				figure.moves.push(loc(x+1, y+1));
			} else if(figure.name.slice(0,1) != who(loc(x+1, y+1))){
				figure.strikes.push(loc(x+1, y+1));
			}
      if(!who(loc(x+1, y))){
				figure.moves.push(loc(x+1, y));
			} else if(figure.name.slice(0,1) != who(loc(x+1, y))){
				figure.strikes.push(loc(x+1, y));
			}
      if(!who(loc(x-1, y))){
				figure.moves.push(loc(x-1, y));
			} else if(figure.name.slice(0,1) != who(loc(x-1, y))){
				figure.strikes.push(loc(x-1, y));
			}
      if(!who(loc(x-1, y+1))){
				figure.moves.push(loc(x-1, y+1));
			} else if(figure.name.slice(0,1) != who(loc(x-1, y+1))){
				figure.strikes.push(loc(x-1, y+1));
			}
      if(!who(loc(x-1, y-1))){
				figure.moves.push(loc(x-1, y-1));
			} else if(figure.name.slice(0,1) != who(loc(x-1, y-1))){
				figure.strikes.push(loc(x-1, y-1));
			}
    }
	};
  //FOR KINGS
  allWhiteMoves = [];
  allBlackMoves = [];
  for (key in figures) {
    let figure = figures[key];
    if(figure.color == 'white' && figure.name.slice(1) != 'King'){
      allWhiteMoves = allWhiteMoves.concat(figure.strikes);
      if(figure.name.slice(1,2) == 'P'){
        allWhiteMoves = allWhiteMoves.concat(figure.pownStrikes);
      } else {
        allWhiteMoves = allWhiteMoves.concat(figure.moves);
      }
    } else if(figure.color == 'black' && figure.name.slice(1) != 'King'){
      allBlackMoves = allBlackMoves.concat(figure.strikes);
      if(figure.name.slice(1,2) == 'P'){
        allBlackMoves = allBlackMoves.concat(figure.pownStrikes);
      } else {
        allBlackMoves = allBlackMoves.concat(figure.moves);
      }
    }
  }
  var uniqW = new Set(allWhiteMoves);
  allWhiteMoves = [...uniqW];
  var uniqB = new Set(allBlackMoves);
  allBlackMoves = [...uniqB];
  for(i=figures.WKing.moves.length-1;i>=0;i--){
    if(allBlackMoves.includes(figures.WKing.moves[i])){
      figures.WKing.moves.splice(i,1);
    }
  }
  for(i=figures.WKing.strikes.length-1;i>=0;i--){
    if(allBlackMoves.includes(figures.WKing.strikes[i])){
      figures.WKing.strikes.splice(i,1);
    }
  }
  for(i=figures.BKing.moves.length-1;i>=0;i--){
    if(figures.WKing.moves.includes(figures.BKing.moves[i])){
      let notLegal = figures.WKing.moves.indexOf(figures.BKing.moves[i])
      figures.WKing.moves.splice(notLegal,1);
      figures.BKing.moves.splice(i,1);
    } else if(figures.WKing.strikes.includes(figures.BKing.moves[i])){
      let notLegal = figures.WKing.moves.indexOf(figures.BKing.moves[i])
      figures.WKing.strikes.splice(notLegal,1);
      figures.BKing.moves.splice(i,1);
    }else if(allWhiteMoves.includes(figures.BKing.moves[i])){
      figures.BKing.moves.splice(i,1);
    }
  }
  for(i=figures.BKing.strikes.length-1;i>=0;i--){
    if(figures.WKing.moves.includes(figures.BKing.strikes[i])){
      let notLegal = figures.WKing.moves.indexOf(figures.BKing.strikes[i])
      figures.WKing.moves.splice(notLegal,1);
      figures.BKing.strikes.splice(i,1);
    } else if(figures.WKing.strikes.includes(figures.BKing.strikes[i])){
      let notLegal = figures.WKing.moves.indexOf(figures.BKing.strikes[i])
      figures.WKing.strikes.splice(notLegal,1);
      figures.BKing.strikes.splice(i,1);
    } else if(allWhiteMoves.includes(figures.BKing.strikes[i])){
      figures.BKing.strikes.splice(i,1);
    }
  }
  allWhiteMoves.forEach(function(mo){
    if(mo != false && document.getElementById(mo).hasChildNodes()){
      if(document.getElementById(mo).firstChild.id == 'BKing'){
        document.getElementById('awayCheck').style.visibility = 'visible';
        figures.BKing.check = true;
      }
    }
  });
  allBlackMoves.forEach(function(mo){
    if(mo != false && mo == figures.WKing.location){
      document.getElementById('homeCheck').style.visibility = 'visible';
      figures.WKing.check = true;
      console.log('doing my dirty job', figures.WKing.location);
    }
  });
return figures;
}
//HELPER FUNCTION FOR CHECK
function filterMoves(color, king){
  console.log('not filtering');
  console.log('figures before', boardFigures);
  let fig = JSON.parse(JSON.stringify(boardFigures));
  for(key in boardFigures){
    let figure = boardFigures[key];
    if(figure.color == color){
      for(m=figure.moves.length-1;m>=0;m--){
        if(figure.moves[m] != false){
          fig[figure.name].location = figure.moves[m];
          var oldLoc = whiteLocations;
          var replace = whiteLocations.indexOf(fig[figure.name].location);
          whiteLocations.splice(replace,1);
          whiteLocations.push(fig[figure.name].location);
          console.log('----new start with ', figure.name);
          let newFig = calculateMoves(fig);
          if(newFig[king].check) {
            figure.moves.splice(m,1);
            console.log('deleting', figure, figure.moves);
            fig = JSON.parse(JSON.stringify(newFig));
          }
          whiteLocation = oldLoc;
        }
      }
    }
  }
  console.log('figures after', boardFigures);
}
function check(){
  if(boardFigures.WKing.check && homeMove){
    filterMoves('white', 'WKing');
  }
}
//VALIDATING A MOVE
function ifAllowed(fig, move) {
	let figure = boardFigures[fig];
	var posx = parseInt(figure.location[0]);
	var posy = parseInt(figure.location[1]);
	var desx = posx + move.x;
	var desy = posy + move.y;
	var destination = desx.toString() + desy.toString();
	if(figure.moves.includes(destination)) {
		return moved(figure, destination);
	} else if(figure.strikes.includes(destination)){
		return moved(figure, destination, true);
	} else {
		return getBack();
	}
}

var isDraging = false;
var onTheMove = null;
var startx = 0;
var starty = 0;

//Maybe for touch devices
// window.addEventListener('touchstart', function (ev) {
//   var target = ev.currentTarget
//   var touch = ev.changedTouches[0]
//   var pos = offset(touch, target)
//   //=> [ 128, 52 ]
//   console.log(pos);
// })

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
boardFigures = calculateMoves(boardFigures);

//TESting
// function mouseOver(e){
//   let figure = figures[e.target.id];
//   figure.moves.forEach(function(locid){
//     let loc = document.getElementById(locid);
//     loc.style.borderColor = 'green';
//     loc.style.borderWidth = '2px';
//   });
//   figure.strikes.forEach(function(locid){
//     let loc = document.getElementById(locid);
//     loc.style.borderColor = 'red';
//     loc.style.borderWidth = '2px';
//   });
// }
// function mouseOut(e){
//   let figure = figures[e.target.id];
//   figure.moves.forEach(function(locid){
//     let loc = document.getElementById(locid);
//     loc.style.borderColor = 'black';
//     loc.style.borderWidth = '1px';
//   });
//   figure.strikes.forEach(function(locid){
//     let loc = document.getElementById(locid);
//     loc.style.borderColor = 'black';
//     loc.style.borderWidth = '1px';
//   });
// }

function grab() {
	if(homeMove){
		var moving = document.querySelectorAll('.figure.white');
	} else {
		var moving = document.querySelectorAll('.figure.black');
	}
	moving.forEach(function(move) {
    //TESTING
    // move.addEventListener("mouseover", mouseOver);
    // move.addEventListener("mouseout", mouseOut);
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

