
import os
import click

@click.command()
@click.argument('assignment_name')
@click.option("--gh_usernames", type=click.Path(), default='users.txt', help='File that contains all the github usernames that needs to be graded', show_default=True)

def run(assignment_name, gh_usernames):
	os.mkdir('temp/')
	os.chdir('temp/')

	#Magic

	os.rmdir('temp/')
	pass

if __name__ == '__main__':
    run()
