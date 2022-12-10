# BrainFunctional
Another Brainfuck derivative. But also so much more.

Do you love brainfuck but also never use it because you value your braincells? Well worry not, the solution to all your problems is here.

We bring to you simple, scalable brainfuck! Ok no. That was a lie to get your attention. But it worked didn't it? I mean if you're reading this it either worked or you're mentally deranged. Probably from too much brainfuck. That is a problem we will fix.

## What is it?
Brainfuck but with functions.

If you have no idea what brainfuck is but for some reason are still reading this, here is a [wikepedia article](https://en.wikipedia.org/wiki/Brainfuck) explaining the fundamentals of the esoteric programming language. I will not be exploring how to use brainfuck or going over it in this guide, so if you don't understand some of the examples given or want another guide on the language, here is a [tutorial](https://gist.github.com/roachhd/dce54bec8ba55fb17d3a) by @roachhd, which covers some of the fundamentals quite well.

The syntax is minimalistic, simple and impractical, following the fundamentals of the language.

However, unlike many features of brainfuck, it is a powerful and versatile tool which makes the language more high level. Not a lot more, but it actually allows you to solve more complex problems with brainfuck, in a style that is still quintessential brainfuck. Not brainfucking bad if I'd say so myself.

So let's jump into the syntax.

By the way, if you haven't figured it out yet, the only reason I use the horrible name "BrainFunctional" is because [Brainfunc](https://esolangs.org/wiki/Brainfunc) and [Brainfunction](https://github.com/ryanfox/brainfunction) already exist.

## The Commands
This table provides a very basic overview of the 14 commands involved (including the 8 commands from original brainfuck), so for a more in-depth guide and in order to understand the exact behaviour of each command, keep reading.

Command | Description
--- | ---
`>` |	Move the pointer to the right
`<`	| Move the pointer to the left
`+` | Increment the memory cell at the pointer if it is a byte, otherwise decorates the function at the pointer by incrementing the values returned
`-`	| Decrement the memory cell at the pointer if it is a byte, otherwise decorates the function at the pointer by decrementing the values returned
`.`	| Output the character signified by the cell at the pointer if it is a byte, otherwise executes the function at the pointer as if it were a set of ordinary brainfuck commands
`,`	| Input a character and store it in the cell at the pointer
`[`	| Jump past the matching `]` if the cell at the pointer is 0 (functions are considered to be nonzero)
`]`	| Jump back to the matching `[` if the cell at the pointer is nonzero
`{` | Indicates the start of a function. Functions are treated as objects and stored in the memory
`}` | Indicates the end of a function. Within functions, special rules apply to the `.` and `,` commands
`(` | Indicates the start of a function call. Within function calls, special rules apply to the `.` and `,` commands
`)` | Indicates the end of a function call
`/` | "Cuts" a function, deleting it and allowing it to be moved elsewhere in the memory
`*` | "Pastes" a function, allowing it to be stored in that position in the cell at the pointer

## Defining a Function
Functions are wrapped with curly brackets: `{}`.

Code stored inside uses its own local memory space, or local scope.

Functions can't interact with the console - they can only take parameters and return values. The only exception to this rule is with the `.` command, which we'll elaborate on later.

### Taking Parameters
Parameters are input into the function with `,`.

There is no limit to the number of parameters accepted by the function, they can even be accepted dynamically using code such as this: 

```{->,[->+>+<<]>>[-<<+>>]<-[[->+<]>-]+[,<+]}```

In which the first argument decides how many parameters will be required by the function.

Since functions have their own local scope, `,` determines where arguments are stored in the function's scope, as if the function were a normal piece of brainfuck code and the arguments were `stdin`.

### Returning values (or functions)
Functions can return values with `.`.

Much like with the parameters, any number of values can be output and this is done so dynamically. For example, by modifying our code from above, we can do this:

```{->,[->+>+<<]>>[-<<+>>]<-[[->+<]>-]+[,+.<+]}```

In which each parameter other than the first (which determines the number of parameters) is incremented by 1 and then returned.

## Calling Functions
Functions are stored in the memory like bytes and can be called using circular brackets: `()`.

Code within the circular brackets determines how parameters are passed to the function and how returned values are stored

Function calls (code wrapped in circular braces) can't interact with the console - they can only pass parameters to the function and handle return values. They can however access modular memory (but not the function's local memory) to pass parameters and store returned values.

