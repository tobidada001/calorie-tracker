from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from calorieapp.models import Meal, Consumed
from django.contrib import messages
from django.db.models import Sum
import datetime
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models.functions import TruncDay
# Create your views here.

def index(request):
    meals = Meal.objects.all()
    consumed_meals = Consumed.objects.filter(owner  = request.user)
    t_carbs = consumed_meals.aggregate(total = Sum('food__meal_carbohydrates_level') )
    t_pros = consumed_meals.aggregate(total = Sum('food__meal_protein_level') )
    t_fats = consumed_meals.aggregate(total = Sum('food__meal_fats_level') )
    t_cals = consumed_meals.aggregate(total = Sum('food__meal_cal_level') )
    t_mgs = consumed_meals.aggregate(total = Sum('food__meal_mg_level') )
    t_nas = consumed_meals.aggregate(total = Sum('food__meal_na_level') )
    t_chols = consumed_meals.aggregate(total = Sum('food__meal_chol_level') )

    if t_cals.get('total'):
        progress = (int(t_cals['total']) / 100) * 100
    else: 
        progress = 0

    days = datetime.datetime.today()
    last_7_days = consumed_meals.filter(date_added__gte = str(days - datetime.timedelta(days= 7))).aggregate(total_7_days = Sum('food__meal_cal_level'))
    last_30_days = consumed_meals.filter(date_added__gte = str(days - datetime.timedelta(days= 30))).aggregate(total_30_days = Sum('food__meal_cal_level'))
    last_52_weeks = consumed_meals.filter(date_added__gte = str(days - datetime.timedelta(weeks= 52))).aggregate(total_52_weeks = Sum('food__meal_cal_level'))
    
    context = {'meals': meals, 'consumed_meals': consumed_meals, 't_carbs': t_carbs, 't_pros': t_pros, 't_fats': t_fats, 't_cals': t_cals,
               't_mgs': t_mgs, 't_nas': t_nas, 't_chols': t_chols, 'progress': progress, 'last7days': last_7_days, 'last30days': last_30_days,
               'last52weeks': last_52_weeks}
    
    print(consumed_meals.values('id', date = TruncDay('date_added')).annotate(totaltoday = Sum('food__meal_cal_level')))

    if request.GET.get('readyToFetch'):
        all_calorie_data = []

        for meal in consumed_meals.values('id', date = TruncDay('date_added')).annotate(totaltoday = Sum('food__meal_cal_level')):
            
            all_calorie_data.append({'date': meal['date'], 'calorie_quantity': meal['totaltoday']})

        return JsonResponse({'alltimedata': all_calorie_data})
    
    if request.method == 'POST':
        food = request.POST['meal_name']
        meal = Meal.objects.filter(meal_name = food).first()

        newly_consumed = Consumed(food = meal, owner = request.user)
        newly_consumed.save()
        messages.success(request, 'Newly consumed meal added')
        return redirect('/')

    return render(request, 'index.html', context=context)


def delete(request, id):

    consumed = get_object_or_404(Consumed, id = id, owner= request.user)
    consumed.delete()
    messages.success(request, 'Expense record deleted successfully.')
    return redirect('/')


def loginuser(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        auth = authenticate(request, username= request.POST['username'], password = request.POST['password1'])
        if auth:
            login(request, auth)
            return redirect('/')
        else:
            messages.error(request, 'Could not login.')
            return redirect('/new-user')
        
    return render(request, 'signin.html')



def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        if not request.POST['password1'] == request.POST['password2']:
            messages.error(request, 'Your passwords don\'t match')
            return redirect('new-user')
        
        user = User.objects.create(first_name = request.POST['firstname'], last_name = request.POST['lastname'], username= request.POST['username'])
        user.set_password(request.POST['password1'])
        user.save()
        messages.success(request, 'Your account has been created successfully.')

        auth = authenticate(request=request, username= request.POST['username'], password = request.POST['password1'])

        if auth:
            login(request, auth)
            return redirect(to='/')
        else:
            messages.error(request, 'Could not login you in.')
            return redirect(request.path)
        
    return render(request, 'signup.html')


def logoutuser(request):
    logout(request)
    return redirect('loginuser')
