#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py) that.

distributes an archive to your web servers, using the function do_deploy.
"""
from fabric.api import *
import os
from datetime import datetime

env.hosts = ['34.224.4.61', '18.206.192.35']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """Do the actual deployment."""
    a_list = archive_path.split(".tgz")
    archive_wo_ext = "".join(a_list)
    b_list = archive_wo_ext.split("versions/")
    archive_wo_ext_ver = "".join(b_list)
    c_list = archive_path.split("versions/")
    archive_wo_ver = "".join(c_list)
    if archive_path:
        put(archive_path, '/tmp/')
        run("mkdir -p /data/web_static/releases/{}/".
            format(archive_wo_ext_ver))
        run("tar -zxf /tmp/{} -C /data/web_static/releases/{}/"
            .format(archive_wo_ver, archive_wo_ext_ver))
        run("rm -r /tmp/{}".format(archive_wo_ver))
        run("mv /data/web_static/releases/{}/web_static/*\
        /data/web_static/releases/{}/".format(archive_wo_ext_ver,
                                              archive_wo_ext_ver))
        run("rm -rf /data/web_static/releases/{}/web_static".
            format(archive_wo_ext_ver))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
            format(archive_wo_ext_ver))
        print("New version deployed!")
        return True
    else:
        return False


def do_pack():
    """Do the packing."""
    try:
        filepath = "versions/web_static_" + datetime.now().\
                   strftime("%Y%m%d%H%M%S") + ".tgz"
        local("mkdir -p versions")
        local("tar -zcvf versions/web_static_$(date +%Y%m%d%H%M%S).tgz\
        web_static")
        print("web_static packed: {} -> {}".
              format(filepath, os.path.getsize(filepath)))
    except Exception:
        return None