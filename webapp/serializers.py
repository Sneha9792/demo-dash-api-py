from rest_framework import serializers
from .models import new_table

class new_tableSerializer(serializers.ModelSerializer):
    class Meta:
        model=new_table
        #fields=('first_name','last_name')
        fields='idnew_table'
