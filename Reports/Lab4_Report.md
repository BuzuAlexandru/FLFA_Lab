# Laboratory work nr.4
# Chomsky Normal Form
### University: Technical University of Moldova
### Course: Formal Languages & Finite Automata
### Author: Alexandru Buzu, FAF 212 (variant 4)

---

## Objectives:
1. Learn about Chomsky Normal Form (CNF).
2. Get familiar with the approaches of normalizing a grammar.
3. Implement a method for normalizing an input grammar by the rules of CNF.
    1. The implementation needs to be encapsulated in a method with an appropriate signature (also ideally in an appropriate class/type).
    2. The implemented functionality needs executed and tested.
    3. A BONUS point will be given for the student who will have unit tests that validate the functionality of the project.
    4. Also, another BONUS point would be given if the student will make the aforementioned function to accept any grammar, not only the one from the student's variant.

## Implementation description
For the purpose of this laboratory work, I added a new method to the already existing
`Grammar` class. The method is aptly named `ChomskyNormalForm()` and it returns
a `Grammar` object. It additionally has a keyword argument `show_proccess`, that
is by default `False`, but when set to `True`, it will print the production rules
after each step of the grammar normalization.

The method is generic and works for grammars of any shape as long as they don't 
have hundreds of production rules, which would make the function run out of letters of
alphabet to assign to new rules.

To start, a copy of the non-terminal symbols is made and the list of `Production`
objects is transformed into a python dictionary using the `productionToDict()` method,
where the left side of production is the key, and the value is a python set with the
right side of the productions which in code is referenced as `rule` for each 
individual right side, or `rules` for the entire set.
```python
def ChomskyNormalForm(self, show_proccess = False):
  prod = self.productionToDict()
  vn = self.nonTerminalVar.copy()
```
### 1. Removing ε-productions
To remove empty productions, the method iterates through all production rules,
if it finds an empty one, it iterates through all of them once more while keeping track
of the left side symbol where epsilon was found, and if it finds that symbol in a right side
of a rule, then it passes them to the `createCombinations()` function along with the
left side where the right side was found. The productions dict is then updated using 
the `updateProductions()` method and the epsilon rule is removed.
```python
 for leftSide in prod.keys():
   for rule in prod[leftSide]:
       if rule == 'ε':
           for leftSide1 in prod.keys():
               for rule1 in prod[leftSide1]:
                   if len(rule1) > 1 and rule1.find(leftSide) != -1:
                       createCombinations(rule1, leftSide1, leftSide)
           updateProductions()
           prod[leftSide].discard('ε')
           break
```
The `createCombinations()` function gets passed the right side that contains the
empty production symbol, the left side that has the mentioned right side, and the
empty production symbol itself. The function then creates all the combinations from
the right side, that would allow the removal of the empty production while keeping
the original functionality of the grammar. It first creates a string with only the
symbols that are non-empty, then creates combinations of characters of different
lengths from the original string, and discards the ones that don't contain the 
non-empty symbols, while keeping the other ones, for example:
```text
B -> ε
A -> bBAB
combinations = [BA, bB, bA, BB, AB, bAB, bBB, bBA, BAB]
```
In this case `non-empty symbols = 'bA'` and the kept combinations are `[bA, bAB, bBA]`.

