from django.shortcuts import render
from django.views import View


class Pages(View):
    async def get(self, request):
        return render(request, 'pages/index.html')
