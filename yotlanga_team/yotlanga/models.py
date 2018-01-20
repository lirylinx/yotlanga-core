from django.db import models
from django.core.files.storage import FileSystemStorage
from django.utils import timezone

import logging


agora = timezone.now()

class Usuario(models.Model):
    nome = models.CharField(max_length=255)
    apelido = models.CharField(max_length=32)
    username = models.CharField(max_length=255, unique=True, null=True)
    senha = models.CharField(max_length=1024)
    sexo = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    numero = models.IntegerField(unique=True, null=True, blank=True)
    data_nascimento = models.DateField()
    data_entrada = models.DateField(default=agora)
    is_online = models.BooleanField(default=False)
    status = models.CharField(max_length=255, default="activo")
    imagem = models.ImageField(null=True, blank=True)
    
    #class Meta:
    #app_label = 'yotlanga'
    
    def __str__(self):
        return self.username
    
    def __cmp__(self, other):
        if self.username == other.username:
            return  True
        else:       
            return False
    
    
    
    def getNome(self):
        return  self.nome
    
    def getApelido(self):
        return self.apelido
    
    def getUsername(self):
        return self.username
    
    def getSexo(self):
        return self.sexo
    
    def getIdade(self):
        return self.data_nascimento
    
    def getEmail(self):
        return self.email
    
    def getIsOnline(self):
        return  self.is_online
    
    def getDataEntranda(self):
        return self.data_entrada
    
    def getDataNascimento(self):
        return self.data_nascimento
    
    def getNumero(self):
        return self.numero
    
    
    def getSenha(self):
        return self.senha
    
    def getStatus(self):
        return self.status

    def getIsOnline(self):
        return self.is_online
    
    
    
    
    
    
    
    def guardar(self):
        senha = self.senha
        data_formatado = self.data_nascimento
        try:
            user = Usuario(nome=self.nome,  apelido = self.apelido, username = self.username, senha = senha, sexo = self.sexo,
            email = self.email, data_nascimento = data_formatado, numero = self.numero)
            user.save()
        except:
            #dict["guardar"] = {"msg": ["Erro ao gravar %s" % user.nome, ]}
            user = None
        logger = logging.getLogger(__name__)
        logger.debug("USUARIO ")
        #print(user)
        return user


    def actualizar(self):
        data_formatado = self.data_nascimento
        user = Usuario.objects.filter(pk=self.id).update(nome = self.nome,  apelido = self.apelido, username = self.username, sexo = self.sexo,
                       email = self.email, data_nascimento = data_formatado, numero = self.numero)

    def remover(self):
        user = self.find_user(self.id)
        if user != None:
            try:
                user.delete()
            except :
                print("Usuario Nao existe")
            #dict["remover"] = {"msg": ["Erro ao remover %s" % user.nome, ]}

    @classmethod
    def find_user(cls, id):
        try:
            user = cls.objects.get(pk=id)
        except:
            #dict["find_user"] = {"msg": ["ID %d Nao encontrado." % id, ]}
            user = None
            print("Usuario Nao existe")

        return user


class Ficheiro(models.Model):
    """ Ficheiros aceites pelos nossos servidores
        como imagem, audio, video
    """
    #fs = FileSystemStorage(upload_to="uploads/")
    tipo = models.CharField(max_length=50)
    formato = models.CharField(max_length=16)
    nome = models.CharField(max_length=255)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    ficheiro = models.FileField(upload_to="uploads/")
    data_entrada = models.DateField(default=agora)

    def guardar(self):
        pass


class AudioTag(models.Model):
    """ Tags de audio como artista, titulo, album """
    ficheiro = models.ForeignKey(Ficheiro, on_delete=models.CASCADE)
    artista = models.CharField(max_length=255)
    titulo = models.CharField(max_length=255)
    album = models.CharField(max_length=255)
    bitrate = models.CharField(max_length=255, blank=True, null=True)
    disco_num = models.IntegerField(blank=True, null=True)
    disco_total = models.IntegerField(blank=True, null=True)
    duracao = models.FloatField(blank=True, null=True)
    tamanho = models.FloatField(blank=True, null=True)
    genero = models.CharField(max_length=255, default="Outro", null=True)
    ano = models.IntegerField(blank=True, null=True)
    filename = models.CharField(max_length=255, blank=True, unique=True, null=True)
    img = models.ImageField(blank=True, null=True)
    convidado = models.CharField(max_length=255, blank=True, null=True)
    produtor = models.CharField(max_length=255, blank=True, null=True)
    instrumental = models.CharField(max_length=255, blank=True, null=True)
    outros = models.CharField(max_length=255, blank=True, null=True)




class Publicacao(models.Model):
    """ Publicacao de qualquer artigo
        aceite: texto, imagem, audio, video.
    """
    cabecalho = models.CharField(max_length=255)
    texto = models.CharField(max_length=32)
    is_file = models.BooleanField(default=False)
    ficheiro = models.ForeignKey(Ficheiro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data_entrada = models.DateField(default=agora)
