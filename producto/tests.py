from django.urls import path, include
from views import *


urlPatters = [
    path('rest/list/', vistaproducto.as_view())

]