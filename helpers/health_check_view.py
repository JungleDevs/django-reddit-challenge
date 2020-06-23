"""
Health check view
"""
###
# Libraries
###

from django.http import HttpResponse


###
# View
###
def health_check(request):
    return HttpResponse("Health Check")
