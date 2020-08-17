from django.contrib import admin
from django.urls import path, include


# Request routing to sub-apps is done based on these route configurations.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
    path('api/quiz/', include('quiz.urls')),
    path('nested_admin', include('nested_admin.urls')),
]
