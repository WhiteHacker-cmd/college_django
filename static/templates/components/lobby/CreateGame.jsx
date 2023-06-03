import React from 'react'
import PropTypes from 'prop-types';
import $ from 'jquery'


class CreateGame extends React.Component{
  constructor(props) {
      super(props)
   

  
    this.onCreateGameClick = this.onCreateGameClick.bind(this);
    this.exit = this.exit.bind(this);
   
  }

  exit(){
    document.querySelector("#hide").style.visibility = "hidden";
    document.querySelector("body").style.visibility = "visible";
    this.props.sendSocketMessage({action: "exit"})
  }

  

  onCreateGameClick(event) {
    document.querySelector("button").onclick = this.exit
    document.querySelector("body").style.visibility = "hidden";
    document.querySelector("#hide").style.visibility = "visible";
    this.props.sendSocketMessage({action: "create"})

      
      
      
  }


  render() {
    
    return (
      <div>

          <div className="panel panel-primary">
                  <div className="panel-heading">
                      <span>Create Game</span>
                      <a href="#" className="pull-right badge" onClick={this.onCreateGameClick} id="create_game">Create</a>
                  </div>
                  
          </div>

      </div>
    )
  }
}

CreateGame.defaultProps = {

};

CreateGame.propTypes = {
    player: PropTypes.object,
    sendSocketMessage: PropTypes.func
};


export default CreateGame