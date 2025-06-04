from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, View
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import Inscricao, Pagamento

# Create your views here.

class InscricoesView(LoginRequiredMixin, ListView):
    model = Inscricao
    template_name = 'home.html'
    context_object_name = 'inscricoes'
    queryset = Inscricao.objects.all().order_by('-data_inscricao')

class InscricaoCreateView(LoginRequiredMixin, CreateView):
    model = Inscricao
    fields = ['nome', 'telefone', 'idade', 'grupo']
    template_name = 'inscricao_form.html'

    def form_valid(self, form):
        form.instance.criador = self.request.user
        form.save()
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string('partials/inscricao_row.html', {'inscricao': form.instance})
            return JsonResponse({'success': True, 'row_html': html})
        return super().form_valid(form)

class InscricaoDetailView(LoginRequiredMixin, DetailView):
    model = Inscricao
    template_name = 'details.html'
    context_object_name = 'inscricao'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagamentos'] = Pagamento.objects.filter(inscricao=self.object)
        return context

class PagamentoCreateView(LoginRequiredMixin, CreateView):
    model = Pagamento
    fields = ['valor_pago', 'metodo_pagamento', 'observacao', 'data_pagamento']
    template_name = 'pagamento_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        inscricao_id = self.kwargs['inscricao_id']
        inscricao = Inscricao.objects.get(pk=inscricao_id)

        form.instance.inscricao_id = inscricao_id
        response = super().form_valid(form)

        if form.instance.valor_pago:
            inscricao.valor_pagar = (inscricao.valor_pagar or 0) - form.instance.valor_pago
            if inscricao.valor_pagar <= 0:
                inscricao.valor_pagar = 0
                inscricao.status = 'quitado'
            print(inscricao.valor_pagar)
            inscricao.save()

        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string('partials/pagamento_row.html', {'pagamento': form.instance})
            return JsonResponse({'success': True, 'row_html': html})

        return response

class InscricaoDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        inscricao = get_object_or_404(Inscricao, pk=pk)
        inscricao.delete()
        return redirect('home')
    