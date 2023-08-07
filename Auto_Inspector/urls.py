"""Auto_Inspector URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from login.views import verify_otp, login_request, logout_request
from django.urls import path
from cnn import report_generation
from inspection.views import initiate_inspection,post_to_s3,process_inspection


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', login_request, name='login'),
    path('verify_otp', verify_otp, name="verify_otp"),
    path('logout', logout_request, name='logout'),
    path('initiate-inspection',initiate_inspection,name='initiate-inspection'),
    path('api/image-upload', post_to_s3, name='image-upload'),
    path('process-inspection',process_inspection,name='process-inspection'),
    path('generate-pdf/', report_generation.PDFGeneratorView.as_view(), name='generate_pdf'),
]
