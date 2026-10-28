from django.urls import path
from . import views

urlpatterns = [

    # HOME PAGE
    path(
        '',
        views.landing_page,
        name='landing_page'
    ),

    # BIRDS DATABASE
    path(
        'birds/',
        views.home,
        name='birds'
    ),

    # AI IDENTIFICATION
    path(
        'identify/',
        views.identify_bird,
        name='identify_bird'
    ),

    # DETAIL PAGE
    path(
        'bird/<int:id>/',
        views.bird_detail,
        name='bird_detail'
    ),
    path(
    'gallery/',
    views.gallery,
    name='gallery'
),
path(
    'about/',
    views.about,
    name='about'
),
path(
    'contributors/',
    views.contributors,
    name='contributors'
),
path(
    'contact/',
    views.contact,
    name='contact'
),
]
