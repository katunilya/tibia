# `tibia`

> If you ask why `tibia` is called `tibia` - i don't remember why 😄

## Value

`Value` is a simple container that brings to python so called **pipe operator**.

So how to use it? Put some concrete value to the container, for example a
number. Now instead of passing this value as an argument to a function pass a
function as some action that you want to be performed on this value:

```python
from tibia import Value


def add(x: int, y: int) -> int:
    return x + y


def multiply_by(x: int, y: int) -> int:
    return x * y


def subtract(x: int, y: int) -> int:
    return x - y


_ = (
    Value(1)
    .map(add, 1)
    .map(multiply_by, 3)
    .map(subtract, 10)
    .map(multiply_by, -1)
    .inspect(print)
    .unwrap()
)
```

Thus we build a declarative chain of actions we perform on some piece of data.

### `Value.map`

`Value.map` is method that invokes passed function on contained value. It
supports not only single-argument functions, but actually any function with only
one requirement: **contained value must be the first argument for the
function**. Other arguments can be passed as `*args` and/or `**kwargs` to the
`Value.map` method.

So image we have a `Value[int]`. The following example function will be
completely valid for `Value.map`:

```python
# simple single-argument function, contained value will be x
def add_one(x: int) -> int:
    return x + 1

# 2 argument function, contained value will be x again, and argument for y must
# be passed following the function argument to map method
def add(x: int, y: int) -> int:
    return x + y

# again 2 argument function, but in this case y argument can be ommited in map
def multiply_by(x: int, y: int = 1) -> int:
    return x * y
```

`Value.map` returns new `Value` container for data returned from the passed
function, thus with `Value.map` method chaining one can build pipelines on data.

`Value.map` works only with synchronous functions. For asynchronous functions
use `Value.map_async`.

### `Value.map_async`

`Value.map_async` is direct analogue of `Value.map` but for async functions.
Main difference is that instead of `Value` it returns `Future` - `tibia`s simple
container over coroutine (`Future` is discussed further, but most things valid
for `Value` are valid for `Future` and their interface are very similar).

### `Value.inspect`

`Value.inspect` has nearly the same signature as `Value.map` with only
difference: it does not wrap returned from the passed function value into new
`Value` container, but returns the current self `Value` container.

Simply this is function for making side-effects - something we want to happen,
but don't care about result. In the example above `Value.inspect` was used to
print contained in container value. `print` returns `None`, so if we've used
`Value.map` we would lost the data, but with `Value.inspect` we just performed
an action and continued working on already contained data.

Like `Value.map` can be used only with synchronous functions.

### `Value.inspect_async`

Like `Value.map_async` is analogue of `Value.map` for async function that
returns `Future` containers `Value.inspect_async` is the same for
`Value.inspect`.

### `Value.unwrap`

Method for extracting value from container if one is not further needed.

### `Value.wraps`

Decorator that changes signature of wrapped function by containing returned
value in `Value` container. For example initial signature was:

```txt
fn: (int, int, str) -> str
```

With `Value.wraps` decorator applied it becomes:

```txt
fn: (int, int, str) -> Value[str]
```
