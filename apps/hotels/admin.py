from django.contrib import admin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from apps.hotels.models import (
    TipoHabitacion,
    Habitaciones,
)


def habitacion_en_mantenimiento(modeladmin, request, queryset):
    """[Django action]: Para cambiar el estatus de una lista de habitaciones
        para que sean excluidas del sistema de reserva mientras estan en mantenimiento.
        esta accion excluiria a las habitaciones seleccionadas de todos los filtros de reserva.
    """
    try:
        queryset.update(estatus_habitacion='mantenimiento')
        messages.success(request, f'Se ha cambiado el estatus a {queryset.count()} habitaciones.')
    except Exception as e:
        messages.error(request, f'{e}')
habitacion_en_mantenimiento.short_description = _("Habitacion en mantenimiento")


def habitacion_habilitada(modeladmin, request, queryset):
    """[Django action]: Para habilitar una habitacion una vez finalizado su mantenimiento.
        Esta accion permite que las habitaciones seleccionadas puedan aparecer nuevamente en los filtros.
    """
    try:
        queryset.filter(estatus_habitacion='mantenimiento').update(estatus_habitacion='disponible')
        messages.warning(request, f'Recuerde que solo se podran habilitar habitaciones en mantenimiento.')
        messages.success(request, f'Las habitaciones en mantenimiento seleccionadas han sido habilitadas.')
    except Exception as e:
        messages.error(request, f'{e}')
habitacion_habilitada.short_description = _("Habilitar habitacion")


def cancelar_reserva(modeladmin, request, queryset):
    """[Django action]: Para cancelar una reserva.
        Esto habilita las habitaciones para ser incluidas en los filtros.
    """
    try:
        queryset.filter(estatus_habitacion='reservada').update(estatus_habitacion='disponible')
        messages.success(request, f'Las reservas seleccionadas han sido canceladas.')
    except Exception as e:
        messages.error(request, f'{e}')
cancelar_reserva.short_description = _("Cancelar reserva")


@admin.register(Habitaciones)
class HabitacionesAdmin(admin.ModelAdmin):
    """[ModelAdmin]: Codificado para la administracion de las habitaciones.
        -Permite busquedas, por los campos definidos en ´´´list_display´´´
        -Permite filtrar la lista, por los campos definidos en ´´´list_filter´´´
        -Permite busquedas dentro de la lista, basadas en los campos definidos en ´´´search_fields´´´
        -Permite las acciones de cambiar el estatus de las habitaciones o habilitarlas.
    """
    list_display = (
        'nombre',
        'descripcion_corta',
        'get_precio',
        'get_huespedes',
        'estatus_habitacion',
    )

    list_filter = (
        ('tipo_habitacion', admin.RelatedFieldListFilter),
        ('tipo_habitacion__precio'),
    )

    search_fields = (
        'nombre',
        'descripcion_corta',
        'estatus_habitacion',
    )

    list_select_related = ('tipo_habitacion',)

    def get_precio(self, obj):
        return obj.tipo_habitacion.precio
    get_precio.admin_order_field  = 'tipo_habitacion'
    get_precio.short_description = 'precio'

    def get_huespedes(self, obj):
        return obj.tipo_habitacion.huespedes_permitidos
    get_huespedes.admin_order_field  = 'tipo_habitacion'
    get_huespedes.short_description = 'Huespedes permitidos'

    actions = [
        habitacion_en_mantenimiento,
        habitacion_habilitada,
        cancelar_reserva,
    ]


def activar_tipo(modeladmin, request, queryset):
    """[Django action]: Permita activar el/los tipos de habitacion seleccionados.
    """
    try:
        queryset.update(status=True)
        messages.success(request, f'Se han activado los tipos seleccionados.')
    except Exception as e:
        messages.error(request, f'{e}')
activar_tipo.short_description = _("Activar tipo de habitacion")


def desactivar_tipo(modeladmin, request, queryset):
    """[Django action]: Permita desactivar el/los tipos de habitacion seleccionados.
    """
    try:
        queryset.update(status=False)
        messages.success(request, f'Se han activado los tipos seleccionados.')
    except Exception as e:
        messages.error(request, f'{e}')
desactivar_tipo.short_description = _("Desactivar tipo de habitacion")


@admin.register(TipoHabitacion)
class TipoHabitacionAdmin(admin.ModelAdmin):
    """[ModelAdmin]: Creado para administrar los tipos de habitacion disponibles.
        -Permite busquedas, por los campos definidos en ´´´list_display´´´
        -Permite filtrar la lista, por los campos definidos en ´´´list_filter´´´
        -Permite busquedas dentro de la lista, basadas en los campos definidos en ´´´search_fields´´´
        -Permite las acciones de cambiar el estatus de los tipos seleccionados (activo/inactivo).
    """
    list_display = (
        'alias',
        'nombre',
        'descripcion_corta',
        'huespedes_permitidos',
        'precio',
        'status',
    )

    list_filter = (
        'precio',
        'status',
    )

    search_fields = (
        'alias',
        'nombre',
        'descripcion_corta',
        )

    actions = [activar_tipo, desactivar_tipo]
