from django.contrib import admin
from django.apps import apps


# Register your models here.
# 自动注册所有model
models = apps.get_models()
for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
