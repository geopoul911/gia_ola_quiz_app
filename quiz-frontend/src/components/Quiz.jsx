import React, { Component, Fragment } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { findCurrentQuestionIndex, updatedQuestions } from '../logic/QuizManager';
import Summary from './Summary';

const BACKEND_LOAD_QUIZ_ENDPOINT = 'http://localhost:8001/api/quiz/quizzes';
const BACKEND_SUBMIT_ANSWER_ENDPOINT = 'http://localhost:8001/api/quiz/save-answer/';

const HEADERS = {
    "Content-type": "Application/json",
};


// Main component that renders the quiz question and answers
class Play extends Component {

    constructor( props) {
        super(props);

        //State required by our application
        this.state = {
            questions: [], //All the questions of our quiz
            currentQuestionIndex: 0, //Index of the current question that is displayed
            currentQuestion: {}, //Current question details
            selectedAnswer: null, //The answer a user has selected
            quizTakerId: null, //Id of the person taking the quiz. this id maps to the id in the backend QuizTaker model
            loaded: false, //Is the quiz loaded.
            noData: false, // Is there data to be displayed
            slug: '', //Url path for the quiz (eg: cricket-quiz)
            completed: false, // is the quiz completed
            score: null, //Score for quiz. used once the quiz is completed to display the final score
        }

    }

    // Called when the component is mounted. makes API request to load quiz
    componentDidMount() {
        HEADERS['Authorization'] = 'Token ' + localStorage.getItem('userToken');
        axios.get(BACKEND_LOAD_QUIZ_ENDPOINT, {
            headers: HEADERS
        })
        .then(res => {
            if (res.status === 204) {
                this.setState({
                    loaded: true,
                    noData: true,
                });
                return;
            }
            const quizData = res.data;

            // Loaded quiz data is set to the state
            if (quizData && quizData['quiz']) {
                const questions = updatedQuestions(quizData);
                const currentQuestionIndex = findCurrentQuestionIndex(quizData);
                const quizTakerId = quizData['quiz']['quiztakers_set']['id'];

                this.setState({
                    questions,
                    currentQuestionIndex,
                    quizTakerId,
                    currentQuestion: questions[currentQuestionIndex],
                    selectedAnswer: questions[currentQuestionIndex].selectedAnswer,
                    loaded: true,
                    slug: quizData['quiz']['slug'],
                    noData: false,
                });
            }
        })
    }


    // When an answer is clicked, take note and update the state
    handleAnswerClick = (e) => {
        const answer = e.target.id;

        const questions = this.state.questions;
        const currentQuestion = this.state.currentQuestion;
        const selectedIndex = this.state.currentQuestionIndex;

        currentQuestion['selectedAnswer'] = answer;
        questions[selectedIndex] = currentQuestion;


        this.setState({
            selectedAnswer: e.target.id,
            questions,
        });
    };

    // When an answer is submitted, update the backend
    handleAnswerSubmit = (e) => {
        HEADERS['Authorization'] = 'Token ' + localStorage.getItem('userToken');

        const answer = this.state.selectedAnswer;
        const questions = this.state.questions;
        const question = this.state.currentQuestion.id;
        const quiztaker = this.state.quizTakerId;
        const selectedIndex = this.state.currentQuestionIndex;
        const nextQuestionIndex = selectedIndex + 1;
        const slug = this.state.slug;
        const nextQuestion = questions[nextQuestionIndex];

        if (nextQuestionIndex < questions.length) {
            axios({
                method: 'patch',
                url: BACKEND_SUBMIT_ANSWER_ENDPOINT,
                headers: HEADERS,
                data: {
                    quiztaker,
                    question,
                    answer,
                }
            }).then((res) => {
                this.setState({
                    currentQuestionIndex: nextQuestionIndex,
                    currentQuestion: nextQuestion,
                    selectedAnswer: nextQuestion['selectedAnswer'],
                })
            })
        } else {
            axios({
                method: 'post',
                url: `http://localhost:8001/api/quiz/quizzes/${slug}/submit/`,
                headers: HEADERS,
                data: {
                    quiztaker,
                    question,
                    answer,
                }
            }).then((res) => {
                this.setState({
                    completed: true,
                    score: res.data['quiztaker_set']['score']
                })
            })
        }
    };

