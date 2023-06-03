import React, {Component} from 'react'
import PropTypes from 'prop-types';

// const creator_icon = <img src="/static/img/blue-player.png" />


class AnswerBox extends Component {
    constructor(props) {
        super(props)
        this.state = {
            answer: this.props.answer,
            isDisabled: this.props.isDisabled
        }
        
        this.answerClicked = this.answerClicked.bind(this)
    }



    componentWillReceiveProps(newProps){
        this.setState({
            answer: newProps.answer,
            quiz_id: newProps.quiz_id,
            isDisabled: newProps.isDisabled
            })
    }


    answerClicked(){
        if(this.state.isDisabled === false){
            this.props.handler()
            this.props.sendSocketMessage({action: "answer", 
                                      answer: this.state.answer,
                                      quiz_id:this.props.quiz_id})
        }
        
    }

    render() {
        return (
        <button style={{margin: "3px"}} type="button" className="btn btn-primary" onClick={this.answerClicked} disabled={this.state.isDisabled}>{this.state.answer}</button>
        )
    }

    
}

AnswerBox.PropTypes = {
    handler: PropTypes.func,
    isDisabled: PropTypes.bool,
    answer: PropTypes.string,
    sendSocketMessage: PropTypes.func,
    quiz_id: PropTypes.number
}


export default AnswerBox