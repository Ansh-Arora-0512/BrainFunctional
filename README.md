# BrainFunctional
Another BF derivative. But also so much more.

Do you love BF but also never use it because you value your braincells? Well worry not, the solution to all your problems is here.

We bring to you simple, scalable BF! Ok no. That was a lie to get your attention. But it worked didn't it? I mean if you're reading this it either worked or you're mentally deranged. Probably from too much BF. That is a problem we will fix.

## What is it?
BF but with functions.

If you have no idea what BF is but for some reason are still reading this, here is a [wikepedia article](https://en.wikipedia.org/wiki/BF) explaining the fundamentals of the esoteric programming language. I will not be exploring how to use BF or going over it in this guide, so if you don't understand some of the examples given or want another guide on the language, here is a [tutorial](https://gist.github.com/roachhd/dce54bec8ba55fb17d3a) by @roachhd, which covers some of the fundamentals quite well.

The syntax is minimalistic, simple and impractical, following the fundamentals of the language.

However, unlike many features of BF, it is a powerful and versatile tool which makes the language more high level. Not a lot more, but it actually allows you to solve more complex problems with BF, in a style that is still quintessential BF.

So let's jump into the syntax.

## The Commands
This table provides a very basic overview of the 12 commands involved (including the 8 commands from original BF), so for a more in-depth guide and in order to understand the exact behaviour of each command, keep reading.

Command | Description
--- | ---
`>` |	Move the pointer to the right
`<`	| Move the pointer to the left
`+` | Increment the memory cell at the pointer. If the cell is a function, overwrite it with 1
`-`	| Decrement the memory cell at the pointer. If the cell is a function, overwrite it with 255
`.`	| Output the character signified by the cell at the pointer if it is a byte, otherwise executes the function at the pointer as if it were a set of ordinary BF commands
`,`	| Input a character and store it in the cell at the pointer
`[`	| Jump past the matching `]` if the cell at the pointer is 0 (functions are considered to be nonzero)
`]`	| Jump back to the matching `[` if the cell at the pointer is nonzero
`{` | Indicates the start of a function. Functions are treated as objects and stored in the memory
`}` | Indicates the end of a function. Within functions, special rules apply to the `.` and `,` commands
`(` | Indicates the start of a function call. Within function calls, special rules apply to the `.` and `,` commands
`)` | Indicates the end of a function call
`\|` | Used within a function call to separate handling the function call and handling the return values
`#` | Used to pause the the interpretation of code for debugging purposes

## Defining a Function
Functions are wrapped with curly brackets: `{}`.

Code stored inside uses its own local memory space, or local scope.

Functions can't interact with the console - they can only take parameters and return values. The only exception to this rule is with the `.` command, which we'll elaborate on later.

### Taking Parameters
Parameters are input into the function with `,`.

There is no limit to the number of parameters accepted by the function, they can even be accepted dynamically using code such as this: 

```BF
{->,[->+>+<<]>>[-<<+>>]<-[[->+<]>-]+[,<+]}
```

In which the first argument decides how many parameters will be required by the function.

Since functions have their own local scope, `,` determines where arguments are stored in the function's scope, as if the function were a normal piece of BF code and the arguments were `stdin`.

### Returning values (or functions)
Functions can return values with `.`.

Much like with the parameters, any number of values can be output and this is done so dynamically. For example, by modifying our code from above, we can do this:

```BF
{->,[->+>+<<]>>[-<<+>>]<-[[->+<]>-]+[,+.<+]}
```

In which each parameter other than the first (which determines the number of parameters) is incremented by 1 and then returned.

## Calling Functions
Functions are stored in the memory in the same manner as bytes and can be called using circular brackets: `()`.

Code within the circular brackets determines how parameters are passed to the function and how returned values are stored

Function calls (code wrapped in circular braces) can't interact with the console - they can only pass parameters to the function and handle return values. They can however access modular memory (but not the function's local memory) to pass parameters and store returned values.

### Passing Arguments
Arguments are passed to the function call with `.`.

Arguments can be passed dynamically to the function much like they are retrieved. For example, making use of our function from earlier:

```BF
{->,[->+>+<<]>>[-<<+>>]<-[[->+<]>-]+[,<+]}>+++>+>+>+<<<<(>.>[.>])
```

