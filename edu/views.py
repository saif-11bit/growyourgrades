from django.shortcuts import render, redirect
from django.views.generic import View, DetailView
from .models import Course, Subject, Lesson, Lesson_Part, UserCourses, LiveDoubtSession, TimeTable, Questions, Answer
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import QuestionsForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_user_course(request):
    user_course_qs = UserCourses.objects.filter(user=request.user)
    if user_course_qs.exists():
        user_course = user_course_qs.first()
        return user_course
    return None


def get_today_timetable(request):
    now = datetime.datetime.now()
    today = now.strftime("%A")
    course = get_user_course(request)
    timetable_qs = TimeTable.objects.filter(day=today, course=course.courses)
    if timetable_qs.exists():
        timetable = timetable_qs.all()
        # print(timetable)
        return timetable
    return None


def get_question_list(request):
    user_course = get_user_course(request)
    question_qs = Questions.objects.filter(course=user_course.courses)
    questions = question_qs.all()
    return questions


class AboutView(View):
    def get(self, *args, **kwargs):

        return render(self.request, 'about.html')


class CoursesView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, *args, **kwargs):
        context = {'courses': Course.objects.all()}
        return render(self.request, 'index.html', context=context)

    def post(self, request, *args, **kwargs):
        selected_course_title = request.POST.get('course_title')

        selected_course_qs = Course.objects.filter(title=selected_course_title)
        selected_course = selected_course_qs.first()

        user_courses = get_user_course(request)
        user_courses.courses = selected_course
        user_courses.save()

        context = {
            'selected_course': selected_course,
            # 'course': selected_course,
        }
        messages.info(request, f'{selected_course} selected!')
        return render(request, 'home.html', context=context)


class CourseListView(View):
    login_url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        context = {'courses': Course.objects.all()}
        if request.user.is_authenticated:
            user_courses_qs = UserCourses.objects.filter(user=request.user)

            if user_courses_qs.exists():
                user_courses = user_courses_qs.first()
                selected_course = user_courses

                context = {
                    'selected_course': selected_course.courses,
                    # 'course': selected_course.courses,
                }

                return render(self.request, 'home.html', context=context)

        return render(request, 'index.html', context=context)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            selected_course_title = request.POST.get('course_title')

            selected_course_qs = Course.objects.filter(
                title=selected_course_title)
            selected_course = selected_course_qs.first()

            user_courses = UserCourses(user=request.user,
                                       courses=selected_course)
            user_courses.save()

            context = {
                'selected_course': selected_course,
                # 'course': selected_course,
            }
            messages.info(request, f'{selected_course} selected!')
            return render(request, 'home.html', context=context)

        return redirect('/accounts/login')


class CourseDetailView(LoginRequiredMixin, DetailView):
    login_url = '/accounts/login/'
    model = Course
    context_object_name = 'course'
    template_name = 'subjects.html'


class SubjectDetailView(View):
    def get(self, request, course_slug, subject_slug, *args, **kwargs):

        course_qs = Course.objects.filter(slug=course_slug)
        if course_qs.exists():
            course = course_qs.first()

        subject_qs = course.subjects.filter(slug=subject_slug)
        if subject_qs.exists():
            subject = subject_qs.first()

        context = {
            'subject': subject,
            'course': course,
        }

        return render(request, 'lesson-list.html', context=context)


class LessonDetailView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, course_slug, subject_slug, lesson_slug, *args,
            **kwargs):

        subject_qs = Subject.objects.filter(slug=subject_slug)
        subject = subject_qs.first()

        lesson_qs = subject.lessons.filter(slug=lesson_slug)
        lesson = lesson_qs.first()

        context = {
            'lesson': lesson,
        }

        return render(request, 'lessons.html', context=context)


class LiveSession(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        user_course = get_user_course(request)

        if user_course is None:
            messages.info(request, 'select a courses from course available!')
            return redirect('/')

        now = datetime.datetime.now()
        today = now.strftime("%A")
        live = LiveDoubtSession.objects.filter(day=today,
                                               course=user_course.courses)

        context = {
            'course': user_course.courses,
            'live': live,
        }
        return render(self.request, 'live.html', context=context)


class VideosView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        user_course = get_user_course(request)

        if user_course is None:
            messages.info(request, 'select a courses from course available!')
            return redirect('/')

        lesson_parts_qs = Lesson_Part.objects.filter(
            course=user_course.courses)
        lesson_parts = lesson_parts_qs.all()

        page = request.GET.get('page', 1)
        paginator = Paginator(lesson_parts, 1)

        try:
            lessons = paginator.page(page)
        except PageNotAnInteger:
            lessons = paginator.page(1)
        except EmptyPage:
            lessons = paginator.page(paginator.num_pages)

        context = {'videos': lessons}
        return render(self.request, 'videos.html', context=context)


class QuestionView(LoginRequiredMixin, View):
    login_url = '/accounts/login'

    def get(self, request, *args, **kwargs):

        user_course = get_user_course(request)
        if user_course is None:
            messages.info(request, 'select a courses from course available!')
            return redirect('/')

        course = user_course.courses
        subject = Subject.objects.filter(course=course)

        questions = get_question_list(request)
        form = QuestionsForm()
        context = {'questions': questions, 'subject': subject, 'form': form}

        return render(self.request, 'discussion.html', context=context)

    def post(self, request, *args, **kwargs):
        user_course = get_user_course(request)

        heading = request.POST.get('heading')
        subject = request.POST.get('subject')
        sub = Subject.objects.filter(id=subject).first()
        ques_img = request.FILES.get('ques_img')
        print(ques_img)
        question = request.POST.get('question')
        asked_by = request.user
        course = user_course.courses

        question_db = Questions()
        question_db.heading = heading
        question_db.subject = sub
        question_db.question = question
        question_db.ques_img = ques_img
        question_db.asked_by = asked_by
        question_db.course = course
        question_db.save()

        return redirect('edu:questions')


class DisscussionView(LoginRequiredMixin, View):
    login_url = '/accounts/login'

    def get(self, request, pk, *args, **kwargs):
        context = {'question': Questions.objects.filter(pk=pk).first()}
        return render(self.request, 'discussion-detail.html', context=context)

    def post(self, request, pk, *args, **kwargs):

        answer = request.POST.get('answer-name')
        question = Questions.objects.filter(pk=pk).first()

        print(request.user.is_staff)

        answer_qs = Answer(answer_for=question,
                           answer_by=request.user,
                           answer=answer)
        answer_qs.save()

        return redirect('edu:discussion-detail', pk=pk)
