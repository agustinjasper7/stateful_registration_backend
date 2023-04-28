def to_camelcase(snake_str):
    """
    Convert snake_case string to camelCase.
    """
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def convert_fields_to_camelcase(snake_str):
    """
    Convert snake_case string to camelCase.
    Accepts string with nested fields (i.e. input_data.this_data -> inputData.thisData)
    """
    return ".".join(to_camelcase(field) for field in snake_str.split("."))
