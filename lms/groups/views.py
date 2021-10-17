from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt


from groups.forms import GroupCreateForm
from groups.models import Group

from groups.utils import format_records
from django.core.exceptions import BadRequest
from webargs import djangoparser


parser = djangoparser.DjangoParser()


@parser.error_handler
def handle_error(error, req, schema, *, error_status_code, error_headers):
    raise BadRequest(error.messages)


def get_groups(request):
    groups = Group.objects.all().order_by("-id")
    result = format_records(groups)
    return HttpResponse(result)


@csrf_exempt
def create_group(request):

    if request.method == "POST":
        form = GroupCreateForm(request.POST)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse("groups:list"))

    elif request.method == "GET":
        form = GroupCreateForm()

    form_html = f"""
    <form method="POST">
      {form.as_p()}
      <input type="submit" value="Create">
    </form>
    """

    return HttpResponse(form_html)


@csrf_exempt
def update_group(request, pk):

    group = get_object_or_404(Group, id=pk)

    if request.method == "POST":
        form = GroupCreateForm(request.POST, instance=group)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse("groups:list"))

    elif request.method == "GET":
        form = GroupCreateForm(instance=group)

    form_html = f"""
       <form method="POST">
         {form.as_p()}
         <input type="submit" value="Save">
       </form>
       """

    return HttpResponse(form_html)
