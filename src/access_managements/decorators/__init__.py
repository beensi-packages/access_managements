from functools import wraps
from responses import not_access, exception


def apikey_authorization(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        rsp = {}
        try:
            if 'logger' in kwargs and 'request_url' in kwargs:
                kwargs['logger'].info(f"Start requesting \'{kwargs['request_url']}\'.")

            if not kwargs['db'].query(kwargs['model']).filter(kwargs['model'].id == kwargs['apikey'],
                                                              kwargs['model'].is_active == True).first():
                if 'logger' in kwargs:
                    kwargs['logger'].info('APIKey is not entered or the entered APIKey is not acceptable.')
                rsp = not_access()
            else:
                rsp = await func(*args, **kwargs)
        except Exception as exp:
            if 'logger' in kwargs:
                kwargs['logger'].error(exp.args[0])
            rsp = exception(exp.args[0])
        finally:
            if 'logger' in kwargs and 'request_url' in kwargs:
                kwargs['logger'].info(f"End of request \'{kwargs['request_url']}\'.")
            return rsp

    return wrapper
