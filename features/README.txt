A quick note on approach and tests not included:

  I've stuck to testing 'positive' actions with very concrete outcomes. Some examples I've left out are below, and
  I've tried to separate them into lists of 'negatives' and 'non concrete'. I want to explain, briefly, my thoughts on
  those. This is more to explain my thoughts on these than to give a conclusive list.
    - Negative testing: Required for 100% test coverage, but not where I begin my thinking nor what I think are the most
       vital tests (unless the negative outcome would cause a showstopped or data-integrity issue).
    - Non-concrete: I believe these can be useful, but often are better kept in a separate repository/area as they
        are for manual/smoke testing and, too often, I have seen people write very convoluted automated tests trying to
        get at them.
        Sometimes there are tests *within* the scenarios that can/should be ripped out for smaller
        automated tests. I gave one example of this below.


## NEGATIVES ##
  "a student wishes to see their grade, but has not yet taken a test"
  "a class needs a teacher, but none are available"
  "a teacher wants to add a test, but already has the max number of quizzes for a class"

## NON-CONCRETE ##
  "a student wishes to see their grade, but is not able to see anyone else's"
    ^^ This could be done partially with "on a page where students are able to see class grade information, they can
        see their own grade, the average grade, etc, but no one else's grade directly". The problem here is that
        other grades could still be inferred (eg, avg = 33%, the student got 100%, there are 3 students),
        so indirectly is a hard problem to write ALL tests for.
  "a teacher "