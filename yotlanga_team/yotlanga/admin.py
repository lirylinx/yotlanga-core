from django.contrib import admin
from .models import AudioTag, Ficheiro, Usuario


# Registrando modelo para painel administrativo
admin.site.register(Usuario)
admin.site.register(Ficheiro)
admin.site.register(AudioTag)
# admin.site.register(Pu)