### Passing Arguments
Arguments are passed to the function call with `.`.

Arguments can be passed dynamically to the function much like they are retrieved. For example, making use of our function from earlier:

```{->,[->+>+<<]>>[-<<+>>]<-[[->+<]>-]+[,<+]}>+++>+>+>+<<<<(>.>[.>])```

This code simply stores the function, 3, 1, 1 and 1 in the memory. Then the function is called and the first argument is introduced `3`. This parameter tells the function how many more arguments to accept (3). The function call loops through the modular memory and passes every value in the (not yet) covered memory to the function till it hits 0. There are 3 more values in the memory till 0, the exact number of values our function demands, so these values (1, 1 and 1) are passed to the function.

Functions are not stored in each others' local scopes, however they can accept themselves and other functions as parameters, allowing for callback functions and recursion (I dare you to make use of this reader).

If too many or too few parameters are passed to the function, an error will be raised. Also, note, unless you hope to use recursion within the program, don't pass the value at the cell the pointer is at at the start of the function call. For example, if you wish to pass 1 as an argument, don't do `(+.)`, as this will pass a decorated version of the function to itself as a parameter. This quite obvious and an intended feature, but at times also easy to forget about, resulting in some unusual bugs.

### Handling Returns
Returned values are retrieved from the function with `,`.

As with every other feature of brainfuck functions, returned values are handled with their own little snippet of brainfuck code which allows the most control over data that brainfuck has to offer. For example:

```{->,[->+>+<<]>>[-<<+>>]<-[[->+<]>-]+[,+.<+]}}>+++>+>+>+<<<<(>.>[.>]+[>,])```

Basically, returned values are saved in their own little memory space/array which is appended to by the function each time `.` is used within the function and is stored to modular memory each time `,` is used within the function call. Each time a returned value is pulled from the function, the pointer of the returned array is incremented by one, and the next time `,` is used within the function call, the next returned value is pulled. Not all returned values have to be pulled and if there are more pulls than returns, 0 gets pulled. So if (in this example) the fourth returned value is requested but only 3 values are returned by the function, the fourth value returned will be 0. In our example, this will end the loop, so all values returned by the function (1,1,1) will be saved to the modular memory till one of these values is 0.

Returned values can replace a function in the memory and the function will still run. The function will only cease to exist after the function call is complete. However note that the function will not exist in the modular memory, so it will not be callable again within the function call and it can't be passed to the function as a parameter (allowing recursion) if it is deleted first.

Evaluation of the function call is handled somewhat lazily but also in a weird fashion, so function calls are executed twice. In the first execution returned values are ignored and only parameters are taken into account and evaluated. It is, of, course, ensured that none of the parameters is a manipulation of a returned value from the function (as this would result in unexpected behaviour) by raising an error in this scenario. In the second evaluation, parameters are ignored and only returned values are evaluated.

Though you have the option to do some disgusting function calls, such as `(.,<,>>.<<.)` or something of the sort, please do not. It is recommended to pass all arguments to the function within the call before handling returns. If it increases functionality not to do so then go ahead, but for the sake of your own mental health it is not recommended. After all, this is BrainFunctional not Brainfuck.

## Other Commands
Functions can be called when the pointer is on their location in the memory, however, if they are not called and rather normal brainfuck operations are performed on them then other things happen.

If the pointer is on a function and rather than calling this function, `.` is used to output the function, then the function is evaluated on the spot as if it were a normal piece of code. This means that rather than `,` (from inside the function) being an input for a parameter, `,` is used as an input from the console. Similarly, `.` (from within the function) will not serve to return values (or functions) but instead will output values to the console. The function will also not use it's own local scope and will instead access modular memory for that one evaluation, resulting in potentially buggy code if `.` is used instead of a function call and data in the memory is overwritten.

Functions are detected by `[` and `]` as not being equal to zero.

Taking inputs at a modular level with `,` in a cell where a function exists will overwrite the function, replacing it with data input by the user.

### Decorators
`+` and `-` can serve somewhat as decorators for the function, in the sense that they modify the values returned by the function. `+` being used on a function (not a function call, remember) means that later when a function is called, `+` will be used on every value returned by a function. So, for example, we have a function that returns 1, 2 and 3. Using `+` on this function means that when its called, it will return 2, 3 and 4 instead. Below is a demonstration.

