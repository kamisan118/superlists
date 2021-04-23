from django.db import models

# Create your models here.

class List(models.Model):
    text = models.TextField(default="")

class Item(models.Model):
    text = models.TextField(default="")

    # link 到其他的 model object
    # on_delete 代表的是當對應的類別被刪除(i.e., when a referenced value from the other table is deleted)之後，這些對應到別人的資料要怎麼被處理， CASCADE 就是一倂刪除
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
