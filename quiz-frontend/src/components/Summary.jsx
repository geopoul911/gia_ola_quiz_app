import React, { Component, Fragment } from 'react';
import { Link } from 'react-router-dom';

// Display final score
class Summary extends Component {
    constructor (props) {
        super(props);
    }


    render () {
        const { score } = this.props;

        return (
            <Fragment>
                <title>Quiz App - Summary</title>
                <div className="quiz-summary">
                    <Fragment>
                        <div style={{ textAlign: 'center' }}>
                            <span className="mdi mdi-check-circle-outline success-icon"></span>
                        </div>
                        <h1>Quiz has ended</h1>
                        <div className="container stats">
                            <h2>Your Score: {score}&#37;</h2>
                        </div>
                        <section>
                            <ul>
                                <li>
                                    <Link to ="/">Back to Home</Link>
                                </li>
                            </ul>
                        </section>
                    </Fragment>
                </div>
            </Fragment>
        );
    }
}
export default Summary;
