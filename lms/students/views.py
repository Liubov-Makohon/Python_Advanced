from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from webargs import fields
from webargs.djangoparser import use_kwargs, use_args

from students.forms import StudentCreateForm
from students.models import Student
from students.utils import format_records
from django.core.exceptions import BadRequest
from webargs import djangoparser


def hello(request):
    return HttpResponse('SUCCESS')


parser = djangoparser.DjangoParser()


@parser.error_handler
def handle_error(error, req, schema, *, error_status_code, error_headers):
    raise BadRequest(error.messages)


@parser.use_args(
    {
        "first_name": fields.Str(
            required=False,
        ),
        "text": fields.Str(
            required=False
        ),
    },
    location="query",
)
def get_students(request, params):
    form = """
    <form >

      <label>First name:</label><br>
      <input type="text" name="first_name"><br>

      <label>Text:</label><br>
      <input type="text" name="text" placeholder="Enter text to search"><br><br>

      <input type="submit" value="Submit">
    </form>
    """

    students = Student.objects.all()

    text_fields = ['first_name', 'last_name', 'email']

    for param_name, param_value in params.items():
        if param_value:
            if param_name == 'text':
                or_filter = Q()
                for field in text_fields:
                    or_filter |= Q(**{f'{field}__contains': param_value})
                students = students.filter(or_filter)
            else:
                students = students.filter(**{param_name: param_value})

    result = format_records(students)

    response = form + result

    return HttpResponse(response)

@csrf_exempt
def create_student(request):
    # form = """
    # <form method="POST">
    #
    #   <label>First name:</label><br>
    #   <input type="text" name="first_name"><br>
    #
    #   <label>Last name:</label><br>
    #   <input type="text" name="last_name" placeholder="Enter last name"><br>
    #
    #   <label>Email:</label><br>
    #   <input type="text" name="email"><br><br>
    #
    #   <input type="submit" value="Submit">
    # </form>
    # """

    @csrf_exempt
    def create_student(request):

        if request.method == 'POST':
            # validation
            form = StudentCreateForm(request.POST)
            if form.is_valid():
                # st = Student(
                #     first_name=request.POST['first_name'],
                #     last_name=request.POST['last_name'],
                #     email=request.POST['email'],
                # )
                # st.save()
                form.save()

                return HttpResponseRedirect('/students')

        elif request.method == 'GET':
            form = StudentCreateForm()

        form_html = f"""
        <form method="POST">
          {form.as_p()}
          <input type="submit" value="Create">
        </form>
        """

        return HttpResponse(form_html)