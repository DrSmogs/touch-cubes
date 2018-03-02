import ujson

def load_config:
    try:
        f = open('config.json', 'r')
        config = ujson.loads(f.readall())
        f.close()
        return config
    except:
        return None

def save_config(config):
    try:
        f = open('config.json', 'w')
        f.write(ujson.dumps(config))
        f.close()
    except:
        return None
