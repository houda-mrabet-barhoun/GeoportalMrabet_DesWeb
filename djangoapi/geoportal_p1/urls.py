from django.urls import path
from . import views

urlpatterns = [
    path("hello_geoportal_p1/", views.HelloGeoportalP1.as_view(), name="hello_geoportal_p1"),

    # CLIENTES
    path(
        "clientes_view/<str:action>/",
        views.ClientesView.as_view(),
        name="clientes_view"
    ),
    path(
        "clientes_view/<str:action>/<int:id>/",
        views.ClientesView.as_view(),
        name="clientes_view"
    ),

    # BARRIOS
    path(
        "barrios_view/<str:action>/",
        views.BarriosView.as_view(),
        name="barrios_view"
    ),
    path(
        "barrios_view/<str:action>/<int:id>/",
        views.BarriosView.as_view(),
        name="barrios_view"
    ),

    # RUTAS
    path(
        "rutas_view/<str:action>/",
        views.RutasView.as_view(),
        name="rutas_view"
    ),
    path(
        "rutas_view/<str:action>/<int:id>/",
        views.RutasView.as_view(),
        name="rutas_view"
    ),
]