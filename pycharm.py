from dragonfly import (Grammar, AppContext, MappingRule, Dictation,
                       Key, Text, FocusWindow, IntegerRef, Choice,
                       Pause)
from dragonglue import LinuxAppContext

#---------------------------------------------------------------------------
# Create this module's grammar and the context under which it'll be active.

context = LinuxAppContext(executable='pycharm')
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
        'command': Key('cs-a'),
        'command <text>': Key('cs-a/5') + Text('%(text)s'),

        # file and editor navigation
        '[Activate] editor': Key('escape:2'),
        'close [file]': Key('c-f4'),
        'close tab': Key('c-f4'),
        'save [file]': Key('c-s'),
        'entab': Key('a-right'),
        'pretab': Key('a-left'),
        'flip': Key('c-tab'),
        'Flop': Key('cs-a/10') + Text('Previous Splitter') + Pause('20') + Key('enter'),
        'File list': Key('c-e'),
        'New File': Key('a-insert/20, down:3'), # (*)
        'Open recent': Key('a-f/20, r'),
        '(last | previous) edit': Key('cs-backspace'),
        '[go] back': Key('cas-comma'),
        '[go] forward': Key('cas-dot'),

        'File <text>': Key('c-e/5') + Text('%(text)s'),

        '(Navigate|Nav) tree': Key('a-home/20, down:1'),
        'Nav': Key('cs-n'),
        'Nav <text>': Key('cs-n/5') + Text('%(text)s'),
        'Nav in': Key('c-f12'),
        'Nav in <text>': Key('c-f12/5') + Text('%(text)s'),
        'Warp': Key('cas-n'),
        'Warp <text>': Key('cas-n/5') + Text('%(text)s'),

        # User interface navigation
        '<view_name> view': Key('a-%(view_name)d'),
        'last (view|tool)': Key('f12'),
        'start (Termie|termee)': Key('a-t/20, up:3, enter'),
        'Termie': Key('a-f12'),
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
        'warp here': Key('c-b'),
        'Quick outline': Key('c-f12'),
        'rename it': Key('s-f6'),
        'Re-factor [it]': Key('cas-t'),

        'Convert to spaces': Key('a-e, up, right, enter'),
        'Convert to tabs': Key('a-e, up, right, down, enter'),

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

        # Run the action twice due to focus problems
        'Tree Show': Key('a-f1/20, right, enter') * 2,


        # Special dictations

        '[pytest] parameterize': Text('@pytest.mark.parametrize('),
        '(defun | pytest) fixture': Text('@pytest.fixture\ndef '),
        '(defun | define) property': Text('@property\ndef '),
        'Mark (xfail | ex fail)': Text('@pytest.mark.xfail'),
        '[pytest] use fixtures': Text('@pytest.mark.usefixtures('),
        'Set (trace | pee dee bee)': Text('import pdb; pdb.set_trace()'),
        'dunder dict': Text('__dict__'),
        'dot dunder dict': Text('.__dict__'),
        'comment': Key('c-slash'),
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


commit_context=LinuxAppContext(executable='pycharm', title='Commit Changes')
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
