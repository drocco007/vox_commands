from dragonfly import (Grammar, AppContext, MappingRule, Dictation,
                       Key, Text, FocusWindow, IntegerRef, Function)
from dragonglue import LinuxAppContext


#---------------------------------------------------------------------------
# Create this module's grammar and the context under which it'll be active.

context = LinuxAppContext(executable='chrome')
grammar = Grammar('Chrome commands', context=context)


#---------------------------------------------------------------------------
# Create a mapping rule which maps things you can say to actions.
#
# Note the relationship between the *mapping* and *extras* keyword
#  arguments.  The extras is a list of Dragonfly elements which are
#  available to be used in the specs of the mapping.  In this example
#  the Dictation("text")* extra makes it possible to use "<text>"
#  within a mapping spec and "%(text)s" within the associated action.

c_n = Key('c-%(n)d/5')
c_pgup = Key('c-pgup:%(n)d')
c_pgdown = Key('c-pgdown:%(n)d')

def go_to_tab(n):
    if n <= 8:
        c_n.execute({'n': n})
    else:
        c_n.execute({'n': 8})
        c_pgdown.execute({'n': n - 8})


def go_to_tab_right(n):
    c_n.execute({'n': 9})

    if n > 1:
        c_pgup.execute({'n': n - 1})


example_rule = MappingRule(
    name='Chrome commands',
    mapping={
        'new incognito': Key('cs-n'),

        'back': Key('a-left'),
        'forward': Key('a-right'),
        'reload': Key('c-r'),
        'new tab': Key('c-t'),
        'Close tab': Key('c-w'),
        'entab': Key('c-pgdown'),
        'pretab': Key('c-pgup'),
        'flip': Key('c-tab'),
        '[Select] address': Key('a-d'),
        'Copy address': Key('a-d/20, c-c'),
        'Tab <n>': Function(go_to_tab),
        'Rab <n>': Function(go_to_tab_right),

        # supported by the vimium extension
        'Nav': Key('T/10'),
        'Nav <text>': Key('T/10') + Text('%(text)s'),

        # Links and stuff
        'link': Key('f'),
        'link <text>': Key('f/10') + Text('%(text)s'),
        'copy link': Key('y, f'),
        'copy link <text>': Key('y/10, f/10') + Text('%(text)s'),
        'click <n>': Text('%(n)d'),
        'click <digit> zero <digit2>': Text('%(digit)d0%(digit2)d'),
        'click <digit> <n>': Text('%(digit)d%(n)d'),
        'Focus <n>': Text('%(n)d'),
        'Focus <digit> zero <digit2>': Text('%(digit)d0%(digit2)d'),
        'Focus <digit> <n>': Text('%(digit)d%(n)d'),
        'Touch <n>': Text('%(n)d') + Key('f'),
        'Touch <digit> zero <digit2>': Text('%(digit)d0%(digit2)d') + Key('f'),
        'Touch <digit> <n>': Text('%(digit)d%(n)d') + Key('f'),
        'Field': Key('g, i'),
        'Field <n>': Text('%(n)dgi'),
        'Next': Key('rbracket:2'),
        'Previous': Key('lbracket:2'),

        "find <text>":            Key("slash/10") + Text("%(text)s\n"),
    },
    extras=[           # Special elements in the specs of the mapping.
        Dictation("text"),
        IntegerRef("digit", 0, 9),  # Times to repeat the sequence.
        IntegerRef("digit2", 0, 9),  # Times to repeat the sequence.
        IntegerRef("n", 0, 100),  # Times to repeat the sequence.
        IntegerRef("bign", 0, 500),  # Times to repeat the sequence.
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
