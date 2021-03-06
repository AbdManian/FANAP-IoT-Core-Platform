# Setup Application in Flask rest framework

from flask_restful import Resource
from flask import request

from app.validation import json_validator, check_user_token, reqparam_validate
from .role_op import role_add, role_list
from .role_op import role_show, role_update, role_delete
from .role_grant import role_grant, role_grant_list
from .role_grant import role_take


class Role_Add_List(Resource):
    @json_validator('role_add')
    @check_user_token
    def post(self, user, data):
        return role_add(user, data, request.args)

    @check_user_token
    def get(self, user):
        params = reqparam_validate('role_list', request.args)
        return role_list(user, params)


class Role_Show_Update_Delete(Resource):

    @check_user_token
    def get(self, roleid, user):
        return role_show(user, roleid, request.args)

    @json_validator('role_update')
    @check_user_token
    def put(self, user, roleid, data):
        return role_update(user, data, roleid, request.args)

    @check_user_token
    def delete(self, roleid, user):
        return role_delete(user, roleid, request.args)


class Role_Grant_List(Resource):

    @json_validator('role_grant')
    @check_user_token
    def post(self, user, data):
        return role_grant(user, data, request.args)

    @check_user_token
    def get(self, user):
        params = reqparam_validate('rolegrant_list', request.args)
        return role_grant_list(user, params)


class Role_Grant_Take(Resource):

    @json_validator('role_grant')
    @check_user_token
    def post(self, user, data):
        return role_take(user, data, request.args)


def connect(rest_api, endpoint):
    rest_api.add_resource(Role_Add_List, endpoint)
    rest_api.add_resource(Role_Show_Update_Delete, endpoint + '/<roleid>')

    rest_api.add_resource(Role_Grant_List, endpoint + '/grant')
    rest_api.add_resource(Role_Grant_Take, endpoint + '/take')
