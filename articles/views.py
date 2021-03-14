from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.generic import View 
from datetime import datetime
from articles.forms import CommentsForm, CommentsFormPreview
from articles.models import *
# Create your views here.


class Home(View):

    def get(self, request):
        data = {}
        sort = request.GET.get('sort')
        sort2 = request.GET.get('sort2')

        if sort == None:
            sort = 'created_at'

        if sort2 == None or sort2 == 'desc':
            sort2 = 'desc'
            result_sort = '-' + sort
        else:
            result_sort = sort
            sort2 = 'asc'

        comments = Comments.objects.filter(parent=None).order_by(result_sort)
        paginator = Paginator(comments, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        data['page_obj'] = page_obj

        comments = []
        for x in page_obj:
            page_obj = list(Comments.objects.get(pk=x.id).get_root().get_family())
            comments.extend(page_obj) 
            
        form = CommentsForm()

        data['comments'] = comments
        data['form'] = form
        data['sort'] = sort
        data['sort2'] = sort2

        return render(request, 'articles/home.html', data)

    def post(self, request):
        form = CommentsForm(request.POST, request.FILES)
        data = {}

        if form.is_valid():

            pk = request.POST.get('parent')
            parent = Comments.objects.filter(pk=pk).first()
            
            comment = Comments(**form.cleaned_data)
            comment.parent = parent
            comment.ip = request.META.get('REMOTE_ADDR', '') or request.META.get('HTTP_X_FORWARDED_FOR', '')
            comment.browser_info = request.META['HTTP_USER_AGENT']
            comment.save()
            data = {
                'result': 'success'
            }
            return JsonResponse(data)

        else:
            data = {
                'result': 'error',
                'response': form.errors
            }
            return JsonResponse(data)


class Preview(View):
    def post(self, request):
        form = CommentsFormPreview(request.POST, request.FILES)
        data = {}

        if form.is_valid():
            pk = request.POST.get('parent')
            data = {
                'result': 'success',
                'response': form.cleaned_data
            }

            data['response']['parent'] = request.POST.get('parent')
            data['response']['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M")
            return JsonResponse(data)

        else:
            data = {
                'result': 'error',
                'response': form.errors
            }
            return JsonResponse(data)
  
   

