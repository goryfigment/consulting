import time
import json
from django.shortcuts import render
from django.http import HttpResponseRedirect
from base import get_base_url, models_to_dict
# MODELS
from consulting.models.default import User as DefaultUser, Query
from consulting.settings import open_database_connection
from django.contrib.auth import logout


def error_page(request):
    data = {
        'base_url': get_base_url()
    }

    return render(request, '404.html', data)


def server_error(request):
    data = {
        'base_url': get_base_url()
    }

    return render(request, '500.html', data)


def home(request):
    data = {
        'base_url': get_base_url()
    }

    # If user is login redirect to overview
    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard/')

    return render(request, 'home.html', data)


def register(request):
    data = {
        'base_url': get_base_url()
    }

    # If user is login redirect to overview
    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard/')

    return render(request, 'register.html', data)


def login(request):
    data = {
        'base_url': get_base_url()
    }

    # If user is login redirect to overview
    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard/')

    return render(request, 'login.html', data)


def forgot_password(request):
    data = {
        'base_url': get_base_url(),
        'expired': False
    }

    if 'code' in request.GET:
        current_user = DefaultUser.objects.get(reset_link=request.GET['code'])

        if (int(round(time.time())) - current_user.reset_date) > 86400:
            data['expired'] = True

    # If user is login redirect to overview
    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard/')

    return render(request, 'forgot_password.html', data)


def dashboard(request):
    current_user = request.user

    # Only go to overview if user is logged in
    if not current_user.is_authenticated():
        return HttpResponseRedirect('/login/')

    user_name = ''
    try:
        user_name = current_user.first_name + ' ' + current_user.last_name
    except:
        logout(request)

    database = {}
    database_connection = open_database_connection()
    mysql = database_connection.cursor()
    mysql.execute("SHOW DATABASES")

    exclude_list = ['information_schema', 'performance_schema', 'sys', 'mysql', 'ktdemo$kt-database']

    # Make database list
    for database_name in mysql:
        database_name = database_name[0]
        if database_name not in exclude_list:
            database[str(database_name)] = {}

    # Get tables and columns
    for database_name in database:
        mysql.execute("USE `" + database_name + "`")
        mysql.execute("SHOW TABLES")

        columns = []

        for column in mysql:
            columns.append(str(column[0]))
            database[database_name] = columns

        database[database_name] = columns

    mysql.close()
    database_connection.close()

    # GET ALL QUERIES
    queries = Query.objects.all()

    data = {
        'base_url': get_base_url(),
        'username': current_user.username,
        'name': user_name,
        'database': database,
        'queries': json.dumps(models_to_dict(queries))
    }

    return render(request, 'dashboard.html', data)
