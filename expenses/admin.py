from django.contrib import admin
from .models import Expense  # ←ここがズレていないかチェック！

# 管理画面に登録
admin.site.register(Expense)