from django.db.models import Q

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt
from webargs import fields

from students.forms import StudentCreateForm
from students.models import Student
from students.utils import format_records
from django.core.exceptions import BadRequest
from webargs import djangoparser


def hello(request):
    return HttpResponse("SUCCESS")


def index(request):
    return render(
        request=request,
        template_name="index.html",
    )


parser = djangoparser.DjangoParser()


@parser.error_handler
def handle_error(error, req, schema, *, error_status_code, error_headers):
    raise BadRequest(error.messages)


def handler404(request, exception):
    return render(request, "error_404.html")


@parser.use_args(
    {
        "first_name": fields.Str(
            required=False,
        ),
        "text": fields.Str(required=False),
    },
    location="query",
)
def get_students(request, params):
    students = Student.objects.all().order_by("-id")

    text_fields = ["first_name", "last_name", "email"]

    for param_name, param_value in params.items():
        if param_value:
            if param_name == "text":
                or_filter = Q()
                for field in text_fields:
                    or_filter |= Q(**{f"{field}__contains": param_value})
                students = students.filter(or_filter)
            else:
                students = students.filter(**{param_name: param_value})

    return render(
        request=request,
        template_name="students_table.html",
        context={"students_list": students},
    )


@csrf_exempt
def create_student(request):
    if request.method == "POST":
        form = StudentCreateForm(request.POST)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse("students:list"))

    elif request.method == "GET":
        form = StudentCreateForm()

    return render(
        request=request,
        template_name="students_create.html",
        context={
            "form": form,
        },
    )


@csrf_exempt
def update_student(request, pk):
    student = get_object_or_404(Student, id=pk)

    if request.method == "POST":
        form = StudentCreateForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("students:list"))

    elif request.method == "GET":
        form = StudentCreateForm(instance=student)

    return render(
        request=request, template_name="students_edit.html", context={"form": form}
    )


def delete_student(request, pk):
    student = get_object_or_404(Student, id=pk)
    student.delete()

    return HttpResponseRedirect(reverse("students:list"))


# def handler404(request, *args, **argv):
#     response = render_to_response('404.html', {},
#                                   context_instance=RequestContext(request))
#     response.status_code = 404
#     return response
