from functools import wraps
from responses import not_access, exception


def apikey_authorization(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        rsp = {}
        try:
            kwargs['logger_func'].info('Start requesting.', kwargs['request'].url._url)

            if not kwargs['db'].query(kwargs['model']).filter(kwargs['model'].id == kwargs['apikey'],
                                                              kwargs['model'].is_active == True).first():
                rsp = not_access()
                kwargs['logger_func'].info('APIKey is not entered or the entered APIKey is not acceptable.',
                                           kwargs['request'].url._url)
            else:
                rsp = await func(*args, **kwargs)
        except Exception as exp:
            rsp = exception(exp.args[0])
            kwargs['logger_func'].error(exp.args[0], kwargs['request'].url._url)
        finally:
            kwargs['logger_func'].info('End of request.', kwargs['request'].url._url)
            return rsp

    return wrapper
