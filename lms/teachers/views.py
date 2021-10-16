from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from webargs import fields
from students.utils import format_records
from django.core.exceptions import BadRequest
from webargs import djangoparser

from teachers.forms import TeacherCreateForm
from teachers.models import Teacher

parser = djangoparser.DjangoParser()


@parser.error_handler
def handle_error(error, req, schema, *, error_status_code, error_headers):
    raise BadRequest(error.messages)


@parser.use_args(
    {
        "first_name": fields.Str(
            required=False,
        ),
        "last_name": fields.Str(
            required=False,
        ),
        "speciality": fields.Str(
            required=False,
        ),
        "text": fields.Str(required=False),
    },
    location="query",
)
def get_teachers(request, params):
    teachers = Teacher.objects.all().order_by("-id")

    text_fields = ["first_name", "last_name", "speciality"]

    for param_name, param_value in params.items():
        if param_value:
            if param_name == "text":
                or_filter = Q()
                for field in text_fields:
                    or_filter |= Q(**{f"{field}__contains": param_value})
                teachers = teachers.filter(or_filter)
            else:
                teachers = teachers.filter(**{param_name: param_value})

    result = format_records(teachers)

    return HttpResponse(result)


@csrf_exempt
def create_teachers(request):

    if request.method == "POST":
        form = TeacherCreateForm(request.POST)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect("/teachers")

    elif request.method == "GET":
        form = TeacherCreateForm()

    form_html = f"""
    <form method="POST">
      {form.as_p()}
      <input type="submit" value="Create">
    </form>
    """

    return HttpResponse(form_html)
