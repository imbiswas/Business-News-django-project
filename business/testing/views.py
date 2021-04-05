from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from .forms import *
from django.contrib import messages
from .models import *
from django.forms import modelformset_factory
# Create your views here.
def post(request):

    ImageFormSet = modelformset_factory(Images,
                                        form=ImageForm, extra=4)

    if request.method == 'POST':

        postForm = PostForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Images.objects.none())


        if postForm.is_valid() and formset.is_valid():
            post_form = postForm.save(commit=False)
            post_form.user = request.user
            post_form.save()

            for form in formset.cleaned_data:
                image = form['image']
                photo = Images(post=post_form, image=image)
                photo.save()
            messages.success(request,
                             "Posted!")
            return HttpResponseRedirect("/")
        else:
            pass
    else:
        postForm = PostForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    return render(request, 'testing.html',
                  {'postForm': postForm, 'formset': formset},
                  )