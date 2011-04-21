RUNS
=====================
Runs are a recipe to produce a space.

Runs are python scripts (*.run.py) that call a preprocessing, corpus, and model. 
At the end there are serializations for the space, and a metadata file that describes 
the recipe.

Runs are designed to work with sumatra.

Sumatra takes a script (say main.py) and a parameter file. For us, then, we keep
the logic on the script and the metadata on the parameter file. For example, You
may have a run that creates an lsa space. You can switch parameters on the
parameter (e.g., dimensions 10,100,1000, 10000) file and call the run file with 
those different parameter files.

When the space is done and serialized, there are two files to look at to
reproduce it -although sumatra should take care of this!- : the run and the
parameter file. The parameter file contains metadata of which run script should
use the paramenter file (sort of like binding them together). 

The basic chain is :
plainText -> preprocessing -> Corpus -> Model

But you can chain models together (see the tutorials):

plainText -> preprocessing -> Corpus -> Model -> Model

For example, it'd be pretty common to chain tfidf -> lsa

At the end of the pipe we should have the serialization of the last model, and
serialization of the corpus object.

Running a run could take hours, even days. So we don't do it often and reuse the
serializations to do tasks.

TASKs
==============================================
A task is a python file (*.task.py) that produces something useful. For example,
it may produce a figure from a paper, or actually be in production on a web site
serving pages. 
The task uses the serializations that a run produces. They are bound together,
so if something changed in the run, expect your task to produce different
results (!). We want to prevent that by accident we run tasks with the wrong
space, and for that we use sumatra.
