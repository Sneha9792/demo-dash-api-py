from django.db import models

class new_table(models.Model):
    idnew_table = models.Field()
    
    #class Meta:
     #   db_table = 'new_table'
    def __str__(self):
        return str(self.idnew_table)
''''
class employees(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    emp_id = models.IntegerField()

    def __str__(self):
        return self.first_name
'''
