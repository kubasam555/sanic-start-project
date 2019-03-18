from playhouse.shortcuts import model_to_dict
from playhouse.shortcuts import update_model_from_dict
from sanic import Blueprint
from sanic.response import json
from sanic.views import HTTPMethodView

from core.models import Post
from core.utils import class_login_required

post_bp = Blueprint('post_app', url_prefix='/post')


class PostListView(HTTPMethodView):
    model = Post

    async def get(self, request):
        queryset = self.model.select()
        result = []
        for item in queryset:
            result.append(model_to_dict(item, exclude=[self.model.user.password]))
        return json(result)

    @class_login_required
    async def post(self, request):
        data = request.json or {}
        data['user_id'] = request['user'].id
        instance = self.model.create(
            **data
        )
        return json(model_to_dict(instance))


class PostDetailView(HTTPMethodView):
    model = Post

    def get_object(self, id):
        try:
            instance = self.model.get(self.model.id == id)
        except self.model.DoesNotExist:
            return json({'data': 'NotFound'}, status=404)
        return instance

    async def get(self, request, id):
        instance = self.get_object(id)
        return json(model_to_dict(instance))

    @class_login_required
    async def put(self, request, id):
        instance = self.get_object(id)
        update_model_from_dict(instance, request.json, ignore_unknown=True)
        instance.save()
        return json(model_to_dict(instance))


post_bp.add_route(PostListView.as_view(), '/')
post_bp.add_route(PostDetailView.as_view(), '/<id:number>')
