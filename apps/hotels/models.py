from django.db import models
from djmoney.money import Money
from djmoney.models.fields import MoneyField
from django.utils.translation import gettext_lazy as _


class TipoHabitacion(models.Model):
    """[Model]: Modelo habilitado para registrar los tipos de habitacion que estaran disponibles\
        en las reservas.
    """
    nombre = models.CharField(
        _('Nombre o categoria'),
        max_length=50,
    )

    alias = models.CharField(
        _('Alias'),
        null=True,
        blank=True,
        max_length=20,
    )

    descripcion_corta = models.CharField(
        _('Breve descripcion'),
        max_length=50,
    )

    huespedes_permitidos = models.IntegerField(
        _('Huespedes permitidos'),
        blank=True,
        null=True,
    )

    precio = MoneyField(
        _('Precio de reserva'),
        max_digits=10,
        decimal_places=2,
        default_currency='EUR',
        default=Money(0, 'EUR'),
    )

    status = models.BooleanField(
        _('Status'),
        default=True
    )

    def __str__(self):
        return f'{self.nombre}-{self.alias}'

    class Meta:
        verbose_name = _("tipo de habitacion")
        verbose_name_plural = _("tipo de habitaciones")


class Habitaciones(models.Model):
    """[Model]: Modelo habilitado para definir las habitaciones y relacionarlas con su tipo de habitacion.
    """
    tipo_habitacion = models.ForeignKey(
        TipoHabitacion,
        on_delete=models.CASCADE,
        verbose_name=_("Tipo de habitacion"),
        blank=True,
        null=True,
    )

    nombre = models.CharField(
        _('Nombre de la habitacion'),
        max_length=20,
        blank=True,
        null=True,
    )

    descripcion_corta = models.CharField(
        _('Breve descripcion'),
        max_length=50,
    )

    descripcion = models.TextField(
        _('Descripcion'),
        blank=True,
        null=True,
    )

    estatus_habitacion = models.CharField(
        _('Estatus actual de la habitacion'),
        max_length=20,
        choices=(
            ('disponible', _('Disponible')),
            ('reservada', _('Reservada')),
            ('ocupada', _('Ocupada')),
            ('mantenimiento', _('En mantenimiento')),
        ),
        default='disponible',
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.nombre}-{self.descripcion_corta}'

    class Meta:
        verbose_name = _("habitacion")
        verbose_name_plural = _("habitaciones")
