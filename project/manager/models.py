from django.db import models
from django.contrib.auth.models import User

class Inscricao(models.Model):
    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
    
    OPCOES_STATUS = [
        ('pendente', 'Pendente'),
        ('quitado', 'Quitado'),
    ]

    OPCOES_GRUPO = [
        ('grupo_a', '0 a 9 anos'),
        ('grupo_b', '10 a 12 anos'),
        ('grupo_c', '13 anos ou mais'),
    ]
    
    nome = models.CharField(max_length=255)
    telefone = models.CharField(max_length=255, null=True, blank=True)
    grupo = models.CharField(max_length=255, choices=OPCOES_GRUPO)
    idade = models.IntegerField()
    data_inscricao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, choices=OPCOES_STATUS)
    valor_pagar = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    criador = models.ForeignKey(User, on_delete=models.CASCADE)

    def verificar_valor_pagar(self):
        if self.grupo == 'grupo_a':
            return 0
        elif self.grupo == 'grupo_b':
            return 80
        else:
            return 160

    def save(self, *args, **kwargs):
        if self.valor_pagar == 0:
            self.status = 'quitado'
            super().save(*args, **kwargs)
            return
        if not self.valor_pagar:
            self.valor_pagar = self.verificar_valor_pagar()
            if self.valor_pagar == 0:
                self.status = 'quitado'
            else:
                self.status = 'pendente'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
    
class Pagamento(models.Model):
    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
    
    OPCOES_METODO_PAGAMENTO = [
        ('pix', 'Pix'),
        ('dinheiro', 'Dinheiro'),
        ('cartao', 'Cartão'),
    ]

    inscricao = models.ForeignKey(Inscricao, on_delete=models.CASCADE)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    data_pagamento = models.DateTimeField(auto_now_add=True)
    metodo_pagamento = models.CharField(max_length=255, choices=OPCOES_METODO_PAGAMENTO)
    observacao = models.TextField(null=True, blank=True)
