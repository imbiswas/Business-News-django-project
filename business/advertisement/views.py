from django.views.generic import (
    CreateView, 
    UpdateView, 
    ListView, 
    DeleteView
)
from .models import Ads
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.http import HttpResponseRedirect

from django.db.models import Q

from datetime import datetime

from .forms import PostForm

class CreateAdView(LoginRequiredMixin,UserPassesTestMixin, CreateView, ):
    model = Ads
    form_class = PostForm
    template_name = 'advertisement/createad.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        return self.request.user.is_superuser

class EditAdView(UpdateView, UserPassesTestMixin, LoginRequiredMixin):
    model = Ads
    form_class = PostForm
    template_name = 'advertisement/editad.html'
    success_url = reverse_lazy('show_ad')

    def form_valid(self, form):
        form.instance.timestamp = datetime.now()
        return super().form_valid(form)

class ListAdView(ListView, UserPassesTestMixin):
    template_name = 'ads_list.html'
    queryset = Ads.objects.order_by('-timestamp')
    context_object_name = 'adslist'
    # paginate_by = 5


class DeleteAdView(DeleteView, UserPassesTestMixin, LoginRequiredMixin):
    model = Ads
    def get_success_url(self):
        return reverse_lazy('show_ad')
    
def search(request):
    
    if request.method == 'GET':
        query= request.GET.get('search')

        if query is not None:
            lookups= Q(company_name__icontains=query) | Q(url__icontains=query) | Q(duration_start__icontains=query) | Q(duration_end__icontains=query)

            results= Ads.objects.filter(lookups).distinct()

            context={
                'results': results,
            }
            return render(request, 'advertisement/search.html', context)

        else:
            return redirect ('create_ad')

    else:
        return redirect ('index')

class AdClickView(SingleObjectMixin, View):

    def get_queryset(self):
        return Ads.objects.all()

    def get(self, request, *args, **kwargs):
        ad = self.get_object()
        ad.clicks = ad.clicks + 1
        ad.save()
        return HttpResponseRedirect(ad.url)