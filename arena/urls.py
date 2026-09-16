from django.urls import path

from . import views


app_name = "arena"


urlpatterns = [

    path(
        "",
        views.arena,
        name="arena"
    ),

    path(
        "acao/<str:acao>/",
        views.executar_acao,
        name="acao"
    ),

    path(
        "nome/",
        views.definir_nome,
        name="nome"
    ),

    path(
        "reiniciar/",
        views.reiniciar,
        name="reiniciar"
    ),

]