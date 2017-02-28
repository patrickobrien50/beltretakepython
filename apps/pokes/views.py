from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count, Sum

from .models import User, Poke

# Create your views here.

def index(request):
    if 'id' in request.session:
        request.session.pop('id')
    return render(request, 'pokes/index.html')

def register(request):
    user = User.objects.validateRegister(request.POST)
    if user[0] == False:
        for error in user[1]:
            messages.error(request, error)
        return redirect('/')
    else:
        request.session['id'] = user[1].id
        print "Welcome User", request.session['id']
        context = {
        'users': User.objects.get(email=request.POST['email'])
        }
        return redirect("/success")

def login(request):
    user = User.objects.loginValidate(request.POST)
    if user[0] == False:
        for error in user[1]:
            messages.error(request, error)
        return redirect('/')
    else:
        print "We made it"
        request.session['id'] = user[1].id

        return redirect("/success")

def success(request):
    user = User.objects.get(id=request.session['id'])
    context = {
    'you': user,
    'users': User.objects.all().exclude(id=request.session['id']),
    'pokes': Poke.objects.all(),
    'your_pokes': Poke.objects.all().filter(poked=request.session['id'])
    }
    return render(request, 'pokes/home_page.html', context)

def pokeUser(request, id):
    poker = User.objects.get(id=request.session['id'])
    pokee = User.objects.get(id=id)
    if len(Poke.objects.filter(poker=poker, poked=pokee)) < 1:
        Poke.objects.create(poker=poker, poked=pokee, counter = 1)
        pokee.total += 1
        pokee.save()
        return redirect("/success")

    else:
        poke = Poke.objects.filter(poker=poker, poked=pokee)
        poked = poke[0]
        poked.counter += 1
        pokee.total += 1
        poked.save()
        pokee.save()


        print "GOT POKED", poked.poker.name, poked.poked.name, poked.counter
        return redirect("/success")

def logout(request):
    request.session.pop('id')
    return render(request, 'pokes/index.html')
