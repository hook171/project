import uuid

def get_random_code():
        code = str(uuid.uuid4().hex[:8])
        return code