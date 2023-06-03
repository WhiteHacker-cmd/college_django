import React from 'react';
import PropTypes from 'prop-types';
import ReactDOM from 'react-dom';
import Websocket from 'react-websocket'
import $ from 'jquery'
import CreateGame from './CreateGame'
import JoinGame from './JoinGame';

class LobbyBase extends React.Component {

    constructor(props) {
        super(props);
        // bind button click
        this.sendSocketMessage = this.sendSocketMessage.bind(this);
    }

  


    componentDidMount() {
        
    }

    componentWillUnmount() {
        // this.serverRequest.abort();
    }

    handleData(data) {
        //receives messages from the connected websocket
        let result = JSON.parse(data)
        if(this.props.current_user.username === result.creator_username || this.props.current_user.username === result.opponent_username){
            window.location.href = result.game_url;
        }
        
        

        
    }

    sendSocketMessage(message){
        // sends message to channels back-end
       const socket = this.refs.socket
       socket.state.ws.send(JSON.stringify(message))
    }

    render() {
        return (

            <div className="row">
                <Websocket ref="socket" url={this.props.socket}
                    onMessage={this.handleData.bind(this)} reconnect={true}/>
                <div className="col-lg-4">
                    <CreateGame player={this.props.current_user}
                                 sendSocketMessage={this.sendSocketMessage} />
                </div>
                <div className="col-lg-4">
                     <JoinGame player={this.props.current_user}
                                sendSocketMessage={this.sendSocketMessage} />
                </div>
            </div>

        )
    }
}

LobbyBase.propTypes = {
    socket: PropTypes.string
};

export default LobbyBase;