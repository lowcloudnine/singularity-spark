# Configuration file for ipython-notebook.

c = get_config()

# The IP address the notebook server will listen on.
c.NotebookApp.ip = '*'

c.NotebookApp.open_browser = False

# The port the notebook server will listen on.
c.NotebookApp.port = 8081

# The full path to an SSL/TLS certificate file.
c.NotebookApp.certfile = u'/path/to/.ipython/profile_pyspark/nbcert.pem'

# The string should be of the form type:salt:hashed-password.
PWDFILE='/path/to/.ipython/profile_pyspark/nbpasswd.txt'
c.NotebookApp.password = open(PWDFILE).read().strip()

