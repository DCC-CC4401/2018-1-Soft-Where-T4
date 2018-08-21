from django.shortcuts import render, redirect
from django.utils.timezone import localtime
import datetime
from spacesApp.models import Space
from reservationsApp.models import Reservation

import random, os
import pytz
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from spacesApp.forms import SpaceForm


@login_required
def space_data(request, space_id, date=None):
    try:
        espacio = Space.objects.get(id=space_id)

        last_reservations = Reservation.objects.filter(space=espacio,
                                                       ending_date_time__lt=datetime.datetime.now(tz=pytz.utc)
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

        if date:
            current_date = date
            current_week = datetime.datetime.strptime(current_date, "%Y-%m-%d").date().isocalendar()[1]
        else:
            try:
                current_week = datetime.datetime.strptime(request.GET["date"], "%Y-%m-%d").date().isocalendar()[1]
                current_date = request.GET["date"]
            except:
                current_week = datetime.date.today().isocalendar()[1]
                current_date = datetime.date.today().strftime("%Y-%m-%d")

        reservations = Reservation.objects.filter(starting_date_time__week=current_week, state__in=['P', 'A'],
                                                  space=espacio)
        colores = {'A': 'rgba(0,153,0,0.7)',
                   'P': 'rgba(51,51,204,0.7)'}

        res_list = []
        for i in range(5):
            res_list.append(list())
        for r in reservations:
            reserv = list()
            reserv.append(r.space.name)
            reserv.append(localtime(r.starting_date_time).strftime("%H:%M"))
            reserv.append(localtime(r.ending_date_time).strftime("%H:%M"))
            reserv.append(colores[r.state])
            res_list[r.starting_date_time.isocalendar()[2] - 1].append(reserv)

        move_controls = list()
        move_controls.append(
            (datetime.datetime.strptime(current_date, "%Y-%m-%d") + datetime.timedelta(weeks=-4)).strftime("%Y-%m-%d"))
        move_controls.append(
            (datetime.datetime.strptime(current_date, "%Y-%m-%d") + datetime.timedelta(weeks=-1)).strftime("%Y-%m-%d"))
        move_controls.append(
            (datetime.datetime.strptime(current_date, "%Y-%m-%d") + datetime.timedelta(weeks=1)).strftime("%Y-%m-%d"))
        move_controls.append(
            (datetime.datetime.strptime(current_date, "%Y-%m-%d") + datetime.timedelta(weeks=4)).strftime("%Y-%m-%d"))

        delta = (datetime.datetime.strptime(current_date, "%Y-%m-%d").isocalendar()[2]) - 1
        monday = ((datetime.datetime.strptime(current_date, "%Y-%m-%d") - datetime.timedelta(days=delta)).strftime(
            "%d/%m/%Y"))
        context = {'reservations': res_list,
                   'current_date': current_date,
                   'controls': move_controls,
                   'actual_monday': monday,
                   'espacio': espacio,
                   'last_reservations': reservation_list
                   }

        return render(request, 'space_data.html', context)
    except Exception as e:
        print(e)
        return redirect('/')


def verificar_horario_habil(horario):
    if horario.isocalendar()[2] > 5:
        return False
    if horario.hour < 9 or horario.hour > 18:
        return False

    return True


@login_required
def space_request(request):
    if request.method == 'POST':
        space = Space.objects.get(id=request.POST['space_id'])

        if request.user.enabled:
            try:
                string_inicio = request.POST['fecha_inicio'] + " " + request.POST['hora_inicio']
                start_date_time = datetime.strptime(string_inicio, '%Y-%m-%d %H:%M')
                string_fin = request.POST['fecha_fin'] + " " + request.POST['hora_fin']
                end_date_time = datetime.strptime(string_fin, '%Y-%m-%d %H:%M')

                if start_date_time > end_date_time:
                    messages.warning(request, 'La reserva debe terminar después de iniciar.')
                elif start_date_time < datetime.datetime.now() + datetime.timedelta(hours=1):
                    messages.warning(request, 'Los pedidos deben ser hechos al menos con una hora de anticipación.')
                elif start_date_time.date() != end_date_time.date():
                    messages.warning(request, 'Los pedidos deben ser devueltos el mismo día que se entregan.')
                elif not verificar_horario_habil(start_date_time) and not verificar_horario_habil(end_date_time):
                    messages.warning(request, 'Los pedidos deben ser hechos en horario hábil.')
                else:
                    reservation = Reservation(space=space, starting_date_time=start_date_time,
                                              ending_date_time=end_date_time,
                                              user=request.user)
                    reservation.save()
                    messages.success(request, 'Pedido realizado con éxito')
            except Exception as e:
                messages.warning(request, 'Ingrese una fecha y hora válida.')
        else:
            messages.warning(request, 'Usuario no habilitado para pedir préstamos')

        return redirect('/space/' + str(space.id))


@login_required
def space_data_admin(request, space_id, date=None):
    if not request.user.is_staff:
        return redirect('/')
    else:
        try:

            if date:
                current_date = date
                current_week = datetime.datetime.strptime(current_date, "%Y-%m-%d").date().isocalendar()[1]
            else:
                try:
                    current_week = datetime.datetime.strptime(request.GET["date"], "%Y-%m-%d").date().isocalendar()[1]
                    current_date = request.GET["date"]
                except:
                    current_week = datetime.date.today().isocalendar()[1]
                    current_date = datetime.date.today().strftime("%Y-%m-%d")

            espacio = Space.objects.get(id=space_id)
            reservations = Reservation.objects.filter(starting_date_time__week=current_week, state__in=['P', 'A'],
                                                      space=espacio)
            colores = {'A': 'rgba(0,153,0,0.7)',
                       'P': 'rgba(51,51,204,0.7)'}

            res_list = []
            for i in range(5):
                res_list.append(list())
            for r in reservations:
                reserv = list()
                reserv.append(r.space.name)
                reserv.append(localtime(r.starting_date_time).strftime("%H:%M"))
                reserv.append(localtime(r.ending_date_time).strftime("%H:%M"))
                reserv.append(colores[r.state])
                res_list[r.starting_date_time.isocalendar()[2] - 1].append(reserv)

            move_controls = list()
            move_controls.append(
                (datetime.datetime.strptime(current_date, "%Y-%m-%d") + datetime.timedelta(weeks=-4)).strftime(
                    "%Y-%m-%d"))
            move_controls.append(
                (datetime.datetime.strptime(current_date, "%Y-%m-%d") + datetime.timedelta(weeks=-1)).strftime(
                    "%Y-%m-%d"))
            move_controls.append(
                (datetime.datetime.strptime(current_date, "%Y-%m-%d") + datetime.timedelta(weeks=1)).strftime(
                    "%Y-%m-%d"))
            move_controls.append(
                (datetime.datetime.strptime(current_date, "%Y-%m-%d") + datetime.timedelta(weeks=4)).strftime(
                    "%Y-%m-%d"))

            delta = (datetime.datetime.strptime(current_date, "%Y-%m-%d").isocalendar()[2]) - 1
            monday = ((datetime.datetime.strptime(current_date, "%Y-%m-%d") - datetime.timedelta(days=delta)).strftime(
                "%d/%m/%Y"))

            space = Space.objects.get(id=space_id)
            context = {
                'reservations': res_list,
                'current_date': current_date,
                'controls': move_controls,
                'actual_monday': monday,
                'space': space
            }
            return render(request, 'space_data_admin.html', context)
        except:
            return redirect('/')


@login_required
def space_edit_name(request, space_id):
    if request.method == "POST":
        s = Space.objects.get(id=space_id)
        s.name = request.POST["name"]
        s.save()
    return redirect('/space/' + str(space_id) + '/edit')


@login_required
def space_edit_image(request, space_id):
    if request.method == "POST":
        u_file = request.FILES["image"]
        extension = os.path.splitext(u_file.name)[1]
        s = Space.objects.get(id=space_id)
        s.image.save(str(space_id) + "_image" + extension, u_file)
        s.save()

    return redirect('/space/' + str(space_id) + '/edit')


@login_required
def space_edit_description(request, space_id):
    if request.method == "POST":
        s = Space.objects.get(id=space_id)
        s.description = request.POST["description"]
        s.save()

    return redirect('/space/' + str(space_id) + '/edit')


@login_required
def space_creation(request):
    if request.method == "POST":
        form = SpaceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/admin/items-panel/')
    else:
        form = SpaceForm()
        return render(request, "space_create.html", {'form': form})


@login_required
def space_delete(request, space_id):
    if not request.user.is_staff:
        return redirect('/')
    else:
        try:
            space = Space.objects.get(id=space_id)
            space.delete()
            return redirect('/admin/items-panel/')
        except:
            return redirect('/')
