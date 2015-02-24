# singularity-spark
Experiments and documentation for work with learning and integrating Apache Spark.

This is the local configuration branch.  The initial work started on a single node
cluster and thus local[*] was used to make things work as connecting using 
yarn-client or a server address did not work.  Of course that could have been an
operator issue.  Regardless this branch is useful for getting IPython with PySpark
to work on a local machine, i.e. a laptop or desktop.  It will be kept for 
documentation purposes and will be tagged as well so it can be easily found.  
However, it should not be merged into master as that is where the project is
moving forward.  If the tests are needed use the testing branch.

Further documentation is available in the [docs](docs/README.md) folder.