This code simply stores the function, 3, 1, 1 and 1 in the memory. Then the function is called and the first argument is introduced `3`. This parameter tells the function how many more arguments to accept (3). The function call loops through the modular memory and passes every value in the (not yet) covered memory to the function till it hits 0. There are 3 more values in the memory till 0, the exact number of values our function demands, so these values (1, 1 and 1) are passed to the function.

Functions are not stored in each others' local scopes, however they can accept themselves and other functions as parameters, allowing for callback functions and recursion (I dare you to make use of this reader).

If too many or too few parameters are passed to the function, an error will be raised. Also, note, unless you hope to use recursion within the program, don't pass the value at the cell the pointer is at at the start of the function call. For example, if you wish to pass 0 as an argument, don't do `(.)`, as this will pass the function to itself as a parameter. This quite obvious and an intended feature, but at times also easy to forget about, resulting in some unusual bugs. Suitable alternatives could be `(>[-].<)`. You may also choose to do `(+-.)` but this will erase the function from memory and prevent it's further use. Note that the function will continue to run even after it has been destroyed, but at the end of the function call it will cease to exist (unless you've stored a copy elsewhere).

### Handling Returns
Returned values are retrieved from the function with `,`.

As with every other feature of BF functions, returned values are handled with their own little snippet of BF code which allows the most control over data that BF has to offer. For example:

```BF
{->,[->+>+<<]>>[-<<+>>]<-[[->+<]>-]+[,+.<+]}>+++>+>+>+<<<<(>.>[.>]+[>,])
```

Basically, returned values are saved in their own little memory space/array which is appended to by the function each time `.` is used within the function and is stored to modular memory each time `,` is used within the function call. Each time a returned value is pulled from the function, the pointer of the returned array is incremented by one, and the next time `,` is used within the function call, the next returned value is pulled. Not all returned values have to be pulled and if there are more pulls than returns, 0 gets pulled. So if (in this example) the fourth returned value is requested but only 3 values are returned by the function, the fourth value returned will be 0. In our example, this will end the loop, so all values returned by the function (1,1,1) will be saved to the modular memory till one of these values is 0.

Returned values can replace a function in the memory and the function will still run. The function will only cease to exist after the function call is complete. However note that the function will not exist in the modular memory, so it will not be callable again within the function call and it can't be passed to the function as a parameter (allowing recursion) if it is deleted first.

Evaluation of the function call is handled somewhat lazily but also in a weird fashion, so function calls are executed twice. In the first execution returned values are ignored and only parameters are taken into account and evaluated. It is, of, course, ensured that none of the parameters is a manipulation of a returned value from the function (as this would result in unexpected behaviour) by raising an error in this scenario. In the second evaluation, parameters are ignored and only returned values are evaluated.

Though you have the option to do some disgusting function calls, such as `(.,<,>>.<<.)` or something of the sort, please do not. It is recommended to pass all arguments to the function within the call before handling returns. If it increases functionality not to do so then go ahead, but for the sake of your own mental health it is not recommended. After all, this is BrainFunctional not BF.

## Other Commands
Functions can be called when the pointer is on their location in the memory, however, if they are not called and rather normal BF operations are performed on them then other things happen.

If the pointer is on a function and rather than calling this function, `.` is used to output the function, then the function is evaluated on the spot as if it were a normal piece of code. This means that rather than `,` (from inside the function) being an input for a parameter, `,` is used as an input from the console. Similarly, `.` (from within the function) will not serve to return values (or functions) but instead will output values to the console. The function will also not use it's own local scope and will instead access modular memory for that one evaluation, resulting in potentially buggy code if `.` is used instead of a function call and data in the memory is overwritten.

Functions are detected by `[` and `]` as not being equal to zero.

Taking inputs at a modular level with `,` in a cell where a function exists will overwrite the function, replacing it with data input by the user.

### Moving and Deleting Functions
`+` and `-` overwrite (therefore deleting) functions from the memory. When `+` or `-` act on the function, it is treated as an empty cell, so `+` replaced the function with 1 and `-` replaces it with 255.

We can use one function to move another in the memory. This mechanic works due to the way functions allow us to return functions as objects and input them in function calls.

