#
#  Copyright (c) 2013 Helmut Merz helmutm@cy55.de
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

"""
Questionnaires, questions and other stuff needed for surveys.
"""

from zope.interface import implements
from cybertools.knowledge.survey.interfaces import IQuestionnaire
from cybertools.knowledge.survey.interfaces import IQuestionGroup, IQuestion
from cybertools.knowledge.survey.interfaces import IFeedbackItem, IResponse


class Questionnaire(object):

    implements(IQuestionnaire)
    
    def __init__(self):
        self.questionGroups = []
        self.questions = []
        self.responses = []
        self.defaultAnswerOptions = range(5)


class QuestionGroup(object):

    implements(IQuestionGroup)

    def __init__(self, questionnaire):
        self.questionnaire = questionnaire
        self.questions = []
        self.feedbackItems = []


class Question(object):

    implements(IQuestion)

    _answerOptions = None

    revertAnswerOptions = False
    
    def __init__(self, questionnaire, text=u''):
        self.questionnaire = questionnaire
        self.feedbackItems = {}
        self.text = text

    def getAnswerOptions(self):
        result = self._answerOptions or self.questionnaire.defaultAnswerOptions
        if self.revertAnswerOptions:
            result.reverse()
        return result
    def setAnswerOptions(self, value):
        self._answerOptions = value
    answerOptions = property(getAnswerOptions, setAnswerOptions)


class FeedbackItem(object):

    implements(IFeedbackItem)
    
    def __init__(self, text=u''):
        self.text = text


class Response(object):

    implements(IResponse)
    
    def __init__(self, questionnaire, party):
        self.questionnaire = questionnaire
        self.party = party
        self.values = {}

    def getResult(self):
        result = {}
        for question, value in self.values.items():
            for fi, rf in question.feedbackItems.items():
                result[fi] = result.get(fi, 0.0) + rf * value
        return sorted(result.items(), key=lambda x: -x[1])

    def getGroupedResult(self):
        result = []
        for qugroup in self.questionnaire.questionGroups:
            score = scoreMax = 0.0
            for qu in qugroup.questions:
                score += self.values.get(qu, 0.0)
                scoreMax += max(qu.answerOptions)
            relScore = score / scoreMax
            wScore = relScore * (len(qugroup.feedbackItems) - 1)
            result.append((qugroup.feedbackItems[int(wScore)], wScore))
        return result
