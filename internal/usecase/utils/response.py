from internal.usecase.utils import ResponseExample, ResponseSchema

HTTP_404_NOT_FOUND = ResponseSchema(
    status_code=404,
    description='Not found',
    example=ResponseExample(successful=False, detail='Not found'),
)
HTTP_401_NOT_AUTHORIZED = ResponseSchema(
    status_code=401,
    description='Invalid credentials',
    example=ResponseExample(successful=False, detail='Invalid credentials')
)
HTTP_403_FORBIDDEN = ResponseSchema(
    status_code=403,
    description='Access denied',
    example=ResponseExample(successful=False, detail='Access denied'),
)