Here's an example of these two techniques:
```BF
{,[->+>+<<]>[->+<]>.} This function returns the double of a given parameter
>{,.} This function allows us to return a function and store it wherever is needed
(<.-+>-+,) This function call copies the first funtion, deletes both functions and then moves the first function to the second cell
```

In this example, we used `{,.}`, which allows us to copy the input function. However, `{,.}` only returns one value, meaning that it can only produce one copy of a function if used once. To copy a function an unlimited number of times, it is recommended to use:
```BF
{,[.]}
```
Which yields as many copies of the functions as the player wishes to accept with the function call.

### Decorators
Decorators. An uncharacteristically high-level idea for BF, and probably a bad one too. In the case of BrainFunctional, if a function is written on top of another function, that function serves to decorate the original function.

When one function is written on top of another, each time the resulting function is called only the top layer function is called, but the top function is modified in the sense that it's first few parameter are replaced by the returned values of the function it decorates. The decorated function's parameters are input first. What we get is a combination of both functions. So if we have one function that doubles a number:

```BF
{,[->+>+<<]>[->+<]>.}
```

and another function on top of this that triples a given argument

```BF
{,[->+>+>+<<<]>[->+<]>[->+<]>.}
```

then these functions chained together with the tripling function on top will look like this

```BF
{,[->+>+<<]>[->+<]>.}{,[->+>+>+<<<]>[->+<]>[->+<]>.}
```

Our new function will calculate the triple of the values returned by our doubling function, so together they will return a given argument multiplied by 6.

_The total number of parameters given to the decorated function =
the number of parameters accepted by the original function - the number of values the original function returns + the number parameters for the decorator._

