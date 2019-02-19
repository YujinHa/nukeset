import nuke
import nukescripts

tb = nuke.toolbar("Nodes")
m = tb.addMenu("Mingco", icon="mingco.png")
m.addMenu("Draw")
m.addCommand("Draw/timecode_burnin","nuke.createNode('timecode_burnin')")
m.addCommand("Draw/slate","nuke.createNode('slate')")

mb = menubar.addMenu("Yujin")
mb.addCommand("Issue_and_Bugs", "nukescripts.start('https://github.com/YujinHa/nukeset/issues')")
mb.addCommand("Slack", "nukescripts.start('https://voiceplayer.slack.com')")
mb.addCommand("-","","")
mb.addCommand("StartPerformanceTimers", "nuke.startPerformanceTimers()")
mb.addCommand("StopPerformanceTimers", "nuke.stopPerformanceTimers()")
