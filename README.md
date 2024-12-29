# `tibia`

> If you ask why `tibia` is called `tibia` - i don't remember why 😄

## Containers

`tibia` provides several containers for values:

- `Value` for already computed (sync) values with **pipe operator** / **fluent**
  API
- `Future` for not yet computed (async) values with **pipe operator** /
  **fluent** API
- `Maybe` is well-known monad for present and non-present already competed
  values with **pipe operator** / **fluent** API; provides 2 containers:
  - `Some` - value is present and actually contained inside
  - `Empty` - nothing is contained (something like python `None`)
- `FutureMaybe` is like `Future` for `Value`, but for `Maybe`
- `Result` is well-known monad for successful or failed contained value states
  with **pipe operator** / **fluent** API; provides 2 containers:
  - `Ok` - value is successfully computed
  - `Err` - failed to compute value
- `FutureResult` is like `Future` for `Value`, but for `Maybe`

Also `tibia` provides some utilitarian functions for `Iterable` and `Mapping` in
pipeline-based context:

- `Iterable`
  - eager
    - `map` - applies passed function to each element of iterable eagerly
    - `filter` - filter values in iterable with passed predicate eagerly
    - `reduce` & `reduce_to` - aggregates iterable values into single value
    - `sort_asc` & `sort_desc` - sort iterable values
    - `take` - take first or last N values from iterable (can fail on infinite
      iterable)
    - `first` - take first value or default
    - `skip` - skip first or last N values from iterable (can fail on infinite
      iterable)
    - `join` - flatten iterable of iterables into single iterable
  - async (aio)
    - `map` - applies passed async function to each element of iterable
    - `filter` - filters elements in iterable with async predicate function
    - `group_by` - groups items of iterable with passed function
  - lazy
    - `map` - applies passed async function to each element of iterable lazily
    - `filter` - filters elements in iterable with async predicate function
      lazily
    - `take_while` - takes elements from iterable until predicate is true
    - `skip_while` - skips elements from iterable until predicate is true
    - `join` - flattens iterable of iterables lazily
  - threaded
    - `map` - applies passed sync function to each element of iterable in
      threads
    - `filter` - filters in threads elements of iterable
- `Mapping`
  - value
    - `map` - applies function to each value of mapping
    - `filter` - filters mapping pairs based on value
    - `iterate` - returns iterable of values (lazy as generator)
    - `set` - set value to key
    - `get` - get value by key (can raise `KeyError`)
    - `get_or` - get value or passed default by key
    - `maybe_get` - get value by key in `Maybe` container (`Some` if key is
      present, `Empty` if not)
  - key
    - `map` - applies function to each key of mapping
    - `filter` - filters mapping pairs based on key
    - `iterate` - returns iterable of keys (lazy as generator)
  - item
    - `map` - maps key-value pair to new key-value pair
    - `map_to_value` - maps value based on key-value pair
    - `map_to_key` - maps key based on key-value pair
    - `filter` - filters mapping elements based on key-value pairs
    - `iterate` - returns iterable of key-value pairs (lazy as generator of
      tuples)

## Value

`Value` is a simple container that brings to python so called **pipe operator**.

So how to use it? Put some concrete value to the container, for example a
number. Now instead of passing this value as an argument to a function pass a
function as some action that you want to be performed on this value:

```python
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

## `Future`

`Future` is direct analogue of `Value`, but for values that are not calculated
(awaited) yet. For JS developers it might be widely know as `Promise`. It has
the same as `Value` interface:

- `Future.map` & `Future.inspect` for sync functions
- `Future.map_async` & `Future.inspect_async` for async functions
- `Future.unwrap` for extracting contained value (must be awaited)

Additionally one can `await` directly `Future` without `unwrap`:

```python
_ = await future.unwrap()

# same as

_ = await future
```

This is just a shortcut, but I would generally recommend explicit unwrapping and
waiting of contained value.

## `Maybe` & `FutureMaybe`

`Maybe` is an alternative for python `Optional`. At first glance it might seem
that it is not needed, but it provides to apply functions without checks on
emptiness and also can consider `None` as actual value.

It consists of 2 containers:

- `Some` - indicates that value is present (even if one is `None`)
- `Empty` - indicates that there is no value

For example let's imagine one is creating data structure for updating some data
(for example table in DB). Naive approach would be to create some class with
all-optional fields:

```python
class UpdateUser:
  first_name: str | None = None
  second_name: str | None = None
  birthdate: datetime | None = None
