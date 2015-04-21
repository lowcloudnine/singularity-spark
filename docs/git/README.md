## Git Tips and Tricks

Below are some simple tips and tricks for using git and github that have 
tripped me up more than once and so I'm writing them down.

#### Initialization

* When first cloning a github repository clone using your username for the
account, for example:

	git clone https://username@github.com/username/projectname.git

* Some common configurations for git, I create a shell script for mine:

	git config --global user.name "first last"
	git config --global user.email "you.email@domain.net"
	git config --global help.autocorrect true
	git config --global credential.helper 'cache --timeout=300'