```{+.>++.>+++.}+```

`-` does the same as `+` when acting on a function, but it subtracts 1 instead of adding 1.

The real use of this decorator idea is when functions are used to decorate other functions, as is the case in higher level languages. In the case of BrainFunctional, if a function is written on top of another function, that function serves to decorate the original function.

When one function is written on top of another, each time the resulting function is called only the top layer function is called, but the top function is modified in the sense that it's first few parameter are replaced by the returned values of the function it decorates. The decorated function's parameters are input first. What we get is a combination of both functions. So if we have one function that doubles a number:

```{,[->+>+<<]>[->+<]>.}```

and another function on top of this that triples a given argument

```{,[->+>+>+<<<]>[->+<]>[->+<]>.}```

then these functions chained together with the tripling function on top will look like this

```{,[->+>+<<]>[->+<]>.}{,[->+>+>+<<<]>[->+<]>[->+<]>.}```
Our new function will calculate the triple of the values returned by our doubling function, so together they will return a given argument multiplied by 6.

_The total number of parameters given to the decorated function =
the number of parameters accepted by the decorated function - the number of values the decorated function returns + the number parameters for the decorator._

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
```
{,>,[-<+>]<.} sum_two_numbers 
>--[----->+<]>---- "b" we can use - on this to convert it to "a"
Because this is brainfuck, I will not store the strings "before Execution" and "after Execution", but will denote them with "b" and "a" instead. This letter will also be input to the hello decorator function for simplicity's sake.

<{,>,.<.>-.} @hello_decorator
Here we create the hello decorator function and since it is on top of the sum_two_numbers function, it automatically decorates it. To create hello_decorator as an individual function, it needs to be stored elsewhere in the memory and cloned onto sum_two_numbers.

(+.+.>.,>,>,)<<.>.>.
Outputs the decorated function taking 1 and 2 as parameters.
The python equivalent of this would be: print(sum_two_numbers(1, 2))
```

### Moving Functions in the Memory
As you can see, the BrainFunctional version is a lot more simple and concise but with more brainfucking potential. Of course, you're not really going to be able to chain decorators or reuse decorators or use them practically using the methods shown above, since the decorator doesn't exist as a separate function in the memory - it is simply written on top of our original function to form a combination of the 2.

To move functions around in the memory, I propose a copy-paste like mechanism with `/` being used to cut a function (delete it and copy it to a clipboard of sorts where it can be pasted to any other space in the memory at any time) and `*` to paste a function (place a function from the clipboard onto a spot in the memory as if the code for that function had been written there).

Note that if one function is cut and then another is function is cut, the first function will be overwritten in (therefore removed from) the clipboard

Here is the example from above rewritten so that the hello_decorator decorator can also be used on a function to double inputs (called doubler):

```bf
{,>,[-<+>]<.} sum_two_numbers 
>--[----->+<]>---- "b" we can use - on this to convert it to "a"
Because this is brainfuck, I will not store the strings "before Execution" and "after Execution", but will denote them with "b" and "a" instead. This letter will also be input to the hello decorator function for simplicity's sake.

>{+[>>>,]<<<[<<<]>>>->>>[[->+>+<<]>[->+<]>.>]} doubler
Accepts an unlimited number of parameters till a given parameter is equal to 0, and then returns the double of all parameters given

>{,>,.<.>-.} hello_decorator
/*<*<<*
Clones hello_decorator on top of sum_two_numbers and doubler, causing it to act as a decorator for both

(<+.+.-->>.<<,<,<,)>>.<.<.
Calls sum_two numbers (after its been decorated), taking 1 and 2 as parameters. 
The returned values are stored in the memory and output, printing "b3a" to the console.

>>>>>(>>+++++.-----.<<<.>>>,>,>,)<<.>.>.
Calls doubler (after its been decorated), taking 5 and 0 as parameters (the 0 tells doubler to stop taking parameters).
The returned values are stored in the memory and output, printing "b10a" to the console.

Note that in this example "3" and "10" won't really be output due to the way outputs are handled in brainfuck. Instead chr(3) (the third character on the ascii table) and chr(10) (the tenth character on the ascii table) will be output (both chr(3) and chr(10) are not actually characters, so nothing will be output), but I commented "3" and "10" for simplicity's sake.
```

