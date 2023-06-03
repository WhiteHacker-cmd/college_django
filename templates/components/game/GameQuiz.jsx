import React, { Component} from 'react'
import PropTypes from 'prop-types';
import $, { removeData } from 'jquery'
import Websocket from 'react-websocket'
import AnswerBox from './AnswerBox'



class GameQuiz extends Component {
    // lifecycle methods
    constructor(props) {
        super(props);
        this.state = {
            game: "",
            isDisabled: false,
            score_of_player1: 0,
            score_of_player2: 0

        }
        // bind button click
        this.sendSocketMessage = this.sendSocketMessage.bind(this);
        this.nextClicked = this.nextClicked.bind(this);
        this.counter = this.counter.bind(this);
        this.quit = this.quit.bind(this);
        this.handler = this.handler.bind(this)
    }


    handler() {
        this.setState({ isDisabled: true })
    }

    nextClicked() {
        this.sendSocketMessage({
            action: "next",
        })




    }


    counter() {

        let countDownDate = 10;
        let next = this.nextClicked;
        var time = this.myfunc = setInterval(function () {




            // Calculating the days, hours, minutes and seconds left

            // Result is output to the specific element
            document.getElementById("countdown").innerHTML = countDownDate
            countDownDate = countDownDate - 1

            // Display the message when countdown is over
            if (countDownDate < 0) {


                clearInterval(time);
                document.getElementById("countdown").innerHTML = "TIME UP!!"

                next()



            }
        }, 1000)


    }


    componentDidMount() {
        this.getGame()
        this.counter()
    }

    componentWillUnmount() {
        this.serverRequest.abort();
       

    }

    getGame() {
        const game_url = 'https://'+ window.location.host +'/game-from-id/' + this.props.game_id

        this.serverRequest = $.get(game_url, function (result) {
    


            this.setState({ game: result.quiz[0],
            score_of_player1: result.score_of_current_user,
            score_of_player2: result.score_of_opponent})
         



        }.bind(this))

    }





    handleData(data) {
        //receives messages from the connected websocket
        let result = JSON.parse(data)
     
        
        if (result === "stop") {
            window.location.href = 'https://'+window.location.host+'/winner-from-hash/' + this.props.game_id
        }
     
        else if(result["text"] === "nothing") {
         
        }
        else if(result["action"]== "close"){
            alert(result["data"])
            clearInterval(this.myfunc)
        }
        else if(result["action"] ==="answer"){
     
            this.setState({
                score_of_player1: result["data"].score_of_current_user,
                score_of_player2: result["data"].score_of_opponent
            })
        }
        else {

            clearInterval(this.myfunc)
            this.setState({
                game: result["game"],
                isDisabled: false
            })
            this.counter()


        }
    }


    quit() {

        clearInterval(this.myfunc)
    }

    sendSocketMessage(message) {
        // sends message to channels back-end
        const socket = this.refs.socket
        socket.state.ws.send(JSON.stringify(message))
    }

    render() {
        return (

            <div className="row">
                <div className="col-sm-2 col-sm-offset-3">
                    {this.state.score_of_player1}
                </div>
                <div className="col-sm-2 text-center">
                    <h2 id="countdown" className="edited"></h2>
                </div>
                {/* <p className="edited" id="countdown"></p> */}
                <div className="col-sm-2">
                {this.state.score_of_player2}
                </div>
                <hr/>
                <hr/>
                <hr/>
                <div className="row">
                    
                    <h3 className="edited">{this.state.game.question}</h3>
                    
                    <hr />
                    <AnswerBox answer={this.state.game.option1}
                        sendSocketMessage={this.sendSocketMessage}
                        quiz_id={this.state.game.id}
                        isDisabled={this.state.isDisabled}
                        handler={this.handler} />
                    <AnswerBox answer={this.state.game.option2}
                        sendSocketMessage={this.sendSocketMessage}
                        quiz_id={this.state.game.id}
                        isDisabled={this.state.isDisabled}
                        handler={this.handler} />
                    <AnswerBox answer={this.state.game.option3}
                        sendSocketMessage={this.sendSocketMessage}
                        quiz_id={this.state.game.id}
                        isDisabled={this.state.isDisabled}
                        handler={this.handler} />
                    <AnswerBox answer={this.state.game.option4}
                        sendSocketMessage={this.sendSocketMessage}
                        quiz_id={this.state.game.id}
                        isDisabled={this.state.isDisabled}
                        handler={this.handler} />
                    {/* <button style={{ margin: "20px" }} type="button" className="btn btn-danger" onClick={this.quit}>next</button> */}

                    <Websocket ref="socket" url={this.props.socket}
                        onMessage={this.handleData.bind(this)} reconnect={true} />
                </div>
            </div>

        )
    }
}

GameQuiz.propTypes = {
    game_id: PropTypes.string,
    socket: PropTypes.string,
    current_user: PropTypes.object

}


export default GameQuiz