import base64

def b64encode(value):
    if value is None:
        return ''
    return base64.b64encode(value).decode('utf-8')

