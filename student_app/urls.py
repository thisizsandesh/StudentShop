from django.contrib import admin
from django.urls import path
from student_app import views
from .views import  register
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home',views.home),
    path('product_details/<pid>',views.product_details),
    path('register/', register, name='register'),
    path('user_login',views.user_login),
    path('user_logout',views.user_logout),
    path('addtocart/<pid>',views.addtocart),
    path('viewcart',views.viewcart),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('remove/<cid>',views.remove),
    path('range',views.range),
    path('catfilter',views.catfilter),
    path('placeorder',views.placeorder),
    path('makepayment',views.makepayment),
     
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
