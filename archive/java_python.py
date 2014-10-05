from dragonfly import (Grammar, AppContext, MappingRule, Dictation,
                       Key, Text, FocusWindow, IntegerRef, Function)


#---------------------------------------------------------------------------
# Create this module's grammar and the context under which it'll be active.

context = AppContext(executable='java', title='py')
grammar = Grammar('pycharm Python commands', context=context)


#---------------------------------------------------------------------------
# Create a mapping rule which maps things you can say to actions.
#
# Note the relationship between the *mapping* and *extras* keyword
#  arguments.  The extras is a list of Dragonfly elements which are
#  available to be used in the specs of the mapping.  In this example
#  the Dictation("text")* extra makes it possible to use "<text>"
#  within a mapping spec and "%(text)s" within the associated action.

example_rule = MappingRule(
    name='pycharm Python commands',
    mapping={
        'Document comment': Text('"""') + Key('enter'),
        'dunder <text>': Text('__%(text)s__'),
        'defun': Text('def') + Key('tab'),

        'Set trace': Text('import pdb; pdb.set_trace()\n'),

        'for <text> in <text2>': Text('for %(text)s in %(text2)s:') + Key('enter'),
        'for <text> in X range <n>': Text('for %(text)s in xrange(%(n)d:') + Key('enter')
    },
    extras=[           # Special elements in the specs of the mapping.
        Dictation("text"),
        Dictation("text2"),
        IntegerRef("n", 1, 10000),  # Times to repeat the sequence.
    ],
    )

# Add the action rule to the grammar instance.
grammar.add_rule(example_rule)


#---------------------------------------------------------------------------
# Load the grammar instance and define how to unload it.

grammar.load()

# Unload function which will be called by natlink at unload time.
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
