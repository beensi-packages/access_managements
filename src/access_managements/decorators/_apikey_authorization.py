from functools import wraps
from responses import not_access, exception


def apikey_access_check(apikey, db, model):
    if db.query(model).filter(model.id == apikey, model.is_active == True, ).first():
        return True
    return False


def apikey_authorization(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        rsp = {}
        try:
            if not apikey_access_check(apikey=kwargs['apikey'], db=kwargs['db'], model=kwargs['model']):
                rsp = not_access()
            else:
                rsp = await func(*args, **kwargs)
        except Exception as exp:
            rsp = exception(exp.args[0])
        finally:
            return rsp

    return wrapper
