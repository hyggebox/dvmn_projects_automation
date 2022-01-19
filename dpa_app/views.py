from django.shortcuts import render

# Create your views here.

def show_time_slots(request, user_id):
    return render(request, 'choose_time.html', context={'user_id': user_id})