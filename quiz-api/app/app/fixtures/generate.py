import requests
import json
import random
import datetime

API_URL = 'https://opentdb.com/api.php?amount=50&type=multiple'
LIMIT = 100
QUIZ_COUNT = 10
QUESTIONS_PER_QUIZ = 10

processed_questions = set()


# Write to json file
def write_to_file(content, path):
    with open(path, 'w') as f:
        json.dump(content, f)

# Chunk list into equal sized smaller lists.
# We use this to break our questions into chunks of 10
def chunks(mylist, chunk_size):
    return [mylist[offs:offs+chunk_size] for offs in range(0, len(mylist), chunk_size)]


def load_questions():
    question_answer_list = []

    while len(question_answer_list) < LIMIT:
        res = requests.get(API_URL)
        questions = json.loads(res.content)['results']

        for q in questions:
            label = q['question']

            # If we have processed this question before, ignore it
            if label in processed_questions:
                continue

            # Create question answer list
            answers = [
                {
                    'answer': q['incorrect_answers'][0],
                    'is_correct': False
                },
                {
                    'answer': q['incorrect_answers'][1],
                    'is_correct': False
                },
                {
                    'answer': q['incorrect_answers'][2],
                    'is_correct': False
                },
                {
                    'answer': q['correct_answer'],
                    'is_correct': True
                }
            ]

            # Shuffle to change order of answers
            random.shuffle(answers)

            # Add to our questions list
            question_answer_list.append({
                'question': label,
                'answers': answers  # Last answer is correct
            })

            # Keep track of the questions we add. to avoid duplicates
            processed_questions.add(label)

            # Terminate loop if 1000 question limit is reached
            if len(question_answer_list) >= LIMIT:
                break

            print('{} unique questions collected'.format(len(question_answer_list)))

    print('Question collection is complete'.format(LIMIT))
    return question_answer_list


# load questions
questions = load_questions()

quiz_pk = 1
question_pk = 1
answer_pk = 1
chunks = chunks(questions, QUESTIONS_PER_QUIZ)  # Break our questions into separate chunks. each chunk will belong to an individual quiz

QUIZ_JSON = []
QUESTION_JSON = []
ANSWER_JSON = []

# Loop to create quiz, question, answer data
print('generating model data...')
while quiz_pk <= QUIZ_COUNT:
    questions_for_quiz = chunks[quiz_pk-1]
    quiz_model = 'quiz.quiz'

    # Create quiz model and append to QUIZ_JSON list
    quiz_data = {
        "model": "quiz.quiz",
        "pk": quiz_pk,
        "fields": {
            "name": 'Quiz {}'.format(quiz_pk),
            "description": "quiz {} description".format(quiz_pk),
            "slug": "quiz-{}".format(quiz_pk),
            "roll_out": True,
            "timestamp": str(datetime.datetime.utcnow())
        }
    }
    QUIZ_JSON.append(quiz_data)

    # Create question model and append to question list
    for q in questions_for_quiz:
        question_data = {
            "model": "quiz.question",
            "pk": question_pk,
            "fields": {
                "quiz": quiz_pk,
                "label": q['question'],
                "order": 0
            }
        }
        QUESTION_JSON.append(question_data)

        # Generate answers
        count = 0
        while count < 4:
            answer_data = {
                "model": "quiz.answer",
                "pk": answer_pk,
                "fields": {
                    "question": question_pk,
                    "label": q['answers'][count]['answer'],
                    "is_correct": q['answers'][count]['is_correct']
                }
            }
            ANSWER_JSON.append(answer_data)
            answer_pk += 1
            count += 1

        question_pk += 1

    quiz_pk += 1

print('writing to json files...')
write_to_file(QUIZ_JSON, 'quiz.json')
write_to_file(QUESTION_JSON, 'question.json')
write_to_file(ANSWER_JSON, 'answer.json')

print('initial data has been generated!')



