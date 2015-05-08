"""Initializes the file filters singleton with the ICCS filters.  Used by apex_importer and
_Test
"""
from file_filters import *
from support.local_logging import Logger, LineLogger, FunctionLogger

lineLogger = LineLogger()
lineLog = lineLogger.logger.info

fileFilters = FileFilters ()

def initFileFilters (tower):
	"""
	Filter entries below take the form:
	 
	 	fileFilters.addFilter (<directory filter name/pattern>, {
										<file name/pattern> : <action>, ...
										})
										
	"file" means a file, directory, or symbolic link - i.e. a directory entry.
	"directory" means an actual directory.
										
	If a file IS in an entry below, it will be included or silently excluded.
	If it is included, explicitlyIncluded is set to True.
	If a file IS NOT in an entry below, it will be included, and explicitlyIncluded 
	is  set to False.
	(explicitlyIncluded is used by clients for debugging and testing.)  
	
	Explicit (name) matches have precedence over pattern matches.
	All Directory filter pattern matches are used.
	Multiple file pattern matches for the same file are an erroneous, and
	raise an exception at run time.. 
	
	The patterns below use regular expression syntax, NOT file system syntax!  
	For example, "*" is treated differently.
	
	If there is no comment before a line below, the normal behavior is desired:
	1) Files are copied
	2) Directories, subsystems, and views are processed
	3) if copyTarget is False (default), just the link is copied.  Otherwise, 
	    links are treated like the items they point to (e.g. if the link points 
	    to a directory, the directory contents are copied, not the link).
	"""
	
	def nothingBut (string):
		"""Given a string (which may be a pattern), returns a pattern that matches 
		a string containing nothing but that pattern.
		"""
		return "^" + string + "$"

	EVERYTHING_ELSE = nothingBut (".*")
	# Pattern that matches everything.  Since patterns are matched after 
	# explicits, matches everything that hasn't matched so far.   
	
	fileFilters.addFilter ("/nif", {
										"code" : Directory(removeTargetTreeFirst=True),
										# This is imported explicitly in apex_importer:
										# "rational" :  Directory(removeTargetTreeFirst=True),
										EVERYTHING_ELSE : Exclude(),
										})
			 
	fileFilters.addFilter ("/nif/code", {
										"Application_Behavior" : Directory(),
										"Application_Support" : Directory(),
										"Controllers" : Directory(),
										"Devices" : Directory(),
										"Embedded_Controllers" : Directory(),
										"Framework_Services" : Directory(),
										"Framework_Templates" : Directory(),
										"Main_Programs" : Directory(),
										"Slices" : Directory(),
										"Support" : Directory(),
										EVERYTHING_ELSE : Exclude(),
										})
			
	fileFilters.addFilter ("/nif/code/Application_Behavior", {
										# No release view:
										"Alert_Watcher.ss" : Exclude(),
										# No views:
										"Automatic_Alignment_C.ss" : Exclude(),
										# No views:
										"Automatic_Alignment_GUI.ss" : Exclude(),
										# No 7.2.1+ release view:
										"Automatic_Alignment_IDL.GARBAGE.ss" : Exclude(),
										# No views:
										"Automatic_Alignment_IDL.ss" : Exclude(),
										# No views:
										"Common_Gadgets.ss" : Exclude(),
										# No release view:
										"Ind_Control_GUI.ss" : Exclude(),
										# No views:
										"Ind_Control_GUI_C.ss" : Exclude(),
										# No 7.2.1+ release view:
										"OI_Analysis_C.ss" : Exclude(),
										# No release view:
										"OI_Analysis_Matlab.ss" : Exclude(),
										# No 7.2.1+ release view:
										"OI_Analysis_Scripts.ss" : Exclude(),
										# No 7.2.1+ release view:
										"OI_Analysis_Util.ss" : Exclude(),
										# No 7.2.1+ release view:
										"OPG_Shot_Activities.ss" : Exclude(),
										# No views:
										"PAMMA.ss" : Exclude(),
										# No views:
										"PAM_FEP_GUI.ss" : Exclude(),
										# No views:
										"PDS_BC_Shot.ss" : Exclude(),
										# No release views:
										"Power_Cond_Super_GUI.ss" : Exclude(),
										# No release views:
										"Sample_Devices_Interface.ss" : Exclude(),
										# No views:
										"Shot_Dir_Super_GUI.ss" : Exclude(),
										# No release views:
										"Shot_Dir_Super_GUI_C.ss" : Exclude(),
										# No views:
										"Shot_GUI_Support.ss" : Exclude(),
										# No views:
										"Special_CCD_Devices_Interface.ss" : Exclude(),
										# No views:
										"Target_Diag_GUI.ss" : Exclude(),
										# No views:
										"Target_Diag_GUI_C.ss" : Exclude(),
										# Last file left after all filters are applied:
										nothingBut ("subsystems\.dat") : Exclude(),
										})
	
	fileFilters.addFilter ("/nif/code/Application_Support", {
										# No 7.2.1+ release view:
										"Shot_Commands.ss" : Exclude(),
										# Last file left after all filters are applied:
										nothingBut ("subsystems\.dat") : Exclude(),
										})
	
	fileFilters.addFilter ("/nif/code/Controllers", {
										# Now controlled in AccuRev only.
										"Camera_Controllers_C.ss" : Exclude(),
										# No release view:
										"CTS_Controllers.ss" : Exclude(),
										# No views:
										"Digitizer_Controllers.ss" : Exclude(),
										# No views:
										"Digitizer_Controllers_C.ss" : Exclude(),
										# No views:
										"MOR_Controllers_C.ss" : Exclude(),
										})
	
	fileFilters.addFilter ("/nif/code/Devices", {
										# No 7.2.1+ release view:
										"CMS.ss" : Exclude(),
										# No 7.2.1+ release view:
										"Emulation_Bus.ss" : Exclude(),
										# No 7.2.1+ release view:
										"Timing_GPIB_Devices.ss" : Exclude(),
										# Last file left after all filters are applied:
										nothingBut ("subsystems\.dat") : Exclude(),
										})
	
	fileFilters.addFilter ("/nif/code/Embedded_Controllers", {
										# No release view:
										"Energy_Diag_Controller.ss" : Exclude(),
										# No release view:
										"IC_LB2_Tminus1_PLC.ss" : Exclude(),
										# No release view:
										"MOR_Chopper.ss" : Exclude(),
										})
	
	fileFilters.addFilter ("/nif/code/Framework_Services", {
										# Last file left after all filters are applied:
										nothingBut ("subsystems\.dat") : Exclude(),
										})

	fileFilters.addFilter ("/nif/code/Framework_Templates", {
										# No views:
										"App_Configuration.ss" : Exclude(),
										# No 7.2.1+ release view + "DO_NOT_USE":
										"Shot_Aid.ss" : Exclude(),
										# No 7.2.1+ release view + "DO_NOT_USE":
										"Shot_Life_Cycle.ss" : Exclude(),
										# No views + "DEPRECATED"
										"Timing.ss" : Exclude(),
										# Last file left after all filters are applied:
										nothingBut ("subsystems\.dat") : Exclude(),
										})
	
	fileFilters.addFilter ("/nif/code/Main_Programs", {
                                                                                "..Legacy" : Exclude(),
                                                                                # No release view:
                                                                                "Alert_GUI.ss" : Exclude(),
                                                                                # No views:
                                                                                "Automatic_Alignment_GUI.ss" : Exclude(),
                                                                                # No views:
                                                                                "Beam_Control_Super_GUI.ss" : Exclude(),
                                                                                # No release view:
                                                                                "CTS_FEP_Test.ss" : Exclude(),
                                                                                # No release view:
                                                                                "Components_Controller.ss" : Exclude(),
                                                                                # No 7.2.1+ release view + "MOVED":
                                                                                "IDL_Client_Examples.ss" : Exclude(),
                                                                                # No release view:
                                                                                "ISP_GUI_Main.ss" : Exclude(),
                                                                                # No views:
                                                                                "Ind_Control_FEP_GUI.ss" : Exclude(),
                                                                                # No views:
                                                                                "Ind_Control_Super_GUI.ss" : Exclude(),
                                                                                # No views + "GARBAGE":
                                                                                "Laser_Diag_Super_GUI.ss" : Exclude(),
                                                                                # No 7.2.1+ release view:
                                                                                "Laser_Diag_Supervisor.ss" : Exclude(),
                                                                                # No views:
                                                                                "Navigation_GUI.ss" : Exclude(),
                                                                                # No views:
                                                                                "OSP_Super_GUI.ss" : Exclude(),
                                                                                # No views:
                                                                                "Optics_Inspection_FEP.ss" : Exclude(),
                                                                                # No views:
                                                                                "Optics_Inspection_Super_GUI.ss" : Exclude(),
                                                                                # No views:
                                                                                "PAMMA.ss" : Exclude(),
                                                                                # No views + "GARBAGE":
                                                                                "PAM_Super_GUI.ss" : Exclude(),
                                                                                # No views:
                                                                                "PDS_BC_Super.ss" : Exclude(),
                                                                                # No views:
                                                                                "PEPC_LAB_Config_Server.ss" : Exclude(),
                                                                                # No views:
                                                                                "Power_Cond_Config_Server.ss" : Exclude(),
                                                                                # No views:
                                                                                "Power_Cond_Super_GUI.ss" : Exclude(),
                                                                                # No 7.2.1+ release view + "delete_me":
                                                                                "Sample_GUI.ss" : Exclude(),
                                                                                # No release view:
                                                                                "Sample_GUI_Main.ss" : Exclude(),
                                                                                # No 7.2.1+ release view:
                                                                                "Shot_Archive_Client_Examples.ss" : Exclude(),
                                                                                # No views:
                                                                                "Shot_Archive_Server.ss" : Exclude(),
                                                                                # No views:
                                                                                "Shot_Dir_Super_GUI_Main.ss" : Exclude(),
                                                                                # No 7.2.1+ release view:
                                                                                "Shot_Services.ss" : Exclude(),
                                                                                # No views:
                                                                                "Shot_Services_GUI.ss" : Exclude(),
                                                                                # No views:
                                                                                "Shot_Setup_Server.ss" : Exclude(),
                                                                                # No 7.2.1+ release view:
                                                                                "Special_CCD_FEP.ss" : Exclude(),
                                                                                # No views:
                                                                                "Special_CCD_FEP_GUI.ss" : Exclude(),
                                                                                # No 7.2.1+ release view:
                                                                                "Stat_Mon_Client_Examples.ss" : Exclude(),
                                                                                # No release view:
                                                                                "Stress_Test.ss" : Exclude(),
                                                                                # No views:
                                                                                "Sys_Mgr_Client_Examples.ss" : Exclude(),
                                                                                # No 7.2.1+ release view:
                                                                                "TA-DAS_Config_Server.ss" : Exclude(),
                                                                                # No 7.2.1+ release view:
                                                                                "Target_Diag_GUI.ss" : Exclude(),
                                                                                # No views:
                                                                                "Timing_Server.ss" : Exclude(),
                                                                                # No views:
                                                                                "Video_FEP_Client.ss" : Exclude(),
                                                                               # No views:
                                                                                "Video_FEP_GUI_Main.ss" : Exclude(),
                                                                                # No release view:
                                                                                "Video_FEP_GUI_Main_C.ss" : Exclude(),
                                                                                # No 7.2.1+ release view:
                                                                            "Wavefront_FEP_GUI_Main.ss" : Exclude(),
                                                                                # No views:
                                                                                "Wavefront_IP_FEP_Main.ss" : Exclude(),
                                                                                # No release view:
                                                                                "basic_ACFEP_test.ss" : Exclude(),
                                                                                # No 7.2.1+ release view:
                                                                                "config_LE_hardware.ss" : Exclude(),
										# Last file left after all filters are applied:
										nothingBut ("subsystems\.dat") : Exclude(),
										})
		
	fileFilters.addFilter ("/nif/code/Slices", {
										"Shadow_Deployment.ss" : Subsystem(),
										EVERYTHING_ELSE : Exclude(),
										})
			 
	fileFilters.addFilter ("/nif/code/Slices/Shadow_Deployment.ss/", {
										tower : View(removeTargetTreeFirst=True),
										EVERYTHING_ELSE : Exclude(),
										})

	fileFilters.addFilter ("/nif/code/Support", {
										"Intel_IPP.ss" : Subsystem(),
										"Utilities.ss" : Subsystem(),
										"VxWorks.ss" : Subsystem(),
										"subsystems.dat" : File(),
										EVERYTHING_ELSE : Exclude(),
										})
			
	# Unwanted entries under Controllers:
	# 	exclude all files except those that end with .idl
	fileFilters.addFilter (nothingBut (r"/nif/code/Controllers/An_Dig_Controllers\.ss/" + VIEW_PATTERN + ".*"), {
										"^.*[.](?!idl$).*$" : Exclude(),
										})
			
	# Unwanted entries under Controllers:
	# 	exclude all files except those that end with .idl
	fileFilters.addFilter (nothingBut (r"/nif/code/Controllers/Camera_Controllers\.ss/" + VIEW_PATTERN + ".*"), {
										"^.*[.](?!idl$).*$" : Exclude(),
										})
			
	# Unwanted entries under Controllers:
	# 	exclude all files except those that end with .idl
	fileFilters.addFilter (nothingBut (r"/nif/code/Controllers/Comm_Controllers\.ss/" + VIEW_PATTERN + ".*"), {
										"^.*[.](?!idl$).*$" : Exclude(),
										nothingBut ("ReadMe") : Exclude(), # Comm_Controllers
										})
			
	# Unwanted entries under Controllers:
	# 	exclude all files except those that end with .idl
	fileFilters.addFilter (nothingBut (r"/nif/code/Controllers/Motor_Controllers\.ss/" + VIEW_PATTERN + ".*"), {
										"^.*[.](?!idl$).*$" : Exclude(),
										})
			
	# Unwanted entries under Controllers:
	# 	exclude all files except those that end with .idl
	fileFilters.addFilter (nothingBut (r"/nif/code/Controllers/PLC_Controllers\.ss/" + VIEW_PATTERN + ".*"), {
										"^.*[.](?!idl$).*$" : Exclude(),
										})
			
	# Unwanted entries under Controllers:
	# 	exclude all files except those that end with .idl
	fileFilters.addFilter (nothingBut (r"/nif/code/Controllers/Power_Cond_Controllers\.ss/" + VIEW_PATTERN + ".*"), {
										"^.*[.](?!idl$).*$" : Exclude(),
										nothingBut ("README_Power_Cond_Controllers") : Exclude(), # Power_Cond_Controllers
										})
			
	# Unwanted entries under Controllers:
	# 	exclude all files except those that end with .idl
	fileFilters.addFilter (nothingBut (r"/nif/code/Controllers/Sample_Controllers\.ss/" + VIEW_PATTERN + ".*"), {
										"^.*[.](?!idl$).*$" : Exclude(),
										})
			
	# Unwanted entries under Controllers:
	# 	exclude all files except those that end with .idl
	fileFilters.addFilter (nothingBut (r"/nif/code/Controllers/Timing_Controllers\.ss/" + VIEW_PATTERN + ".*"), {
										"^.*[.](?!idl$).*$" : Exclude(),
										})
			
	fileFilters.addFilter (nothingBut (r"/nif/code/Support/Abstract_Data_Types\.ss/" + VIEW_PATTERN), {
										# Files in this directory are redundant in the gnat compilation environment: 		
										"gnat" : Exclude(),
										})
			
	fileFilters.addFilter (nothingBut (r"/nif/code/Framework_Templates/System_Manager\.ss/" + VIEW_PATTERN), {
										# TODO delete from Apex		
										"System_Manager.gpr" : Exclude(),
										})
			
	fileFilters.addFilter ("/nif/rational", {
										"base" : Directory(),
										"config" : Directory(),
										EVERYTHING_ELSE : Exclude(),
										})
	
	fileFilters.addFilter ("/nif/rational/base", {
										"ada" : Directory(),
										EVERYTHING_ELSE : Exclude(),
										})
	
	fileFilters.addFilter ("/nif/rational/base/ada", {
										"rational.ss" : Directory(),
										"rts_vads_exec.ss" : Directory(),
										EVERYTHING_ELSE : Exclude(),
										})
	
	fileFilters.addFilter ("/nif/rational/base/ada/rational.ss", {
										"sun4_solaris2.ada95.4.2.0.rel" : Directory(),
										"power.vw_ppc.ada95.4.2.0.rel" : Directory(),
										EVERYTHING_ELSE : Exclude(),
										})
	
	fileFilters.addFilter (nothingBut (r"/nif/rational/base/ada/rational\.ss/" + VIEW_PATTERN), {
										"ada_krn_defs.1.ada" : File(),
										EVERYTHING_ELSE : Exclude(),
										})
	
	fileFilters.addFilter ("/nif/rational/base/ada/rts_vads_exec.ss", {
										"sun4_solaris2.ada95.4.2.0.rel" : Directory(),
										"power.vw_ppc.ada95.4.2.0.rel" : Directory(),
										EVERYTHING_ELSE : Exclude(),
										})

	fileFilters.addFilter (nothingBut (r"/nif/rational/base/ada/rts_vads_exec\.ss/"  + VIEW_PATTERN), {
										"v_interrupts.1.ada" : File(), # Sol and Vx sources are identical.
										"v_interrupts.2.ada" : File(), # Sol and Vx sources are identical.
										"v_mailboxes.1.ada" : File(),
										"v_mailboxes.2.ada" : File(), # Sol and Vx sources are identical.
										EVERYTHING_ELSE : Exclude(),
										})

	fileFilters.addFilter ("/nif/rational/config", {
										"license.dat" : Link(File(), copyTarget=True),
										EVERYTHING_ELSE : Exclude(),
										})
	
	# Only match subsystems, and nothing else, in /nif/code/<layer>:
	fileFilters.addFilter (nothingBut (NIF_CODE_LAYER_PATTERN), {
										nothingBut (SUBSYSTEM_PATTERN) : Subsystem(),
										"(?!" + nothingBut (SUBSYSTEM_PATTERN) + ")": Exclude(),
										})
					
	# Only match the "tower" view in a subsystem (unless overridden by a filter
	# for a specific subsystem: 
	fileFilters.addFilter (nothingBut (NIF_CODE_LAYER_SS_PATTERN), {
										tower : View(),
										EVERYTHING_ELSE : Exclude(),
										})
	# Unwanted files anywhere:
	fileFilters.addFilter (EVERYTHING_ELSE, {
										"core" : Exclude(),
										nothingBut (r".*~") : Exclude(),
										nothingBut (r".*\.pyc") : Exclude(),
										})
			
	# Unwanted Rational subsystem entries:
	fileFilters.addFilter (nothingBut (SUBSYSTEM_PATTERN), {
										".Rational" : Exclude(),
										".Rational_Location" : Exclude(),
										"Policy" : Exclude(),
										})
			 
	# Unwanted Rational view entries:
	fileFilters.addFilter (nothingBut (".*" + SUBSYSTEM_VIEW_PATTERN), {
										".Rational" : Exclude(),
										".Rational_Location" : Exclude(),
										"Policy" : Exclude(),
										"Imports" : Exclude(),
										"Exports" : Exclude(),
										})
			 
	# Unwanted entries anywhere in a view or its subdirectories:
	fileFilters.addFilter (nothingBut (".*" + SUBSYSTEM_VIEW_PATTERN + ".*"), {
										".Makefiles.rtnl" : Exclude(),
										"IDL_Ada" : Exclude(),
										"Links" : Exclude(),
#										nothingBut (".*_version.1.ada") : Exclude(),
										})

	# Unwanted entries under Application_Behavior:
	# 	exclude all files except those that end with .idl
	fileFilters.addFilter (nothingBut ("/nif/code/Application_Behavior/" + SUBSYSTEM_VIEW_PATTERN + ".*"), {
										"^.*[.](?!idl$).*$" : Exclude(),
										"OI_Assist_Cmds.Readme" : File(),
										})
			 
	# Unwanted entries under Application_Support:
	# 	exclude all files except those that end with .idl
	fileFilters.addFilter (nothingBut ("/nif/code/Application_Support/" + SUBSYSTEM_VIEW_PATTERN + ".*"), {
										"^.*[.](?!idl$).*$" : Exclude(),
										})
			 
	# Unwanted entries under Devices:
	# 	exclude all files except those that end with .idl
	#	remove assorted files that remain (files without an extension)
	fileFilters.addFilter (nothingBut ("/nif/code/Devices/" + SUBSYSTEM_VIEW_PATTERN + ".*"), {
										"^.*[.](?!idl$).*$" : Exclude(),
										nothingBut ("makefile") : Exclude(),
										})
			 
	# Unwanted entries under Framework_Services:
	# 	exclude all files except those that end with .idl
	#	remove assorted files that remain (files without an extension)
	fileFilters.addFilter (nothingBut ("/nif/code/Framework_Services/" + SUBSYSTEM_VIEW_PATTERN + ".*"), {
										"^.*[.](?!idl$).*$" : Exclude(),
										nothingBut (".*-File") : Exclude(),
										})
			 
	# Unwanted entries under Framework_Templates:
	# 	exclude all files except those that end with .idl
	#	remove assorted files that remain (files without an extension)
	fileFilters.addFilter (nothingBut ("/nif/code/Framework_Templates/" + SUBSYSTEM_VIEW_PATTERN + ".*"), {
										"^.*[.](?!idl$).*$" : Exclude(),
										nothingBut ("ReadMe") : Exclude(),
										nothingBut ("KNOWN_BUGS") : Exclude(),
										nothingBut ("makefile") : Exclude(),
										})
			 
	# Unwanted entries under Main_Programs:
	# 	exclude all files except those that end with .idl
	#	remove assorted files that remain (files without an extension)
	fileFilters.addFilter (nothingBut ("/nif/code/Main_Programs/" + SUBSYSTEM_VIEW_PATTERN + ".*"), {
										"^.*[.](?!idl$).*$" : Exclude(),
										nothingBut ("ReadMe") : Exclude(),
										nothingBut ("Readme") : Exclude(),
										nothingBut (".*_amc") : Exclude(),
										nothingBut (".*_bug") : Exclude(),
										nothingBut (".*_file") : Exclude(),
										nothingBut (".*_main") : Exclude(),
										nothingBut (".*_plan") : Exclude(),
										nothingBut (".*_procedure") : Exclude(),
										})
			 
	# Unwanted entries under Support/Utilities:
	# 	exclude all files except those that end with .idl
	#	remove assorted files that remain (files without an extension)
	fileFilters.addFilter (nothingBut ("/nif/code/Support/Utilities.ss/" + VIEW_PATTERN + ".*"), {
										"^.*[.](?!idl$)" : Exclude(),
										nothingBut ("ReadMe") : Exclude(),
										nothingBut ("readme") : Exclude(),
										nothingBut ("makefile") : Exclude(),
										})
			 
