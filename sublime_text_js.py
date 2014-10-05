from dragonfly import (Grammar, AppContext, MappingRule, Dictation,
                       Key, Text, FocusWindow, IntegerRef)


#---------------------------------------------------------------------------
# Create this module's grammar and the context under which it'll be active.

context = AppContext(executable='sublime_text', title='js')
grammar = Grammar("sublime text js", context=context)

left_2 = Key('left:2')

example_rule = MappingRule(
    name="sublime text js",    # The name of the rule.
    mapping={
        'console [dot] log': Text('console.log();') + left_2,
        '[console] [dot] log this': Text('console.log(this, arguments);') + left_2,

        'colon function': Text(': function() {}') + left_2,

        'Fix me': Text('// FIXME: '),
    },
    extras=[           # Special elements in the specs of the mapping.
        Dictation("text"),
        IntegerRef("n", 1, 100),  # Times to repeat the sequence.
        IntegerRef("digit", 1, 10),  # Times to repeat the sequence.
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
