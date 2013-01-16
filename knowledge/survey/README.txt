==========================
Surveys and Questionnaires
==========================

Let's first set up a  questionaire.

  >>> from cybertools.knowledge.survey.questionnaire import Questionnaire, Question
  >>> quest = Questionnaire()

  >>> qu01 = Question(quest)
  >>> qu02 = Question(quest)
  >>> qu03 = Question(quest)

We now assign result elements with the questions of this questionnaire.

  >>> from cybertools.knowledge.survey.questionnaire import ResultElement
  >>> re01 = ResultElement('re01')
  >>> re02 = ResultElement('re02')
  >>> re03 = ResultElement('re03')

  >>> qu01.resultElements = {re01: 0.8, re03: 0.2}
  >>> qu02.resultElements = {re01: 0.3, re02: 0.7, re03: 0.1}
  >>> qu03.resultElements = {re01: 0.2, re03: 0.9}


Responses
---------

  >>> from cybertools.knowledge.survey.questionnaire import Response
  >>> resp01 = Response(quest, 'john')

  >>> resp01.values = {qu01: 2, qu02: 1, qu03: 4}

Now let's calculate the result for resp01.

  >>> res = resp01.getResult()
  >>> for re, score in res:
  ...     print re.text, score
  re03 4.1
  re01 2.7
  re02 0.7
