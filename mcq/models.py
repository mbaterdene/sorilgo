from django.db import models
from quiz.models import Question

ANSWER_ORDER_OPTIONS = (
    ('none', 'Оруулсан дарааллаар'),
    ('random', 'Санамсаргүй')
)


class MCQQuestion(Question):

    answer_order = models.CharField(
        max_length = 30, 
        null = True, 
        blank = True,
        choices = ANSWER_ORDER_OPTIONS,
        help_text = "Шалгалт бүр дээр даалгаврын хариултыг с",
        verbose_name = "Хариултын эрэмбэ"
    )

    def check_if_correct(self, guess):
        answer = Answer.objects.get(id=guess)

        if answer.correct is True:
            return True
        else:
            return False

    def order_answers(self, queryset):
        return queryset.order_by('?')
        # if self.answer_order == 'content':
        #   return queryset.order_by('Content')
    #     if self.answer_order == 'random':
    #         return queryset.order_by('?')
    #     if self.answer_order == 'none':
    #         return queryset.order_by('None')

    def get_answers(self):
        return self.order_answers(Answer.objects.filter(question = self))

    def get_answers_list(self):
        return [(answer.id, answer.content) for answer in self.order_answers(Answer.objects.filter(question = self))]
        

    def answer_choice_to_string(self, guess):
        return Answer.objects.get(id=guess).content

    class Meta:
        verbose_name = "Даалгавар"
        verbose_name_plural = "Даалгаврууд"


class Answer(models.Model):
    question = models.ForeignKey(
        MCQQuestion, 
        verbose_name = 'Даалгавар', 
        on_delete = models.CASCADE
    )

    content = models.CharField(
        max_length = 1000,
        blank = True,
        default = "",
        help_text = "Зохимжит бүх хариултыг оруулна уу. Хэдэн ч хариулттай байж болно.",
        verbose_name = "Хариулт"
    )
    picture = models.ImageField(
        upload_to = 'uploads/problem/pic/%Y/%m/answer',
        blank = True,
        null = True,
        verbose_name = "Зураг"
    )
    correct = models.BooleanField(
        blank = False,
        default = False,
        help_text = "Зөвхөн ганцхан хариултыг зөв гэж бөлгөнө үү",
        verbose_name = "Зөв хариулт эсэх"
    )

    def __str__(self):
        return self.content


    class Meta:
        verbose_name = "Хариулт"
        verbose_name_plural = "Хариултууд"





