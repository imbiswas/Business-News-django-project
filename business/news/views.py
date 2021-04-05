from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from .forms import *
from django.contrib import messages
from .models import *
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from home import recommender
from home.views import get_cat
from bs4 import BeautifulSoup
from django.db.models import Q
from django.urls import  reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from hitcount.views import HitCountDetailView



# Create your views here.
@login_required (login_url='/')
def add_news(request):
    Imageformset = modelformset_factory(Images, fields= ('image',),extra=4)
    if request.method == 'POST':
        formset = Imageformset(request.POST or None, request.FILES or None)
        forms = NewsForm(request.POST,request.FILES,)
        if forms.is_valid() and formset.is_valid:
            form_data = forms.save(commit=False)
            form_data.save()
            img_image = BeautifulSoup(form_data.News)
            links = []
            for link in img_image.find_all('img'):  #Cycle through all 'img' tags
                imgSrc = link.get('src')   #Extract the 'src' from those tags
                links.append(imgSrc)
            l = len(links)
            for i in range(l):
                photo = Images(News = form_data, image = links[i][6:])
                photo.save()

            for f in formset.cleaned_data:
                try:
                    if 'image' in f:
                        image = f['image']
                        photo = Images(News=form_data, image=image)
                        photo.save()
                except Exception as e:
                    break
            
            messages.success(request, f'New data added successfully!')
            return redirect('all_news')
    else:
        forms = NewsForm()
        formset = Imageformset(queryset = Images.objects.none())

    
        
    context_dict = {'forms': forms, 'formset':formset, }

    return render (request,'news/newsForm.html',context_dict)

@login_required (login_url='/')
def add_headline_news(request):
    Imageformset = modelformset_factory(Images, fields= ('image',),extra=4)
    if request.method == 'POST':
        formset = Imageformset(request.POST or None, request.FILES or None)
        forms = NewsForm(request.POST,request.FILES,)
        if forms.is_valid() and formset.is_valid():
            form_data = forms.save(commit=False)
            form_data.save()
            headline = HeadlineNews(news_id = form_data)
            headline.save()
            img_image = BeautifulSoup(form_data.News)
            links = []
            for link in img_image.find_all('img'):  #Cycle through all 'img' tags
                imgSrc = link.get('src')   #Extract the 'src' from those tags
                links.append(imgSrc)
            l = len(links)
            for i in range(l):
                photo = Images(News = form_data, image = links[i][6:])
                photo.save()

            for f in formset.cleaned_data:
                try:
                    if 'image' in f:
                        image = f['image']
                        photo = Images(News=form_data, image=image)
                        photo.save()
                except Exception as e:
                    break

            
            messages.success(request, f'New data added successfully!')
            return redirect('add_headline')
    else:
        forms = NewsForm()
        formset = Imageformset(queryset = Images.objects.none())
        
    context_dict = {'forms': forms, 'formset':formset, }

    return render (request,'news/newsForm.html',context_dict)
    

def all_news (request):
    queryset = news.objects.all()
    
    cat = get_cat(request)

    news_ = news.objects.order_by('?') # to get unordered/shuffled list
    a = 9
    recommended_news = news_[:a]
    
    context = {
        "news":queryset,
        'recommended_news':recommended_news[:9],
        'categories': cat
        
    }
    return render(request,'news/allnews.html',context)


def category(request):
    if request.method == 'POST':
        forms = CategoryForm(request.POST,)
        if forms.is_valid():
            form_data = forms.save(commit=False)
            form_data.save()
            messages.success(request, f'New data added successfully!')
            return redirect('category')

    else:
        forms = CategoryForm()
        context_dict = {'forms': forms, }

    return render (request,'news/category.html',context_dict)

class NewsListView(ListView):
    template_name = 'news/edit.html'
    queryset = news.objects.order_by('-timestamp')
    context_object_name = 'results'

class HeadlineListView(ListView):
    template_name = 'news/edit_headlines.html'
    queryset = HeadlineNews.objects.all().order_by('-id')
    context_object_name = 'results'

