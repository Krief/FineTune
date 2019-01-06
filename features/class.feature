Feature: classes
    Scenario: getting a teacher
     Given a teacher who is able to teach it is available
      When a class needs a teacher assigned
      Then the class will be assigned the teacher

    Scenario: changing teachers
     Given a class with an existing teacher
       And a different teacher who is able to teach it is available
      When the existing teacher leaves the class
      Then the class will be assigned the new teacher

    Scenario: getting a student
     Given a class with quizzes assigned
      When a student is newly assigned to the class
      Then the student will get assigned all of the quizzes the class already has

    Scenario: teacher messages
     Given a valid text message
      When a teacher tries to send out the message to the class
      Then all students in the class will receive the message in their Message Queue

