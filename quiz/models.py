import re
import json

from django.db import models
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.core.validators import MaxValueValidator, validate_comma_separated_integer_list
from django.utils.timezone import now
from django.conf import settings

from model_utils.managers import InheritanceManager
from django.db.models.signals import pre_save, post_save
import io
from django.contrib.auth.models import User
from django.contrib import messages


class CategoryManager(models.Manager):

    def new_category(self, category):
        new_category = self.create(category=re.sub('\s+', '-', category)
                                   .lower())
        new_category.save()
        return new_category


class Category(models.Model):

    category = models.CharField(
        verbose_name = "Ай",
        max_length = 250, 
        blank = True,
        unique = True, 
        null = True
    )

    objects = CategoryManager()

    class Meta:
        verbose_name = "Ай"
        verbose_name_plural = "Айнууд"

    def __str__(self):
        return self.category

class LevelManager(models.Manager):

    def new_level(self, level):
        new_level = self.create(level = re.sub('\s+', '-', level)
                                   .lower())

        new_level.save()
        return new_level


class Level(models.Model):

    level = models.CharField(
        verbose_name = "Түвшин",
        max_length = 250, 
        blank = True,
        unique = True, 
        null = True
    )

    objects = LevelManager()

    class Meta:
        verbose_name = "Түвшин"
        verbose_name_plural = "Түвшингүүд"

    def __str__(self):
        return self.level

class Quiz(models.Model):

    title = models.CharField(
        verbose_name = "Гарчиг",
        help_text = "Шалгалтыг төлөөлөх 60 тэмдэгтэд багтсан товч нэршил оруулна уу. Заавал бөглөнө.",
        max_length = 60, 
        blank = False
    )

    description = models.TextField(
        verbose_name = "Зорилго",
        blank = True, 
        help_text = "Шаардлагатай бол шалгалтын зорилгыг тодорхойлж бичнэ үү."
    )

    url = models.SlugField(
        max_length = 60, 
        blank = False,
        help_text = "Цаашид уг шалгалтад энэ линк үгээр хандах учраас шалгалтыг төлөөлөх товч латин үг оруулна уу",
        verbose_name="Шалгалтын линк"
        )

    random_order = models.BooleanField(
        blank = False, 
        default = False,
        verbose_name = "Даалгаврыг санамсаргүйгээр өгөх",
        help_text = "Хэрэглэгч бүрт шалгалтын даалгаврын дарааллыг санамсаргүйгээ өгөх эсэхийг тодорхойлно."
    )

    max_questions = models.PositiveIntegerField(
        blank = True, 
        null = True, 
        verbose_name = "Даалгаврын тоо",
        help_text = "Хамгийн ихдээ уг шалгалт хэдэн даалгавартай байхыг тодорхойлно."
    )

    answers_at_end = models.BooleanField(
        blank = False, 
        default = False,
        help_text = "Энэ тохиргоо даалгавар бөглөөд шууд зөв буруугаа мэдэх эсвэл шалгалтын сүүлд мэдэх эсэхийг тохируулна.",
        verbose_name = "Шалгалтын төгсгөлд даалгавруудын анализийг харах"
    )

    exam_paper = models.BooleanField(
        blank = False, 
        default = False,
        help_text = "Шалгалт гэж тодорхойлсон тохиолдолд хэрэглэгчийн бүх явцийг бүртгэнэ.",
        verbose_name = "Шалгалтын дэвтэр эсэх"
    )

    single_attempt = models.BooleanField(
        blank = False, 
        default = False,
        help_text = "Хэрэглэгч бүр ганцхан удаа өгнө. Энэ тохиолдолд автоматаар ШАЛГАЛТЫН ДЭВТЭР гэж бүртгэнэ.",
        verbose_name = "Ганцхан оролдлоготой эсэх"
    )

    pass_mark = models.SmallIntegerField(
        blank = True, 
        default = 0,
        verbose_name = "Нийт авах оноо",
        help_text = "Хамгийн ихдээ 100 оноо авна. Анхдагч утга нь 0 байгаа.",
        validators = [MaxValueValidator(100)]
    )

    success_text = models.TextField(
        blank = True,
        help_text = "Хэрэв хэрэглэгч шалгалтыг амжилттай дуусгавал хэлэх үг бичнэ.",
        verbose_name = "Амжилттай дуусахад гарах үг"
    )

    fail_text = models.TextField(
        verbose_name = "Амжилтгүй дуусахад гарах үг",
        blank = True, 
        help_text = "Хэрэв хэрэглэгч шалгалтыг амжилтгүй дуусгавал хэлэх үг бичнэ."
    )

    draft = models.BooleanField(
        blank = True,
        default = False,
        verbose_name = "Туршилт эсэх",
        help_text = "Туршилт тохиолдолд хэрэглэгчдэд харагдахгүй."
    )

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.url = re.sub('\s+', '-', self.url).lower()

        self.url = ''.join(letter for letter in self.url if
                           letter.isalnum() or letter == '-')

        if self.single_attempt is True:
            self.exam_paper = True

        if self.pass_mark > 100:
            raise ValidationError('%s нь 100-аас их байна' % self.pass_mark)

        super(Quiz, self).save(force_insert, force_update, *args, **kwargs)

    class Meta:
        verbose_name = "Шалгалт"
        verbose_name_plural = "Шалгалтууд"
        ordering=['id']

    def __str__(self):
        return self.title

    def get_questions(self):
        return self.question_set.all().select_subclasses()

    @property
    def get_max_score(self):
        return self.get_questions().count()

    def anon_score_id(self):
        return str(self.id) + "_score"

    def anon_q_list(self):
        return str(self.id) + "_q_list"

    def anon_q_data(self):
        return str(self.id) + "_data"