    // Handle previous navigation by changing current index
    handlePreviousNavigation = (e) => {
        const nextQuestionIndex = this.state.currentQuestionIndex - 1;
        const currentQuestion = this.state.questions[nextQuestionIndex];

        if (nextQuestionIndex >= 0) {
            this.setState({
                currentQuestionIndex: nextQuestionIndex,
                currentQuestion: currentQuestion,
                selectedAnswer: currentQuestion.selectedAnswer,
            })
        }
    };

    handleHomeClick = () => {
        this.props.history.push('/');
    };

    render() {
        // Quiz is completed. show score
        if (this.state.completed) {
            return (<Summary score={this.state.score}/>)
        // No quizzes available in backend
        } else if (this.state.loaded && this.state.noData){
            return (
                <Fragment>
                    <div className='questions'>
                        <h5>You have completed all available quizzes.</h5>
                    </div>
                    <div className='quiz-summary'>
                    <section>
                        <ul>
                            <li>
                                <Link to="/">Back to Home</Link>
                            </li>
                        </ul>
                    </section>
                    </div>
                </Fragment>
            )
        }
        // Quiz available and loaded
        else if (this.state.loaded) {
            const currentQuestion = this.state.questions[this.state.currentQuestionIndex];
            const questionTitle = currentQuestion.label.replace(/&quot;/g, '\"');
            const answers = currentQuestion.answer_set;
            const isLastQuestion = this.state.currentQuestionIndex === this.state.questions.length - 1;
            const selectedAnswer = currentQuestion.selectedAnswer;

            return (
                <Fragment>
                    <div className='questions'>

                        <h5>{`${this.state.currentQuestionIndex + 1}/10 `}</h5>
                        <h5>{questionTitle}</h5>
                            <div className='answers-container'>
                                <p className={selectedAnswer && selectedAnswer == answers[0].id ?
                                    'answer answer-selected' : 'answer'} id = {answers[0].id}
                                onClick={this.handleAnswerClick}>{answers[0].label}</p>
                                <p className={selectedAnswer && selectedAnswer == answers[2].id ?
                                    'answer answer-selected' : 'answer'} id = {answers[2].id}
                                onClick={this.handleAnswerClick}>{answers[2].label}</p>
                            </div>
                            <div className='answers-container'>
                                <p className={selectedAnswer && selectedAnswer == answers[1].id ?
                                    'answer answer-selected' : 'answer'} id = {answers[1].id}
                                onClick={this.handleAnswerClick}>{answers[1].label}</p>
                                <p className={selectedAnswer && selectedAnswer == answers[3].id ?
                                    'answer answer-selected' : 'answer'} id = {answers[3].id}
                                onClick={this.handleAnswerClick}>{answers[3].label}</p>
                            </div>

                            <div className='button-container'>
                                <button className='button-previous' onClick={this.handlePreviousNavigation}>Previous</button>
                                {
                                    isLastQuestion ?
                                            <button onClick={this.handleAnswerSubmit} className='button-next'>Submit</button> :
                                        <button onClick={this.handleAnswerSubmit} className='button-next'>Next</button>
                                }
                                <button onClick={this.handleHomeClick} className='button-home'>Home</button>
                            </div>
                    </div>
                </Fragment>
            )
        } else {
            // We are still loading the quiz
            return (
                <Fragment>
                    <div className='questions'>
                        <h5>Loading Quiz...</h5>
                    </div>
                </Fragment>
            )
        }
    }
}

export default Play;
