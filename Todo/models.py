
from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    title=models.CharField(max_length=200)
    created_date=models.DateTimeField(auto_now_add=True,blank=True)
    user_object=models.ForeignKey(User,on_delete=models.CASCADE)

    options=(
         ("completed","completed"),
         ("inprogress","inprogress"),
         ("pending","pending")
    )
    status=models.CharField(max_length=200,choices=options,default="pending")

    def _str_(self):
        return self.title
    

    

