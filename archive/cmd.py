from dragonfly import (Grammar, AppContext, MappingRule, Dictation,
                       Key, Text, FocusWindow, IntegerRef, Choice)


context = AppContext(executable='cmd')
grammar = Grammar('cmd.exe commands', context=context)


example_rule = MappingRule(
    name='cmd.exe commands',
    mapping={
        # 'Work on': Text('workon '),
        # 'Work on <client>': Text('workon %(client)s'),
        'exit': Text('exit\n'),

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


sql_rule = MappingRule(
    name='SQL commands',
    mapping={
        'select': Text('select '),
        'select (star | splat)': Text('select * '),
        'select (star | splat) from': Text('select * from'),
    },
    context=AppContext(title='psql')
)

# Add the action rule to the grammar instance.
grammar.add_rule(example_rule)
grammar.add_rule(sql_rule)


#---------------------------------------------------------------------------
# Load the grammar instance and define how to unload it.

grammar.load()

# Unload function which will be called by natlink at unload time.
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
