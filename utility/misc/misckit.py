def singleton(cls):
    """decorator making a class singleton"""

    # a dict registering single-instances for each class decorated
    registered = {}

    # wrapper replacing calls to <class>()
    def wrapped_class(*args, **kwargs):
        if cls not in registered:
            # if 1st time, create single instance, and register with key <cls>
            registered[cls] = cls(*args, **kwargs)
        return registered[cls]
    # <cls> is now replaced. calls to <cls>() now directs to <wrapped_class>()
    return wrapped_class
