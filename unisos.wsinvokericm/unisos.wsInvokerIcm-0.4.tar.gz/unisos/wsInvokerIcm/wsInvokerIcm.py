# -*- coding: utf-8 -*-
"""\
* TODO *[Summary]* ::  A /library/ for Web Services Invoker ICMs (wsInvokerIcm) -- make all operations invokable from command line based on swagger sepc input.
"""

####+BEGIN: bx:icm:python:top-of-file :partof "bystar" :copyleft "halaal+minimal"
"""
*  This file:/de/bx/nne/dev-py/pypi/pkgs/unisos/wsInvokerIcm/dev/unisos/wsInvokerIcm/newLibIcm.py :: [[elisp:(org-cycle)][| ]]
 is part of The Libre-Halaal ByStar Digital Ecosystem. http://www.by-star.net
 *CopyLeft*  This Software is a Libre-Halaal Poly-Existential. See http://www.freeprotocols.org
 A Python Interactively Command Module (PyICM). Part Of ByStar.
 Best Developed With COMEEGA-Emacs And Best Used With Blee-ICM-Players.
 Warning: All edits wityhin Dynamic Blocks may be lost.
"""
####+END:


"""
*  [[elisp:(org-cycle)][| *Lib-Module-INFO:* |]] :: Author, Copyleft and Version Information
"""

####+BEGIN: bx:global:lib:name-py :style "fileName"
__libName__ = "newLibIcm"
####+END:

####+BEGIN: bx:global:timestamp:version-py :style "date"
__version__ = "201807115259"
####+END:

####+BEGIN: bx:global:icm:status-py :status "Production"
__status__ = "Production"
####+END:

__credits__ = [""]

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/libre/ByStar/InitialTemplates/update/sw/icm/py/icmInfo-mbNedaGpl.py"
icmInfo = {
    'authors':         ["[[http://mohsen.1.banan.byname.net][Mohsen Banan]]"],
    'copyright':       "Copyright 2017, [[http://www.neda.com][Neda Communications, Inc.]]",
    'licenses':        ["[[https://www.gnu.org/licenses/agpl-3.0.en.html][Affero GPL]]", "Libre-Halaal Services License", "Neda Commercial License"],
    'maintainers':     ["[[http://mohsen.1.banan.byname.net][Mohsen Banan]]",],
    'contacts':        ["[[http://mohsen.1.banan.byname.net/contact]]",],
    'partOf':          ["[[http://www.by-star.net][Libre-Halaal ByStar Digital Ecosystem]]",]
}
####+END:

####+BEGIN: bx:icm:python:topControls 
"""
*  [[elisp:(org-cycle)][|/Controls/| ]] :: [[elisp:(org-show-subtree)][|=]]  [[elisp:(show-all)][Show-All]]  [[elisp:(org-shifttab)][Overview]]  [[elisp:(progn (org-shifttab) (org-content))][Content]] | [[file:Panel.org][Panel]] | [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] | [[elisp:(bx:org:run-me)][Run]] | [[elisp:(bx:org:run-me-eml)][RunEml]] | [[elisp:(delete-other-windows)][(1)]] | [[elisp:(progn (save-buffer) (kill-buffer))][S&Q]]  [[elisp:(save-buffer)][Save]]  [[elisp:(kill-buffer)][Quit]] [[elisp:(org-cycle)][| ]]
** /Version Control/ ::  [[elisp:(call-interactively (quote cvs-update))][cvs-update]]  [[elisp:(vc-update)][vc-update]] | [[elisp:(bx:org:agenda:this-file-otherWin)][Agenda-List]]  [[elisp:(bx:org:todo:this-file-otherWin)][ToDo-List]]
"""
####+END:

"""
* 
####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/libre/ByStar/InitialTemplates/software/plusOrg/dblock/inserts/pythonWb.org"
*  /Python Workbench/ ::  [[elisp:(org-cycle)][| ]]  [[elisp:(python-check (format "pyclbr %s" (bx:buf-fname))))][pyclbr]] || [[elisp:(python-check (format "pyflakes %s" (bx:buf-fname)))][pyflakes]] | [[elisp:(python-check (format "pychecker %s" (bx:buf-fname))))][pychecker (executes)]] | [[elisp:(python-check (format "pep8 %s" (bx:buf-fname))))][pep8]] | [[elisp:(python-check (format "flake8 %s" (bx:buf-fname))))][flake8]] | [[elisp:(python-check (format "pylint %s" (bx:buf-fname))))][pylint]]  [[elisp:(org-cycle)][| ]]
####+END:
"""


