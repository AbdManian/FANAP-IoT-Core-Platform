# Setup Application in Flask rest framework

from flask_restful import Resource
from app.validation import check_jsonbody
from .impl import user_list, user_add

class Access_User_List(Resource):
    def get(self):
        return user_list()
    

class Access_User_Add(Resource):
    @check_jsonbody
    def put(self, data):
        return user_add(data)


def connect(rest_api, endpoint):
    rest_api.add_resource(Access_User_List, endpoint)
    rest_api.add_resource(Access_User_Add, endpoint + '/add')
    