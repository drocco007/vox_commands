from dragonfly import (Grammar, AppContext, MappingRule, Dictation,
                       Key, Text, FocusWindow, IntegerRef)


#---------------------------------------------------------------------------
# Create this module's grammar and the context under which it'll be active.

context = AppContext(executable='sublime_text')
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
        'close [file]': Key('c-w'),
        'open [file]': Key('c-o'),
        'save [file]': Key('c-s'),
        'entab': Key('c-pgdown'),
        'pretab': Key('c-pgup'),
        'flip': Key('c-tab'),

        # 'line <n>': Key('c-g/5') + Text('%(n)d') + Key('enter, home'),
        # 'line <digit> <n>': Key('c-g/5') + Text('%(digit)d%(n)d') + Key('enter, home'),
 
        # 'dupe': Key('cs-d'),
        # '<n> dupe': Key('cs-d:%(n)d'),
        # 'whip': Key('c-d'),
        # 'Slurp': Key('cs-k'),
        # '<n> Slurp': Key('cs-k:%(n)d'),

        # 'comment': Key('c-slash'),

        "find <text>":            Key("c-f/20") + Text("%(text)s\n"),
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
