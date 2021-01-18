from django.urls import path
from .views import (
    BookingsListView,
    BookingsCreateView,
    BookingsConfirmView,
    BookingsDetailView,
    BookingsUpdateView,
    BookingsDeleteView,
)


urlpatterns = [
    path(
        '',
        BookingsListView.as_view(),
        name='home',
    ),

    path(
        'create',
        BookingsCreateView.as_view(),
        name='bookings-create',
    ),

    path(
        'confirm',
        BookingsConfirmView.as_view(),
        name='bookings-confirm',
    ),

    path(
        '/<int:pk>',
        BookingsDetailView.as_view(),
        name='bookings-detail',
    ),

    path(
        '/<int:pk>/update',
        BookingsUpdateView.as_view(),
        name='bookings-update',
    ),

    path(
        '/<int:pk>/delete',
        BookingsDeleteView.as_view(),
        name='bookings-delete',
    ),

]
