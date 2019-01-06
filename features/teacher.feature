Feature: teachers

    Scenario: teacher creates a quiz
     Given a valid set of quiz data
      When a teacher tries to make a quiz
      Then the teacher can use the valid data to create their quiz

    Scenario: teacher creates a set of quizzes
     Given valid sets of quiz data
      When a teacher tries to make all their quizzes in one click
      Then the teacher can use the valid data to create all their quizzes

    Scenario: teacher is making an additional lesson
     Given a valid set of quiz data
       And a teacher who already created quizzes
      When the teacher tries to make another quiz
      Then the teacher can use the valid data to create their new quiz

    Scenario: converting questions to multiple choice
     Given a valid set of quiz data that is not in multiple choice form
      When a teacher tries to make a quiz
      Then teacher can use the valid data to have a quiz with only multiple choice answers

    Scenario: assigning quizzes to an individual student
     Given a teacher has an existing quiz
      When the teacher tries to assign it to a student
      Then the student will have the quiz in their list of unfinished quizzes

    Scenario: assigning quizzes to a class
     Given a teacher has an existing quiz
      When the teacher tries to assign it to a class
      Then all students in the class will have the quiz in their list of unfinished quizzes

    Scenario: grading a student
     Given a student in a class taught by a teacher
      When the teacher tries to determine the student's grade
      Then the students grade in the class will be available to the teacher