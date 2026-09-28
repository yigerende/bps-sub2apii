"""Render all Compose variants and verify that a parallel sub2api stack is isolated."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
compose = [os.environ['COMPOSE_TEST_BINARY']] if os.environ.get('COMPOSE_TEST_BINARY') else ['docker', 'compose']
env = dict(os.environ, POSTGRES_PASSWORD='isolation-test-only', DATABASE_HOST='isolated-external-postgres',
           DATABASE_PASSWORD='isolation-test-only', REDIS_HOST='isolated-external-redis')
for key in ('COMPOSE_PROJECT_NAME', 'SERVER_PORT', 'POSTGRES_USER', 'POSTGRES_DB', 'BIND_HOST'):
    env.pop(key, None)

for path in sorted((ROOT / 'deploy').glob('docker-compose*.yml')):
    result = subprocess.run(compose + ['--env-file', os.devnull, '-f', str(path), 'config', '--format', 'json'],
                            env=env, check=True, capture_output=True, text=True, encoding='utf-8')
    cfg = json.loads(result.stdout)
    assert cfg['name'].startswith('bps-sub2api'), path
    services = cfg['services']
    app = services['bps-sub2api']
    assert app['ports'][0]['published'] == '8082', path
    assert app['ports'][0]['target'] == 8080, path
    assert app['environment']['SERVER_PORT'] == '8080', path
    for name, service in services.items():
        assert name.startswith('bps-sub2api'), (path, name)
        assert service['container_name'].startswith('bps-sub2api'), (path, name)
        for volume in service.get('volumes', []):
            if volume['type'] == 'bind':
                assert Path(volume['source']).name.startswith('bps-sub2api-'), (path, volume)
    if len(services) > 1:
        for kind, key in (('postgres', 'DATABASE_HOST'), ('redis', 'REDIS_HOST')):
            name = app['environment'][key]
            assert name == 'bps-sub2api-' + kind and name in services, (path, key)
            assert name in app['depends_on'], (path, key)
            assert not services[name].get('ports'), (path, name)
        pg = services['bps-sub2api-postgres']['environment']
        assert app['environment']['DATABASE_DBNAME'] == pg['POSTGRES_DB'] == 'bps-sub2api', path
        assert app['environment']['DATABASE_USER'] == pg['POSTGRES_USER'] == 'bps-sub2api', path
    for section in ('volumes', 'networks'):
        for resource in cfg.get(section, {}).values():
            assert resource['name'].startswith(cfg['name'] + '_'), (path, resource)
    print(path.name + ': isolated project, containers, storage, network and port verified')
