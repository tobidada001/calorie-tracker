from django.shortcuts import render, redirect
from django.http import HttpResponse
from calorieapp.models import Meal, Consumed
from django.contrib import messages
from django.db.models import Sum
import datetime
# Create your views here.

def index(request):
    meals = Meal.objects.all()
    consumed_meals = Consumed.objects.filter(owner  = request.user)
    t_carbs = Consumed.objects.filter(owner  = request.user).aggregate(total = Sum('food__meal_carbohydrates_level') )
    t_pros = Consumed.objects.filter(owner  = request.user).aggregate(total = Sum('food__meal_protein_level') )
    t_fats = Consumed.objects.filter(owner  = request.user).aggregate(total = Sum('food__meal_fats_level') )
    t_cals = Consumed.objects.filter(owner  = request.user).aggregate(total = Sum('food__meal_cal_level') )
    t_mgs = Consumed.objects.filter(owner  = request.user).aggregate(total = Sum('food__meal_mg_level') )
    t_nas = Consumed.objects.filter(owner  = request.user).aggregate(total = Sum('food__meal_na_level') )
    t_chols = Consumed.objects.filter(owner  = request.user).aggregate(total = Sum('food__meal_chol_level') )
    progress = (int(t_cals['total']) / 100) * 100


    days = datetime.datetime.today()
    last_7_days = consumed_meals.filter(date_added__gte = str(days - datetime.timedelta(days= 7))).aggregate(total_7_days = Sum('food__meal_cal_level'))
    last_30_days = consumed_meals.filter(date_added__gte = str(days - datetime.timedelta(days= 30))).aggregate(total_30_days = Sum('food__meal_cal_level'))
    last_52_weeks = consumed_meals.filter(date_added__gte = str(days - datetime.timedelta(weeks= 52))).aggregate(total_52_weeks = Sum('food__meal_cal_level'))
    
    context = {'meals': meals, 'consumed_meals': consumed_meals, 't_carbs': t_carbs, 't_pros': t_pros, 't_fats': t_fats, 't_cals': t_cals,
               't_mgs': t_mgs, 't_nas': t_nas, 't_chols': t_chols, 'progress': progress, 'last7days': last_7_days, 'last30days': last_30_days,
               'last52weeks': last_52_weeks}

    if request.method == 'POST':
        food = request.POST['meal_name']
        meal = Meal.objects.filter(meal_name = food).first()

        newly_consumed = Consumed(food = meal, owner = request.user)
        newly_consumed.save()
        messages.success(request, 'Newly consumed meal added')
        return redirect('/')

    return render(request, 'index.html', context=context)

def delete(request):
    return ""

def signup(request):
    return render(request, 'signup.html')
    

def loginuser(request):
    return render(request, 'signin.html')
    

def logoutuser(request):
    return ""