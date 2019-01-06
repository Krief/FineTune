# SOME NOTES:
# -----------
#  OO Structure: My intentions are below (hopefully my code highlights them, but...)
#   [[ I've used the word list not intending it's python meaning, but just a collection ]]
#   Classes have (list of students), (list of possible quizzes available for students to take)
#   Students have (list of quizzes' answers)
#   Teachers have (list of classes), (list of quizzes unassociated with classes)
#  The reasons for this approach are long for this practice and better suited to a discussion I believe :)

#  Grading: I'm making a large assumption that 1 child can be in multiple classes a single teacher
#   teaches, and that their 'grade' for the semester should really be their grades for each class they

#  IDs vs Names: I've used names in most cases in place of proper ids. I think it makes it more readable
#   for this prototype discussion, though it's almost never how I'd want to tackle these real-world

#  Exception Handling:  Generally, I've left out exception handling as the way we would
#    respond has a lot of variables that seem out of scope. Rather than muddy the code
#    with a lot of raises to just pass the errors up I access the reader to assume at least
#    a try/catch in most cases
#    In the most severe cases, or ones where I've intentionally used ask-for-forgiveness,
#    try/excepts have been included
#   One notable problem (but not exception) that would matter in several cases that I'm not
#   checking for is creating new items in a dictionary over-top of an existing one


# This could just be a tuple or other basic construct. I'm wrapping it for
#   clarity *and* because this is a class that may often need extended to deal with
#   different question types or expanded scoring formulas
class Question:
    def __init__(self, questiontext, possibleanswers, correctanswers):
        self.text = questiontext
        self.possible_answer = possibleanswers
        self.correct_answer = correctanswers

    def score(self, answer):
        if answer in self.correct_answer:
            return 1
        else:
            return 0


class Quiz:
    def __init__(self, quizname, questions = [], weight = 1):
        self.name = quizname
        self.questions = questions
        self.weight = weight


class Student:
    def __init__(self, fullname):
        self.full_name = fullname
        self.quiz_answers = {}

    # We can record a sub or full set for any quiz at any time
    def record_answers(self, quizname, answers):
        if quizname in self.quiz_answers:
            self.quiz_answers[quizname] = {**self.quiz_answers[quizname], **answers}
        else:
            self.quiz_answers[quizname] = answers


class Class:
    def __init__(self, classname, students = {}):
        self.name = classname
        self.students = students
        self.quizzes = {}

    def add_quiz(self, quiz):
        self.quizzes[quiz.name] = quiz

    # Potential for filtering, not testing, just impulse
    def get_students(self):
        return self.students

    # This is easily expandable for if we only offer quizzes between certain dates
    def get_all_quizzes(self):
        return self.quizzes

    def get_unfinished_quizzes(self, studentname):
        past_started_quizzes = self.students[studentname].quiz_answers

        unfinished_quizzes = {}
        print(self.quizzes)
        for k, quiz in self.quizzes.items():
            if (
                    quiz.name not in past_started_quizzes
                    or len(past_started_quizzes[quiz.name]) != len(quiz.questions)
            ):
                unfinished_quizzes[quiz.name] = quiz

        return unfinished_quizzes

    def get_student_grade(self, studentname):
        total_grade = 0
        total_weights = 0

        for k, quiz in self.quizzes.items():
            quiz_grade = 0
            try:
                student_answers = self.students[studentname].quiz_answers[quiz.name]
                for question in quiz.questions:
                    quiz_grade += question.score(student_answers[question.text])
            except:
                pass # really only for the case where the students never attempted that quiz
                     # but unsure how we'd actually want to account for that in grade. Giving 0 now

            total_grade += quiz_grade * quiz.weight
            total_weights += quiz.weight

        # let's assume we don't allow 0 or negative weights
        return total_grade / total_weights


class Teacher:
    def __init__(self, fullname, classes = {}):
        self.full_name = fullname
        self.classes = classes
        # The purpose of the agnostic quizzes is that teachers will often have
        # tests they come up with that they'd like to reuse across classes or over time.
        # This is not always the case, but I expect this would be the general preference.
        self.class_agnostic_quizzes = {}

    def add_class(self, cls):
        self.classes[cls.name] = cls

    def create_quiz(self, classname, quiz):
        if classname in self.classes:
            self.classes[classname].add_quiz(quiz)
        else:
            self.class_agnostic_quizzes[quiz.name] = quiz

    def assign_existing_quiz_to_class(self, quizname, classname):
        try:
            quiz = self.class_agnostic_quizzes[quizname]
            self.classes[classname].add_quiz(quiz)
        except:
            raise

    def grade_student(self, studentname):
        grades = {}

        for k, cls in self.classes.items():
            if studentname in cls.students:
                grades[cls.name] = cls.get_student_grade(studentname)

        return grades


