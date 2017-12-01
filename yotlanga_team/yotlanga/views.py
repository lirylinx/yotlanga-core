from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views import generic
from .models import Usuario, Ficheiro, AudioTag
from django.shortcuts import render
from django.utils import timezone
from . forms import RegistoForm, LoginForm
# from . forms import RegistoForm, LoginForm, uploadForm, EditarTagAudioForm
from yotlanga_team.settings import BASE_DIR, MEDIA_URL, MEDIA_ROOT
# from tinytag import TinyTag
import logging
import json
import os
import sys


# suportar upload
# from yotlanga.backend.upload_handler import handle_upload_file
# from yotlanga.backend.multimidia_handle import audio_extract_tag




def request_user(request, by="username"):
    """ sessao de usuario  """
    user = None

    try:
        if by == "id":
            id = int(request.session['usuario_id'])
            user = Usuario.objects.get(id=id)
        elif by == "username":
            username = request.session['username']
            user = Usuario.objects.get(username=username)
        elif by == "email":
            email = request.session['email']
            user = Usuario.objects.get(email=email)
    except:
        user = None

    return user





def indexView(request):
    user = None
    try:
        username = request.session['username']
        try:
            user = Usuario.objects.get(username=username)
        except:
            user = None
    except:
        user = None
    return render(request, 'yotlanga/index.html', {'usuario_logado': user})


def registoView(request):
    """ view para registo de novo usuario
        validar os campos e informar mensagem de erros
        em caso de ocorrer algum enquanto se regista
    """
    user = None
    msg = ""
    user_existe = False

    """ Se tiver ja logado usuario, redirecionar para pagina inicial """
    try:
        if request_user(request=request) is not None:
            return HttpResponseRedirect('/')
    except:
        user = None
    dias = []
    anos = []
    meses = {1:'Janeiro', 2:'Fevereiro', 3:'Marco', 4:'Abril', 5:'Maio', 6:'Junho',
                7:'Julho',  8:'Agosto', 9:'Setembro',10: 'Outubro', 11:'Novembro',  12: 'Dezembro'}

    for ano in range(1900, 2017):
        anos.append(ano)
    for i in range(1, 31):
        dias.append(i)
    u = None
    # Se for um POST tem de ser processado
    if request.method == 'POST':
        form = RegistoForm(request.POST)
        if form.is_valid():
            "Processar dados"
            data_formatado = "1994-1-26" #"-".join([request.POST['ano'], str(meses[request.POST['mes']]), request.POST['dia']])
            try:
                user = Usuario(nome=request.POST['nome'],  apelido = request.POST['apelido'],
                           username = request.POST['username'], senha = request.POST['senha'],
                           sexo = request.POST['sexo'], email = request.POST['email'],
                           data_nascimento = data_formatado)

                u = user.guardar()
                if u is not None:
                    return HttpResponseRedirect("/entrar/")
                else:
                    user = None
                    form = RegistoForm()

            except:
                user = None
                msg = "erro"

        else:
            try:
                user = Usuario.objects.get(email=request.POST['email'])
                msg = user.email + " Ja registado"
            except:
                pass

            try:
                user = Usuario.objects.get(username=request.POST['username'])
                msg = user.username + " Ja registado"
            except:
                pass

            form = RegistoForm()

    #  Se for GET ou outro tipo de metodo. Limpar os campos
    else:
        form = RegistoForm()

    return render(request, 'yotlanga/registrar.html',
                  {'dias': dias, 'anos': anos, 'form': form, 'user': user,
                   'mensagem': msg})


def loginView(request):
    form = LoginForm()
    user = None
    msg = None
    if request.method == 'POST':
        """ Testando cookies no browser do usuario """
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            form = LoginForm(request.POST)
            if form.is_valid():
                senha = request.POST["senha"]
                usuario = request.POST["username_email"]
                try:
                    user = Usuario.objects.get(
                        email=usuario)
                    if user.getSenha() == senha:
                        request.session['usuario_id'] = user.id
                        try:
                            Usuario.objects.filter(id=user.id).update(is_online=True)
                        except:
                            pass
                        return HttpResponseRedirect("/")
                    else:
                        msg = "ERRO Usuario ou Senha incorreto"
                except Usuario.DoesNotExist:
                    msg = "ERRO Usuario ou Senha incorreto"
                    user = None
            else:
                form = LoginForm()
        else:
            user = None
            msg = "ERRO: Active cookies nas definicoes do teu browser"
    request.session.set_test_cookie()
    return render(request, 'yotlanga/entrar.html', {'form': form, 'user': user,
                  'mensagem': msg})

def logOut(request):
    user = None
    try:
        user = int(request.session['usuario_id'])
        del request.session['usuario_id']
        request.flush()
        try:
            Usuario.objects.filter(id=user).update(is_online=False)
        except:
            pass
        user = None
    except:
        user = None

    return HttpResponseRedirect("/entrar")

