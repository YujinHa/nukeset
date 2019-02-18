import nuke

tb = nuke.toolbar("Nodes")
m = tb.addMenu("Mingco", icon="mingco.png")
m.addMenu("Draw")
m.addCommand("Draw/timecode_burnin","nuke.createNode('timecode_burnin')")
m.addCommand("Draw/slate","nuke.createNode('slate')")
