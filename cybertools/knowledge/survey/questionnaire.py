# cybertools.knowledge.survey.questionnaire

""" Questionnaires, questions and other stuff needed for surveys.
"""

from zope.interface import implementer
from cybertools.knowledge.survey.interfaces import IQuestionnaire
from cybertools.knowledge.survey.interfaces import IQuestionGroup, IQuestion
from cybertools.knowledge.survey.interfaces import IFeedbackItem, IResponse


@implementer(IQuestionnaire)
class Questionnaire(object):

    def __init__(self):
        self.questionGroups = []
        self.questions = []
        self.responses = []
        self.defaultAnswerRange = 5

    def getQuestionGroups(self, party):
        return self.questionGroups


@implementer(IQuestionGroup)
class QuestionGroup(object):

    def __init__(self, questionnaire):
        self.questionnaire = questionnaire
        self.questions = []
        self.feedbackItems = []


@implementer(IQuestion)
class Question(object):

    _answerRange = None
    
    def __init__(self, questionnaire, text=u''):
        self.questionnaire = questionnaire
        self.feedbackItems = {}
        self.text = text
        self.revertAnswerOptions = False
        self.questionType = 'value_selection'
        self.answerRange = None


@implementer(IFeedbackItem)
class FeedbackItem(object):

    def __init__(self, text=u''):
        self.text = text


@implementer(IResponse)
class Response(object):

    def __init__(self, questionnaire, party):
        self.questionnaire = questionnaire
        self.party = party
        self.values = {}
        self.texts = {}

    def getResult(self):
        result = {}
        for question, value in self.values.items():
            if question.questionType != 'value_selection':
                continue
            for fi, rf in question.feedbackItems.items():
                if question.revertAnswerOptions:
                    answerRange = (question.answerRange or 
                            self.questionnaire.defaultAnswerRange)
                    value = answerRange - value - 1
                result[fi] = result.get(fi, 0.0) + rf * value
        return sorted(result.items(), key=lambda x: -x[1])

    def getGroupedResult(self):
        result = []
        for qugroup in self.questionnaire.getQuestionGroups(self.party):
            score = scoreMax = 0.0
            for qu in qugroup.questions:
                if qu.questionType not in (None, 'value_selection'):
                    continue
                value = self.values.get(qu)
                if value is None or isinstance(value, basestring):
                    continue
                answerRange = (qu.answerRange or 
                               self.questionnaire.defaultAnswerRange)
                if qu.revertAnswerOptions:
                    value = answerRange - value - 1
                score += value 
                scoreMax += answerRange - 1
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

    def getTeamResult(self, groups, teamData):
        result = []
        for idx, group in enumerate(groups):
            values = [data.values.get(group) for data in teamData]
            values = [v for v in values if v is not None]
            #avg = sum(values) / len(teamData)
            if not values:
                continue
            avg = sum(values) / len(values)
            result.append(dict(group=group, average=avg))
        ranks = getRanks([r['average'] for r in result])
        for idx, r in enumerate(result):
            r['rank'] = ranks[idx]
        return result

def getRanks(values):
    ordered = list(reversed(sorted(values)))
    return [ordered.index(v) + 1 for v in values]
