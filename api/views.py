import json

from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from .models import DailySummaryPrice
from .services import VALID_RANGES


@api_view(['GET'])
def get_mms(request, pair):
    parameters = {
        'from': request.GET.get('from', 0),
        'to': request.GET.get('to', 0),
        'range': request.GET.get('range', 20)
    }

    from_date = parameters.get('from')
    to_date = parameters.get('to')
    range_for_mms = int(parameters.get('range'))

    print(parameters)

    if range_for_mms not in VALID_RANGES:
        # TODO: levantar exceção
        return JsonResponse(
            {'message': 'Range for mms must be 20, 50 or 200'},
            status=status.HTTP_403_FORBIDDEN
        )

    results = DailySummaryPrice.objects.filter(
        pair=pair,
        timestamp__gte=from_date,
        timestamp__lte=to_date,
    )

    responses = []
    
    for result in results:
        response = {'timestamp': result.timestamp}
        response['mms'] = eval(f'result.mms_{range_for_mms}')
        responses.append(response)


    return HttpResponse(json.dumps(responses))