####+BEGIN: bx:icm:python:section :title "ContentsList"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *ContentsList*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] 
"""
####+END:


####+BEGIN: bx:dblock:python:icmItem :itemType "=Imports=" :itemTitle "*IMPORTS*"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || =Imports=      :: *IMPORTS*  [[elisp:(org-cycle)][| ]]
"""
####+END:

import os
import collections
import enum

####+BEGIN: bx:dblock:global:file-insert :file "/libre/ByStar/InitialTemplates/update/sw/icm/py/importUcfIcmG.py"
from unisos import ucf
from unisos import icm

icm.unusedSuppressForEval(ucf.__file__)  # in case icm and ucf are not used

G = icm.IcmGlobalContext()
G.icmLibsAppend = __file__
G.icmCmndsLibsAppend = __file__

####+END:


import pprint    
from bravado.requests_client import RequestsClient
from bravado.client import SwaggerClient

import re
import requests
import sys
import yaml

from functools import partial
from bravado_core.spec import Spec
from bravado.client import construct_request
from bravado.requests_client import RequestsClient

REPLACEABLE_COMMAND_CHARS = re.compile('[^a-z0-9]+')

#import requests
import logging
import httplib


####+BEGIN: bx:dblock:python:section :title "Library Description (Overview)"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *Library Description (Overview)*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] 
"""
####+END:

####+BEGIN: bx:icm:python:cmnd:classHead :cmndName "icmBegin_libOverview" :parsMand "" :parsOpt "" :argsMin "0" :argsMax "3" :asFunc "" :interactiveP ""
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || ICM-Cmnd       :: /icmBegin_libOverview/ parsMand= parsOpt= argsMin=0 argsMax=3 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
"""
class icmBegin_libOverview(icm.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 3,}

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
        interactive=False,        # Can also be called non-interactively
        argsList=[],         # or Args-Input
    ):
        cmndOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=cmndOutcome):
                return cmndOutcome
            effectiveArgsList = G.icmRunArgsGet().cmndArgs
        else:
            effectiveArgsList = argsList

        callParamsDict = {}
        if not icm.cmndCallParamsValidate(callParamsDict, interactive, outcome=cmndOutcome):
            return cmndOutcome

        cmndArgsSpecDict = self.cmndArgsSpec()
        if not self.cmndArgsValidate(effectiveArgsList, cmndArgsSpecDict, outcome=cmndOutcome):
            return cmndOutcome
####+END:

        moduleDescription="""
*       [[elisp:(org-show-subtree)][|=]]  [[elisp:(org-cycle)][| *Description:* | ]]
**  [[elisp:(org-cycle)][| ]]  [Xref]          :: *[Related/Xrefs:]*  <<Xref-Here->>  -- External Documents  [[elisp:(org-cycle)][| ]]

**  [[elisp:(org-cycle)][| ]]	Model and Terminology 					   :Overview:
This module is part of BISOS and its primary documentation is in  http://www.by-star.net/PLPC/180047
**      [End-Of-Description]
"""
        
        moduleUsage="""
*       [[elisp:(org-show-subtree)][|=]]  [[elisp:(org-cycle)][| *Usage:* | ]]

**      How-Tos:
**      [End-Of-Usage]
"""
        
        moduleStatus="""
*       [[elisp:(org-show-subtree)][|=]]  [[elisp:(org-cycle)][| *Status:* | ]]
**  [[elisp:(org-cycle)][| ]]  [Info]          :: *[Current-Info:]* Status/Maintenance -- General TODO List [[elisp:(org-cycle)][| ]]
** TODO [[elisp:(org-cycle)][| ]]  ICM Common       :: Add -i cmndFpUpdate .  and -i cmndFpShow . [[elisp:(org-cycle)][| ]]
** TODO [[elisp:(org-cycle)][| ]]  wsIcmInvoker     :: Add -p headers=fileName  [[elisp:(org-cycle)][| ]]
** TODO [[elisp:(org-cycle)][| ]]  wsIcmInvoker     :: Auto generate cmndsList with no args  [[elisp:(org-cycle)][| ]]
** TODO [[elisp:(org-cycle)][| ]]  wsIcmInvoker     :: Instead of parName=parNameVALUE do parName=partType (int64) [[elisp:(org-cycle)][| ]]
** TODO [[elisp:(org-cycle)][| ]]  rinvokerXxxx     :: Create a thin template for using wsIcmInvoker [[elisp:(org-cycle)][| ]]

**      [End-Of-Status]
"""

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/libre/ByStar/InitialTemplates/update/sw/icm/py/moduleOverview.py"
        icm.unusedSuppressForEval(moduleUsage, moduleStatus)
        actions = self.cmndArgsGet("0&2", cmndArgsSpecDict, effectiveArgsList)
        if actions[0] == "all":
            cmndArgsSpec = cmndArgsSpecDict.argPositionFind("0&2")
            argChoices = cmndArgsSpec.argChoicesGet()
            argChoices.pop(0)
            actions = argChoices
        for each in actions:
            print each
            if interactive:
                #print( str( __doc__ ) )  # This is the Summary: from the top doc-string
                #version(interactive=True)
                exec("""print({})""".format(each))
                
        return(format(str(__doc__)+moduleDescription))

    """
**  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Method-anyOrNone :: /cmndArgsSpec/ retType=bool argsList=nil deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(self):
        """
