
This file describes how to use the runs and tasks in this repository.
=====================================================================

They can (should) be used in combination with Sumatra in order to track the results, but in the latest version can also be run without.


With Sumatra:
-------------

* configure Sumatra
    * where to store the results
    * which binary to use
    * how to label the results

I usually do the following:

    smt configure --addlabel=parameters
    smt configure --executable=python
    smt configure -d /path/to/results/folder

Sumatra complains if you have uncommitted changes in your repository. This also makes sense since it wants to record the current state of your code. To not always commit after applying changes to the parameter files (which are recorded by sumatra anyway), they are not tracked by git. I only added an example parameter file for each of the runs and tasks, which can be found in the test folder. You should make a not git-tracked copy of a param-file into to param_files folder where you can then edit the values.

A script is then executed by e.g. the following command:

    smt run --main=create_corpus_run.py param_files/create_corpus_copy.param


Without Sumatra
---------------

Simply execute:

    python create_corpus_run.py param_files/create_corpus_copy.param

The *sumatra_label* set in the param-file will then be used as output folder.


