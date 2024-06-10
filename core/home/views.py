from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def index(request):
    courses = {
        'course_name': 'Python',
        'learn': ['flask', 'django', 'FastApi'],
        'course_provider': 'Udemy'
    }
    return Response(courses)
