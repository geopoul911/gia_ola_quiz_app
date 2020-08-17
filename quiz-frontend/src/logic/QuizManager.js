//Manager logic required by our components

// When a quiz is returned when a user clicks Play, we have to find the first unanswered question.
export const findCurrentQuestionIndex = quizData => {
  if (quizData) {
      const lastAnsweredQuestionId = quizData['last_question_id'];
      const quiz = quizData['quiz'];

      if (!lastAnsweredQuestionId)
          return 0;

      const questions = quiz['question_set'];

      const currentQuestionIndex = questions.findIndex(q => q.id === lastAnsweredQuestionId) + 1;
      return currentQuestionIndex < questions.length ? currentQuestionIndex : (questions.length - 1);

  }
};

// Update API response questions with user selected answer
export const updatedQuestions = quizData => {
    if (quizData){
        const userAnswers = quizData['quiz']['quiztakers_set']['useranswer_set'];
        const questions = quizData['quiz']['question_set'];

        return questions.map(q => {
            q['selectedAnswer'] = userAnswers.find(ua => q.id === ua.question).answer;
            return q;
        })
    }
    return [];
};


// Get questions with user answers
export const cleanUpQuizQuestions = (quizData) => {
    const quiz = quizData['quiz'];
    const userAnswers = quiz['quiztakers_set']['useranswer_set'];
    const questions = quiz['question_set'];

    const updatedQuestions = questions.map(q => {
        const ua = userAnswers.find(ua => ua.question == q.id)
        q['userAnswer'] = q.answer_set.find(as => as.id == ua.answer).label;
        q['correctAnswer'] = q.answer_set.find(as => as.is_correct).label;
        return q;
    })

    quiz['questions'] = updatedQuestions;
    return quiz;

};
