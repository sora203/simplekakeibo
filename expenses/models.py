from django.db import models
from django.utils import timezone

# expenses/models.py

class Expense(models.Model):
    # 既存の選択肢
    BALANCE_TYPES = [('out', '支出'), ('in', '収入')]
    CATEGORY_CHOICES = [
        ('shokuhi', '食費'), ('nichiyou', '日用品'), 
        ('koutsu', '交通費'), ('kounetsu', '光熱費'),
        ('goraku', '娯楽・趣味'), ('kyuryo', '給料'), ('sonota', 'その他'),
    ]

    # ★追加：支払い方法の選択肢
    PAYMENT_METHODS = [
        ('cash', '現金'),
        ('card', 'クレジットカード'),
        ('debit', 'デビットカード'),
        ('qr', 'QR決済'),
        ('none', 'なし（収入など）'),
    ]

    date = models.DateField('日付', default=timezone.now)
    title = models.CharField('内容', max_length=100)
    amount = models.PositiveIntegerField('金額')
    category = models.CharField('カテゴリ', max_length=20, choices=CATEGORY_CHOICES, default='shokuhi')
    balance_type = models.CharField('収支タイプ', max_length=3, choices=BALANCE_TYPES, default='out')

    # ★追加：支払い方法フィールド
    payment_method = models.CharField(
        '支払い方法',
        max_length=10,
        choices=PAYMENT_METHODS,
        default='cash'
    )

    def __str__(self):
        return f"{self.date} {self.title}"