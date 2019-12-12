from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from consulting.decorators import login_required, data_required
from consulting.models.default import Query
from base import models_to_dict


@login_required
@data_required(['id', 'name', 'description', 'query'], 'POST')
def edit_query(request):
    query_name = request.POST['name']
    query_description = request.POST['description']
    query_sql = request.POST['query']

    if query_name == '':
        return HttpResponseBadRequest('Name is required.', 'application/json')

    query = Query.objects.get(id=request.POST['id'])
    query.name = query_name
    query.description = query_description
    query.query['query'] = query_sql
    query.save()

    queries = Query.objects.all()

    return JsonResponse({'queries': models_to_dict(queries), 'id': request.POST['id']}, safe=False)


@login_required
@data_required(['id'], 'POST')
def delete_query(request):
    query_id = request.POST['id']
    query = Query.objects.get(id=query_id)

    query.delete()

    queries = Query.objects.all()

    return JsonResponse({'queries': models_to_dict(queries)}, safe=False)
