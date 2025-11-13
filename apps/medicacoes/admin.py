from django.contrib import admin
from .models import Bebe, Medicacao, Estoque, Lembrete, RegistroAdministracao, Alerta


@admin.register(Bebe)
class BebeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_nascimento', 'responsavel')


@admin.register(Medicacao)
class MedicacaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'bebe', 'dosagem', 'frequencia', 'data_inicio')


@admin.register(Estoque)
class EstoqueAdmin(admin.ModelAdmin):
    list_display = ('medicacao', 'quantidade_total', 'unidade', 'data_atualizacao')


@admin.register(Lembrete)
class LembreteAdmin(admin.ModelAdmin):
    list_display = ('medicacao', 'horario', 'canal')


@admin.register(RegistroAdministracao)
class RegistroAdmin(admin.ModelAdmin):
    list_display = ('medicacao', 'status', 'data', 'horario', 'observacoes')


@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'descricao', 'bebe', 'data_criacao', 'status')
