#!/usr/bin/python
import sys
import argparse
import re
import subprocess

parser = argparse.ArgumentParser(description='Dockerflix DNS updater')
parser.add_argument('-c', '--configdir', help='Dockerflix config dir', default='./config', required=False)
parser.add_argument('-d', '--dockerpath', help='Path to docker on the command line', default='/usr/bin/docker', required=False)
parser.add_argument('-g', '--gitpath', help='Path to git on the command line', default='/usr/bin/git', required=False)

args = parser.parse_args()

status = {}

print("Running 'git pull'")
gitpull = subprocess.Popen([args.gitpath, 'pull'], stdout=subprocess.PIPE)
gitpull.communicate()    # run it, output to stdout
status['git_pull'] = gitpull.wait()    # returns exit code

print("Running 'docker stop dockerflix'")
docker_stop = subprocess.Popen([args.dockerpath, 'stop', 'dockerflix'], stdout=subprocess.PIPE)
docker_stop.communicate()
status['docker_stop'] = docker_stop.wait()

print("Running 'docker rm dockerflix'")
docker_rm = subprocess.Popen([args.dockerpath, 'rm', 'dockerflix'], stdout=subprocess.PIPE)
docker_rm.communicate()
status['docker_rm'] = docker_rm.wait()

print("Running 'bash build.sh (Please be patient)'")
status['build_sh'] = subprocess.call('bash build.sh >/dev/null 2>/dev/null', shell=True)

print("Running 'docker run -d -p 80:80 -p 443:443 --restart=always --name dockerflix trick77/dockerflix'")
docker_run = subprocess.Popen([args.dockerpath, 'run', '-d', '-p', '80:80', '-p', '443:443', '--restart=always', '--name', 'dockerflix', 'trick77/dockerflix'], stdout=subprocess.PIPE)
docker_run.communicate()
status['docker_run'] = docker_run.wait()

print('Update complete: ')

for key, value in status.items():
	if value == 0:
		print("%s was successful" % key)
	else:
		print("%s failed, or didn't run correctly. Please update manually" % key)

print("if you see no failure messages above then it is probably safe to assume that dockerflix has been updated\ndockerflix should be running again.\nYou may need to re-run gendns-conf.py to generate new rules for your router")
