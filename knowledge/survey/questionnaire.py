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
        self.defaultAnswerRange = 5


class QuestionGroup(object):

    implements(IQuestionGroup)

    def __init__(self, questionnaire):
        self.questionnaire = questionnaire
        self.questions = []
        self.feedbackItems = []


class Question(object):

    implements(IQuestion)

    _answerRange = None
    
    def __init__(self, questionnaire, text=u''):
        self.questionnaire = questionnaire
        self.feedbackItems = {}
        self.text = text
        self.revertAnswerOptions = False

    def getAnswerRange(self):
        return self._answerRange or self.questionnaire.defaultAnswerRange
    def setAnswerRange(self, value):
        self._answerRange = value
    answerRange = property(getAnswerRange, setAnswerRange)


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
                if question.revertAnswerOptions:
                    value = question.answerRange - value - 1
                result[fi] = result.get(fi, 0.0) + rf * value
        return sorted(result.items(), key=lambda x: -x[1])

    def getGroupedResult(self):
        result = []
        for qugroup in self.questionnaire.questionGroups:
            score = scoreMax = 0.0
            for qu in qugroup.questions:
                value = self.values.get(qu)
                if value is None or isinstance(value, basestring):
                    continue
                if qu.revertAnswerOptions:
                    value = qu.answerRange - value - 1
                score += value 
                scoreMax += qu.answerRange - 1
            if scoreMax > 0.0:
                relScore = score / scoreMax
                wScore = relScore * len(qugroup.feedbackItems) - 0.00001
                if qugroup.feedbackItems:
                    feedback = qugroup.feedbackItems[int(wScore)]
                else:
                    feedback = FeedbackItem()
                result.append(dict(
                        group=qugroup,
                        feedback=feedback,
                        score=relScore))
        ranks = getRanks([r['score'] for r in result])
        for idx, r in enumerate(result):
            r['rank'] = ranks[idx]
        return result

    def getTeamResult(self, mine, teamData):
        result = []
        for idx, qgdata in enumerate(mine):
            values = [data.values.get(qgdata['group']) for data in teamData]
            values = [v for v in values if v is not None]
            #avg = sum(values) / len(teamData)
            avg = sum(values) / len(values)
            result.append(dict(group=qgdata['group'], average=avg))
        ranks = getRanks([r['average'] for r in result])
        for idx, r in enumerate(result):
            r['rank'] = ranks[idx]
        return result

def getRanks(values):
    ordered = list(reversed(sorted(values)))
    return [ordered.index(v) + 1 for v in values]
