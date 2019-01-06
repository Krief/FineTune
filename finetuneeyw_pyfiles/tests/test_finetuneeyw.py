import pytest

from finetuneeyw import Teacher, Quiz, Question, Student, Class

# NOTE :: Tests against unwritten functionality
#       - I've included several tests which I stubbed out, but for which the functionality
#         is missing. I don't believe the scope of the project included the creation
#         mechanisms for Teachers, Students, or Classes. I wanted to include somewhere
#         that I realize we will want to test these *if* we are the ones doing the
#         creation, but not go too far out of scope on the actual story.  These are kept
#         simple and lean, but represent what I believe are a good, lean set of tests
#         given the limited information on the classes.
#         ** They are all titled with _FORSHOW in the name
# NOTE :: Tests for actions
#       - There are a lot of tests for empty cases or collection edge case behavior
#           that I have cut intentionally with scope in mind. An easy example
#           is removing a student from a class isn't tested, definitely is relevant,
#           but the functionality seems non-vital right now.
#           Further, there's plenty more edgecases for functionality that was built,
#           but I've capped it at some I consider most vital for 'working functionality'.
#           Given that there is a second question all about testing, it seemed I should
#           focus on that there.

@pytest.fixture
def basicquestion():
    return Question('When?', [('1312', 'a'), ('1212', 'b')], 'b')

@pytest.fixture
def basicquestion2():
    return Question('Where?', [('Georgia', 'a'), ('Florida', 'b')], 'a')

@pytest.fixture
def teststudent():
    return Student('John')

@pytest.fixture
def studentwithcompletedquiz(regularquiz, basicquestion):
    student = Student('Eric')
    student.record_answers(regularquiz.name, {basicquestion.text: basicquestion.correct_answer})
    return student

@pytest.fixture
def historyclass(teststudent):
    return Class('History', {teststudent.full_name: teststudent})

@pytest.fixture
def advancedhistoryclass(studentwithcompletedquiz):
    return Class('History II', {studentwithcompletedquiz.full_name: studentwithcompletedquiz})

@pytest.fixture
def testteacher(historyclass):
    teach = Teacher('JoAnn')
    teach.add_class(historyclass)
    return teach

@pytest.fixture
def teacherwithquizzes(historyclass, advancedhistoryclass):
    teach = Teacher('JoAnn')
    teach.add_class(historyclass)
    teach.add_class(advancedhistoryclass)
    return teach

@pytest.fixture
def emptyquiz():
    return Quiz('Test Quiz', [], 1)


@pytest.fixture
def regularquiz(basicquestion):
    return Quiz('History', [basicquestion], 3)

@pytest.fixture
def regularquiz2(basicquestion, basicquestion2):
    return Quiz('History II', [basicquestion, basicquestion2], 3)


class TestQuestion(object):
    def test_correct_answer(self, basicquestion):
        assert basicquestion.score('b') == 1

    def test_incorrect_answer(self, basicquestion):
        assert basicquestion.score('a') == 0


class TestClass(object):
    def test_class_creation(self, historyclass, teststudent):
        assert teststudent.full_name in historyclass.get_students()

    # It would be fair for us to test for only assigning a quiz to a class inside of here, but see Teacher tests for
    #   that test and thoughts on why it exists there.

    def test_getting_quiz_list(self, historyclass, regularquiz, regularquiz2):
        historyclass.add_quiz(regularquiz)
        historyclass.add_quiz(regularquiz2)
        assert regularquiz2.name in historyclass.get_all_quizzes()

    def test_getting_partially_completed_quiz_list(self, advancedhistoryclass, studentwithcompletedquiz, regularquiz, regularquiz2):
        advancedhistoryclass.add_quiz(regularquiz)
        advancedhistoryclass.add_quiz(regularquiz2)
        assert regularquiz2.name in advancedhistoryclass.get_unfinished_quizzes(studentwithcompletedquiz.full_name)

    # The following include a failing on my part with pytest (or perhaps general testing philsophy)
    #   What I'd like to represent with these tests is a class having available tests, showing them to a student,
    #   they choose one to take (or continue taking) and then submit the answers. Much of that requires
    #   the UI, so what I'm testing is a more broken down unit test.  This is nice for better 'unit' testing,
    #   but means that there's a fair amount of overlap with student and quiz unit tests
    def test_student_taking_test_single_attempt(self, historyclass, teststudent, regularquiz, basicquestion2, basicquestion):
        studentsanswers = {basicquestion.text: basicquestion.correct_answer}
        historyclass.students[teststudent.full_name].record_answers(regularquiz.name, studentsanswers)

        recordedanswers = historyclass.students[teststudent.full_name].quiz_answers[regularquiz.name]
        assert basicquestion.score(recordedanswers[basicquestion.text]) == 1


    def test_student_taking_test_multi_attempt(self, historyclass, teststudent, regularquiz, regularquiz2, basicquestion, basicquestion2):
        firstanswers = {}
        historyclass.students[teststudent.full_name].record_answers(regularquiz.name, firstanswers)
        secondanswers = {basicquestion.text: basicquestion.correct_answer}
        historyclass.students[teststudent.full_name].record_answers(regularquiz.name, secondanswers)

        recordedanswers = historyclass.students[teststudent.full_name].quiz_answers[regularquiz.name]
        assert basicquestion.score(recordedanswers[basicquestion.text]) == 1

    def test_student_grade(self, advancedhistoryclass, studentwithcompletedquiz, regularquiz, regularquiz2):
        advancedhistoryclass.add_quiz(regularquiz)
        advancedhistoryclass.add_quiz(regularquiz2)

        students_correct_score = regularquiz.weight / (regularquiz.weight + regularquiz2.weight)

        assert advancedhistoryclass.get_student_grade(studentwithcompletedquiz.full_name) == students_correct_score