***** Cmnd Args Specification
"""
        cmndArgsSpecDict = icm.CmndArgsSpecDict()
        cmndArgsSpecDict.argsDictAdd(
            argPosition="0&2",
            argName="actions",
            argDefault='all',
            argChoices=['all', 'moduleDescription', 'moduleUsage', 'moduleStatus'],
            argDescription="Output relevant information",
        )

        return cmndArgsSpecDict
####+END:

####+BEGIN: bx:icm:python:subSection :title "Common Arguments Specification"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ================ [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]          *Common Arguments Specification*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] 
"""
####+END:

####+BEGIN: bx:icm:python:func :funcName "commonParamsSpecify" :funcType "anyOrNone" :retType "bool" :deco "" :argsList "icmParams"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-anyOrNone :: /commonParamsSpecify/ retType=bool argsList=(icmParams)  [[elisp:(org-cycle)][| ]]
"""
def commonParamsSpecify(
    icmParams,
):
####+END:

    icmParams.parDictAdd(
        parName='svcSpec',
        parDescription="URI for OpenApi/Swagger Specification",
        parDataType=None,
        parDefault=None,
        parChoices=list(),
        parScope=icm.ICM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--svcSpec',
    )

    icmParams.parDictAdd(
        parName='perfSap',
        parDescription="Performer SAP For Constructing Full URLs with end-points",
        parDataType=None,
        parDefault=None,
        parChoices=list(),
        parScope=icm.ICM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--perfSap',
    )

    icmParams.parDictAdd(
        parName='resource',
        parDescription="Resource Name (end-point)",
        parDataType=None,
        parDefault=None,
        parChoices=list(),
        parScope=icm.ICM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--resource',
    )

    icmParams.parDictAdd(
        parName='opName',
        parDescription="Operation Name",
        parDataType=None,
        parDefault=None,
        parChoices=list(),
        parScope=icm.ICM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--opName',
    )

    icmParams.parDictAdd(
        parName='headers',
        parDescription="Headers File",
        parDataType=None,
        parDefault=None,
        parChoices=list(),
        parScope=icm.ICM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--headers',
    )
    
    

"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *Common Examples Sections*
"""

