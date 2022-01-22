from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404

from .forms import ChooseTimeForm
from .models import Student


def show_time_slots(request, user_id):
    try:
        student = Student.objects.get(tg_id=user_id)
    except Student.DoesNotExist:
        raise Http404('Page Not Found')
    else:
        if request.method == 'POST':
            form = ChooseTimeForm(request.POST)
            if form.is_valid():
                best_time_slots = form.cleaned_data.get('best_time_slots')
                ok_time_slots = form.cleaned_data.get('ok_time_slots')

                student.best_time_slots.set(best_time_slots)
                student.ok_time_slots.set(ok_time_slots)

                return HttpResponseRedirect('/thanks/')

        form = ChooseTimeForm()
        return render(request, 'choose_time.html',
                      context={
                          'user_id': user_id,
                          'form': form,
                          'name': student.f_name
                      })


def show_thanks(request):
    return render(request, 'thanks.html')