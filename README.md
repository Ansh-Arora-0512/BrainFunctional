# BrainFunctional
Another Brainfuck derivative. But also so much more.

Do you love brainfuck but also never use it because you value your braincells? Well worry not, the solution to all your problems is here.

We bring to you simple, scalable brainfuck! Ok no. That was a lie to get your attention. But it worked didn't it? I mean if you're reading this it either worked or you're mentally deranged. Probably from too much brainfuck. That is a problem we will fix.

## What is it?
Brainfuck but with functions.

If you have no idea what brainfuck is but for some reason are still reading this, here is a [wikepedia article]([url](https://en.wikipedia.org/wiki/Brainfuck)) explaining the fundamentals of the esoteric programming language. I will not be exploring how to use brainfuck or going over it in this guide, so if you don't understand some of the examples given or want another guide on the language, here is a [tutorial]([url](https://gist.github.com/roachhd/dce54bec8ba55fb17d3a)) by @roachhd, which covers some of the fundamentals quite well.

The syntax is minimalistic, simple and impractical, following the fundamentals of the language.

However, unlike many features of brainfuck, it is a powerful and versatile tool which makes the language more high level. Not a lot more, but it actually allows you to solve more complex problems with brainfuck, in a style that is still quintessential brainfuck. Not brainfucking bad if I'd say so myself.

So let's jump into the syntax.

## The Commands
This table provides a very basic overview of the 12 commands involved (including the 8 commands from original brainfuck), so for a more in-depth guide and in order to understand the exact behaviour of each command, keep reading.

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


## Defining a Function
Functions are wrapped with curly brackets: `{}`

Code stored inside uses its own local memory space, or local scope.

Functions can't interact with the console - they can only take parameters and return values. The only exception to this rule is with the `.` command, which we'll elaborate on later.

### Taking Parameters
Parameters are input into the function with `,`

There is no limit to the number of parameters accepted by the function, they can even be accepted dynamically using code such as this: 

```{->,[->+>+<<]>>[-<<+>>]<-[[->+<]>-]+[,<+]}```

In which the first parameter decides how many parameters will be required by the function.

Since functions have their own local scope, `,` determines where parameters are stored in the function, as if the function were a normal piece of brainfuck code and the parameters were `stdin`.

