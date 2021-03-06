from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from consulting.decorators import login_required, data_required
from consulting.settings import open_database_connection
from consulting.models.default import Query
from base import models_to_dict
import mysql.connector as mysql_connector


@login_required
@data_required(['database_name', 'tables'], 'BODY')
def get_table_columns(request):
    database_name = request.BODY['database_name']
    tables = request.BODY['tables']
    database = {}

    database_connection = open_database_connection()
    mysql = database_connection.cursor()
    mysql.execute("USE information_schema")
    for table in tables:
        table = str(table)
        database[table] = []
        mysql.execute("SELECT COLUMN_NAME FROM information_schema.columns WHERE TABLE_NAME='" + table + "' AND TABLE_SCHEMA='" + database_name + "'")

        results = mysql.fetchall()

        for result in results:
            database[table].append(result[0])

    mysql.close()
    database_connection.close()

    return JsonResponse({'tables': database, 'database_name': database_name}, safe=False)


@login_required
@data_required(['database_name', 'table_name', 'columns'], 'BODY')
def get_relationships(request):
    database_name = request.BODY['database_name']
    table_name = request.BODY['table_name']
    columns = request.BODY['columns']

    database_connection = open_database_connection()
    mysql = database_connection.cursor()
    mysql.execute("USE `information_schema`")
    mysql.execute("SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME "
                  "FROM KEY_COLUMN_USAGE "
                  "WHERE TABLE_SCHEMA = '" + database_name + "' AND REFERENCED_TABLE_SCHEMA IS NOT NULL AND REFERENCED_TABLE_NAME IS NOT NULL AND REFERENCED_COLUMN_NAME IS NOT NULL")

    results = mysql.fetchall()

    # Find all relationships
    tables = [table_name]
    relationship_map = []
    for current_table in tables:
        for result in results:
            orig_table_name = str(result[1])
            referenced_table = str(result[3])
            current_reference = orig_table_name + '.' + str(result[2]) + ' = ' + referenced_table + "." + str(result[4])

            if current_table == orig_table_name and referenced_table not in tables:
                tables.append(referenced_table)
                # JOIN receipt ON customer.id = receipt.customer_id
                relationship_map.append(current_reference)

            elif current_table == referenced_table and orig_table_name not in tables:
                tables.append(orig_table_name)
                relationship_map.append(current_reference)

    for result in results:
        orig_table_name = str(result[1])
        referenced_table = str(result[3])
        current_reference = orig_table_name + '.' + str(result[2]) + ' = ' + referenced_table + "." + str(result[4])

        if orig_table_name in tables and referenced_table in tables and current_reference not in relationship_map:
            relationship_map.append(current_reference)

    # GET SAMPLE DATA FOR EACH TABLE FIRST 3!
    # select top 100 colA, colB from myTable
    mysql.execute("USE `" + database_name + "`")

    sample_data = {}

    for table in tables:
        mysql.execute("SELECT * FROM " + table + " LIMIT 0, 3")

        table_columns = columns[table]
        results = mysql.fetchall()

        for result in results:
            dict_data = {}

            for i, data in enumerate(result):
                current_column = table_columns[i]
                dict_data[current_column] = data

            sample_data.setdefault(table, []).append(dict_data)

    mysql.close()
    database_connection.close()

    return JsonResponse({'relationship_map': relationship_map, 'table_name': table_name, 'sample_data': sample_data, 'columns': columns, 'database_name': database_name}, safe=False)


