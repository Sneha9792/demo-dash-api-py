import random
import json
import os
import pandas as pd
# from flask import Flask, render_template,request
import plotly
import plotly.express as px
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import new_table
# class employeeList(APIView):
#     def get(self, request):
#         emp = employees.object.all()  # fetch all the data from model
#         serializer = employeesSerializer(emp, many=True)
#         return Response(serializer.data)
#
#     def post(self):
#         pass

qs= new_table.objects.all()
print('data set',qs)
print('ok')

pddata = pd.DataFrame(qs)
print('dataf',pddata)
class GetCountUtility(APIView):
    def get_data(self):
        APP_ROOT = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(APP_ROOT, 'JanmotsavVariBooking.xlsx')
        data = pd.read_excel(file_path)
        return data

    def get_count(self):
        df = self.get_data()
        df_count = df.groupby('StateName').count().reset_index()
        df_count = df_count[['StateName', 'FullName']]
        df_count = df_count.rename(columns={'FullName': 'Count'})
        # d = {}
        # for row in df_count.iterrows():
        #     statename = row[1][0]
        #     count = row[1][1]
        # #     print(statename, count)
        #     d[statename] = count
        # # d_json = json.dumps(d)
        return df_count

    def get_top10_count(self):
        df = self.get_data()
        top10_StateCount=df.groupby(["StateName"]).size().reset_index(name="count")
        top10_StateCount = top10_StateCount.sort_values(by='count', ascending=False)
        top10_StateCount = top10_StateCount.head(10).reset_index(drop=True)
        #self.top10_StateCount=self.get_data()
       # df_get_top_10 = data.groupby(["StateName"]).size().reset_index(name="count")
        #top10_StateCount = self.df_count.sort_values(by='count', ascending=False)
        #top10_StateCount = top10_StateCount.head(10).reset_index(drop=True)
        return top10_StateCount

    def Taluka_Count(self, state_name, district):
        df=self.get_data()
        # state = input("Enter the StateName:")
        # district = input("Enter the DistrictName:")
        df1 = df.loc[(df["StateName"] == state_name) & (df["DistrictName"] == district)]
        df2 = df1.groupby(["Taluka_Name"]).size().reset_index(name="Talukacount")
        return df2


class PlotStateCount(APIView):
    def plot_graph(self):
        obj = GetCountUtility()
        df_count = obj.get_count()
        fig = px.bar(data_frame=df_count, x='StateName', y='Count', color="StateName")
        return fig
    def Pie_Chart(self):
        obj = GetCountUtility()
        top10_StateCount = obj.get_top10_count()
        # print(top10_StateCount)
        # fig = px.pie(top10_StateCount, values='count', names='StateName')
        return top10_StateCount

    def plot_graph_Taluka_Wise(self, state_name, district):
        obj = GetCountUtility()
        df2 = obj.Taluka_Count(state_name, district)
        # print(df2)
        #fig = px.bar(data_frame=df2, x='Taluka_Name', y='Talukacount', color="Taluka_Name")
        #return fig
        return df2


class GetUniqueStates(APIView):
    def get(self, request):
        obj = GetCountUtility()
        df = obj.get_data()
        # df = self.get_data()
        unique_states = list(df['StateName'].unique())
        res ={}
        for state in unique_states:
            df_state = df[df['StateName'] == state]
            res[state] = list(df_state['DistrictName'].unique())    
        # res['Districts'] = unique_districts
        # res = json.dumps(res)
        
        return Response(res)

    def post(self):
        pass

class StateCount(APIView):
    def get(self, request):
        obj = PlotStateCount()
        fig = obj.plot_graph()
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return Response(graphJSON)

    def post(self):
        pass


class top10StateCount(APIView):
    def get(self,request):
        obj = PlotStateCount()
        top_10_df = obj.Pie_Chart()
        labels = list(top_10_df['StateName'])
        data = list(top_10_df['count'])
        #fig = px.pie(self.top10_StateCount, count='pop', names='Statename')
        # graphJSON1 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        backgroundColor = ['#ffff00','#ff0000','#00ff00','#ffa500','#0000ff','#FFE4C4','#f3cfbb','#808080','#ffc0cb','#E6E6FA']
        new_dict = {}
        datasets={}
        datasets['data'] = data
        datasets['backgroundColor'] = backgroundColor
        new_dict['labels'] = labels
        new_dict['datasets'] = datasets
        
        # print(graphJSON1)
        # graphJSON1 = json.loads(graphJSON1)
        # new_dict['labels'] = graphJSON1['data'][0]['labels']
        # new_dict = json.dumps(new_dict)
        return Response(new_dict)

    def post(self):
        pass


class TalukaWiseCount(APIView):
    def post(self,request):
        data = json.loads(request.body)
        # print(data, type(data))
        state_name = data['State']
        district = data['District']
        obj = PlotStateCount()
        df2 = obj.plot_graph_Taluka_Wise(state_name, district)
        #fig = px.pie(self.top10_StateCount, count='pop', names='Statename')
        #graphJSON2 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        backgroundColor = ['#ffff00','#ff0000','#00ff00','#ffa500','#0000ff','#FFE4C4','#f3cfbb','#808080','#ffc0cb','#E6E6FA']
        labels = list(df2['Taluka_Name'])
        data = list(df2['Talukacount'])
        color_count = len(labels)
        taluka_colors = random.sample(backgroundColor, color_count)
        new_dict = {}
        datasets = {}
        datasets['data'] = data
        datasets['backgroundColor'] = taluka_colors
        new_dict['labels'] = labels
        new_dict['datasets'] = datasets
        # print(new_dict)
        # new_dict = json.dumps(new_dict)
        return Response(new_dict)

    def get(self):
        pass