I will now translate the [geeksforgeeks python decorators example](https://www.geeksforgeeks.org/decorators-in-python/) using BrainFunctional instead.

<u>Python 3</u>:
```python
def hello_decorator(func):
    def inner1(*args, **kwargs):
         
        print("before Execution")
         
        # getting the returned value
        returned_value = func(*args, **kwargs)
        print("after Execution")
         
        # returning the value to the original frame
        return returned_value
         
    return inner1
 
 
# adding decorator to the function
@hello_decorator
def sum_two_numbers(a, b):
    print("Inside the function")
    return a + b
 
a, b = 1, 2
 
# getting the value through return of the function
print("Sum =", sum_two_numbers(a, b))
```

<u>BrainFunctional</u>:
```BF
{,>,[-<+>]<.} sum_two_numbers 
>--[----->+<]>---- "b" we can use - on this to convert it to "a"
Because this is BF, I will not store the strings "before Execution" and "after Execution", but will denote them with "b" and "a" instead. This letter will also be input to the hello decorator function for simplicity's sake.

<{,>,.<.>-.} @hello_decorator
Here we create the hello decorator function and since it is on top of the sum_two_numbers function, it automatically decorates it. To create hello_decorator as an individual function, it needs to be stored elsewhere in the memory and cloned onto sum_two_numbers.

(+.+.>.,>,>,)<<.>.>.
Outputs the decorated function taking 1 and 2 as parameters.
The python equivalent of this would be: print(sum_two_numbers(1, 2))
```

Here's an example of BF code with a few more caveats and including the movement of functions, giving us a practical use for decorators:
```BF
{,>,[-<+>]<.} sum_two_numbers 
>--[----->+<]>---- "b" we can use minus on this to convert it to "a"
Because this is BF I will not store the strings "before Execution" and "after Execution" but will denote them with "b" and "a" instead
This letter will also be input to the hello decorator function for simplicity's sake

>{+[>>>,]<<<[<<<]>>>->>>[[->+>+<<]>[->+<]>.>]} doubler
Accepts an unlimited number of parameters till a given parameter is equal to 0 and then returns the double of all parameters given

>{,>,.<.>-.} hello_decorator
<{,[.]}(>.<,<<,)
Clones hello_decorator on top of sum_two_numbers and doubler causing it to act as a decorator for both

(<+.+.-->>.<<,<,<,)>>.<.<.
Calls sum_two numbers after its been decorated taking 1 and 2 as parameters
The returned values are stored in the memory and output printing "b3a" to the console

>>>>>(>>+++++.-----.<<<.>>>,>,>,)<<.>.>.
Calls doubler after its been decorated taking 5 and 0 as parameters
The 0 tells doubler to stop taking parameters
The returned values are stored in the memory and output printing "b10a" to the console

Note that in this example "3" and "10" won't really be output due to the way outputs are handled in BF
Instead #000003 and #00000A will be output
Both are not actually characters, so nothing will be output but I commented "3" and "10" for simplicity's sake
```

## Thoughts and Concerns
The implementation of decorators is, I feel, a rocky idea, since decorators are a higher level concept used in object oriented programming. BF is most definitely not high-level or object oriented, though functions are considered as objects in brainfunc and are handled in a way that is at least somewhat object oriented. But including decorators when there isn't even an implementation for classes? Of course, implementing classes to BF will change the language immeasurably and completely break away from it. Class objects are probably the most unBFy idea anyone could come up with, so there is no way BrainFunctional will include them or anything similar.

The pros of implementing decorators is that - unlike in other languages where they don't serve too much purpose (and are a little like syntactic sugar) - in BrainFunctional (due to the low-level handling of functions), decorators actually serve a unique role, and without their existence there is no real way to implement what they do in a versatile and dynamic manner. Therefore I feel like they have to stay.

The syntax for decorators however is not as clear of a concept. Decorators are designed in BF in such a way that they can be used as decorators but also as normal functions. However from this a massive conflict occurs in the handling of parameters and returned values in decorated functions. This is probably my second biggest concern here.

The decorator, when used as a decorator, handles the top level of parameters and returns. Its first argument is ignored and is instead considered to be the decorated function (bottom-level function) as it is being run. So our `hello_decorator` function from above takes 2 arguments, the first being the function it decorates or the value it wraps with `"b"` and `"a"`. The second argument is the letter `"b"` (or potentially another letter), allowing the function to surround an output with a before and an after. In the examples I gave, all the functions wrapped by `hello_decorator` only returned one value which could easily be taken as the argument `hello_decorator` has to surround. But what if there were multiple outputs from the base function? Would `hello_decorator` take one input for each output from the base function? This seems like the only way to handle our situation. But this restricts the use of `hello_decorator` as both a function and decorator, since the programmer will have to know how many values hello decorator takes from a base function. This means that it may have to be designed as a custom decorator for a single function, therefore, in a way, destroying the need for a decorator in the first place.

Decorator functions in our implementation do take one input for each output from the decorated function, resulting in the formula above:
_The total number of parameters given to the decorated function =
the number of parameters accepted by the original function - the number of values the original function returns + the number of parameters for the decorator_

Taking a variable number of parameters till one of these paramters is 0 seems to be the solution that covers all fronts of this problem, but doing that is a) up to the programmer, and b) not very BFy. Still, it seems with the current brainfunc decorator implementation, that is the way to go. This does bring up our next problem though, which is a problem already present in normal BF iteration but amplified in the case of BrainFunctional functions.

If inputs and outputs for a function are controlled dynamically, based on `stdin` from the user, then the existence of 0 as a parameter or returned value from a function can break the overall handling of functions. BF iteration is designed to keep going till it hits 0, and usually this 0 signals the end of a data stream. This idea is very much the case with function parameters and returns, where, for a function to take and give an unkown quantity of data, it will have to loop in some way and this loop will inevitably be broken when it hits 0. But what if the 0 does not signal an end but rather is part of the data? In that case, you are doomed. This is a problem that is present in normal BF already but is just made so much more deadly.

The solution? The only possible, complete solution on the brainfunc side would be the implementation of a new kind of iteration, or more rigid, high-level parameter passing and returning system. Both of these options are just not happening. So programmers, you have to find ways to deal with data containing 0 and minimise this phenomenon.

This is my final concern. Its one which is strickingly obvious to anyone who's read this far. Other than with the use of `.` on functions (a feature which has a relatively high likelyhood of being deleted) functions cannot meddle with mudular memory or the modular pointer. I doubt this will change, but it also stands as a major reason to continue with the use of `.` as a way to call functions.

I am open to input on suggestions or criticisms, so please tell me what you think works best. In the form of BF, I am 

```BF
,[>,]
```

**Note: I have since implemented key changes to the syntax, which is not reflected in this README, so I will update this guide in the future.**
