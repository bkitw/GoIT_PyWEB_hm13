from datetime import datetime
from django.shortcuts import render, redirect
from .models import Category, Operations
from django.db.models import Sum


# Create your views here.


def main(request):
    operations = Operations.objects.order_by('-created_at').all()[:10]
    balance = Operations.objects.aggregate(balance=Sum('sum'))
    return render(request, 'finance_accounting/index.html', {'operations': operations, 'balance': balance['balance']})


def add_category(request):
    if request.method == 'POST':
        name = request.POST['name']
        if name:
            category = Category(name=name)
            category.save()
        return redirect(to='/')
    return render(request, 'finance_accounting/add_category.html', {})


def add_operation(request):
    if request.method == 'POST':
        op_sum = request.POST['sum']
        type = request.POST['type']
        if type == "0":
            op_sum = 0 - int(op_sum)
        category_name = request.POST['category']
        if op_sum and type:
            category = Category.objects.get(name=category_name)
            operation = Operations(sum=op_sum, type=type, category=category)
            operation.save()
        return redirect(to='/')

    categories = Category.objects.all()
    return render(request, 'finance_accounting/add_operation.html', {"categories": categories})


def detail(request):
    if request.GET.get('datetime_from', False) and request.GET.get('datetime_to', False):
        operations = Operations.objects.filter(
            created_at__range=[request.GET['datetime_from'], request.GET['datetime_to']])
        balance = 0
        income = 0
        outcome = 0
        if operations:
            for operation in operations:
                balance = balance + int(operation.sum)
                if operation.type is True:
                    income = income + int(operation.sum)
                elif operation.type is False:
                    outcome = outcome + int(operation.sum) * -1
        return render(request, 'finance_accounting/detail.html',
                      {'operations': operations,
                       'datetime_to': datetime.strptime(request.GET['datetime_to'], '%Y-%m-%dT%H:%M'),
                       'datetime_from': datetime.strptime(request.GET['datetime_from'], '%Y-%m-%dT%H:%M'), 'balance': balance,
                       'income': income,
                       'outcome': outcome})

    return render(request, 'finance_accounting/detail.html', {'datetime_to': request.GET.get('datetime_to', False),
                                                              'datetime_from': request.GET.get('datetime_from', False)})
