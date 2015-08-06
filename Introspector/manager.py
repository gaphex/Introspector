__author__ = 'Denis'
from structures import Job


def prepare_job(action, target, auth, flags=None):
    if flags:
        flagstr = ' '.join(flags)
    else:
        flagstr = ''

    if action == 'ping':
        cmd = "sudo ping " + flagstr + ' ' + target
    elif action == 'tcpdump':
        cmd = "sudo tcpdump host " + flagstr + ' ' + target
    elif action == 'traceroute':
        cmd = "sudo traceroute " + flagstr + ' ' + target
    elif action == 'fping':
        cmd = "sudo fping " + flagstr + ' ' + target
    elif action == 'iproute':
        cmd = "sudo ip route get " + flagstr + ' ' + target
    else:
        print 'invalid command, terminating'
        return 0

    if cmd:
        cmd += """ | awk '{ print strftime("\%Y-%m-%d %H:%M:%S\"), $0; fflush(); }'"""

    return Job(auth=auth, command=cmd)


def prepare_jobs(action, targets, auth, flags=None):
    return [prepare_job(action, target, auth, flags) for target in targets]
