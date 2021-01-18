from django.contrib import admin
#from django.contrib import messages
#from django.utils.translation import gettext_lazy as _
from apps.bookings.models import Reservas, Reservantes
from jet.admin import CompactInline


class ReservanteInline(CompactInline):
    """[Django inline]: Para incluir a multiples reservantes a una determinada reserva.
    """
    model = Reservantes
    extra = 1

@admin.register(Reservas)
class ReservasAdmin(admin.ModelAdmin):
    """[ModelAdmin]: Creado para administrar las reservas del sitio.
        -Permite busquedas, por los campos definidos en ´´´list_display´´´
        -Permite filtrar la lista, por los campos definidos en ´´´list_filter´´´
        -Permite busquedas dentro de la lista, basadas en los campos definidos en ´´´search_fields´´´
        -Permite las acciones de cambiar el estatus de los tipos seleccionados (activo/inactivo).
    """
    inlines = [
            ReservanteInline,
    ]

    list_display = (
        'localizador',
        'fecha_entrada',
        'fecha_salida',
        'cantidad_dias',
        'precio_reserva',
        'status',
    )

    list_filter = (
        'status',
    )

    search_fields = (
        'localizador',
        )

    exclude = [
        'reservantes',
    ]

    #actions = [activar_tipo, desactivar_tipo]
