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
from cybertools.knowledge.survey.interfaces import IQuestionnaire, IQuestion
from cybertools.knowledge.survey.interfaces import IResultElement, IResponse


class Questionnaire(object):

    implements(IQuestionnaire)
    
    def __init__(self):
        self.questions = []
        self.responses = []
        self.defaultAnswerOptions = range(5)


class Question(object):

    implements(IQuestion)

    _answerOptions = None
    
    def __init__(self, questionnaire, text=u''):
        self.questionnaire = questionnaire
        self.resultElements = {}
        self.text = text

    def getAnswerOptions(self):
        return self._answerOptions or self.questionnaire.defaultAnswerOptions
    def setAnswerOptions(self, value):
        self._answerOptions = value
    answerOptions = property(getAnswerOptions, setAnswerOptions)


class ResultElement(object):

    implements(IResultElement)
    
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
            for re, rf in question.resultElements.items():
                result[re] = result.get(re, 0.0) + rf * value
                #print re.text, rf, value
        return sorted(result.items(), key=lambda x: -x[1])
