from django.http import HttpResponse


def index(request):
    return HttpResponse("""Conference Room Booking helps to manage the booking\
    of all conference room in an organization.""")
