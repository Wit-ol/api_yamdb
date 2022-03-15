from rest_framework.exceptions import APIException


class Unauthorized(APIException):
    status_code = 401
    default_detail = 'Необходим JWT-токен'


class Forbidden(APIException):
    status_code = 403
    default_detail = ('Только автор, админ или модератор '
                      'могут изменять или удалять отзывы и комментарии')


class MaxOneReview(APIException):
    status_code = 400
    default_detail = 'Вы уже оставили отзыв на это произведение'
