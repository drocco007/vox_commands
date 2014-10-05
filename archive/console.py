from dragonfly import (Grammar, AppContext, MappingRule, Dictation,
                       Key, Text, FocusWindow, IntegerRef, Choice)


context = AppContext(executable='console')
grammar = Grammar('Console2 commands', context=context)


#---------------------------------------------------------------------------
# Create a mapping rule which maps things you can say to actions.
#
# Note the relationship between the *mapping* and *extras* keyword
#  arguments.  The extras is a list of Dragonfly elements which are
#  available to be used in the specs of the mapping.  In this example
#  the Dictation("text")* extra makes it possible to use "<text>"
#  within a mapping spec and "%(text)s" within the associated action.

example_rule = MappingRule(
    name='Console2 commands',
    mapping={
        'Work on': Text('workon '),
        'Work on <client>': Text('workon %(client)s'),

        'git': Text('git'),
        'git svn dcommit': Text('git svn dcommit'),
        'git svn rebase': Text('git svn rebase'),

        'ell ess': Text('ls'),
        'ess cee pee': Text('scp'),
        'pee SQL': Text('psql')
    },
    extras=[           # Special elements in the specs of the mapping.
        Dictation("text"),
        IntegerRef("n", 0, 100),  # Times to repeat the sequence.
        Choice('client', {k:k.lower() for k in ('asppb', 'NHA')})
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
