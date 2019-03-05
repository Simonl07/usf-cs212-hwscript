import shutil
import os
import click
import subprocess
from datetime import datetime
from datetime import timedelta

BASE_URL = "git@github.com:usf-cs212-spring2019/"

def run(cmd, sh=False):
	print("Running: {0}".format(cmd))
	result = subprocess.run(cmd.split(" "), stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=sh, capture_output=True)
	print(result)
	return result.stdout.decode('utf-8')


@click.command()
@click.argument('assignment_name')
@click.argument('due_date')
@click.option("--gh_usernames", type=click.Path(), default='users.txt', help='File that contains all the github usernames that needs to be graded', show_default=True)
def grade(assignment_name, due_date, gh_usernames):
	grace_period = timedelta(minutes=15)
	due = datetime.strptime(due_date, '%m-%d')
	due = due.replace(year=2019, hour=23, minute=59, second=59)
	due += grace_period

	with open(gh_usernames) as f:
		lines = f.readlines()

	if os.path.exists("temp/"):
		shutil.rmtree('temp/')
	os.mkdir('temp/')
	os.chdir('temp/')
	for username in lines:
		dir_name = "homework-{0}-{1}".format(assignment_name, username.strip())
		run("git clone " + BASE_URL + dir_name + ".git")
		os.chdir(dir_name)
		lastcommit = datetime.strptime(run("git log -1 --format=%cd"), '%a %b %d %H:%M:%S %Y -0800 ')
		grade_coefficient = 1
		if lastcommit > due:
			delta = lastcommit - due_date
			if delta.days > 2:
				grade_coefficient = 0
			elif delta.days > 1:
				grade_coefficient = 0.8
			else:
				grade_coefficient = 0.9
		print("CHECK" + run('/home/public/cs212/homework {0} {1}'.format(username.strip(), assignment_name), sh=True))
		os.chdir("../")
		print("END")


	os.chdir('../')
	shutil.rmtree('temp/')
	pass

if __name__ == '__main__':
	grade()