class TestTeacher(object):
    # teacher model creation tests
    def test_FORSHOW_teacher_has_no_classes(self):
        assert True

    def test_FORSHOW_teacher_has_one_class_no_student(self):
        assert True

    def test_FORSHOW_teacher_has_one_class_with_students(self):
        assert True

    def test_FORSHOW_teacher_has_multi_classes_with_students(self):
        assert True

    # teacher existence test (since we're skipping creation)
    # I'm cramming this into a single test since I believe it really
    # is better handled by individual creation scenarios, similar to above
    def test_teacher_has_attr(self, testteacher):
        assert testteacher.full_name


    # quiz making tests
    def test_create_empty_quiz(self, testteacher, emptyquiz):
        testteacher.create_quiz('', emptyquiz)
        assert emptyquiz.name in testteacher.class_agnostic_quizzes

    # I am only semi-comfortable with the following 'quiz' tests
    #  I include them and what their concept, because I do like having quizzes originate through
    #  teachers because of creating quizzes that are not tied to classes,
    #  but this does create this non-clean series where I'm already testing classes' getting
    #  quizzes in their own test suite and this pass-through has an ugly coupling
    #  I'd prefer to keep the concept (even with it's current failing) to discuss why I think
    #  this is still a realistic, good approach -OR- to hear ideas for a nicer, decoupled approach
    def test_create_regular_quiz(self, testteacher, historyclass, regularquiz):
        testteacher.create_quiz(historyclass.name, regularquiz)
        assert regularquiz.name in testteacher.classes[historyclass.name].quizzes

    def test_create_multiple_quizzes(self, teacherwithquizzes, historyclass, advancedhistoryclass, regularquiz,
                                     regularquiz2):
        teacherwithquizzes.create_quiz(historyclass.name, regularquiz)
        teacherwithquizzes.create_quiz(advancedhistoryclass.name, regularquiz2)
        assert (
            regularquiz.name in teacherwithquizzes.classes[historyclass.name].quizzes
            and regularquiz2.name in teacherwithquizzes.classes[advancedhistoryclass.name].quizzes
        )

    # quiz assignment tests
    def test_assigning_existing_quizzes_to_classes(self, teacherwithquizzes, historyclass, regularquiz):
        teacherwithquizzes.create_quiz('', regularquiz)
        teacherwithquizzes.assign_existing_quiz_to_class(regularquiz.name, historyclass.name)
        assert regularquiz.name in teacherwithquizzes.classes[historyclass.name].quizzes

    # grading tests
    def test_grade_one_student(self, teacherwithquizzes, advancedhistoryclass, studentwithcompletedquiz,
                               regularquiz, regularquiz2):
        advancedhistoryclass.add_quiz(regularquiz)
        advancedhistoryclass.add_quiz(regularquiz2)

        students_correct_score = regularquiz.weight / (regularquiz.weight + regularquiz2.weight)

        grades = teacherwithquizzes.grade_student(studentwithcompletedquiz.full_name)

        assert (len(grades) == 1
               and grades[advancedhistoryclass.name] == students_correct_score)

