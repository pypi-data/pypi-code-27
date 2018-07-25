from pyforms import conf

if conf.PYFORMS_MODE=='GUI':
	import logging, traceback; logger=logging.getLogger(__file__)

	from pyforms.gui.controls.ControlBase 			import ControlBase
	from pyforms.gui.controls.ControlText 			import ControlText
	from pyforms.gui.controls.ControlBoundingSlider import ControlBoundingSlider
	from pyforms.gui.controls.ControlButton 		import ControlButton
	from pyforms.gui.controls.ControlToolButton 	import ControlToolButton
	from pyforms.gui.controls.ControlCheckBoxList 	import ControlCheckBoxList
	from pyforms.gui.controls.ControlCheckBox 		import ControlCheckBox
	from pyforms.gui.controls.ControlCombo 			import ControlCombo
	from pyforms.gui.controls.ControlDir 			import ControlDir
	from pyforms.gui.controls.ControlDockWidget 	import ControlDockWidget
	from pyforms.gui.controls.ControlEmptyWidget 	import ControlEmptyWidget
	from pyforms.gui.controls.ControlFile 			import ControlFile
	from pyforms.gui.controls.ControlFilesTree 		import ControlFilesTree
	from pyforms.gui.controls.ControlLabel 			import ControlLabel
	from pyforms.gui.controls.ControlList 			import ControlList
	from pyforms.gui.controls.ControlMdiArea 		import ControlMdiArea
	from pyforms.gui.controls.ControlNumber 		import ControlNumber
	from pyforms.gui.controls.ControlProgress 		import ControlProgress
	from pyforms.gui.controls.ControlSlider 		import ControlSlider
	from pyforms.gui.controls.ControlTextArea 		import ControlTextArea
	from pyforms.gui.controls.ControlToolBox 		import ControlToolBox
	from pyforms.gui.controls.ControlTableView 		import ControlTableView
	from pyforms.gui.controls.ControlTree 			import ControlTree
	from pyforms.gui.controls.ControlTreeView 		import ControlTreeView