@login_required
@data_required(['database_name', 'query', 'table_name', 'relationship_map'], 'BODY')
def create_query(request):
    current_user = request.user
    database_name = request.BODY['database_name']
    table_name = request.BODY['table_name']
    query = request.BODY['query']
    relationship_map = request.BODY['relationship_map']
    relationship_counter = 0

    # Create SELECT statement
    select_statement = 'SELECT'
    join_statement = 'FROM ' + table_name + ' '

    columns = []

    for i, (table_key, table_value) in enumerate(query.items()):
        if table_key != table_name:
            join_statement += "LEFT JOIN " + table_key + " " + "ON " + relationship_map[relationship_counter] + " "
            relationship_counter += 1
        for t, (orig_value, new_value) in enumerate(table_value.items()):
            columns.append(new_value)
            select_statement += " " + table_key + "." + orig_value

            if orig_value != new_value:
                select_statement += " as " + "'" + new_value + "',"
            else:
                select_statement += ","

    # for i, relationship in enumerate(relationship_map):
    #     print relationship
    #     on_statement += relationship
    #
    #     if i != (len(relationship_map) - 1):
    #         on_statement += ' AND '

    # on_statement += relationship_map[0]

    # if on_statement == 'ON ':
    #     on_statement = ''

    # print select_statement
    # print join_statement
    # print on_statement

    sql_statement = select_statement[:-1] + ' ' + join_statement

    print sql_statement

    database_connection = open_database_connection()
    mysql = database_connection.cursor()
    mysql.execute("USE `" + database_name + "`")
    mysql.execute(sql_statement)
    results = mysql.fetchall()

    query_database = []
    for row in results:
        current_row = {}
        for i, column in enumerate(row):
            current_row[columns[i]] = column
        query_database.append(current_row)

    created_query = Query.objects.create(
        user=current_user,
        database=database_name,
        query={'query': sql_statement, 'columns': columns}
    )

    query_name = 'Query#' + str(created_query.id)
    created_query.name = query_name
    created_query.save()

    queries = Query.objects.all()

    mysql.close()
    database_connection.close()

    return JsonResponse({'columns': columns, 'results': query_database, 'name': query_name, 'id': created_query.id, 'queries': models_to_dict(queries)}, safe=False)


@login_required
@data_required(['database', 'columns', 'query'], 'BODY')
def custom_query(request):
    current_user = request.user
    database_name = request.BODY['database']
    columns = request.BODY['columns']
    sql_statement = request.BODY['query']
    query_database = []

    created_query = Query.objects.create(
        user=current_user,
        database=database_name,
        query={'query': sql_statement, 'columns': columns}
    )

    query_name = 'Query#' + str(created_query.id)
    created_query.name = query_name
    created_query.save()

    database_connection = open_database_connection()
    mysql = database_connection.cursor()
    mysql.execute("USE `" + created_query.database + "`")
    mysql.execute(created_query.query['query'].strip())

    results = mysql.fetchall()

    for row in results:
        current_row = {}
        for i, column in enumerate(row):
            current_row[columns[i]] = column

        query_database.append(current_row)

    queries = Query.objects.all()

    mysql.close()
    database_connection.close()

    return JsonResponse({'columns': columns, 'results': query_database, 'name': query_name, 'id': created_query.id, 'queries': models_to_dict(queries)}, safe=False)


@login_required
@data_required(['database', 'columns', 'query'], 'BODY')
def update_query(request):
    database_name = request.BODY['database']
    columns = request.BODY['columns']
    sql_statement = request.BODY['query']
    query_database = []
    results = {}

    try:
        database_connection = open_database_connection()
        mysql = database_connection.cursor()
        mysql.execute("USE `" + database_name + "`")
        mysql.execute(sql_statement.strip())
        results = mysql.fetchall()
        mysql.close()
        database_connection.close()
    except mysql_connector.Error as err:
        return HttpResponseBadRequest(err.msg, 'application/json')

    for row in results:
        current_row = {}
        for i, column in enumerate(row):
            current_row[columns[i]] = column

        query_database.append(current_row)

    return JsonResponse({'columns': columns, 'results': query_database}, safe=False)


@login_required
@data_required(['id'], 'GET')
def get_query(request):
    query_object = Query.objects.get(id=request.GET['id'])

    database_connection = open_database_connection()
    mysql = database_connection.cursor()
    mysql.execute("USE `" + query_object.database + "`")
    mysql.execute(query_object.query['query'].strip())

    results = mysql.fetchall()

    columns = query_object.query['columns']
    query_database = []

    for row in results:
        current_row = {}
        for i, column in enumerate(row):
            current_row[columns[i]] = column

        query_database.append(current_row)

    mysql.close()
    database_connection.close()

    return JsonResponse({'results': query_database, 'name': query_object.name, 'description': query_object.description, 'columns': columns, 'id': query_object.id}, safe=False)
