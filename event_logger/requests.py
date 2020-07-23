
class RequestExtractor:
    """This class extracts a typical Django request object and prepare them for a nice LogRecord message.
       We will get 'actor_id' from request.user attribute. 'log_detail' depends on the request method
       (Check constract_log_detail() method for details). 'targeted_instance_id' can be retrived from
       the url. 'event_path' can be retrived from request.path_info"""

    def extract_actor_id(self, request):
        """Extracting the user primary key value from the request object"""
        if hasattr(request, 'user'):
            if hasattr(request.user, 'is_authenticated'):
                if request.user.is_authenticated:
                    return str(request.user.pk)
                else:
                    return '2'
            else:
                return '0'
        else:
            return '0'

    def constract_log_detail(self, request):
        """Constructing the log_detail message. If the request.method is GET then it is a READ operation.
           If request.method is POST then it is a WRITE operation"""
        prefix_word = 'operation'
        if hasattr(request, 'method'):
            if request.method == 'GET':
                return 'read %s' % prefix_word
            elif request.method == 'POST':
                return 'write %s' % prefix_word
            elif request.method == 'PUT':
                return 'update %s' % prefix_word
            elif request.method == 'PATCH':
                return 'patch %s' % prefix_word
            else:
                return 'unknown %s' % prefix_word
        else:
            return 'suspicious %s' % prefix_word