####+BEGIN: bx:icm:python:func :funcName "examples_commonInvoker" :funcType "anyOrNone" :retType "bool" :deco "" :argsList "svcSpecUrl svcSpecFile perfSap headers"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-anyOrNone :: /examples_commonInvoker/ retType=bool argsList=(svcSpecUrl svcSpecFile perfSap headers)  [[elisp:(org-cycle)][| ]]
"""
def examples_commonInvoker(
    svcSpecUrl,
    svcSpecFile,
    perfSap,
    headers,
):
####+END:
    """."""
    
    def cpsInit(): return collections.OrderedDict()
    def menuItem(verbosity): icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity=verbosity) # 'little' or 'none'
    def execLineEx(cmndStr): icm.ex_gExecMenuItem(execLine=cmndStr)

    icm.cmndExampleMenuChapter('*Service Specification Digestion*')

    cmndName = "svcOpsList"

    if svcSpecUrl:

        icm.cmndExampleMenuSection('* -i svcOpsList  svcSpecUrl*')        
        
        cps = cpsInit();
        cps['svcSpec'] = svcSpecUrl
        cps['headers'] = headers
        cmndArgs = "";
        menuItem(verbosity='none')
        icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='full')

        cps = cpsInit();
        cps['svcSpec'] = svcSpecUrl
        cps['perfSap'] = perfSap
        cps['headers'] = headers
        cmndArgs = "";
        menuItem(verbosity='none')    

    if svcSpecFile:

        icm.cmndExampleMenuSection('* -i svcOpsList  svcSpecFile*')        
        
        cps = cpsInit();
        cps['svcSpec'] = svcSpecFile
        cps['headers'] = headers
        cmndArgs = "";
        menuItem(verbosity='none')
        icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='full')

        cps = cpsInit();
        cps['svcSpec'] = svcSpecFile

        
        cps['perfSap'] = perfSap
        cps['headers'] = headers
        cmndArgs = "";
        menuItem(verbosity='none')    
        


####+BEGIN: bx:icm:python:section :title "ICM Commands"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *ICM Commands*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] 
"""
####+END:
    

####+BEGIN: bx:icm:python:cmnd:classHead :cmndName "svcOpsList" :parsMand "svcSpec" :parsOpt "perfSap headers" :argsMin "0" :argsMax "1" :asFunc "" :interactiveP ""
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || ICM-Cmnd       :: /svcOpsList/ parsMand=svcSpec parsOpt=perfSap headers argsMin=0 argsMax=1 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
"""
class svcOpsList(icm.Cmnd):
    cmndParamsMandatory = [ 'svcSpec', ]
    cmndParamsOptional = [ 'perfSap', 'headers', ]
    cmndArgsLen = {'Min': 0, 'Max': 1,}

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
        interactive=False,        # Can also be called non-interactively
        svcSpec=None,         # or Cmnd-Input
        perfSap=None,         # or Cmnd-Input
        headers=None,         # or Cmnd-Input
        argsList=[],         # or Args-Input
    ):
        cmndOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=cmndOutcome):
                return cmndOutcome
            effectiveArgsList = G.icmRunArgsGet().cmndArgs
        else:
            effectiveArgsList = argsList

        callParamsDict = {'svcSpec': svcSpec, 'perfSap': perfSap, 'headers': headers, }
        if not icm.cmndCallParamsValidate(callParamsDict, interactive, outcome=cmndOutcome):
            return cmndOutcome
        svcSpec = callParamsDict['svcSpec']
        perfSap = callParamsDict['perfSap']
        headers = callParamsDict['headers']

        cmndArgsSpecDict = self.cmndArgsSpec()
        if not self.cmndArgsValidate(effectiveArgsList, cmndArgsSpecDict, outcome=cmndOutcome):
            return cmndOutcome
####+END:

        #print("YYYYYYYYYY")
        #print(svcSpec)
        #print(perfSap)

        try:         
            loadedSvcSpec, origin_url = loadSvcSpec(svcSpec, perfSap)
        except:
            print("wsInvokerIcm.svcOpsList Failed -- svcSpec={svcSpec}".format(
                svcSpec=svcSpec,
            ))
            return

        #pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(loadedSvcSpec)


        processSvcSpec(loadedSvcSpec, origin_url, perfSap, headers, svcSpec)



    
    def cmndDocStr(self): return """
** Place holder for ICM's experimental or test code.  [[elisp:(org-cycle)][| ]]
 You can use this Cmnd for rapid prototyping and testing of newly developed functions.
