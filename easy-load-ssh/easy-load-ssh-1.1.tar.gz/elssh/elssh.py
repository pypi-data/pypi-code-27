import subprocess, sys, getpass, click, yaml, os.path
from pathlib import Path
from functools import reduce

default_config = {
    'username': getpass.getuser(),
    'domain': 'mines.edu', # TODO: Load from env
    'hostgroups': {'default': 'ch215l-[01-16].mines.edu'},
}

cfg_file_name = '{}/.elsshrc'.format(str(Path.home()))

def dump_dict(d):
    noalias_dumper = yaml.dumper.SafeDumper
    noalias_dumper.ignore_aliases = lambda self, date: True
    return yaml.dump(d, default_flow_style=False, Dumper=noalias_dumper)

def add_hostgroup(group_name, host_ranges):
    file_cfg = load_config_file()
    if 'hostgroups' in file_cfg:
        file_cfg['hostgroups'][group_name] = host_ranges
        save_config_file(file_cfg)
    else:
        update_config_file({
            'hostgroups': {
                group_name: host_ranges
            }
        })

def save_config_file(config_obj):
    with open(cfg_file_name, 'w') as f:
        f.write(dump_dict(config_obj))

def update_config_file(new_config):
    file_cfg = load_config_file()
    file_cfg.update(new_config)
    save_config_file(file_cfg)

def load_config_file():
    file_cfg = {}
    if os.path.isfile(cfg_file_name):
        with open(cfg_file_name, 'r') as f:
            file_cfg = yaml.safe_load(f)
    else:
        print('Missing config file. Created it at {}'.format(cfg_file_name))
        save_config_file({})

    return file_cfg if file_cfg else {}

def load_config(**kw):
    cfg = default_config

    file_cfg = load_config_file()
    cfg.update(file_cfg)

    # Only accept valid keyword pairs
    kw = {k: v for k, v in kw.items() if v is not None}
    cfg.update(**kw) # Command config
    return cfg

@click.group()
@click.option('--username')
@click.option('--domain')
@click.pass_context
def cli(ctx, **kw):
    # config = load_config(username=kw['username'], domain=kw['domain'])
    config = load_config(**kw)
    ctx.obj = config

@cli.command()
@click.argument('host_groups', nargs=-1)
@click.option('--host-range', '-r', multiple=True)
@click.pass_obj
def run(config, host_groups, host_range):
    host_groups = list(host_groups)
    if len(host_groups) == 0:
        host_groups = ['default']

    host_patterns = list(host_range)
    if len(host_patterns) > 0:
        if click.confirm('Do you want to add "{}" to your hostgroups config?'.format(host_patterns)):
            group_name = click.prompt('Give it a name', default='default')
            add_hostgroup(group_name, host_patterns)
    else:
        host_patterns = reduce(lambda acc, g: acc + config['hostgroups'][g] if g in config['hostgroups'] else [], host_groups, [])

    if len(host_patterns) == 0:
        sys.exit('No host patterns found')

    host_ranges_str = ' '.join(map(lambda x: '-w ' + x, host_patterns))

    def host_sort_key(host):
        return host[1][2]

    def least_busy_host_name(name_load_dict):
        name, shortest_load_avgs = sorted(name_load_dict.items(), key=host_sort_key)[0]
        return name

    cmd_str = "pdsh -R ssh -l {} {} 'uptime' 2>/dev/null".format(config['username'], host_ranges_str)
    print('Running command: {}'.format(cmd_str))

    result = subprocess.run(cmd_str, shell=True, stdout=subprocess.PIPE)
    if result.returncode != 0:
        sys.exit('Command failed--have you installed pdsh?')

    host_str = result.stdout.decode('utf-8')
    if not host_str:
        sys.exit('No hosts were returned with the supplied pattern')

    print()

    name_load_dict = {}
    for line in host_str.splitlines():
        name, *stuff, str_load_avgs = line.split(':')
        num_load_avgs = list(map(lambda x: float(x.strip()), str_load_avgs.split(',')))
        name_load_dict[name] = num_load_avgs

    candidate_host = least_busy_host_name(name_load_dict)
    subprocess.run(['ssh', '{}@{}.{}'.format(config['username'], candidate_host, config['domain'])])
