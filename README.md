arg-lisp
==========

arg-lisp is an alternative lisp syntax built around the concept of n-expressions, where an n-expression is

1. An atom
2. An unordered list of key-value pairs (a map/dictionary)

e.g. 2+2 is represented as {add:2 and:2} in n-expression form.

More clearly, if an s-expression function call has the form:

```lisp
(function_name arg1 arg2 ...)
```

The equivalent n-expression has the form:
```ts
{name1:arg1 name2:arg2 ....}
```

Notice that the `function_name` is dropped in favour of argument names. By convention the first argument of a function is typically the same as `function_name`, but this doesn't have to be the case! A function is more accurately described using all the argument names, e.g. `{add and}` instead of `add`.

The braces are generally optional, but required in the case of ambiguity. This means that

```ts
{add:2 and:2}
```

is equivalent to

```ts
add:2 and:2
```

The former is totally un-ambiguous, but as you'll see, the later can be much more pleasing to work with.

## Fibonacci Sequence
The below is an example of a recursive Fibonacci sequence generator. It uses the brace-less syntax, which is fine in this case because there is no ambiguity.

```plaintext
fn:{fib:n} on:
    if: is:n lessthan:2 then:
        n
    else:
        add:fib:subtract:1 from:n and:fib:subtract:2 from:n
```
