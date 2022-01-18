from rest_framework.response import Response


class OKResponse(Response):

    default_status = 200

    def __init__(self,
                 data=None,
                 status=None,
                 template_name=None,
                 headers=None,
                 exception=False,
                 content_type=None):
        if not isinstance(data, dict) or \
            not 'status' in data or \
                data['status'] != 'OK':
            data = {'status': 'OK', 'result': data}
        if status == None:
            status = self.default_status
        super().__init__(data, status, template_name, headers, exception,
                         content_type)
