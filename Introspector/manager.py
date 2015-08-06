__author__ = 'Denis'
from structures import Job

def prepare_job(action, target, auth):
    if action == 'ping':
        cmd = "sudo ping " + target
    elif action == 'tcpdump':
        cmd = 'sudo tcpdump host ' + target
    elif action == 'traceroute':
        cmd = "sudo traceroute -I " + target
    elif action == 'fping':
        cmd = "sudo fping -g " + target
    elif action == 'iproute':
        cmd = "sudo ip route get " + target
    else:
        cmd = None
        print 'invalid command, terminating'
        return 0

    if cmd:
        cmd += """ | awk '{ print strftime("\%Y-%m-%d %H:%M:%S\"), $0; fflush(); }'"""

    return Job(auth=auth, command=cmd)

def prepare_jobs(action, targets, auth):

    return [prepare_job(action, target, auth) for target in targets]









