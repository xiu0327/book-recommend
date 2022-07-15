from flask import request
from flask_restx import Resource, Api, Namespace, fields
from func import print_json, userLoanlist

List = Namespace('List', description="각종 목록을 가져오기 위한 API (ex: 도서관 목록, 키워드, 사용자 대출 목록 등)")

@List.route('/lib')
class ListGet(Resource):
    def get(self):
        """전국 도서관 목록을 가져오는 API"""
        path = "/home/ubuntu/data/libraryList.json"
        return print_json.get_data(path)

@List.route('/keyword')
class ListGet(Resource):
    def get(self):
        """사용자 블로그에서 추출한 키워드 목록 가져오는 API"""
        path = "/home/ubuntu/data/keyword_test.json"
        return print_json.get_data(path)

@List.route('/user', methods=['POST'])
class ListPost(Resource):
    user_fields = List.model('List', {  # Model 객체 생성
    'id': fields.String(description='id', required=True, example="아이디 입력"),
    'pw': fields.String(description='pw', required=True, example="비밀번호 입력")
})
    @List.expect(user_fields)
    def post(self):
        """사용자 대출목록을 가져오는 API"""
        params = request.get_json()
        uid = params["id"]
        upw = params["pw"]
        return userLoanlist.get_data(uid, upw)


