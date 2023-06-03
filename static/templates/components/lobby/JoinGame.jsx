import React from 'react'
import PropTypes from 'prop-types';
import $ from 'jquery'


class JoinGame extends React.Component{
  constructor(props) {
      super(props)
    
      // bind button click
     this.join = this.join.bind(this);
     this.exit = this.exit.bind(this);
    
    }


    exit(){
      document.querySelector("#hide").style.visibility = "hidden";
      document.querySelector("body").style.visibility = "visible";
      this.props.sendSocketMessage({action: "exit"})
    }

    join(event) {
      document.querySelector("button").onclick = this.exit
      document.querySelector("body").style.visibility = "hidden";
      document.querySelector("#hide").style.visibility = "visible";
      this.props.sendSocketMessage({action: "join"})

        
            
        
        
    }

    
    render() {
      return (
        <div>

            <div className="panel panel-primary">
                    <div className="panel-heading">
                        <span>Join</span>
                        <a href="#" className="pull-right badge" onClick={this.join} id="create_game">Join</a>
                    </div>
                    
            </div>

        </div>
      )
    }
}

JoinGame.defaultProps = {

};

JoinGame.propTypes = {
    player: PropTypes.object,
    sendSocketMessage: PropTypes.func
};


export default JoinGame