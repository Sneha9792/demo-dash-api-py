import json

import pandas as pd
# from flask import Flask, render_template,request
import plotly
import plotly.express as px
from rest_framework.response import Response
from rest_framework.views import APIView


# class employeeList(APIView):
#     def get(self, request):
#         emp = employees.object.all()  # fetch all the data from model
#         serializer = employeesSerializer(emp, many=True)
#         return Response(serializer.data)
#
#     def post(self):
#         pass


class GetCountUtility(APIView):
    def get_data(self):
        data = pd.read_excel('JanmotsavVariBooking.xlsx')
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
        fig = px.pie(top10_StateCount, values='count', names='StateName')
        return fig

    def plot_graph_Taluka_Wise(self, state_name, district):
        obj = GetCountUtility()
        df2 = obj.Taluka_Count(state_name, district)
        fig = px.bar(data_frame=df2, x='Taluka_Name', y='Talukacount', color="Taluka_Name")
        return fig





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
        fig = obj.Pie_Chart()
        #fig = px.pie(self.top10_StateCount, count='pop', names='Statename')
        graphJSON1 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return Response(graphJSON1)

    def post(self):
        pass


class TalukaWiseCount(APIView):
    def post(self,request):
        data = json.loads(request.body)
        # print(data, type(data))
        state_name = data['State']
        district = data['Distirct']
        obj = PlotStateCount()
        fig = obj.plot_graph_Taluka_Wise(state_name, district)
        #fig = px.pie(self.top10_StateCount, count='pop', names='Statename')
        graphJSON2 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return Response(graphJSON2)

    def get(self):
        pass







