from django.shortcuts import render, HttpResponse
from django.views import View

from .services.hackerrank_api import fetch_new_data
from .services.filter import get_filtered_data
from .forms import FilterForm
from .models import IotDeviceData


class IndexView(View):
    template_name = "core/index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': FilterForm})

    def post(self, request, *args, **kwargs):
        fetch_new_data()
        data = IotDeviceData.objects.all()
        user_filter = FilterForm(request.POST)
        if user_filter.is_valid():
            try:
                if int(user_filter.cleaned_data['status']) > 0 or \
                        int(user_filter.cleaned_data['operating_param']) > 0:
                    data = get_filtered_data(user_filter.cleaned_data)
            except ValueError:
                return HttpResponse("Bad request", status=400)
        return render(request, self.template_name, {'data': data})

