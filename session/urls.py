from django.urls import path
from .views import ListCreateSessionLogView, SessionLogDetailView, \
    session_types, session_feelings

urlpatterns = [
    path('sessions/', ListCreateSessionLogView.as_view(),
         name="session-list-create"),
    path('sessions/<int:pk>/', SessionLogDetailView.as_view(),
         name="session-detail"),
    path('sessions/types/', session_types, name="session-types"),
    path('sessions/feelings/', session_feelings, name="session-feelings")
]