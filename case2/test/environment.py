import yaml
import subprocess
import os


def load_e2e_config(filepath):
    with open(filepath, 'r') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    config = dict()
    workers = data.get('workers', [])
    for i, w in enumerate(workers):
        w['id'] = i + 1
        config['gw%d' % i] = w
    return config

def docker_compose_up(config):
    for name, c in config.items():
        env = os.environ.copy()
        env['ID'] = str(c['id'])
        env['WEB_PORT'] = str(c['web_port'])
        subprocess.run(['docker-compose', '-p', name, 'up', '-d'], env=env)

def docker_compose_down(config):
    for name, c in config.items():
        subprocess.run(['docker-compose', '-p', name, 'down'])
