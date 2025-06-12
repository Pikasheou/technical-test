from django.urls import path

from . import views

urlpatterns = [
    path("import", views.import_data, name="import"),
    path("overall_stats", views.overall_stats, name="overall_stats"),
    path("query_stats", views.query_stats, name="query_stats"),
    path("add_url", views.add_url, name="add_url")
]