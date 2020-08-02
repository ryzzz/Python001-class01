from django.shortcuts import render
from django.http import HttpResponse
from .models import T1


def start_gt_3(request):
    # 大于3星的
    queryset = T1.objects.all()
    condition = {'n_star__gt': 3}
    shorts = queryset.filter(**condition)
    # return HttpResponse('text')
    return render(request, 'result.html', locals())


def search_comment(request):
    text = request.GET.get('q')
    # 大于3星的
    queryset = T1.objects.all()
    condition = {'n_star__gt': 3, 'short__icontains': text}
    shorts = queryset.filter(**condition)
    # return HttpResponse('text')
    return render(request, 'result.html', locals())