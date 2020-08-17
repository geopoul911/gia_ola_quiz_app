import React, { Component, Fragment } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { cleanUpQuizQuestions } from '../logic/QuizManager';

const BACKEND_MY_QUIZZES_ENDPOINT = 'http://localhost:8001/api/quiz/my-quizzes';
const BACKEND_QUIZ_DETAIL_ENDPOINT = 'http://localhost:8001/api/quiz/quizzes/';

const HEADERS = {
    "Content-type": "Application/json",
};

// History view
class History extends Component {
    constructor (props) {
        super(props);
        this.state = {
            quizzes: [],
            detailView: false,
            quizDetail: {},
        }
    }

    // Load all completed quizzes
    componentDidMount() {
        HEADERS['Authorization'] = 'Token ' + localStorage.getItem('userToken');
        axios.get(BACKEND_MY_QUIZZES_ENDPOINT, {
            headers: HEADERS
        })
        .then((res) => {
            this.setState({
                quizzes: res.data,
            })
        })

    }

    // When a quiz is clicked, load that quiz data
    rowClickHandler = (quiz) => {
        axios.get(BACKEND_QUIZ_DETAIL_ENDPOINT + quiz.slug, {
            headers: HEADERS
        })
            .then((res) => {
                this.setState({
                    quizDetail: cleanUpQuizQuestions(res.data),
                    detailView: true,
                })
            })
    };

    resetToMyQuizzes = () => {
        this.setState({
            detailView: false,
        })
    }


    render () {

        return (
            <Fragment>
                <div className="quiz-summary container">
                    {
                        !this.state.detailView ?
                        <Fragment>
                            <div style={{textAlign: 'center'}}>
                                <span className="mdi mdi-check-circle-outline success-icon"></span>
                            </div>
                            <h1>Completed Quizzes</h1>
                            <table style={{textAlign: 'center'}}>
                                <thead>
                                <tr >
                                    <th>Quiz</th>
                                    <th>My Score</th>
                                    <th style={{textAlign: 'center'}}>Submission Rate Over 70 (%)</th>
                                </tr>
                                </thead>

                                <tbody>
                                {
                                    this.state.quizzes.map(quiz => {
                                        return (
                                            <tr key={quiz.slug} onClick={() => this.rowClickHandler(quiz)}>
                                                <td>{quiz.name}</td>
                                                <td>{quiz.score}</td>
                                                <td>{quiz.threshold_rate}</td>
                                            </tr>
                                        )
                                    })
                                }
                                </tbody>
                            </table>

                            <section>
                                <ul>
                                    <li>
                                        <Link to="/">Back to Home</Link>
                                    </li>
                                </ul>
                            </section>
                        </Fragment> :

                        <Fragment>
                            <div style={{textAlign: 'center'}}>
                                <span className="mdi mdi-check-circle-outline success-icon"></span>
                            </div>
                            <h1>{this.state.quizDetail.name}</h1>
                            <table>
                                <thead>
                                <tr>
                                    <th>Question</th>
                                    <th>My Answer</th>
                                    <th>Correct Answer</th>
                                    <th>Correct Percentage (%)</th>
                                </tr>
                                </thead>

                                <tbody>
                                {
                                    this.state.quizDetail.questions.map(detail => {
                                        return (
                                            <tr key={detail.id}>
                                                <td>{detail.label.replace(/&quot;/g,'\"')}</td>
                                                <td>{detail.userAnswer}</td>
                                                <td>{detail.correctAnswer}</td>
                                                <td>{detail.useranswer_percent}</td>
                                            </tr>
                                        )
                                    })
                                }
                                </tbody>
                            </table>

                            <section>
                                <ul>
                                    <li>
                                        <Link onClick={this.resetToMyQuizzes}>Back to My Quizzes</Link>
                                    </li>
                                    <li>
                                        <Link to="/">Back to Home</Link>
                                    </li>
                                </ul>
                            </section>
                        </Fragment>
                    }
                </div>
            </Fragment>
        );
    }
}
export default History;
