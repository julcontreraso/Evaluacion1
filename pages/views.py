from django.shortcuts import render, redirect
import folium.map
from api.models import Producto
from django.conf import settings
from django.core.mail import EmailMessage
import folium
from django.contrib.auth.decorators import login_required
from .models import Location
# Create your views here.


def home(request):
    
    locations = Location.objects.all()
    initialMap = folium.Map(location=[-33.43292210194037, -70.61491263182941], zoom_start=18)
    for location in locations:
        coordinates = (location.lat, location.lng)
        folium.Marker(coordinates, popup='Sucursal' + location.name).add_to(initialMap)
    map_html = initialMap._repr_html_()
    context = {'map': map_html, 'locations':locations}
    productosListado = Producto.objects.all()
    return render(request, "index.html", context)




def tienda(request):
    marca = request.GET.get("marca")
    if marca:
        productosListado = Producto.objects.filter(marca__icontains=marca)
    else:
        productosListado = Producto.objects.all()
    return render(request, "tienda.html", {"productos": productosListado})


def compra(request, codigo):
    productoSpecific = Producto.objects.get(codigo=codigo)
    return render(request, "compra.html", {"producto": productoSpecific})

def customer_service_success(request):
    return render(request, "customer_service_success.html")

def customer_service(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        message = request.POST["message"]

        full_message = (
            f"Nombre: {name}\nCorreo Electrónico: {email}\n\nMensaje:\n{message}"
        )

        email_message = EmailMessage(
            subject="Consulta de Servicio al Cliente",
            body=full_message,
            from_email=settings.EMAIL_HOST_USER,
            to=["jul.contreraso@duocuc.cl"],
        )
        email_message.content_subtype = "plain"
        email_message.encoding = "utf-8"

        email_message.send(fail_silently=False)

        return redirect("customer_service_success")

    return render(request, "customer_service.html")

