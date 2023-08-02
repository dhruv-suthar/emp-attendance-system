from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from ninja import NinjaAPI, Router
from employee.apis import views
from employee import urls
from employee.views import wish_birthday

api_v1 = Router()
ninja = NinjaAPI()



api_v1.add_router(prefix='/',router=views.router,tags=['User'])
ninja.add_router('/v1',api_v1)




urlpatterns = [
    path('admin/wish_birthday/<int:pk>/', wish_birthday, name='wish_birthday'),
    path('admin/', admin.site.urls),

   
    path('',include("employee.urls")),

    path("api/", ninja.urls),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