"""


####+BEGIN: bx:icm:python:cmnd:classHead :cmndName "rinvoke" :parsMand "svcSpec resource opName" :parsOpt "perfSap headers" :argsMin "0" :argsMax "999" :asFunc "" :interactiveP ""
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || ICM-Cmnd       :: /rinvoke/ parsMand=svcSpec resource opName parsOpt=perfSap headers argsMin=0 argsMax=999 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
"""
class rinvoke(icm.Cmnd):
    cmndParamsMandatory = [ 'svcSpec', 'resource', 'opName', ]
    cmndParamsOptional = [ 'perfSap', 'headers', ]
    cmndArgsLen = {'Min': 0, 'Max': 999,}

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
        interactive=False,        # Can also be called non-interactively
        svcSpec=None,         # or Cmnd-Input
        resource=None,         # or Cmnd-Input
        opName=None,         # or Cmnd-Input
        perfSap=None,         # or Cmnd-Input
        headers=None,         # or Cmnd-Input
        argsList=[],         # or Args-Input
    ):
        cmndOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=cmndOutcome):
                return cmndOutcome
            effectiveArgsList = G.icmRunArgsGet().cmndArgs
        else:
            effectiveArgsList = argsList

        callParamsDict = {'svcSpec': svcSpec, 'resource': resource, 'opName': opName, 'perfSap': perfSap, 'headers': headers, }
        if not icm.cmndCallParamsValidate(callParamsDict, interactive, outcome=cmndOutcome):
            return cmndOutcome
        svcSpec = callParamsDict['svcSpec']
        resource = callParamsDict['resource']
        opName = callParamsDict['opName']
        perfSap = callParamsDict['perfSap']
        headers = callParamsDict['headers']

        cmndArgsSpecDict = self.cmndArgsSpec()
        if not self.cmndArgsValidate(effectiveArgsList, cmndArgsSpecDict, outcome=cmndOutcome):
            return cmndOutcome
####+END:

        opParsList = self.cmndArgsGet("0&-1", cmndArgsSpecDict, effectiveArgsList)


        #print(svcSpec)
        #print(perfSap)

        #generateSvcInfo("http://localhost:8080/swagger.json")
        loadedSvcSpec, origin_url = loadSvcSpec(svcSpec, perfSap)
        #print("MMMM")
        #print(origin_url)

        if perfSap:
            #origin_url = "http://localhost:8080"
            origin_url = perfSap

        pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(loadedSvcSpec)

        op = getOperationWithResourceAndOpName(loadedSvcSpec, origin_url, resource, opName)

        
        opInvokeEvalStr="opInvoke(headers, op, "
        for each in opParsList:
            parVal = each.split("=")
            parValLen = len(parVal)

            if parValLen == 2:
                parName=parVal[0]
                parValue=parVal[1]
            else:
                print(parValLen)
                continue
            
            opInvokeEvalStr = opInvokeEvalStr + """{parName}="{parValue}", """.format(
                parName=parName, parValue=parValue
                )
            
        opInvokeEvalStr = opInvokeEvalStr + ")"
        print("Invoking With Eval: str={opInvokeEvalStr}".format(opInvokeEvalStr=opInvokeEvalStr,))

        eval(opInvokeEvalStr)
        
        return

    
    def cmndDocStr(self): return """
** Place holder for ICM's experimental or test code.  [[elisp:(org-cycle)][| ]]
 You can use this Cmnd for rapid prototyping and testing of newly developed functions.
"""

####+BEGIN: bx:icm:python:method :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList ""
    """
**  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Method-anyOrNone :: /cmndArgsSpec/ retType=bool argsList=nil deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(self):
####+END:
        """
        ***** Cmnd Args Specification
        """
        cmndArgsSpecDict = icm.CmndArgsSpecDict()
        cmndArgsSpecDict.argsDictAdd(
            argPosition="0&-1",
            argName="actionPars",
            argDefault=None,
            argChoices='any',
            argDescription="Rest of args for use by action"
            )

        return cmndArgsSpecDict
        
    
        
####+BEGIN: bx:icm:python:section :title "Supporting Classes And Functions"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *Supporting Classes And Functions*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] 
"""
####+END:

