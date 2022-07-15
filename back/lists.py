from flask import request
from flask_restx import Resource, Api, Namespace
from func import print_json, userLoanlist

List = Namespace('List', description="각종 목록을 가져오기 위한 API (ex: 도서관 목록, 키워드, 사용자 대출 목록 등)")

@List.route('/<string:name>')
class ListGet(Resource):
    def get(self, name):
        if name == "lib": path = "/home/ubuntu/data/libraryList.json"
        elif name == "keyword": path = "/home/ubuntu/data/keyword_test.json"
        return print_json.get_data(path)

@List.route('/user-list', methods=['POST'])
class ListPost(Resource):
    user_fields = Todo.model('List', {  # Model 객체 생성
    'id': fields.String(description='id', required=True, example="aaa"),
    'pw': fields.String(description='pw', required=True, example="bbb")
})
    @List.expect(user_fields)
    def post(self):
        params = request.get_json()
        uid = params["id"]
        upw = params["pw"]
        return userLoanlist.get_data(id, pw)


