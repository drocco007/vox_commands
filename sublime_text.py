from dragonfly import (Grammar, AppContext, MappingRule, Dictation,
                       Key, Text, FocusWindow, IntegerRef, Choice)
from dragonglue import LinuxAppContext


#---------------------------------------------------------------------------
# Create this module's grammar and the context under which it'll be active.

context = LinuxAppContext(executable='sublime_text')
grammar = Grammar("sublime text", context=context)


#---------------------------------------------------------------------------
# Create a mapping rule which maps things you can say to actions.
#
# Note the relationship between the *mapping* and *extras* keyword
#  arguments.  The extras is a list of Dragonfly elements which are
#  available to be used in the specs of the mapping.  In this example
#  the Dictation("text")* extra makes it possible to use "<text>"
#  within a mapping spec and "%(text)s" within the associated action.

example_rule = MappingRule(
    name="sublime text",    # The name of the rule.
    mapping={
        'close [(file | tab)]': Key('c-w'),
        'file new': Key('c-n'),
        'open [file]': Key('c-o'),
        'save [file]': Key('c-s'),

        '[Enter] distraction free [mode]': Key('s-f11'),
        '[toggle] sidebar': Key('c-k,c-b'),
        '[toggle] menu': Key('cs-p') + Text('menu\n'),
        '[toggle] tabs': Key('cs-p') + Text('tabs\n'),

        'entab': Key('c-pgdown'),
        'pretab': Key('c-pgup'),
        'flip': Key('c-tab'),

        'See it': Key('cs-r'),

        'Nav': Key('c-p'),
        'file list': Key('c-p'),
        'Nav <text>': Key('c-p/5') + Text('%(text)s'),
        'Nav in': Key('c-r'),
        'Nav in <text>': Key('c-r/5') + Text('%(text)s'),
        'command': Key('cs-p'),
        'command <text>': Key('cs-p/5') + Text('%(text)s'),
        'Panel <n>': Key('c-%(n)d'),
        'Tab <n>': Key('a-%(n)d'),
        'Rab <n>': Key('a-1/5, c-pgup/5:%(n)d'),

        'project': Key('ca-p'),
        'project <text>': Key('ca-p/5') + Text('%(text)s'),
        'swap project': Key('ca-p, enter'),

        "find <text>":            Key("c-f/20") + Text("%(text)s\n"),

        're-browse': Key('c-s, w-F'),


        # Selection commands


        # Editing commands

        'centerize': Key('c-k, c-c'),
        'lower (it | that)': Key('c-k, c-l'),


        # Special phrases

        'pound <directive>': Text('#%(directive)s '),
        'dot H': Key('dot, h'),

        'New slide': Text('slide\n-----\n\n\n\n\n') + Key('left:3'),
    },
    extras=[           # Special elements in the specs of the mapping.
        Dictation("text"),
        IntegerRef("n", 1, 100),  # Times to repeat the sequence.
        IntegerRef("digit", 1, 10),  # Times to repeat the sequence.
        Choice('directive', {'include': 'include', 'define': 'define'})
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