The combinations are then added to an auxiliary dictionary.
```python
    def createCombinations(prod_rule, leftSide, empty):
      new_rules = set()
      non_empty_symbols = prod_rule.replace(empty, '')
      for i in range(len(non_empty_symbols), len(prod_rule)):
          all_combinations = set(combinations(prod_rule, i))
          for combination in all_combinations:
              test = list((Counter(list(non_empty_symbols)) & Counter(list(combination))).elements())
              if test == list(non_empty_symbols):
                  new_rules.add(''.join(combination))
   
      if leftSide in aux.keys():
          aux[leftSide].update(new_rules)
      else:
          aux[leftSide] = new_rules
```
And the `updateProductions()` method takes the created combinations from the
auxiliary dict, and adds them to the original productions dict.
```python
  def updateProductions():
      for leftSide in prod.keys():
          for key in aux.keys():
              if leftSide == key:
                  prod[leftSide].update(aux[key])
```
### 2. Removing unit productions
For the purpose of removing unit production, I created a function called `hasUnitProductions()`
that iterates through the production rules, and if it finds a rule of the form
`A -> B`, it returns `True`.
```python
  def hasUnitProductions(prod_dict):
      for leftSide in prod.keys():
          for rule in prod[leftSide]:
              if rule in self.nonTerminalVar:
                  return True
      return False
```
For the next part, unit productions are removed one by one while they exist in the 
production rules. If a renaming is found while iterating, some values are saved in
auxiliary variables, the renaming is removed, and the `updateProductions()` function is
invoked to update the production rules. 
```python
  while hasUnitProductions(prod):
      for leftSide in prod.keys():
          done = False
          for rule in prod[leftSide]:
              if rule in self.nonTerminalVar:
                  aux[leftSide] = prod[rule]
                  remove_from = leftSide
                  to_remove = rule
                  done = True
                  break
          if done:
              break

      prod[remove_from].discard(to_remove)
      updateProductions()
      aux = {}
```
It's easier to show than to explain, take
for example:
```
A -> ab | B
B -> ba | A
```
On the first pass of the while loop, the rules from B are added to A, and B is 
removed from A.
```
A -> ab | ba | A
B -> ba | A
```
On the second pass of the while loop, the rules from A are added to A, however, 
since the rules are kept in a set datatype, no duplicates are added, and lastly 
A is removed from A.
```
A -> ab | ba
B -> ba | A
```
On the third pass of the while loop, the rules from A are added to B, no duplicates
are added, and A is removed from B.
```
A -> ab | ba
B -> ba | ab
```
### 3. Removing non-productive symbols
For the next step, the productions dict is iterated through two times. First it
searches for symbols that don't have at least one rule comprised of only terminal
symbols, if they're found, they're marked as unproductive and removed from the productions dict and also from the
new list of non-terminal symbols.
```python
  unproductive_symbols = set([])

  copy = prod.copy()
  for leftSide in copy.keys():
      unproductive = True
      for rule in prod[leftSide]:
          if rule.islower():
              unproductive = False
              break

      if unproductive:
          unproductive_symbols.add(leftSide)
          prod.pop(leftSide)
          vn.remove(leftSide)
```
Iterating the second time, it searches on the right side for rules that contain 
unproductive symbols, if they are found, they are removed.
```python
  for leftSide in prod.keys():
      rules = prod[leftSide].copy()
      for rule in rules:
          for unproductive_symbol in unproductive_symbols:
              if rule.find(unproductive_symbol) != -1:
                  prod[leftSide].discard(rule)
```
### 4. Removing inaccessible symbols
To remove inaccessible symbols, I created a function that iterates through all left
side symbols, and for each one it checks all right side rules if they contain that symbol,
if it is not found anywhere, it is removed from productions and from the list of
non-terminal symbols.
```python
  def rmInaccessibleSymbols():
      aux = prod.copy()
      for leftSide in aux.keys():
          if leftSide == list(prod.keys())[0]:
              continue

          copy = aux.copy()
          copy.pop(leftSide)
          inaccessible = True
          for rules in copy.values():
              for rule in rules:
                  if rule.find(leftSide) != -1:
                      inaccessible = False
                      break
              if not inaccessible:
                  break

          if inaccessible:
              prod.pop(leftSide)
              vn.remove(leftSide)


  rmInaccessibleSymbols()
```
### 5. Obtaining CNF
The final transformation into CNF is done in two parts. The first part is creating
new rules for all terminal symbols, and switching them into the existing ones, eg.
`A -> caB` will become:
```
A -> CDB
C -> c
D -> a
```
It first finds new non-terminal symbols to attribute to the terminal symbols, then
adds the rules to the production dict and also to a separate inverse production
dict where the right side and left side of a rule are reversed as key and value,
this later allows to easily make all rules with length more than one, contain
only non-terminal symbols as in the above example. After that is done, if any
of the new added rules were not used, they are remove with the `rmInaccessibleSymbols()` function.
```python
  inverse_prod = {}

  for terminal in self.terminalVar:
      newNT = chr(ord(self.nonTerminalVar[-1]) + 1)
      while newNT in vn:
          newNT = chr(ord(newNT) + 1)

      prod[newNT] = set([terminal])
      inverse_prod[terminal] = newNT
      vn.append(newNT)

  for leftSide in prod.keys():
      rules = prod[leftSide]
      rules_copy = prod[leftSide].copy()
      for rule in rules_copy:
          if len(rule) > 1:
              rules.discard(rule)
              new_rule = rule
              for terminal in self.terminalVar:
                  if rule.find(terminal) != -1:
                      new_rule = new_rule.replace(terminal, inverse_prod[terminal])
              rules.add(new_rule)

  rmInaccessibleSymbols()
```
The second part and final transformation is breaking up sequences longer than
two, into multiple new rules, and the following piece of code works in the 
following way:

