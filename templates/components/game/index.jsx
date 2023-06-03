import React from 'react';
import GameQuiz from './GameQuiz.jsx'
import ReactDOM from 'react-dom'
import $ from 'jquery'

let current_user = null
const game = $("#game_component").data("game")


const game_sock = 'wss://' + window.location.host + "/game/" + game + "/"




$.get('https://'+ window.location.host +'/current-user/?format=json', function(result){
    // gets the current user information from Django
    current_user = result
    render_component()
})


function render_component(){
    ReactDOM.render(<GameQuiz current_user={current_user} game_id={game} socket={game_sock}/>, document.getElementById("game_component"))
}


