import ujson

def load_config():
    f = open('config.json', 'r')
    config = ujson.loads(f.read())
    f.close()
    return config


def save_config(config):

    f = open('config.json', 'w')
    f.write(ujson.dumps(config))
    f.close()
