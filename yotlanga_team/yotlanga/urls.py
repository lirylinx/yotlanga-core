__author__ = 'lirylinx'

from django.conf.urls import url
from . import views
from django.views.generic import TemplateView
from django.views.static import serve

from yotlanga_team import settings

app_label = 'yotlanga'

urlpatterns  = [
    url(r'^$', views.indexView, name='index'),
    url(r'^registrar/$', views.registoView, name='registrar'),
    url(r'^entrar/$', views.loginView, name='entrar'),


    url(r'^sair/$', views.logOut, name='sair'),
    # url(r'^perfil/$', views.perfilView, name='perfil'),
    # url(r'^audio/$', views.audio_perfilView, name='musica'),
    # url(r'^carregar/$', views.carregarView, name='carregar'),
    # url(r'^sucesso/$', views.sucessoView, name='proximo_passo'),
    # url(r'^mural/$', views.muralView, name="mural"),
    # url(r'^pesquisar/$', views.pesquisaView, name="pesquisa"),
    # url(r'^draft/$', views.draftView, name="draft"),

]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
