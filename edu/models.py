from django.db import models
from django.urls import reverse
from embed_video.fields import EmbedVideoField
import datetime
from django.contrib.auth.models import User
from django.contrib import auth


def usercourse(self):
    user_course = UserCourses.objects.filter(user=self).first()
    return user_course.courses


auth.models.User.add_to_class('usercourse', usercourse)


class Course(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("edu:course-detail", kwargs={"slug": self.slug})

    def get_live_url(self):
        return reverse("edu:live")

    @property
    def subjects(self):
        return self.subject_set.all()


class Subject(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course}-{self.title}"

    def get_absolute_url(self):
        return reverse("edu:subject-detail",
                       kwargs={
                           "course_slug": self.course.slug,
                           'subject_slug': self.slug,
                       })

    @property
    def lessons(self):
        return self.lesson_set.all().order_by('position')


class Lesson(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    position = models.IntegerField()

    def __str__(self):

        return f"{self.subject}/{self.title}"

    def get_absolute_url(self):
        return reverse("edu:lesson-detail",
                       kwargs={
                           "course_slug": self.course.slug,
                           'subject_slug': self.subject.slug,
                           'lesson_slug': self.slug
                       })

    @property
    def lesson_parts(self):
        return self.lesson_part_set.all().order_by('position')


class Lesson_Part(models.Model):
    title = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to='Thumbnails', null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True)
    video = EmbedVideoField(blank=True)
    notes_file = models.FileField(upload_to='Notes', null=True, blank=True)
    position = models.IntegerField()

    def __str__(self):
        return f"{self.lesson}/{self.title}"


DAYS = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
]


class TimeTable(models.Model):
    day = models.CharField(max_length=100, choices=DAYS)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subjects = models.ForeignKey(Subject, on_delete=models.CASCADE)
    from_time = models.TimeField()
    to_time = models.TimeField()

    def __str__(self):
        return f"{self.day}-{self.course}-{self.subjects}"

    # @property
    # def livedoubtsessions(self):
    #     return self.livedoubtsession_set.all()


class LiveDoubtSession(models.Model):
    day = models.CharField(max_length=100, choices=DAYS, null=True)
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True)
    subjects = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)

    link = models.CharField(max_length=5000)
    thumbnail = models.ImageField(upload_to='Lives')
    # day_and_time = models.ForeignKey(TimeTable, on_delete=models.CASCADE)
    from_time = models.TimeField(null=True)
    to_time = models.TimeField(null=True)

    def __str__(self):
        return f"{self.subjects}-{self.title}"


class UserCourses(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    courses = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user}"


#discussion
class Questions(models.Model):
    asked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    heading = models.CharField(max_length=200)
    question = models.TextField()
    ques_img = models.ImageField(upload_to='Question', blank=True, null=True)
    date = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return f"{self.asked_by}-{self.subject}"

    def get_absolute_url(self):
        return reverse("edu:discussion-detail", kwargs={"pk": self.pk})

    @property
    def answers(self):
        return self.answer_set.all()

    class Meta:
        ordering = ['-date']


class Answer(models.Model):
    answer_for = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    answer = models.TextField()

    def __str__(self):
        return f"{self.answer_by}"


# Create your models here.
"""
Membership Model--slug                      
                --type(free,pro,enterprise)
                --price
                --stripe plan id


User Membership --user                  (forignkey to default user)
                --stripe customer id
                --membership type       (forignkey to membership)
                
Subscription Model  --slug
                    --user membership
                    --stripe subscription id(forignkey to UserMembership)
                    --active

Course Model    --slug
                --title
                --description
                --allowed memberships (manytomanyfield to membership)


Live Session    --slug
                --course (foreignkey to course)
                --title
                --start time
                --end time
                --url
                --thumbnail
                --days     ()
                --allowed memberships (manytomanyfield to membership)
                


Subject Model   --slug
                --title
                --description
                --course (foreignkey to course)
                --allowed memberships (manytomanyfield to membership)


Lessonn Model   --slug
                --title
                --course (foreignkey to course)
                --position

Lesson Parts    --slug
                --title
                --course
                --subject
                --lesson
                --video
                --filefield

"""
