from dragonfly import (Grammar, AppContext, MappingRule, Dictation,
                       Key, Text, FocusWindow, IntegerRef, Choice,
                       Pause)


#---------------------------------------------------------------------------
# Create this module's grammar and the context under which it'll be active.

context = AppContext(executable='pycharm')
grammar = Grammar("pycharm", context=context)


#---------------------------------------------------------------------------
# Create a mapping rule which maps things you can say to actions.
#
# Note the relationship between the *mapping* and *extras* keyword
#  arguments.  The extras is a list of Dragonfly elements which are
#  available to be used in the specs of the mapping.  In this example
#  the Dictation("text")* extra makes it possible to use "<text>"
#  within a mapping spec and "%(text)s" within the associated action.

example_rule = MappingRule(
    name="pycharm",    # The name of the rule.
    mapping={
        # file and editor navigation
        'Activate editor': Key('escape:2'),
        'close [file]': Key('c-f4'),
        'save [file]': Key('c-s'),
        'entab': Key('a-right'),
        'pretab': Key('a-left'),
        'flip': Key('c-tab'),
        'Flop': Key('cs-a/10') + Text('Previous Splitter') + Pause('20') + Key('enter'),
        'File list': Key('c-e'),
        'File New': Key('a-insert/20, down:3'), # (*)
        'Open recent': Key('a-f/20, r'),

        # User interface navigation
        '<view_name> view': Key('a-%(view_name)d'),
        # 'Close <view_name> view': Key('a-%(view_name)d:2'),

        # version control
        'Open version control': Key('a-c'),
        'VC commit': Key('c-k'),   
        'VC menu': Key('a-backtick'),
        # 'Commit'



        'Run (File | document)': Key('cs-f10'),
        'Run last': Key('s-f10'),


        # working within an editor
        'Fixit': Key('a-enter/20, down, up'), # (*)
        'Pre-bug': Key('s-f2'),
        'enbug': Key('f2'),
        'Maximize file': Key('cs-f12'),
        'Open declaration': Key('c-b'),
        'Quick outline':  Key('c-f12'),


        # 'line <n>': Key('c-g/5') + Text('%(n)d') + Key('enter, home'),
        # 'line <digit> <n>': Key('c-g/5') + Text('%(digit)d%(n)d') + Key('enter, home'),
        #
        # 'dupe': Key('c-d/5'),
        # '<n> dupe': Key('c-d:%(n)d'),
        # 'whip': Key('c-w'),
        # '<n> whip': Key('c-w:%(n)d'),
        # 'whop': Key('cs-w'),
        # '<n> whop': Key('cs-w:%(n)d'),
        # 'Slurp': Key('c-y'),
        # '<n> Slurp': Key('c-y:%(n)d'),
        #
        # 'comment': Key('c-slash'),

        "find <text>":            Key("c-f/20") + Text("%(text)s\n"),
        'Tree find': Key('cs-f'),
        'Tree Show': Key('a-f1/20, enter'),
    },
    extras=[           # Special elements in the specs of the mapping.
        Dictation("text"),
        IntegerRef("n", 1, 100),  # Times to repeat the sequence.
        IntegerRef("digit", 1, 10),  # Times to repeat the sequence.
        Choice('view_name', 
            dict(project=1, run=4, debug=5, todo=6, structure=7,
                 hierarchy=8, changes=9)
        )
    ],
    )


# (*) Extra keys are used to prevent the system menu from triggering...


commit_context=AppContext(title='Commit Changes')
commit_rule=MappingRule(
    name='commit rule',
    mapping={
        'commit': Key('c-enter'),

        '[Show] diff': Key('s-tab, c-d')
    },
    context=commit_context
)


# Add the action rule to the grammar instance.
grammar.add_rule(example_rule)
grammar.add_rule(commit_rule)


#---------------------------------------------------------------------------
# Load the grammar instance and define how to unload it.

grammar.load()

# Unload function which will be called by natlink at unload time.
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
