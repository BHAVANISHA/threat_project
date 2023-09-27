"""
URL configuration for thread_pro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from thread_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('threadpool/',views.Thread_pool.as_view()),
path('multiprocess/',views.Multiprocess.as_view()),
path('httpx/', views.Httpx.as_view( {'get': 'list'} ), name='async-api-call' ),
path('aiohttp/', views.AIO.as_view(), name='async_api_call'),
path('asyncio/',views.Asyncio.as_view()),
path('app/',views.FetchDataView.as_view())

]
