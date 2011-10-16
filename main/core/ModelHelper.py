#
# The model object builder
#
class InvalidError:
    pass

def model_obj_builder(m_obj,dict_obj,handler):
    command_error = {}
    for key,handler in handler.iteritems():
        try:
            v = dict_obj[key]
            if not handler[0].match(v):
                raise InvalidError()
            else:
                handler[2](m_obj, handler[1](v))
        except KeyError:
            command_error[key] = "Missing:"+key
        except InvalidError:
            command_error[key] = "Invalid:"+key
    return command_error


