from rest_framework.decorators import api_view

from score_loader.load import download_pdf
from io import BytesIO


from django.http import HttpResponse

from django.shortcuts import render


@api_view(['POST'])
def return_pdf(request):
    url = request.data['url']
    buff = BytesIO()
    download_pdf(url, buff)
    buff.seek(0)
    response = HttpResponse(buff.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="score.pdf"'
    return response


def index(request):

    return render(request, 'scores/index.html', {})
