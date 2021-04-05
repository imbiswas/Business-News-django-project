from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from news.models import news, Category as newsCategory, HeadlineNews
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .recommender import get_recommended_news
import random
from django.db.models import Q
from .news24scraper import loadOnce
from advertisement.models import Ads
from django.utils import timezone
from hitcount.views import HitCountDetailView


def get_cat(request):

    query_Set = newsCategory.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(query_Set, 20)
    try:
        cat = paginator.page(page)
    except PageNotAnInteger:
        cat = paginator.page(1)
    except EmptyPage:
        cat = paginator.page(paginator.num_pages)
    
    return cat


# Create your views here.
def index (request):
    # query_pk_and_slug = True
    # count_hit = True
    queryset = news.objects.all()

    header_banner_set = Ads.objects.filter (
            duration_start__lte=timezone.now(),
            duration_end__gte=timezone.now(),ad_position = 'H')
    
    sidebar_ads = Ads.objects.filter(
            duration_start__lte=timezone.now(),
            duration_end__gt=timezone.now(),ad_position = 'S'
    )
    
    cat = get_cat(request)

    # popular_news = news.objects.order_by('-viewcount')[0:4]
    popular_news = news.objects.order_by('-hit_count_generic__hits')[0:4]
    headline_news = HeadlineNews.objects.all().order_by('-id')[:6]

    context = {
        "news":queryset[:10],
        'categories': cat,
        # 'ad1':ad1,
        'popular_news':popular_news,
        'headline_news': headline_news,
        'header_ads': header_banner_set,
        'sidebar_ads': sidebar_ads,
    }

    if request.user.is_authenticated:
        recommended_news = get_recommended_news(request)
        context.update({'recommended_news':recommended_news[:5]})
    else:
        news_ = news.objects.order_by('?') # to get unordered/shuffled list
        # a = news_.count()/2
        a = 5
        news_to_recommend = news_[:a]
        context.update({'recommended_news':news_to_recommend})

    return render(request, 'home/index.html', context)

def search(request):

    cat = get_cat(request)

    if request.user.is_authenticated:
        recommended_news = get_recommended_news(request)
    else:
        news_ = news.objects.order_by('?') # to get unordered/shuffled list
        a = 9
        recommended_news = news_[:a]

    if request.method == 'GET':
        query= request.GET.get('search')

        if query is not None:
            lookups= Q(Heading__icontains=query) | Q(News__icontains=query) | Q(tags__icontains=query) | Q(author__icontains=query)

            results= news.objects.filter(lookups).distinct()

            context={
                'results': results,
                'recommended_news':recommended_news[:9],
                'categories': cat,
            }
            print(results)
            return render(request, 'home/search.html', context)

        else:
            return redirect ('index')

    else:
        return redirect ('index')




