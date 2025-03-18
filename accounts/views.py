from django.shortcuts import render, redirect
from django.views.generic import FormView
from .forms import SignUpForm
from django.contrib.auth import login

# def SignUpView(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('/')
#     else:
#         form = SignUpForm()
#         return render(request,'registration/signup.html', {'form': form})

class SignUpView(FormView):
    form_class = SignUpForm
    template_name ='registration/signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')
