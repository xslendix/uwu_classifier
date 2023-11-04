UwU Classifier
==============

Are you annoyed at Discord people "uwuifying" their messages? Well this model
is just for you! You can put it in any bot or any other application that
requires it to eliminate this annoyance.

Creating the dataset
--------------------

You require a couple of things for this:

 - Python's request module
 - An internet connection
 - The `uwuify` tool (the one written in Rust, you'll find it)

The dataset is a modified Topical-Chat one, to get it and then patch it up you
just need to do:

```
$ ./create_dataset.sh
```

Now you can move on to training.

Training the model
------------------

As long as you have installed Tensorflow you should be fine. If you get any
error messages just Google. Just run this command and be patient:

```
./train.py
```

You should then find a "final_model" in the project's root directory.

Using the model
---------------

There's an included `interactive.py` file which shows how you can load the model
and use it to get a result out of it. It is an infinite loop that keeps reading
lines, if they are "uwuified", then it will be closer to 1, and if not it will
be closer to 0.