## Thoughts and Concerns
The interactions of `.`, `-` and `+` with functions is an idea I am unsure of. It adds to the versatility of functions and makes them more interactive, but it feels quintessentially unbrainfucky (yes I just made that word up). This feeling arises from the idea that the base brainfuck funtions can perform 2 completely different tasks. This idea just doesn't sit well with classic brainfuck. This is my biggest concern.

2 other alternatives could be that these operations do nothing when acting on a functions, or that they raise an error.

The overall implementation of decorators is a rocky idea, since decorators are a higher level concept used in object oriented programming. Brainfuck is most definitely not high-level or object oriented, though functions are considered as objects in brainfunc and are handled in a way that is at least somewhat object oriented. But including decorators when there isn't even an implementation for classes? Of course, implementing classes to brainfuck will change the language immeasurably and completely break away from it. Class objects are probably the most unbrainfucky idea anyone could come up with, so there is no way BrainFunctional will include them or anything similar.

The pros of implementing decorators is that - unlike in other languages where they don't serve too much purpose (and are a little like syntactic sugar) - in BrainFunctional (due to the low-level handling of functions), decorators actually serve a unique role, and without their existence there is no real way to implement what they do in a versatile and dynamic manner. Therefore I feel like they have to stay.

The syntax for decorators however is not as clear of a concept. Decorators are designed in brainfuck in such a way that they can be used as decorators but also as normal functions. However from this a massive conflict occurs in the handling of parameters and returned values in decorated functions. This is probably my second biggest concern here.

The decorator, when used as a decorator, handles the top level of parameters and returns. Its first argument is ignored and is instead considered to be the decorated function (bottom-level function) as it is being run. So our `hello_decorator` function from above takes 2 arguments, the first being the function it decorates or the value it wraps with `"b"` and `"a"`. The second argument is the letter `"b"` (or potentially another letter), allowing the function to surround an output with a before and an after. In the examples I gave, all the functions wrapped by `hello_decorator` only returned one value which could easily be taken as the argument `hello_decorator` has to surround. But what if there were multiple outputs from the base function? Would `hello_decorator` take one input for each output from the base function? This seems like the only way to handle our situation. But this restricts the use of `hello_decorator` as both a function and decorator, since the programmer will have to know how many values hello decorator takes from a base function. This means that it may have to be designed as a custom decorator for a single function, therefore, in a way, destroying the need for a decorator in the first place.

Decorator functions in our implementation do take one input for each output from the decorated function, resulting in the formula above:
_The total number of parameters given to the decorated function =
the number of parameters accepted by the decorated function - the number of values the decorated function returns + the number of parameters for the decorator_

Taking a variable number of parameters till one of these paramters is 0 seems to be the solution that covers all fronts of this problem, but doing that is a) up to the programmer, and b) not very brainfucky. Still, it seems with the current brainfunc decorator implementation, that is the way to go. This does bring up our next problem though, which is a problem already present in normal brainfuck iteration but amplified in the case of BrainFunctional functions.

If inputs and outputs for a function are controlled dynamically, based on `stdin` from the user, then the existence of 0 as a parameter or returned value from a function can break the overall handling of functions. Brainfuck iteration is designed to keep going till it hits 0, and usually this 0 signals the end of a data stream. This idea is very much the case with function parameters and returns, where, for a function to take and give an unkown quantity of data, it will have to loop in some way and this loop will inevitably be broken when it hits 0. But what if the 0 does not signal an end but rather is part of the data? In that case, you are doomed. This is a problem that is present in normal brainfuck already but is just made so much more deadly.

The solution? The only possible, complete solution on the brainfunc side would be the implementation of a new kind of iteration, or more rigid, high-level parameter passing and returning system. Both of these options are just not happening. So programmers, you have to find ways to deal with data containing 0 and minimise this phenomenon.

This is my final concern. Its one which is strickingly obvious to anyone who's read this far. Other than with the use of `.` on functions (a feature which has a relatively high likelyhood of being deleted) functions cannot meddle with mudular memory or the modular pointer. I doubt this will change, but it also stands as a major reason to continue with the use of `.` as a way to call functions.

I am open to input on suggestions or criticisms, so please tell me what you think works best. In the form of brainfuck, I am `,[>,]`
