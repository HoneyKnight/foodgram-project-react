from rest_framework import mixins, viewsets


class ListRetrieveViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
):
    ...


class GetIsSubscribedMixin:
    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.follower.filter(author=obj.id).exists()


class AddAndDeleteObjectMixin:
    def add_object_method(self, request, pk, serializer_class, model):
        data = {
            'user': request.user.id,
            'recipe': pk,
        }
        serializer = serializer_class(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        return self.add_object(model, request.user, pk)

    def delete_object_method(self, request, pk, serializer_class, model):
        data = {
            'user': request.user.id,
            'recipe': pk,
        }
        serializer = serializer_class(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        return self.delete_object(model, request.user, pk)
