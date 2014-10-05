from dragonfly import (Grammar, AppContext, MappingRule, Dictation,
                       Key, Text, FocusWindow, IntegerRef, Choice)


#---------------------------------------------------------------------------
# Create this module's grammar and the context under which it'll be active.

context = AppContext(executable='virtualbox')
grammar = Grammar('VirtualBox commands', context=context)


#---------------------------------------------------------------------------
# Create a mapping rule which maps things you can say to actions.
#
# Note the relationship between the *mapping* and *extras* keyword
#  arguments.  The extras is a list of Dragonfly elements which are
#  available to be used in the specs of the mapping.  In this example
#  the Dictation("text")* extra makes it possible to use "<text>"
#  within a mapping spec and "%(text)s" within the associated action.

example_rule = MappingRule(
    name='VirtualBox commands',
    mapping={
        'Launch <n>': Key('w-%(n)s/20'),

        'Close tab': Key('c-w'),
        'entab': Key('c-pgdown'),
        'pretab': Key('c-pgup'),
        'flip': Key('c-tab'),

        'Work on': Text('workon '),
        'Work on <client>': Text('workon %(client)s'),
        'Launch <client>': Text('launch-bt %(client)s'),

        'ess cee pee': Text('scp'),
        'pee SQL': Text('psql'),

        'user postgres': Text('sudo su postgres\n')
    },
    extras=[           # Special elements in the specs of the mapping.
        Dictation("text"),
        IntegerRef("n", 0, 100),  # Times to repeat the sequence.
        Choice('client', {k:k.lower() for k in ('asppb', 'NHA', 'core')})
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
