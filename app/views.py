# capa de vista/presentación
from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    images = services.getAllImages()
    favourite_list = []

    if request.user.is_authenticated:
        favourite_list = services.getAllFavourites(request)
        nombres_fav = []
        for fav in favourite_list: 
            nombres_fav.append(fav.name)
        favourite_list = nombres_fav

    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

# función utilizada en el buscador.
def search(request):
    name = request.POST.get('query', '')
    images = services.getAllImages()
    # si el usuario ingresó algo en el buscador, se deben filtrar las imágenes por dicho ingreso.
    if (name != ''):
        filtered_images = []
        name = name.lower()
        for img in images:
            if name in img.name.lower():
                filtered_images.append(img)
        images = filtered_images

        favourite_list = []
        if request.user.is_authenticated:
            favourite_list = services.getAllFavourites(request)
            nombres_fav = []
            for fav in favourite_list:
                nombres_fav.append(fav.name)
            favourite_list = nombres_fav

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

# función utilizada para filtrar por el tipo del Pokemon
def filter_by_type(request):
    type = request.POST.get('type', '')

    if type != '':
        images = services.getAllImages()
        filtroTipo = [] 
        for img in images:
            type_minus = []
            for t in img.types:
                type_minus.append(t.lower())
            
            if type in type_minus:
                filtroTipo.append(img)

        favourite_list = []
        if request.user.is_authenticated:
            favourite_list = services.getAllFavourites(request)
            fav_name = []
            for fav in favourite_list:
                fav_name.append(fav.name)
            favourite_list = fav_name
        return render(request, 'home.html', { 'images': filtroTipo, 'favourite_list': favourite_list })
    else:
        return redirect('home')

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
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
    return redirect('favoritos')

@login_required
def exit(request):
    logout(request)
    return redirect('home')