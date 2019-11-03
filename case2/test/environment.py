import yaml

def load_e2e_config(filepath):
    with open(filepath, 'r') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    config = dict()
    workers = data.get('workers', [])
    for i, w in enumerate(workers):
        w['id'] = i + 1
        config['gw%d' % i] = w
    return config
