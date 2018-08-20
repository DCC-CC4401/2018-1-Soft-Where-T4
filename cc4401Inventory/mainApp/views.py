from django.shortcuts import render, redirect
from django.utils.timezone import localtime
import datetime
from articlesApp.models import Article
from reservationsApp.models import Reservation
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required
def landing(request):
    if not (request.user.is_superuser and request.user.is_staff):
        return redirect('/articles/')
    return redirect('/admin/')


@login_required
def landing_articles(request):
    context = {}
    return render(request, 'articulos.html', context)


@login_required
def landing_spaces(request, date=None):
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

    reservations = Reservation.objects.filter(starting_date_time__week=current_week, state__in=['P', 'A'])
    colores = {'A': 'rgba(0,153,0,0.7)',
               'P': 'rgba(51,51,204,0.7)'}

    res_list = []
    for i in range(5):
        res_list.append(list())
    for r in reservations:
        reserv = []
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
    monday = (
        (datetime.datetime.strptime(current_date, "%Y-%m-%d") - datetime.timedelta(days=delta)).strftime("%d/%m/%Y"))
    context = {'reservations': res_list,
               'current_date': current_date,
               'controls': move_controls,
               'actual_monday': monday}
    return render(request, 'espacios.html', context)


@login_required
def landing_search(request, products):
    if not products:
        return landing_articles(request)
    else:
        context = {'productos': products,
                   'colores': {'D': '#009900',
                               'R': '#ffcc00',
                               'P': '#3333cc',
                               'L': '#cc0000'}
                   }
        return render(request, 'articulos.html', context)


@login_required
def search(request):
    if request.method == "GET":
        nombre = ""
        resultados = Article.objects.all()
        reservas = Reservation.objects.all()

        search_name = request.GET.get("query")
        if search_name:
            nombre = search_name
            resultados = resultados.filter(name__icontains=nombre.lower())

        search_status = request.GET.get("estado")
        if search_status and search_status != 'A':
            resultados = resultados.filter(state=search_status)

        search_date_st = request.GET.get("fechaInicio")
        search_date_fn = request.GET.get("fechaFin")
        search_time_st = request.GET.get("horaInicio")
        search_time_fn = request.GET.get("horaFin")

        if search_date_fn and search_date_st and search_time_fn and search_time_st:
            search_date_st = datetime.datetime.strptime(search_date_st+' '+search_time_st, "%Y-%m-%d %H:%M").date()
            search_date_fn = datetime.datetime.strptime(search_date_fn+' '+search_time_fn, "%Y-%m-%d %H:%M").date()
            #reservas = reservas.filter(Q(starting_date_time=search_date_st) | Q(ending_date_time=search_date_st)) TODO make el filtro

            for res in reservas:
                resultados = resultados.exclude(id=res.articulo.id)

    return landing_search(request, resultados)
