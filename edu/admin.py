from django.contrib import admin
from .models import Course, Subject, Lesson, TimeTable, LiveDoubtSession, Lesson_Part, UserCourses, Questions, Answer

admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Lesson)
admin.site.register(Lesson_Part)
admin.site.register(TimeTable)
admin.site.register(LiveDoubtSession)
admin.site.register(UserCourses)
admin.site.register(Questions)
admin.site.register(Answer)
