from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from .forms import SignUpForm, LoginForm,ChangePassForm
from .utils import generate_code,send_to_mail

# Create your views here.

# def signup_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         email = request.POST['email']
#         password1 = request.POST['password1']
#         password2 = request.POST['password2']
#
#         if password1 != password2:
#             messages.error(request,'Parollar mos kelmadi!')
#             return redirect('signup')
#
#         if User.objects.filter(username=username).exists():
#             messages.error(request,"Bu username oldin ruyxatdan utgan")
#             return redirect('signup')
#
#         User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,
#                                         password=password1)
#         messages.success(request,'Siz muvaffaqqiyatli ruyxatdan utdingiz!')
#         return redirect('login')
#
#     return render(request,'account/signup.html')
#
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         if username is None or password is None:
#             messages.error(request,'Login yoki parol xato kiritildi!')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             messages.success(request, 'Siz tizimga muvaffaqiyatli kirdingiz!')
#             return redirect('index')
#
#         messages.error(request,'Bunaqa login topilmadi! ')
#         return redirect('login')
#     return render(request,'account/login.html' )
#
def logout_view(request):
    logout(request)
    messages.info(request,'Siz dasturdan chiqdingiz!')
    return redirect('index')


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                messages.error(request,"Bu username oldin ruyxatdan utgan")
                return redirect('signup')
            form.save()
            messages.success(request,"Ro'yxatdan o'tdingiz")
            return redirect('login')
        else:
            messages.error(request,'Nimadir xato')
    form = SignUpForm()
    return render(request,'account/signup.html',{'form':form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request=request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request,'Siz dasturga kirdingiz!')
            return redirect('index')
        else:
            messages.error(request,'Nimadir xato ketdi!')
    form = LoginForm()
    return render(request,'account/login.html',{'form':form})

@login_required(login_url='login')
def profile(request):
    user = User.objects.get(username=request.user.username)
    return render(request,'account/profile.html',{'user':user})

def change_pass_view(request):
    if request.method == 'GET':
        code = generate_code()
        request.session['verification_code'] = code
        send_to_mail(request.user.email, code)
        messages.info(request,"Emailingizga kod yuborildi")
        form = ChangePassForm()
        return render(request,'account/change_pass.html',{'form':form})

    else:
        form = ChangePassForm(request.POST)
        if form.is_valid():
            old_pass = form.cleaned_data['old_pass']
            new_pass = form.cleaned_data['new_pass']
            confirm_pass = form.cleaned_data['confirm_pass']
            code = form.cleaned_data['code']
            session_code = request.session.get('verification_code')

            if not request.user.check_password(old_pass):
                messages.error(request,"eski parol xato kiritildi")
                return redirect('change-pass')

            if new_pass != confirm_pass:
                messages.error(request, "Yangi parollar mos emas.")
                return redirect('change-pass')

            if session_code != code:
                messages.error(request,'Tasdiqlash kodingiz xato')
                return redirect('change-pass')


            user = request.user
            user.set_password(new_pass)
            user.save()
            messages.success(request,"Parolingiz uzgatirildi")

            return redirect('profile')

