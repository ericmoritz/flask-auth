import hashlib


def get_hexdigest(algo, salt, raw):
    h = hashlib.new(algo)
    h.update(salt + raw)
    return h.hexdigest()
    
def check_password(raw_password, enc_password):
    algo, salt, hsh = enc_password.split('$')

    return hsh == get_hexdigest(algo, salt, raw_password)

def encode_password(raw_password):
    import random
    algo = 'sha1'
    salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
    hsh = get_hexdigest(algo, salt, raw_password)
    return '%s$%s$%s' % (algo, salt, hsh)        
