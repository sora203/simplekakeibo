from django.shortcuts import render, redirect
from .models import Expense
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import ExtractYear, ExtractMonth

def index(request):
    now = timezone.now()
    year = int(request.GET.get('year', now.year))
    month = int(request.GET.get('month', now.month))

    if request.method == 'POST':
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        balance_type = request.POST.get('balance_type')
        payment_method = request.POST.get('payment_method') # ★追加
        
        Expense.objects.create(
            title=title,
            amount=amount,
            category=category,
            balance_type=balance_type,
            payment_method=payment_method, # ★追加
            date=timezone.now()
        )
        return redirect(f'/?year={year}&month={month}')

    expenses = Expense.objects.filter(date__year=year, date__month=month).order_by('-date')

    total_out = expenses.filter(balance_type='out').aggregate(Sum('amount'))['amount__sum'] or 0
    total_in = expenses.filter(balance_type='in').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_in - total_out

    month_list = Expense.objects.annotate(
        y=ExtractYear('date'), 
        m=ExtractMonth('date')
    ).values('y', 'm').distinct().order_by('-y', '-m')

    import calendar
    last_day = calendar.monthrange(year, month)[1]
    days = [f"{i}日" for i in range(1, last_day + 1)]
    
    income_data = [0] * last_day
    expense_data = [0] * last_day

    for exp in expenses:
        day_index = exp.date.day - 1
        if exp.balance_type == 'in':
            income_data[day_index] += int(exp.amount)
        else:
            expense_data[day_index] += int(exp.amount)

    context = {
        'expenses': expenses,
        'total_out': total_out,
        'total_in': total_in,
        'balance': balance,
        'month_list': month_list,
        'current_year': year,
        'current_month': month,
        'graph_days': days,
        'graph_income': income_data,
        'graph_expense': expense_data,
    }
    return render(request, 'expenses/index.html', context)

# views.py の一番下
def delete_expense(request, pk):
    if request.method == 'POST':
        expense = Expense.objects.get(pk=pk)
        # 消す前に、そのデータが「何年何月」のものか覚えておく
        y = expense.date.year
        m = expense.date.month
        expense.delete()
        # 消した後、その月の画面に戻る
        return redirect(f'/?year={y}&month={m}')
    return redirect('index')