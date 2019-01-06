Feature: students

    Scenario: student wants to join a class
     Given a class with an opening
      When a student tries to join
      Then the class will have the student on its roster

    Scenario: student finishes a new quiz
     Given a student with an available, unstarted quiz
      When the student starts
       And the student completes the quiz
      Then the quiz is marked completed and all answers are saved

    Scenario: student interrupted during a quiz
     Given a student with an available quiz
      When the student starts the quiz
       But the student does not complete the quiz
      Then the quiz is still available to the student
       And the parts of the quiz completed are saved

    Scenario: student finishes a previously started quiz
     Given a student with an available, partially completed quiz
      When the student restarts
       And the student completes the quiz
      Then the quiz is marked completed and all answers are saved