# progress manager
class ProgressManager(models.Manager):

    def new_progress(self, user):
        new_progress = self.create(user=user,score="")
        new_progress.save()
        return new_progress


class Progress(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        verbose_name = "Хэрэглэгч", 
        on_delete = models.CASCADE
    )

    score = models.CharField(
        validators = [validate_comma_separated_integer_list], 
        max_length = 1024,
        verbose_name="Оноо"
    )

    correct_answer = models.CharField(
        max_length = 10, 
        verbose_name = "Зөв хариулт"
    )

    wrong_answer = models.CharField(
        max_length = 10, 
        verbose_name = "Буруу хариулт"
    ) 

    objects = ProgressManager()

    class Meta:
        verbose_name = "Хэрэглэгчийн явц"
        verbose_name_plural = "Хэрэглэгчийн явц"

    @property
    def list_all_cat_scores(self):
        
        score_before = self.score
        output = {}

        for cat in Category.objects.all():
            to_find = re.escape(cat.category) + r",(\d+),(\d+),"
            #  group 1 is score, group 2 is highest possible

            match = re.search(to_find, self.score, re.IGNORECASE)

            if match:
                score = int(match.group(1))
                possible = int(match.group(2))

                try:
                    percent = int(round((float(score) / float(possible))
                                        * 100))
                except:
                    percent = 0

                output[cat.category] = [score, possible, percent]

            else:  # if category has not been added yet, add it.
                self.score += cat.category + ",0,0,"
                output[cat.category] = [0, 0]

        if len(self.score) > len(score_before):
            # If a new category has been added, save changes.
            self.save()

        return output

    def update_score(self, question, score_to_add=0, possible_to_add=0):
        
        category_test = Category.objects.filter(category = question.category)\
                                        .exists()

        if any([item is False for item in [category_test,
                                           score_to_add,
                                           possible_to_add,
                                           isinstance(score_to_add, int),
                                           isinstance(possible_to_add, int)]]):
            return "error", "category does not exist or invalid score"

        to_find = re.escape(str(question.category)) +\
            r",(?P<score>\d+),(?P<possible>\d+),"

        match = re.search(to_find, self.score, re.IGNORECASE)

        if match:
            updated_score = int(match.group('score')) + abs(score_to_add)
            updated_possible = int(match.group('possible')) +\
                abs(possible_to_add)

            new_score = ",".join(
                [
                    str(question.category),
                    str(updated_score),
                    str(updated_possible), ""
                ])

            # swap old score for the new one
            self.score = self.score.replace(match.group(), new_score)
            self.save()

        else:
            #  if not present but existing, add with the points passed in
            self.score += ",".join(
                [
                    str(question.category),
                    str(score_to_add),
                    str(possible_to_add),
                    ""
                ])
            self.save()

    def show_exams(self):
        return Sitting.objects.filter(
            user = self.user, 
            complete = True
        )

    def __str__(self):
        return self.user.username + ' - '  + self.score


