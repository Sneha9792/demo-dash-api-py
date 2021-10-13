from django.db import models
class JanmoUtsavVari(models.Model):
    fullname = models.CharField(db_column='FullName', max_length=250 )  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=250)  # Field name made lowercase.
    statename = models.CharField(db_column='StateName', max_length=250)  # Field name made lowercase.
    districtname = models.CharField(db_column='DistrictName', max_length=250)  # Field name made lowercase.
    taluka_name = models.CharField(db_column='Taluka_Name', max_length=250)  # Field name made lowercase.
    invoiceno = models.CharField(db_column='InvoiceNo', max_length=250)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'janmo_utsav_vari'
    def __str__(self):
        return self.fullname + " " + self.username +""+ self.statename + " " + self.districtname + " " + self.taluka_name + " " + self.invoiceno    


class employees(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    emp_id = models.IntegerField()

    def __str__(self):
        return self.first_name

