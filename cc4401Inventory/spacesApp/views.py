from django.shortcuts import render, redirect
from spacesApp.models import Space
from reservationsApp.models import Reservation

from datetime import datetime, timedelta

import random, os
import pytz
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def space_data(request, space_id):
    try:
        espacio = Space.objects.get(id=space_id)

        last_reservations = Reservation.objects.filter(space=espacio,
                                                       ending_date_time__lt=datetime.now(tz=pytz.utc)
                                                       ).order_by('-ending_date_time')[:10]

        reservation_list = list()
        for reservation in last_reservations:

            starting_day = reservation.starting_date_time.strftime("%d-%m-%Y")
            ending_day = reservation.ending_date_time.strftime("%d-%m-%Y")
            starting_hour = reservation.starting_date_time.strftime("%H:%M")
            ending_hour = reservation.ending_date_time.strftime("%H:%M")

            if starting_day == ending_day:
                reservation_list.append(starting_day + " " + starting_hour + " a " + ending_hour)
            else:
                reservation_list.append(starting_day + ", " + starting_hour + " a " + ending_day + ", " + ending_hour)

        context = {
            'espacio': espacio,
            'last_reservations': reservation_list
        }

        return render(request, 'space_data.html', context)
    except Exception as e:
        print(e)
        return redirect('/')