class SittingManager(models.Manager):

    def new_sitting(self, user, quiz):
        if quiz.random_order is True:
            question_set = quiz.question_set.all() \
                                            .select_subclasses() \
                                            .order_by('?')
        else:
            question_set = quiz.question_set.all() \
                                            .select_subclasses()

        question_set = [item.id for item in question_set]

        if len(question_set) == 0:
            raise ImproperlyConfigured('Question set of the quiz is empty. '
                                       'Please configure questions properly')

        if quiz.max_questions and quiz.max_questions < len(question_set):
            question_set = question_set[:quiz.max_questions]

        questions = ",".join(map(str, question_set)) + ","

        new_sitting = self.create(user = user,
                                  quiz = quiz,
                                  question_order = questions,
                                  question_list = questions,
                                  incorrect_questions = "",
                                  current_score = 0,
                                  complete = False,
                                  user_answers = '{}'
                        )
        return new_sitting

    def user_sitting(self, user, quiz):
        if quiz.single_attempt is True and self.filter(user = user,
                                                       quiz = quiz,
                                                       complete = True)\
                                               .exists():
            return False

        try:
            sitting = self.get(
                user = user, 
                quiz = quiz, 
                complete = False
            )
        except Sitting.DoesNotExist:
            sitting = self.new_sitting(user, quiz)
        except Sitting.MultipleObjectsReturned:
            sitting = self.filter(
                user = user, 
                quiz = quiz, 
                complete = False
            )[0]
        return sitting


class Sitting(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        verbose_name = "Хэрэглэгч", 
        on_delete = models.CASCADE
    )

    quiz = models.ForeignKey(
        Quiz, 
        verbose_name = "Шалгалт", 
        on_delete = models.CASCADE
    )

    question_order = models.CharField(
        validators = [validate_comma_separated_integer_list],
        max_length = 1024, 
        verbose_name="Даалгаврын дараалал"
    )

    question_list = models.CharField(
        validators = [validate_comma_separated_integer_list],
        max_length = 1024, 
        verbose_name = "Даалгаврын жагсаалт"
    )

    incorrect_questions = models.CharField(
        validators = [validate_comma_separated_integer_list],
        max_length = 1024, 
        blank = True, 
        verbose_name = "Буруу даалгавар"
    )

    current_score = models.IntegerField(
        verbose_name = "Одоогийн оноо"
    )

    complete = models.BooleanField(
        default = False, 
        blank  = False,
        verbose_name = "Дууссан эсэх"
    )

    user_answers = models.TextField(
        blank = True, 
        default = '{}',
        verbose_name = "Хэрэглэгчийн хариулт"
    )

    start = models.DateTimeField(
        auto_now_add = True,
        verbose_name = "Шалгалт эхлэсэн хугацаа"
    )

    end = models.DateTimeField(
        null = True, 
        blank = True, 
        verbose_name = "Шалгалт дууссан хугацаа"
    )

    objects = SittingManager()

    class Meta:
        permissions = (("view_sittings", "Can see completed exams."),)
        ordering = ['-end']

    def get_first_question(self):
        
        if not self.question_list:
            return False

        first, _ = self.question_list.split(',', 1)
        question_id = int(first)
        return Question.objects.get_subclass(id = question_id)

    def remove_first_question(self):
        if not self.question_list:
            return

        _, others = self.question_list.split(',', 1)
        self.question_list = others
        self.save()

    def add_to_score(self, points):
        self.current_score += int(points)
        self.save()

    @property
    def get_current_score(self):
        return self.current_score

    def _question_ids(self):
        return [int(n) for n in self.question_order.split(',') if n]

    @property
    def get_percent_correct(self):
        dividend = float(self.current_score)
        divisor = len(self._question_ids())
        if divisor < 1:
            return 0            # prevent divide by zero error

        if dividend > divisor:
            return 100

        correct = int(round((dividend / divisor) * 100))

        if correct >= 1:
            return correct
        else:
            return 0

    def mark_quiz_complete(self):
        self.complete = True
        self.end = now()
        self.save()

    def add_incorrect_question(self, question):
        
        if len(self.incorrect_questions) > 0:
            self.incorrect_questions += ','
        self.incorrect_questions += str(question.id) + ","
        if self.complete:
            self.add_to_score(-1)
        self.save()

    @property
    def get_incorrect_questions(self):
        return [int(q) for q in self.incorrect_questions.split(',') if q]

    def remove_incorrect_question(self, question):
        current = self.get_incorrect_questions
        current.remove(question.id)
        self.incorrect_questions = ','.join(map(str, current))
        self.add_to_score(1)
        self.save()

    @property
    def check_if_passed(self):
        return self.get_percent_correct >= self.quiz.pass_mark

    @property
    def result_message(self):
        if self.check_if_passed:
            return self.quiz.success_text
        else:
            return self.quiz.fail_text

    def add_user_answer(self, question, guess):
        current = json.loads(self.user_answers)
        current[question.id] = guess
        self.user_answers = json.dumps(current)
        self.save()

    def get_questions(self, with_answers = False):
        question_ids = self._question_ids()
        questions = sorted(
            self.quiz.question_set.filter(id__in = question_ids)
                                  .select_subclasses(),
            key=lambda q: question_ids.index(q.id))

        if with_answers:
            user_answers = json.loads(self.user_answers)
            for question in questions:
                question.user_answer = user_answers[str(question.id)]

        return questions

    @property
    def questions_with_user_answers(self):
        return {
            q: q.user_answer for q in self.get_questions(with_answers = True)
        }

    @property
    def get_max_score(self):
        return len(self._question_ids())

    def progress(self):
        
        answered = len(json.loads(self.user_answers))
        total = self.get_max_score
        return answered, total





