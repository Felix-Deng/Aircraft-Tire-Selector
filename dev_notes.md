# Notes on Development 

Table of Content: 
- [Code commenting style](#code-commenting-style)
- [SOLID principle for OOP](#solid-principles-for-object-oriented-programming-oop)

## Code commenting style

Make sure the "autoDocstring - Python Docstring Generator" extension is added to your VS Code. 

After writing a Python function (including the function definition and the return statement), type `"""` after the function definition, a docstring format will be automatically generated with fields for you to fill out. 

A sample can be found in the `sample.py`. 

## SOLID principles for object-oriented programming (OOP) 

More detailed explainations [here](https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design). 

- S: single-responsibility principle 
    - *Formal def*: A class should have one and only one reason to change, meaning that a class should have only one job. 
    - *Alternative def*: One function should only be built for one task. If more jobs need to be done, considering building additional functions. 
- O: open-closed principle 
    - *Formal def*: Objects or entities should be open for extension but closed for modification.
    - *Alternative def*: If the same property/function is required for multiple classes, add them to individual classes, but avoid adding endless if statements to one external function. 
- L: Liskov substitution principle 
    - *Formal def*: Let $q(x)$ be a property provable about objects of $x$ of type $T$. Then $q(y)$ should be provable for objects $y$ of type $S$ where $S$ is a subtype of $T$.
    - *Alternative def*: Every subclass/subfunction or derived class/function should be substitutable for their base or parent class/function
- I: interface segregation principle 
    - *Formal def*: A client should never be forced to implement an interface that it doesn’t use, or clients shouldn’t be forced to depend on methods they do not use.
    - *Alternative def*: Do not force a function/class to include unnecessary components, simply because other functions/classes have them. 
- D: dependency inversion principle 
    - *Formal def*: Entities must depend on abstractions, not on concretions. It states that the high-level module must not depend on the low-level module, but they should depend on abstractions.
    - *Alternative def*: When inheriting dependency, functions/classes should depend on abstraction. 