####+BEGIN: bx:icm:python:func :funcName "loggingSetup" :funcType "void" :retType "bool" :deco "" :argsList ""
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-void      :: /loggingSetup/ retType=bool argsList=nil  [[elisp:(org-cycle)][| ]]
"""
def loggingSetup():
####+END:
    # Debug logging
    logControler = icm.LOG_Control()
    icmLogger = logControler.loggerGet()
    
    icmLogLevel = logControler.level
    #icmLogLevel = logControler.loggerGetLevel()  # Use This After ICM has been updated

    def requestsDebugLog():
        httplib.HTTPConnection.debuglevel = 1
        logging.basicConfig()
        if icmLogLevel:
            if icmLogLevel <= 10:
                logging.getLogger().setLevel(logging.DEBUG)
        req_log = logging.getLogger('requests.packages.urllib3')
        req_log.setLevel(logging.DEBUG)
        req_log.propagate = True

    if icmLogLevel:
        if icmLogLevel <= 20:
            requestsDebugLog()

    
####+BEGIN: bx:icm:python:func :funcName "loadSvcSpec" :funcType "anyOrNone" :retType "bool" :deco "" :argsList "spec perfSap"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-anyOrNone :: /loadSvcSpec/ retType=bool argsList=(spec perfSap)  [[elisp:(org-cycle)][| ]]
"""
def loadSvcSpec(
    spec,
    perfSap,
):
####+END:
    """Returns a dictionary -- perfSap is unused"""
    origin_url = None
    if isinstance(spec, str):
        if spec.startswith('https://') or spec.startswith('http://'):
            origin_url = spec
            r = requests.get(spec)
            r.raise_for_status()
            spec = yaml.safe_load(r.text)
        else:
            with open(spec, 'rb') as fd:
                spec = yaml.safe_load(fd.read())

    spec = sanitize_spec(spec)
    return spec, origin_url


####+BEGIN: bx:icm:python:func :funcName "processSvcSpec" :funcType "anyOrNone" :retType "bool" :deco "" :argsList "spec origin_url perfSap headers svcSpec"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-anyOrNone :: /processSvcSpec/ retType=bool argsList=(spec origin_url perfSap headers svcSpec)  [[elisp:(org-cycle)][| ]]
"""
def processSvcSpec(
    spec,
    origin_url,
    perfSap,
    headers,
    svcSpec,
):
####+END:
    pp = pprint.PrettyPrinter(indent=4)

    spec = Spec.from_dict(spec, origin_url=origin_url)
    #pp.pprint(spec)

    thisIcm = G.icmMyName()

    perfSapStr = ""
    if perfSap:
        perfSapStr = "--perfSap={perfSap} ".format(perfSap=perfSap)

    headersStr = ""
    if headers:
        headersStr = "--headers={headers} ".format(headers=headers)

    if origin_url:
        svcSpecStr = origin_url
    else:
        svcSpecStr = svcSpec
        
    for res_name, res in spec.resources.items():
        for op_name, op in res.operations.items():
            name = get_command_name(op)

            paramsListStr = ""
            for param_name, param in op.params.items():
                paramsListStr = paramsListStr + " {param_name}={parName}VALUE".format(
                    param_name=param_name, parName=param_name,)
                    
                #print(param.required)
                #print(param.name)

            print("{thisIcm} --svcSpec={svcSpec} {perfSapStr} {headersStr} --resource={res_name} --opName={op_name} -i rinvoke {paramsListStr}".format(
                thisIcm=thisIcm,
                svcSpec=svcSpecStr,
                perfSapStr=perfSapStr,
                headersStr=headersStr,                                                                      
                res_name=res_name,
                op_name=op_name,
                paramsListStr=paramsListStr,
                )
            )
                
                
####+BEGIN: bx:icm:python:func :funcName "getOperationWithResourceAndOpName" :funcType "anyOrNone" :retType "bool" :deco "" :argsList "spec origin_url resource opName"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-anyOrNone :: /getOperationWithResourceAndOpName/ retType=bool argsList=(spec origin_url resource opName)  [[elisp:(org-cycle)][| ]]
"""
def getOperationWithResourceAndOpName(
    spec,
    origin_url,
    resource,
    opName,
):
####+END:
    """Returns op object."""

    pp = pprint.PrettyPrinter(indent=4)

    spec = Spec.from_dict(spec, origin_url=origin_url)
    #pp.pprint(spec)
    
    for res_name, res in spec.resources.items():
        if res_name != resource:
            continue

        for op_name, op in res.operations.items():
            if op_name != opName:
                continue
            
            name = get_command_name(op)

            print("Validated -- resource={resource}  opName={opName}".format(
                resource=resource, opName=op_name))

            return op