class Question(models.Model):

    quiz = models.ManyToManyField(
        Quiz,
        verbose_name = "Шалгалт",
        help_text = "Сонгохгүй байх болно. Сонгосон тохиолдолд шууд шалгалт руу орно.",
        blank = True
    )

    category = models.ForeignKey(
        Category,
        verbose_name = "Ай",
        blank = True,
        null = True, 
        on_delete = models.CASCADE
    )
    level = models.ForeignKey(
        Level,
        verbose_name = "Түвшин",
        blank = True,
        null = True, 
        on_delete = models.CASCADE
    )
    point = models.IntegerField(
        default = 0,
        blank = True,
        verbose_name = "Оноо",
    )
    figure = models.ImageField(
        upload_to = 'uploads/problem/pic/%Y/%m/content',
        blank = True,
        null = True,
        verbose_name = "Зураг"
    )

    content = models.TextField(
        blank = False,
        help_text = "Даалгаврыг ЛаТеКС кодоор оруулна уу?",
        verbose_name = "Даалгавар"
    )

    explanation = models.CharField(
        max_length = 300,
        blank = True,
        help_text = "Нэг ижилхэн төрлийн даалгаврууд олон болоход дараа нь хайхад хэрэг болохууц нэршил оруулна уу.",
        verbose_name = 'Тайлбар'
    )
    video = models.URLField(
        blank = True,
        verbose_name = "Видео хичээлийн линк",
        help_text = "Агуулгын төрөл зөвхөн видео тохиолдолд YOUTUBE-ийн линк оруулж ажиглана. Бусад тохиолдолд хоосон байна."
    )
    author = models.ForeignKey('auth.User',
        on_delete = models.CASCADE,
        verbose_name = 'Нийтлэгч'
    )

    objects = InheritanceManager()

    class Meta:
        verbose_name = "Даалгавар"
        verbose_name_plural = "Даалгаврууд"

    def __str__(self):
        return self.content

def create_user(data):
    user =  User.objects.create_user(
        username = data['username'],
        email = data['email'],
        password = data['password'],
        first_name = data['first_name'],
        last_name = data['last_name']
    )
    user.is_superuser = False
    user.is_staff = False
    user.is_active = False
    user.save()
