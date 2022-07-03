# actor

Uvicorn server template with many faces.

(c) timoniq, 2022

# creating an "actor's face"

structure as follows

```
actor_name
  - STATIC
  - app.py
  ...
```

in `app.py` class named `Handler` derived from `ABCHandler` should be created.

# configure

## addresses

add address scheme to the `ADDRESSES`.

- just address
- or substitution: `what.received -> renamed`

## static

all actors share common `static` folder

but each actor has its own `STATIC` file where names files accessible to specific actor are declared.

names can be changed in format:

`requested.txt -> real.txt`

also after the real name mime type can be declared preceded by ` `.

## favicon

every actor should have a favicon named `{actor name}.ico` and located in `static` folder.

# useful methods

`Handler.getpath(local_path)` in any actor's app returns an absolute path of the local path given.