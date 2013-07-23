ltmjsvis
========

This application visualizes the state of BIGIP LTM partitions and
pools with the help of the following tools:

- pycontrolshed
- pycontrol
- Flask
- D3.js

Run the following:

    python setup.py develop
    ltmjsvis

And you'll see flask running on port 5000.  Go to
http://localhost:5000 and pick an environment and partition from the
select box that you'd like to render.

Then pick another environment and partition and see that rendering a
second partition is broken until someone writes code to clear the
canvas in between renderings.  

Annoyed with the app?  Ask for help: @timfreund on twitter or
timfreund on Freenode.

