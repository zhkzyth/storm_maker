#!/usr/bin/env python
# encoding: utf-8

from fabric.api import (
    env, run, local, put, cd, settings, lcd
)


app_name = "app_name"

home_dir = '/home/deploy'
project_dir = home_dir + '/' + app_name
general_app_dir = '/mnt/%s' % app_name

source_dir = project_dir + '/htdocs'
log_dir = general_app_dir + '/log'
run_dir = general_app_dir + '/run'
backup_dir = general_app_dir + '/' + 'backup'

virtualenv_dir = project_dir + '/env'

config_file = source_dir + '/deploy/supervisord.conf'
supervisor_name = app_name + '_apps:*'

# conf files
current_conf = ""

# 发布的包名
dist = ""


def dev():
    """
    开发环境
    """
    global current_conf

    dev_host = ''
    env.hosts = [dev_host]
    env.passwords = {
        dev_host: "pwd"
    }

    current_conf = "dev.py"


def product():
    """
    产品环境
    """
    global current_conf

    product_host = ''
    env.passwords = {
        product_host: "pwd"
    }
    env.hosts = [product_host]

    current_conf = "product_aliyun.py"


def package_code():

    # create a new source distribution as tarball
    local('python setup.py sdist --formats=gztar', capture=False)


def upload_remote():
    dist = local('python setup.py --fullname', capture=True).strip()

    # upload the source tarball to the temporary folder on the server
    put('dist/%s.tar.gz' % dist, '/tmp/%s.tar.gz' % app_name)

    with settings(warn_only=True):
        run('rm -fr /tmp/%s' % app_name)
        run('mkdir /tmp/%s' % app_name)

    with cd('/tmp/%s' % app_name):
        run('tar xzf /tmp/%s.tar.gz' % app_name)


def backup_remote_files():

    with cd(home_dir):
        run('tar -zcvf %s/%s.tar.gz %s' % (backup_dir, app_name, source_dir))


def stop_remote_process():

    with settings(warn_only=True):
        run('supervisorctl -c %s stop %s' % (config_file, supervisor_name))


def remove_remote_source():

    with settings(warn_only=True):
        run('rm -fr /home/deploy/%s/htdocs/*' % app_name)


def update_remote_source():

    run('mv /tmp/%s/%s/* /home/deploy/%s/htdocs' % (app_name, dist, app_name))


def start_remote_process():

    with settings(warn_only=True):
        run('supervisorctl -c %s shutdown' % config_file)
        run('supervisord -c %s' % config_file)

    run('supervisorctl -c %s start %s' % (config_file, supervisor_name))


def prepare_base_dirs():

    # check if project dir exists
    run('mkdir -p %s' % project_dir)
    run('mkdir -p %s' % source_dir)
    run('mkdir -p %s' % backup_dir)
    run('mkdir -p %s' % run_dir)
    run('mkdir -p %s' % log_dir)
    run('mkdir -p %s' % virtualenv_dir)


def prepare_virtualenv():

    with settings(warn_only=True):
        # TODO 自动找寻服务路径
        run('/usr/local/bin/virtualenv %s' % virtualenv_dir)
        run('%s/bin/pip install -r %s/deploy/requirements.txt' % (virtualenv_dir, source_dir))


def prepare_setting():

    run('ln -nfs {source_dir}/src/settings/conf/{current_conf} {source_dir}/src/settings/conf/current.py'.format(source_dir=source_dir, current_conf=current_conf))


def deploy():

    # figure out the release name and version
    global dist

    with lcd('./..'):
        dist = local('python setup.py --fullname', capture=True).strip()
        package_code()
        upload_remote()

    prepare_base_dirs()
    backup_remote_files()
    stop_remote_process()
    remove_remote_source()
    update_remote_source()
    prepare_virtualenv()
    prepare_setting()
    start_remote_process()
