def include_parameters_from_context(names):
    def decorator(func):
        def wrapper(serializer, *args, **kwargs):
            parameters = {name: serializer.context.get(name) for name in names}
            return func(serializer, *args, **parameters, **kwargs)

        return wrapper

    return decorator


include_request_parameter = include_parameters_from_context(["request"])
