"""
URL configuration for litreview project.

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
import authentication.views
import www.views
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentication.views.login_page, name='login'),
    path('login/', authentication.views.login_page, name='login'),
    path('favicon.ico/', RedirectView.as_view(url='static/images/favicon.ico')),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('home/', www.views.home, name='home'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('ticket/', www.views.new_ticket, name='new_ticket'),
    path('ticket/<int:ticket_id>/', www.views.ticket_detail, name='ticket_detail'),
    path('flux/', www.views.flux, name='flux'),
    path('review/', www.views.review, name='review'),
    path('review/<int:review_id>/', www.views.review_detail, name='review_detail'),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
