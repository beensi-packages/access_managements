def apikey_access_check(apikey, db, model):
    if db.query(model).filter(model.id == apikey, model.is_active == True, ).first():
        return True
    return False
