import datetime
import string
import random

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .models import Reservas, Reservantes
from apps.hotels.models import Habitaciones

@method_decorator(login_required, name='dispatch')
class BookingsListView(ListView):
    model = Reservas
    template_name = 'bookings/list.html'
    context_object_name = 'bookings'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(BookingsListView, self).get_context_data(**kwargs)
        bookings = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(bookings, self.paginate_by)
        try:
            bookings = paginator.page(page)
        except PageNotAnInteger:
            bookings = paginator.page(1)
        except EmptyPage:
            bookings = paginator.page(paginator.num_pages)
        context['bookings'] = bookings
        return context


@method_decorator(login_required, name='dispatch')
class BookingsCreateView(View):
    model = Reservas
    template_name = 'bookings/create.html'
    post_template = 'bookings/disponibles.html'
    fields = "__all__"
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        #import ipdb;ipdb.set_trace()
        datos = request.POST.dict()

        #calcular dias de reserva
        entrada = datetime.datetime.strptime(datos['entrada'], '%M/%d/%Y').date()
        salida = datetime.datetime.strptime(datos['salida'], '%M/%d/%Y').date()
        dias_reserva = (salida - entrada).days

        #Filtrar hab reservadas en fecha.
        ids_hab_reservadas = Reservas.objects.filter(
            fecha_entrada__range=(entrada, salida),
            fecha_salida__range=(entrada, salida),
        ).values_list('habitacion__id', flat=True)

        #Obtener listado de habitaciones disponibles.
        hab_disponibles = Habitaciones.objects.filter(
            tipo_habitacion__huespedes_permitidos__gte=int(datos['huespedes']),
        ).exclude(pk__in=ids_hab_reservadas)

        c = {}
        c.update({
            'entrada': datos['entrada'],
            'salida': datos['salida'],
            'huespedes': datos['huespedes'],
            'hab_disponibles': hab_disponibles,
            'dias_reserva': dias_reserva,
        })

        return render(request, self.post_template, c)


@method_decorator(login_required, name='dispatch')
class BookingsConfirmView(View):
    model = Reservas
    template_name = 'bookings/disponibles.html'
    fields = "__all__"
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        #Obtener datos pertinentes de la reserva.
        datos = request.POST.dict()
        habitacion = Habitaciones.objects.get(pk=datos['idhab'])
        entrada = datetime.datetime.strptime(datos['entrada'], '%M/%d/%Y')
        salida = datetime.datetime.strptime(datos['salida'], '%M/%d/%Y')
        localizador = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 6))

        #Guardando la reserva.
        reserva = Reservas(
            localizador=localizador,
            cantidad_dias=datos['dias'],
            fecha_entrada=entrada,
            fecha_salida=salida,
            precio_reserva=(habitacion.tipo_habitacion.precio.amount * int(datos['dias'])),
            comentarios=datos['comentarios']
        )

        #agregar habitacion a reserva
        reserva.save()
        reserva.habitacion.add(habitacion)

        #Guardando informacion del reservante.
        reservante = Reservantes(
            reserva=reserva,
            nombre=datos['nombre'],
            apellido=datos['apellido'],
            documento_identidad=datos['dni'],
            telefono=datos['telefono'],
            email=datos['email'],
        )
        reservante.save()

        return redirect('home')




@method_decorator(login_required, name='dispatch')
class BookingsDetailView(DetailView):

    model = Reservas
    template_name = 'bookings/detail.html'
    context_object_name = 'bookings'


@method_decorator(login_required, name='dispatch')
class BookingsUpdateView(UpdateView):

    model = Reservas
    template_name = 'bookings/update.html'
    context_object_name = 'bookings'
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy('bookings-detail', kwargs={'pk': self.object.id})


@method_decorator(login_required, name='dispatch')
class BookingsDeleteView(DeleteView):
    model = Reservas
    template_name = 'bookings/delete.html'
    success_url = reverse_lazy('home')
