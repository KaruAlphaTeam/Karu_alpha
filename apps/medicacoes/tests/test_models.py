from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from medicacoes.models import Bebe, Medicacao, Estoque, RegistroAdministracao, Alerta

class TesteModelosMedicacoes(TestCase):
    def setUp(self):
        # Criar um bebê e uma medicação para os testes
        self.bebe = Bebe.objects.create(
            nome="Bebê Teste",
            data_nascimento=timezone.now().date(),
            responsavel="Responsável Teste"
        )
        self.medicacao = Medicacao.objects.create(
            bebe=self.bebe,
            nome="Vitamina D",
            dosagem="1 gota",
            frequencia="diaria",
            via="oral",
            duracao_dias=30,
            data_inicio=timezone.now().date()
        )
        self.estoque = Estoque.objects.create(
            medicacao=self.medicacao,
            quantidade_total=Decimal('5'),
            unidade="ml"
        )

    def test_calculo_consumo_diario(self):
        """Verifica se a função consumo_diario retorna o valor esperado."""
        self.assertEqual(self.medicacao.consumo_diario(), Decimal('1'))

    def test_verificar_estoque_gera_alerta(self):
        """Verifica se o alerta é gerado quando o estoque está abaixo de 3 dias."""
        # Diminui a quantidade de estoque para simular poucos dias restantes
        self.estoque.quantidade_total = Decimal('2')
        alerta = self.estoque.verificar_estoque()
        self.assertIsNotNone(alerta)
        self.assertEqual(alerta.tipo, 'amarelo')
        self.assertIn("Estoque baixo", alerta.descricao)

    def test_registro_administracao_cria_alerta_amarelo(self):
        """Verifica se dois esquecimentos seguidos geram alerta amarelo."""
        RegistroAdministracao.objects.create(
            medicacao=self.medicacao,
            status='esqueci',
            data=timezone.now().date(),
            horario=timezone.now().time()
        )
        RegistroAdministracao.objects.create(
            medicacao=self.medicacao,
            status='esqueci',
            data=timezone.now().date(),
            horario=timezone.now().time()
        )
        alertas = Alerta.objects.filter(bebe=self.bebe, tipo='amarelo')
        self.assertEqual(alertas.count(), 1)

    def test_registro_administracao_cria_alerta_vermelho(self):
        """Verifica se três esquecimentos seguidos geram alerta vermelho."""
        for _ in range(3):
            RegistroAdministracao.objects.create(
                medicacao=self.medicacao,
                status='esqueci',
                data=timezone.now().date(),
                horario=timezone.now().time()
            )
        alertas = Alerta.objects.filter(bebe=self.bebe, tipo='vermelho')
        self.assertEqual(alertas.count(), 1)

    def test_registro_dei_diminui_estoque(self):
        """Verifica se o estoque é reduzido ao registrar uma dose 'dei'."""
        quantidade_inicial = self.estoque.quantidade_total
        RegistroAdministracao.objects.create(
            medicacao=self.medicacao,
            status='dei',
            data=timezone.now().date(),
            horario=timezone.now().time()
        )
        self.estoque.refresh_from_db()
        self.assertLess(self.estoque.quantidade_total, quantidade_inicial)