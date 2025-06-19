# capa de vista/presentación
from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index_page(request):
    return render(request, 'index.html')

def home(request):
    images = services.getAllImages()
    favourite_list = []
    if request.user.is_authenticated:
        favourite_list = services.getAllFavourites(request)
        # Solo los nombres para comparar en el template
        favourite_list = [fav.name for fav in favourite_list]
    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

def search(request):
    name = request.POST.get('query', '')
    images = services.getAllImages()
    if name != '':
        images = [img for img in images if name.lower() in img.name.lower()]
        favourite_list = []
        if request.user.is_authenticated:
            favourite_list = services.getAllFavourites(request)
            favourite_list = [fav.name for fav in favourite_list]
        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

def filter_by_type(request):
    type = request.POST.get('type', '')
    if type != '':
        images = services.getAllImages()
        filtroTipo = [img for img in images if type in [tipo.lower() for tipo in img.types]]
        favourite_list = []
        if request.user.is_authenticated:
            favourite_list = services.getAllFavourites(request)
            favourite_list = [fav.name for fav in favourite_list]
        return render(request, 'home.html', { 'images': filtroTipo, 'favourite_list': favourite_list })
    else:
        return redirect('home')

@login_required
def getAllFavouritesByUser(request):
    favourite_list = services.getAllFavourites(request)
    return render(request, 'favourites.html', {'favourite_list': favourite_list})

@login_required
def saveFavourite(request):
    if request.method == 'POST':
        services.saveFavourite(request)
    return redirect('home')

@login_required
def deleteFavourite(request):
    if request.method == 'POST':
        services.deleteFavourite(request)
    return redirect('get-favourites')

@login_required
def exit(request):
    logout(request)
    return redirect('home')