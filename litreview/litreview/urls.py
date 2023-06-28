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
import www.templates.www.partials
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentication.views.login_page, name='login'),
    path('login/', authentication.views.login_page, name='login'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('post/', www.views.post, name='post'),
    path('flux/', www.views.flux, name='flux'),
    path('subscriptions/', authentication.views.subscriptions, name='subscriptions'),
    path('ticket/', www.views.new_ticket, name='new_ticket'),
    path('ticket/<int:ticket_id>/edit/', www.views.ticket_edit, name='ticket_edit'),
    path('ticket/<int:ticket_id>/delete/', www.views.ticket_delete, name='ticket_delete'),
    path('ticket/<int:ticket_id>/create_review/', www.views.ticket_create_review, name='ticket_create_review'),
    path('review/', www.views.new_review, name='new_review'),
    path('review/<int:review_id>/edit/', www.views.review_edit, name='review_edit'),
    path('review/<int:review_id>/delete/', www.views.review_delete, name='review_delete'),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
