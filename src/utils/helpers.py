from base64 import b64encode

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'xlsx'}

def base64_encode(data):
    if data:
        return b64encode(data).decode('utf-8')
    return ''