```

Imagine that `birthdate` is nullable in table we want to update. If we get this
structure with `None` in `birthdate` field we cannot determine whether we want
to set it to `null` or we do not want to perform any update on this column.

With `Maybe` this problem goes away. `Empty` state tells us that we do not want
to perform action and `Some` unambiguously tells us that we want to set column
to contained value:

```python
class UpdateUser:
  first_name: Maybe[str] = Empty()
  second_name: Maybe[str] = Empty()
  birthdate: Maybe[datetime | None] = Empty()
```

With this approach it is much more clear what each value means and what is valid
state.

### Piping API

For making pipelines `Maybe` & `FutureMaybe` like `Value` & `Future` provide the
following methods:

- `map` / `map_async` - apply contained value to function if one is present and
  wrap result into `Some`
- `map_or` / `map_or_async` - apply contained value to function if one is
  present and return result of function directly or replace it with passed
  default value
- `inspect` / `inspect_async` - apply function as side-effect if value is
  present ignoring result of passed function and return current container

Imagine we apply function that returns `R`:

| Container | Method          | Returns                  |
| --------- | --------------- | ------------------------ |
| `Ok[T]`   | `map`           | `Ok[R]`                  |
| `Ok[T]`   | `map_async`     | `FutureMaybe(Ok[R])`     |
| `Empty`   | `map`           | `Empty`                  |
| `Empty`   | `map_async`     | `FutureMaybe(Empty)`     |
| `Ok[T]`   | `map_or`        | `R`                      |
| `Ok[T]`   | `map_or_async`  | `Future[R]`              |
| `Empty`   | `map_or`        | `R` from default         |
| `Empty`   | `map_or_async`  | `Future[R]` from default |
| `Ok[T]`   | `inspect`       | `Ok[T]`                  |
| `Ok[T]`   | `inspect_async` | `FutureMaybe(Ok[T])`     |
| `Empty`   | `inspect`       | `Empty`                  |
| `Empty`   | `inspect_async` | `FutureMaybe(Empty)`     |

Mainly one would use `map` and `map_async` to perform desired actions without
thinking if value is present, some side-effect functions (for debugging for
example) with `inspect` & `inspect_async` and than unwrap value with `map_or` or
`map_or_async` methods (or via Unwrapping API).

### Unwrapping API

In order to extract value from container one can use one of the following
methods:

- `expect`
  - if `Some`: return contained value
  - if `Empty`: raise `ValueError` with passed error message
- `unwrap` - same as `expect`, but uses built-in error message `"must be some"`
- `unwrap_or`
  - if `Some`: return contained value
  - if `Empty`: return passed default value
- `unwrap_or_none`
  - if `Some`: return contained value
  - if `Empty`: return `None`

### Logical API

In order to check / validate contained value on can use following methods:

- `is_some` - `True` if container is `Some`, otherwise `False`
- `is_empty` - `True` if container is `Empty`, otherwise `False`
- `is_some_and` - `True` if container is `Some` and passed predicate is `True`
  (function that checks contained value), otherwise `False`
- `is_empty_or` - `True` if container is `Empty` or passed predicate is `True`
  (function that check contained in `Some` value), otherwise `False`

For example imagine we have `is_even` predicate:

| Container | Method        | Returns |
| --------- | ------------- | ------- |
| `Ok(2)`   | `is_some_and` | `True`  |
| `Ok(1)`   | `is_some_and` | `False` |
| `Empty()` | `is_some_and` | `False` |
| `Ok(1)`   | `is_empty_or` | `False` |
| `Ok(2)`   | `is_empty_or` | `True`  |
| `Empty()` | `is_empty_or` | `True`  |

`is_some_and` & `is_empty_or` methods also have `is_some_and_async` &
`is_empty_or_async` alternatives for async predicates, as base versions work
only with sync functions. Async alternatives return `Future[bool]` for further
piping if needed.

### Construction API

There are a few static function in `Maybe` class used for constructing `Maybe`
containers:

- `Maybe.from_value` - always wraps value into `Some`
- `Maybe.from_value_when` - wraps value into `Some` if value satisfies passed
  predicate, otherwise `Empty`
- `Maybe.from_optional` - wraps value into `Some` if one is not `None`,
  otherwise `Empty`
- `Maybe.from_optional_when` - wraps value into `Some` if value is not `None`
  and satisfies passed predicate , otherwise `Empty`

### Decorator API

Based on `from_value` and `from_optional` `Maybe` provides 2 decorators for
functions:

- `wraps` - wraps returned from function value via `Maybe.from_value`
- `safe` - wraps returned from function value via `Maybe.from_optional`

> One might also find `Maybe.wraps` & `Maybe.wraps_optional` static methods, but
> they are deprecated and not intended to be used.

### Point-free API

All discussed above methods can also be used as functions contained in
`tibia.maybe` module. They can be found useful when working with iterables of
`Maybe` for example (for massive filtering and unwrapping without loosing type
hints).

---

`FutureMaybe` provides exactly the same API, but for "futurized" `Maybe` value.

## `Result` & `FutureResult`

`Result` & `FutureResult` monads provide the ability for indicating computation
success and error states without implicit error raises. Yes, yes, raising errors
is actually implicit way, that highly resembles to `goto` operator widely
forbidden or not implemented for increasing code complexity exponentially. With
`Result` one does not raise exception, but explicitly returns it (like Rust and
Go do for example).

It consists of 2 containers:

- `Ok` - indicates successful result
- `Err` - indicates failed result

Both of the containers store some value, `Ok` - what was actually computed,
`Err` - some error representation (not always `Exception`).

### Piping API <!--noqa: MD024-->

It is a bit extended relative to `Maybe` or `Value` and consist of the following
methods:

- `map` / `map_async` - mapping for `Ok` container
- `map_err` / `map_err_async` - mapping for `Err` container
- `map_or` / `map_or_async` - mapping and unwrapping for `Ok` container
- `map_err_or` / `map_err_or_async` - mapping and unwrapping for `Err` container
- `inspect` / `inspect_async` - applying side-effect function for `Ok` container
- `inspect_err` / `inspect_err_async` - applying side-effect function for `Err`
  container

### Unwrapping API <!--noqa: MD024-->

Also provides more options for unwrapping both containers:

- `expect`
  - `Ok` - returns container value
  - `Err` - raises `ValueError` with passed error message
- `unwrap`
  - `Ok` - returns container value
  - `Err` - raises `ValueError` with default error message `"must be ok"`
- `unwrap_or`
  - `Ok` - returns container value
  - `Err` - returns passed default value
- `expect_err`
  - `Ok` - raises `ValueError` with passed error message
  - `Err` - returns container value
- `unwrap_err`
  - `Ok` - raises `ValueError` with default error message `"must be err"`
  - `Err` - returns container value
- `unwrap_err_or`
  - `Ok` - returns passed default value
  - `Err` - returns container value

### Logical API <!--noqa: MD024-->

Many more options for validating containers and values:

- `is_ok` - `True` if `Ok`, otherwise `False`
- `is_ok_and` / `is_ok_and_async` - `True` if `Ok` and contained value satisfies
  passed predicate, otherwise `False` (returns `Future[bool]` for async version)
- `is_ok_or` / `is_ok_or` - `True` if `Ok` or `Err` contained value satisfies
  passed predicate, otherwise `False` (returns `Future[bool]` for async version)
- `is_err_` - `True` if `Err`, otherwise `False`
- `is_err__and` / `is_err__and_async` - `True` if `Err` and contained value satisfies
  passed predicate, otherwise `False` (returns `Future[bool]` for async version)
- `is_err__or` / `is_err__or` - `True` if `Err` or `Ok` contained value satisfies
  passed predicate, otherwise `False` (returns `Future[bool]` for async version)

### Decorator API <!--noqa: MD024-->

Provides 2 decorators:

- `wraps` - simply always returns `Ok`-wrapped function result
- `safe` - `try-excepts` `Exception` and returns `Ok` if `Exception` was not
  raised, otherwise wraps `Exception` into `Err`
- `safe_from` - same as `safe` but firstly it excepts a tuple of `Exception`
  types to be excepted in `try-except` block

> One might also find `Result.wraps` & `Result.safe` static methods, but they
> are deprecated and not intended to be used.

### Point-free API <!--noqa: MD024-->

Same as `Maybe`, `Result` provides simple functions that can replace any method.

---

`ResultMaybe` provides exactly the same API, but for "futurized" `Result` value.
