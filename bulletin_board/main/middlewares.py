import re


class MyMiddleware:
    """This class implements switch to mobile version if user-agent is appropriate"""
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_template_response(self, request, response):
        user_agent = request.META['HTTP_USER_AGENT']
        if re.search(r'(iPhone|iPad|iPod|Android|Mobile)', user_agent):
            response.context_data['mobile_view'] = True
        return response