####+BEGIN: bx:icm:python:func :funcName "normalize_command_name" :funcType "anyOrNone" :retType "bool" :deco "" :argsList "str"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-anyOrNone :: /normalize_command_name/ retType=bool argsList=(str)  [[elisp:(org-cycle)][| ]]
"""
def normalize_command_name(
    str,
):
####+END:
    '''
    >>> normalize_command_name('My Pets')
    'my-pets'

    >>> normalize_command_name('.foo.bar.')
    'foo-bar'
    '''
    return REPLACEABLE_COMMAND_CHARS.sub('-', str.lower()).strip('-')



####+BEGIN: bx:icm:python:func :funcName "get_command_name" :funcType "anyOrNone" :retType "bool" :deco "" :argsList "op"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-anyOrNone :: /get_command_name/ retType=bool argsList=(op)  [[elisp:(org-cycle)][| ]]
"""
def get_command_name(
    op,
):
####+END:
    if op.http_method == 'get' and '{' not in op.path_name:
        return 'list'
    elif op.http_method == 'put':
        return 'update'
    else:
        return op.http_method


####+BEGINNOT: bx:icm:python:func :funcName "opInvoke" :funcType "anyOrNone" :retType "bool" :deco "" :argsList "headers op *args **kwargs"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-anyOrNone :: /opInvoke/ retType=bool argsList=(headers op *args **kwargs)  [[elisp:(org-cycle)][| ]]
"""
def opInvoke(
    headers,
    op,
    *args,
    **kwargs
):
####+END:

    pp = pprint.PrettyPrinter(indent=4)

    headerLines = list()
    if headers:
        with open(headers, 'rb') as file:
            headerLines = file.readlines()
        
    # else:
    #     print("Has No Headers")

    headerLinesAsDict = dict()
    for each in headerLines:
        headerLineAsList = each.split(":")
        headerLineAsListLen = len(headerLineAsList)
        
        if headerLineAsListLen == 2:
            headerLineTag = headerLineAsList[0]
            headerLineValue = headerLineAsList[1]
        else:
            print(headerLineAsListLen)
            continue

        headerLinesAsDict[headerLineTag] = headerLineValue.lstrip(' ').rstrip()

    if headerLinesAsDict:
        headersDict = {
            "headers": headerLinesAsDict
        }
    else:
        headersDict = dict()

    #pp.pprint(headerLinesAsDict)
    #pp.pprint(headersDict)

    # headersDict = {
    #     "headers": {
    #         headerBearerTokenTag: headerBearerTokenValue
    #         }
    #     }

    if op.http_method != 'get':
        print(op.http_method)
        print('http_method is not get')
    #request = construct_request(op, _request_options={"headers": {"foo": "bar"}}, {}, **kwargs)
    request = construct_request(op, headersDict, **kwargs)    
    print("request=")
    pp.pprint(request)

    c = RequestsClient()

    #print("RequestsClient=")    
    #pp.pprint(c)    
    future = c.request(request)
    
    #print("future=")        
    #pp.pprint(future)    
    result = future.result()
    #pp.pprint(result)
    print("Operation Result:")
    print(result)


def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.


    Usage:
    req = requests.Request('POST','http://stackoverflow.com',headers={'X-Custom':'Test'},data='a=1&b=2')
    prepared = req.prepare()
    pretty_print_POST(prepared)
    """
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))
    
    
    
####+BEGIN: bx:icm:python:func :funcName "sanitize_spec" :funcType "anyOrNone" :retType "bool" :deco "" :argsList "spec"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-anyOrNone :: /sanitize_spec/ retType=bool argsList=(spec)  [[elisp:(org-cycle)][| ]]
"""
def sanitize_spec(
    spec,
):
####+END:
    for path, path_obj in list(spec['paths'].items()):
        # remove root paths as no resource name can be found for it
        if path == '/':
            del spec['paths'][path]
    return spec

    

####+BEGIN: bx:icm:python:section :title "End Of Editable Text"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *End Of Editable Text*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] 
"""
####+END:

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/libre/ByStar/InitialTemplates/software/plusOrg/dblock/inserts/endOfFileControls.org"
#+STARTUP: showall
####+END:
