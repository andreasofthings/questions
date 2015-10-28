from django import template
from ..models import Question

register = template.Library()


class UserAnswerNode(template.Node):
    """
    TemplateTag RenderNode

    renders whether user answered a question.pk
    """
    def __init__(self, user, question):
        self.user = template.Variable(user)
        self.variable_question = template.Variable(question)

    def render(self, context):
        real_question = Question.objects.get(
            pk=self.variable_question.resolve(context)
        )
        return real_question.has_answer(self.user.resolve(context))


@register.tag('user_answered')
def user_answered(parser, token):
    """
    user_answered
    =============

    Templatetag to render whether a user actually answered a question.
    """
    try:
        tag_name, user, question = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires exactly two arguments" %
            token.contents.split()[0]
        )
    return UserAnswerNode(user, question)
