from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.db import models
from .models import Consumption


def login_view(request):
    """登录视图"""
    if request.user.is_authenticated:
        return redirect('consumption:index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('consumption:index')
        else:
            messages.error(request, '用户名或密码错误')

    return render(request, 'consumption/login.html')


def logout_view(request):
    """登出视图"""
    logout(request)
    return redirect('consumption:login')


@login_required(login_url='/login/')
def index_view(request):
    """首页视图"""
    context = {
        'total_count': Consumption.objects.count(),
        'total_amount': Consumption.objects.aggregate(total=models.Sum('amount'))['total'] or 0,
        'recent_records': Consumption.objects.all()[:5],
        'user': request.user,
    }
    return render(request, 'consumption/index.html', context)


@login_required(login_url='/login/')
def list_view(request):
    """消费列表视图（带分页）"""
    # 获取筛选参数
    location = request.GET.get('location', '')
    consumption_type = request.GET.get('type', '')

    # 基础查询
    records = Consumption.objects.all()

    # 应用筛选
    if location:
        records = records.filter(location=location)
    if consumption_type:
        records = records.filter(consumption_type=consumption_type)

    # 分页配置（每页5条）
    paginator = Paginator(records, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # 获取筛选项的选项列表
    locations = Consumption.objects.values_list('location', flat=True).distinct()
    types = Consumption.objects.values_list('consumption_type', flat=True).distinct()

    context = {
        'page_obj': page_obj,
        'locations': locations,
        'types': types,
        'selected_location': location,
        'selected_type': consumption_type,
        'user': request.user,
    }
    return render(request, 'consumption/list.html', context)