class _Test ():
	def __init__(self):
		self._logger=Logger(name='test_iccs_file_filters', level=Logger.DEBUG, 
						showDate=True, 
						showTime=True, 
						showName=False,
						showFunc=False)
		self._debug = self._logger.logger.debug
		self.log = self._logger.log
	
	def setup (self):	
		tower = "accurev.7.2.1.rel"
		self.log("BEGIN test")
		self.log("tower = '" + tower + "'")
		initFileFilters (tower)
		self.filtering = DirEntryFiltering()
		
	def run (self):
		self.testDirs ()

	def finish (self):
		sourcePath="/nif/code/Framework_Services/Generic_Client.ss/reynolds.SCR21941.sol.ada.7.2.0.wrk"
		self._debug("'" + sourcePath + "'" + str (re.match(re.compile("^" + VIEW_PATTERN + "$"), sourcePath)))
		self._debug("'" + sourcePath + "'" + str (re.search(re.compile(VIEW_PATTERN), sourcePath)))
		self.log("explicit filters:" + str(fileFilters.explicitFilterNames()).replace(",","\n"))
		self.log("pattern filters:" + str(fileFilters.patternFilterNames()).replace(",","\n"))
		self.log("END test")
				
	def testDirs (self):
		self.testDir("/nif")
		self.testDir("/nif/code")
		self.testDir("/nif/code/Slices/")
		self.testDir("/nif/code/Slices/Shadow_Deployment.ss")
		self.testDir("/nif/code/Slices/Shadow_Deployment.ss/accurev.7.2.1.rel")
		self.testDir("/nif/environment")
		self.testDir("/nif/environment/setup.ss")
		self.testDir("/nif/environment/setup.ss/latest.wrk")
		self.testDir("/nif/rational/base/ada")
		self.testDir("/nif/rational/base/ada/rational.ss")
		self.testDir("/nif/rational/base/ada/rational.ss/sun4_solaris2.ada95.4.2.0.rel")
		self.testDir("/nif/rational/base/ada/rational.ss/power.vw_ppc.ada95.4.2.0.rel")
		self.testDir("/nif/rational/base/ada/rts_vads_exec.ss")
		self.testDir("/nif/rational/base/ada/rts_vads_exec.ss/sun4_solaris2.ada95.4.2.0.rel")
		self.testDir("/nif/rational/base/ada/rts_vads_exec.ss/power.vw_ppc.ada95.4.2.0.rel")
		self.testDir("/nif/rational/config")
		self.testDir("/nif/tools")

	def testDir (self, dir):
		self.log("")
		self.log("Testing '" + dir + "'")
		nonExcludedEntries = self.filtering.allNonExcludedEntriesIn (dir, fileFilters)
		keys = nonExcludedEntries.keys()
		self.log("Got " + str(len(keys)) + " included entries:")
		keys.sort()
		for sourceEntry in keys:
			if nonExcludedEntries [sourceEntry].explicitlyIncluded:
				self.log("    '" + sourceEntry + "'" )
			else:
				self._logger.warning("implicitly included (matched no filter) '" + sourceEntry + "'" )
				
if __name__ == '__main__':
	test=_Test()
	test.setup()	
	test.run()
	test.finish()
	