`A -> CBAB`

First pass of the while loop:
```text
A -> CD
D -> BAB
```
Second pass of the while loop:
```text
A -> CD
D -> BE
E -> AB
```
When adding new non-terminal symbols for new rules, it goes through all unicode characters
and the condition is set to only accept uppercase letters of the alphabet and their variations
 such as: Á, À, Â, Ǎ, Ă, Ã, Ả, Ȧ, Ạ, Ä, Å, Ḁ.
```python
  def hasLongSequence(prod_dict):
      for leftSide in prod.keys():
          for rule in prod[leftSide]:
              if len(rule) > 2:
                  return True
      return False


  while hasLongSequence(prod):
      prod_copy = prod.copy()
      for leftSide in prod_copy.keys():
          rules = prod[leftSide]
          rules_copy = prod[leftSide].copy()
          for rule in rules_copy:
              if (len(rule) == 1 and rule.islower()) or (len(rule) == 2 and rule.isupper()):
                  continue
              elif len(rule) >= 3:
                  str_partition = rule.partition(rule[0])
                  to_replace = str_partition[2]

                  if to_replace in inverse_prod.keys():
                      rules.discard(rule)
                      rules.add(rule.replace(to_replace, inverse_prod[to_replace]))

                  else:
                      newNT = chr(ord(vn[-1]) + 1)
                      while newNT in vn:
                          newNT = chr(ord(newNT) + 1)

                      vn.append(newNT)
                      prod[newNT] = set([to_replace])
                      inverse_prod[to_replace] = newNT

                      rules.discard(rule)
                      rules.add(rule.replace(to_replace, newNT))
```
Lastly, after all the transformations, all new production rules are turned into a list of 
`Production` objects and the method returns a new `Grammar` object that is in Chomsky
Normal Form.
```python
  p = []
  for leftSide in prod.keys():
      for rule in prod[leftSide]:
          p.append(Production(leftSide, rule))

  return Grammar(vn, self.terminalVar, p, list(prod.keys())[0])
```
## Unit tests
To perform unit tests, I created a new method for the `Grammar` class that checks if
a grammar object has empty productions, unit production, inaccessible symbols
or rules that are not a single terminal or two non-terminals. If any of those are found,
the method `isInCNF()` returns `False`, else it returns `True`.
```python
def isInCNF(self):
  prod = self.productionToDict()

  for leftSide in prod.keys():
      inaccessible = True
      for rule in prod[leftSide]:
          if not ((len(rule) == 1 and rule.islower()) or (len(rule) == 2 and rule.isupper())):

              return False
          if rule == 'ε':

              return False
          if rule in self.nonTerminalVar:

              return False

      if leftSide != self.start:
          for rules in prod.values():
              for rule1 in rules:
                  if rule1.find(leftSide) != -1:
                      inaccessible = False
                      break
      else: continue

      if inaccessible:
          return False

  return True
```
The `unittest` python library is used for the unit tests and I created 3 tests where
I define a grammar then get the CNF grammar in another variable. After that I use
`assertFalse()` on the original grammar and `assertTrue()` on the CNF grammar, if 
both are true, the test is passed.
```python
class TestCNF(unittest.TestCase):
    def test1(self):
        vn = ['S', 'A', 'B', 'C', 'D']
        vt = ['a', 'b']
        p = [
            Production('S', 'aB'),
            Production('S', 'bA'),
            Production('S', 'A'),
            Production('A', 'B'),
            Production('A', 'AS'),
            Production('A', 'bBAB'),
            Production('A', 'b'),
            Production('B', 'b'),
            Production('B', 'bS'),
            Production('B', 'aD'),
            Production('B', 'ε'),
            Production('D', 'AA'),
            Production('C', 'Ba'),
        ]

        grammar = Grammar(vn, vt, p, 'S')
        cnf = grammar.ChomskyNormalForm()
        self.assertFalse(grammar.isInCNF())
        self.assertTrue(cnf.isInCNF())
```
Running the tests:
```text
Launching unittests with arguments python -m unittest ..\Formal Languages and Finite Automata\src\testing



Ran 3 tests in 0.005s

OK

Process finished with exit code 0
```
## Results
Variant 4 grammar:
```text
VN = [S, A, B, C, D]
VT = [a, b]
P = [
     S → aB | bA | A
     A → B | bBAB | AS | b
     B → bS | aD | ε | b
     D → AA
     C → Ba
]
```
Creating the grammar object and using the `ChomskyNormalForm()` method:
```python
vn = ['S', 'A', 'B', 'C', 'D']
vt = ['a', 'b']
p = [
    Production('S', 'aB'),
    Production('S', 'bA'),
    Production('S', 'A'),
    Production('A', 'B'),
    Production('A', 'AS'),
    Production('A', 'bBAB'),
    Production('A', 'b'),
    Production('B', 'b'),
    Production('B', 'bS'),
    Production('B', 'aD'),
    Production('B', 'ε'),
    Production('D', 'AA'),
    Production('C', 'Ba'),
]

grammar = Grammar(vn, vt, p, 'S')
cnf = grammar.ChomskyNormalForm(show_proccess=True)
```
Output:
```
Intitial production rules
S -> {'bA', 'A', 'aB'}
A -> {'B', 'bBAB', 'b', 'AS'}
B -> {'bS', 'aD', 'ε', 'b'}
D -> {'AA'}
C -> {'Ba'}

After removing empty productions
S -> {'bA', 'A', 'aB', 'a'}
A -> {'bA', 'AS', 'bAB', 'B', 'bBAB', 'bBA', 'b'}
B -> {'bS', 'aD', 'b'}
D -> {'AA'}
C -> {'Ba', 'a'}

After removing unit productions
S -> {'bA', 'aB', 'a', 'aD', 'bBAB', 'AS', 'b', 'bAB', 'bS', 'bBA'}
A -> {'bA', 'aD', 'bBAB', 'AS', 'b', 'bAB', 'bS', 'bBA'}
B -> {'bS', 'aD', 'b'}
D -> {'AA'}
C -> {'Ba', 'a'}

After removing unproductive symbols
S -> {'bA', 'aB', 'a', 'bBAB', 'AS', 'b', 'bAB', 'bS', 'bBA'}
A -> {'bA', 'bBAB', 'AS', 'b', 'bAB', 'bS', 'bBA'}
B -> {'bS', 'b'}
C -> {'Ba', 'a'}

After removing inaccessible symbols
S -> {'bA', 'aB', 'a', 'bBAB', 'AS', 'b', 'bAB', 'bS', 'bBA'}
A -> {'bA', 'bBAB', 'AS', 'b', 'bAB', 'bS', 'bBA'}
B -> {'bS', 'b'}

After final transformation
S -> {'CB', 'a', 'b', 'DF', 'AS', 'DA', 'DS', 'DG', 'DE'}
A -> {'DF', 'DE', 'b', 'AS', 'DA', 'DG', 'DS'}
B -> {'DS', 'b'}
C -> {'a'}
D -> {'b'}
E -> {'BA'}
F -> {'AB'}
G -> {'BF'}
```
Trying on another grammar:
```python
vn1 = ['S', 'A', 'B', 'D', 'Z ']
vt1 = ['a', 'b', 'd']
p1 = [
    Production('S', 'dB'),
    Production('S', 'AB'),
    Production('A', 'd'),
    Production('A', 'dS'),
    Production('A', 'aAaAb'),
    Production('A', 'ε'),
    Production('B', 'a'),
    Production('B', 'aS'),
    Production('B', 'A'),
    Production('D', 'Aba'),
]

grammar1 = Grammar(vn1, vt1, p1, 'S')

grammar1.printGrammar()
cnf = grammar1.ChomskyNormalForm(show_proccess=False)
print('\nAfter transformation')
cnf.printGrammar()
```
Output:
```text
VN = [S, A, B, D, Z ]
VT = [a, b, d]
P = [
     S → dB | AB
     A → aAaAb | ε | d | dS
     B → aS | A | a
     D → Aba
]

After transformation
VN = [S, A, B, Z , C, D, E, F, G, H, I, J]
VT = [a, b, d]
P = [
    S → CH | AB | d | ES | CI | CS | CF | a | EB | CG
    A → CH | d | CI | ES | CF | CG
    B → CH | d | CI | CS | ES | a | CF | CG
    C → a
    D → b
    E → d
    F → CJ
    G → AF
    H → AI
    I → CD
    J → AD
]
```
## Conclusions
During this laboratory work I have studied the Chomsky Normal Form in depth and
have learned the proccess of normalizing a grammar. Once I understood the theory,
writing the implimentation was not too hard, however it was quite lengthy. Another 
thing I discovered during this lab were unit tests, initially I underestimated their
usefulness, however, after implementing and using them I was able to find a few bugs
in the code using them.