class NewsDetailView(HitCountDetailView):
    model = news
    template_name = 'news/single_news.html'
    context_object_name = 'headline_news'
    slug_field = 'slug'
    count_hit = True
      # query_pk_and_slug = True
    # set to True to count the hit

    def get_context_data(self, **kwargs):
        context = super(NewsDetailView, self).get_context_data(**kwargs)
        cat = get_cat(self.request)
        # currentUser = self.request.COOKIES['clientId']
        headline_news = news.objects.get(slug=self.get_object().slug) # returns only one object
        try:
            currentUser = self.request.COOKIES['clientId']
            recommended_news=recommender.recommendationForUserInCookie(currentUser,headline_news.category)
        except:
            recommended_news= news.objects.filter(category = headline_news.category)[:4]
        # recommended_news=recommender.recommendationForUserInCookie(currentUser,headline_news.category)
        context['recent_news'] = news.objects.order_by('-timestamp')[0:4]
        context['categories'] = cat
        context['recommended_news'] = recommended_news
        context.update({
        # 'headline_news': news.objects.get(slug=news.slug), # returns only one object
        'popular_posts': news.objects.order_by('-hit_count_generic__hits')[0:4],
        'headlines': HeadlineNews.objects.all().order_by('-id')[:6]
        })
        return context


def show_one_item(request, slug): 

    cat = get_cat(request)

    currentUser = request.COOKIES['clientId']
    print(currentUser)
    headline_news = news.objects.get(slug=slug) # returns only one object
    recommended_news=recommender.recommendationForUserInCookie(currentUser,headline_news.category)

    headline_news.viewcount = headline_news.viewcount + 1
    headline_news.save()
    images = Images.objects.filter(News = headline_news)
    # print(headline_news.category.title)
    # recommended_news = news.objects.filter(category=headline_news.category)
    # if request.user.is_authenticated:
    #     recommended_news = recommender.get_recommended_news(request)
    #     recommender.save_tags_and_value(request, headline_news.tags)
    # else:
    #     news_ = news.objects.order_by('?') # to get unordered/shuffled list
    #     # a = news_.count()/2
    #     a = 9
    #     recommended_news = news_[:a]
    
    context = {
        'headline_news': headline_news,
        'recommended_news':recommended_news,
        # 'recommended_news':recommended_news[:5],
        'categories': cat,
        'images': images,
    }
    return render(request, 'news/single_news.html', context)

def this_category(request, category):

    cat = get_cat(request)

    # Category is a different object
    news_of_this_category = news.objects.filter(category=Category.objects.get(title=category))
    context={
        'news':news_of_this_category,
        'categories': cat
    }
    return render(request,'news/allfromthiscategory.html',context)
    

def search(request):

    cat = get_cat(request)
    news_ = news.objects.order_by('?') # to get unordered/shuffled list

    if request.method == 'GET':
        query= request.GET.get('search')

        if query is not None:
            lookups= Q(Heading__icontains=query) | Q(News__icontains=query) | Q(tags__icontains=query) | Q(author__icontains=query)

            results= news.objects.filter(lookups).distinct()

            context={
                'results': results,
                'categories': cat,
            }
            print(results)
            return render(request, 'news/edit.html', context)

        else:
            return redirect ('add_news')

    else:
        return redirect ('add_news')


class NewsUpdate(UpdateView,UserPassesTestMixin, LoginRequiredMixin):
    model = news
    fields = ['Heading','News','tags','category','excerpt']
    template_name = 'news/newsForm.html'
    success_url = reverse_lazy('show_all')

class NewsDelete(DeleteView,UserPassesTestMixin, LoginRequiredMixin):
    model = news
    template = 'news/news_confirm_delete.html'
    success_url = reverse_lazy('show_all')

class HeadlineDelete(DeleteView,UserPassesTestMixin, LoginRequiredMixin):
    model = HeadlineNews
    template = 'news/HeadlineNews_confirm_delete.html'
    success_url = reverse_lazy('show_all_headlines')


    