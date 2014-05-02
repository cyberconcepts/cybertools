==========================
Surveys and Questionnaires
==========================

Let's first set up a  questionaire.

  >>> from cybertools.knowledge.survey.questionnaire import Questionnaire, Question
  >>> quest = Questionnaire()

  >>> qu01 = Question(quest)
  >>> qu02 = Question(quest)
  >>> qu03 = Question(quest)
  >>> qu01.revertAnswerOptions = True


Question-related Feedback Items
===============================

We now assign result elements with the questions of this questionnaire.

  >>> from cybertools.knowledge.survey.questionnaire import FeedbackItem
  >>> fi01 = FeedbackItem('fi01')
  >>> fi02 = FeedbackItem('fi02')
  >>> fi03 = FeedbackItem('fi03')

  >>> qu01.feedbackItems = {fi01: 0.8, fi03: 0.2}
  >>> qu02.feedbackItems = {fi01: 0.3, fi02: 0.7, fi03: 0.1}
  >>> qu03.feedbackItems = {fi01: 0.2, fi03: 0.9}


Responses
---------

  >>> from cybertools.knowledge.survey.questionnaire import Response
  >>> resp01 = Response(quest, 'john')
  >>> resp01.values = {qu01: 2, qu02: 1, qu03: 4}

It's possible to leave some of the questions unanswered.

  >>> resp02 = Response(quest, 'john')
  >>> resp02.values = {qu01: 2, qu03: 4}


Evaluation
==========

Now let's calculate the result for resp01.

  >>> res = resp01.getResult()
  >>> for fi, score in res:
  ...     print fi.text, score
  fi03 4.1
  fi01 2.7
  fi02 0.7

  >>> res = resp02.getResult()
  >>> for fi, score in res:
  ...     print fi.text, score
  fi03 4.0
  fi01 2.4

Grouped feedback items
----------------------

  >>> from cybertools.knowledge.survey.questionnaire import QuestionGroup
  >>> qugroup = QuestionGroup(quest)
  >>> quest.questionGroups.append(qugroup)
  >>> qugroup.questions = [qu01, qu02, qu03]
  >>> qugroup.feedbackItems = [fi01, fi02, fi03]

  >>> res = resp01.getGroupedResult()
  >>> for qugroup, fi, score in res:
  ...     print fi.text, round(score, 2)
  fi02 0.58

  >>> res = resp02.getGroupedResult()
  >>> for qugroup, fi, score in res:
  ...     print fi.text, round(score, 2)
  fi03 0.75

Team evaluation
---------------

  >>> resp03 = Response(quest, 'mary')
  >>> resp03.values = {qu01: 1, qu02: 2, qu03: 4}

  >>> res, ranks, averages = resp01.getTeamResult([resp01, resp03])
  >>> ranks, averages
  ([2], [0.6666...])

