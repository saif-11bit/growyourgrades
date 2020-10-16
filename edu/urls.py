from django.urls import path
from .views import CourseListView, CourseDetailView, SubjectDetailView, LessonDetailView, LiveSession, VideosView, CoursesView, QuestionView, DisscussionView, AboutView
app_name = 'edu'

urlpatterns = [
    path('live/', LiveSession.as_view(), name='live'),
    path('about/', AboutView.as_view(), name='about'),
    path('questions/', QuestionView.as_view(), name='questions'),
    path('discussion-detail/<pk>/',
         DisscussionView.as_view(),
         name='discussion-detail'),
    path('courses/', CoursesView.as_view(), name='courses'),
    path('videos/', VideosView.as_view(), name="videos"),
    path('', CourseListView.as_view(), name="course-list"),
    path('<slug>/', CourseDetailView.as_view(), name='course-detail'),
    path('<course_slug>/<subject_slug>/',
         SubjectDetailView.as_view(),
         name='subject-detail'),
    path('<course_slug>/<subject_slug>/<lesson_slug>/',
         LessonDetailView.as_view(),
         name='lesson-detail'),
]
