# urls.py

from django.urls import path
from .views import drill_view, answer_view

urlpatterns = [
    path('drill/', drill_view, name='xword-drill'),
    path('answer/<int:clue_id>/', answer_view, name='xword-answer'),
]
