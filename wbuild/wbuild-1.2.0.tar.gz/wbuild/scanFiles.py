import os
import sys
import pathlib
import re
from snakemake.logging import logger
from wbuild.utils import parseWBInfosFromRFiles, parseMDFiles, getYamlParam, pathsepsToUnderscore, \
    Config

pathsep = "/"
sys.path.insert(0, os.getcwd() + "/.wBuild")

# SNAKEMAKE  = ["input", "output", "threads"]

#dict containing snakemake supported fields
SNAKEMAKE_FIELDS = ["input",
                    "output",
                    "params",
                    "threads",
                    "resources",
                    "priority",
                    "version",
                    "log",
                    "message",
                    "run",
                    "shell",
                    "script"]


def writeDependencyFile():
    """
    Entry point for writing .wBuild.depend.
    """
    logger.info("Structuring dependencies...")
    conf = Config()
    htmlOutputPath = conf.get("htmlOutputPath")
    logger.debug("Loaded config.\n html output path (key htmlOutputPath): " + htmlOutputPath + "\n")
    scriptsPath = conf.get("scriptsPath")
    logger.debug("Scripts path (key scriptsPath): " + scriptsPath + "\nprocessedDataPath: " + conf.get(
        "processedDataPath") + "\n")
    wbData = parseWBInfosFromRFiles(script_dir=scriptsPath, htmlPath=htmlOutputPath)
    mdData = parseMDFiles(script_dir=scriptsPath, htmlPath=htmlOutputPath)
    with open('.wBuild.depend', 'w') as f: #start off with the header
        f.write('######\n')
        f.write('#This is a autogenerated snakemake file by wBuild\n')
        f.write('#wBuild by Leonhard Wachutka\n')
        f.write('######\n')

        # write rules
        for r in wbData:
            writeRule(r, f)
        # write md rules
        for r in mdData:
            writeMdRule(r, f)

        # write build index rule
        writeIndexRule(wbData, mdData, f)
    logger.info("Dependencies file generated.\n")


def joinEmpty(string_list):
    """
    :param string_list:
    :return: sting representation of a list without the blank elements.
    """
    return ", ".join([x for x in string_list if x.strip() != ''])


def escapeSMString(item):
    """
    Convert item to the appropriate string representation.

    :param item: string or dict
    :return: "key = 'value'" (dict), "'value'" (string) or '' (other type)
    """
    if type(item) is dict:
        #return "key = value"
        return str(list(item.keys())[0]) + ' = ' + escapeSMString(str(list(item.values())[0]))
    elif type(item) is str:
        if item.startswith("`sm ") and item.endswith("`"): #strip `sm ... `
            return item[4:-1]
        return "'" + item + "'" #return item as quoted string
    return ''


def ensureString(elem):
    if elem is None:
        return ''
    elif type(elem) is list:
        if len(elem) == 0:
            return ''
        else:
            # make sure each element is a character
            elem = [escapeSMString(item) for item in elem]
            elem = [x for x in elem if str(x).strip() != '']

            return ", ".join(elem)
    elif type(elem) is str:
        if "," not in elem:
            return "'" + elem + "'"
        else:
            return elem
    else:
        raise TypeError("Don't know how to handle type: " + str(type(elem)))


def dumpSMRule(ruleInfos, outputFile, inputFile):
    """
    Write the rule to the file.

    :param ruleInfos: dictionary containing all the rule's data
    :param outputFile: file to print the rule to
    :param inputFile: the object of the rule
    """
    if 'py' in ruleInfos:
        code = ruleInfos['py']
        if type(code) is str:
            outputFile.write(insertPlaceholders(code, inputFile))
        elif type(code) is list:
            [outputFile.write(insertPlaceholders(line, inputFile) + '\n') for line in code]

    outputFile.write('rule ' + ruleInfos['rule'] + ':\n')
    for field in SNAKEMAKE_FIELDS:
        if field in ruleInfos:
            outputFile.write('    ' + field + ': ' + str(ruleInfos[field]) + '\n')


def insertPlaceholders(dest, source):
    """
    Infer placeholders' substitutions.

    :param dest: string to replace placeholders in
    :param source: file; from its path we infer the placeholders values
    :return: dest with replaced placeholders
    """
    path = pathlib.Path(source) #get the path to the file
    conf = Config()
    processedDataPath = conf.get("processedDataPath")
    PD = pathlib.Path(processedDataPath)

    PP = path.parts[-2] #last two nodes of the path
    dest = dest.replace("{wbPD}", str(PD))
    dest = dest.replace("{wbPP}", str(PP))

    if len(path.parts) <= 2 and bool(re.search('{wbP(D_P*)?}', source)):
        print("If using placeholders please make sure you have the right",
              " directory structure.")

    if len(path.parts) > 2:
        P = path.parts[-3] #last 3 nodes of the path
        dest = dest.replace("{wbPD_P}", str(PD / P))
        dest = dest.replace("{wbPD_PP}", str(PD / P / PP))
        dest = dest.replace("{wbP}", str(P))

    return dest


def writeRule(r, file):
    """
    Write Snakemake rule from the parsed WB header informations.

    :param r: parsed WB data dictionary entry
    :param file: to write the rule to
    """
    #TODO cleanup boilerplate commented code here
    wbInfos = r["param"]["wb"]
    inputFile = r['file'] #input R script for Snakemake

    # extract rule
    # rule = r['file'].replace('.','_').replace('/','_')

    # determine input, output and script
    wbInfos["input"] = insertPlaceholders(joinEmpty([ensureString(wbInfos.get("input")), "RScript = '" + inputFile + "'"]), inputFile)
    if wbInfos.get("type") == 'script':
        wbInfos["output"] = insertPlaceholders(ensureString(wbInfos.get("output")), inputFile)
        wbInfos["script"] = '\'' + inputFile + '\''
    elif wbInfos.get("type") == 'noindex':
        wbInfos["output"] = insertPlaceholders(ensureString(wbInfos.get("output")), inputFile)
        wbInfos["script"] = "'.wBuild/wBRender.R'"
    else:
        wbInfos["output"] = insertPlaceholders(joinEmpty([ensureString(wbInfos.get("output")), "wBhtml = '" + r['outputFile'] + "'"]), inputFile)
        wbInfos["script"] = "'.wBuild/wBRender.R'"

    # remove wb related elements
    # wbInfos = {key: wbInfos[key] for key in wbInfos if key not in WB_FIELDS}
    # if not set(wbInfos.keys()).issubset(SNAKEMAKE_FIELDS):
    #    Warning("File: {0}. The following fields don't correspond to any snakemake or wBuild tag: {1}"
    #            .format(r['file'], ",".join(set(wbInfos.keys()).difference(SNAKEMAKE_FIELDS))))

    # remove fields not in SNAKEMAKE_FIELDS
    # wbInfos = {key: wbInfos[key] for key in wbInfos if key in SNAKEMAKE_FIELDS}
    wbInfos['rule'] = pathsepsToUnderscore(r['file'], True) # convert filepath to the unique id of the rule
    # write to file
    file.write('\n')
    # dumpDict = {'rule ' + rule: wbInfos}
    # file.write(yaml.dump(dumpDict, default_flow_style = False, indent=4).replace("\'\'\'", "'").replace("\'\'", "'"))
    dumpSMRule(wbInfos, file, inputFile)
    file.write('\n')


def writeMdRule(ruleInfos, file):
    """
    :param ruleInfos:
    :param file: file to write the rule to
    """
    file.write('\n')
    file.write('rule ' + pathsepsToUnderscore(ruleInfos['file'], True) + ':\n')
    file.write('    input: "' + ruleInfos['file'] + '"\n')
    file.write('    output: "' + ruleInfos['outputFile'] + '"\n')
    file.write('    shell: "pandoc --from markdown --to html --css .wBuild/lib/github.css --toc --self-contained -s -o {output} {input}"\n')

    file.write('\n')


def writeIndexRule(wbRRows, wbMDrows, file):
    """
    Write the rule of mapping the R and md wbData to the index.html.

    :param wbRRows: info dict parsed from R wB files
    :param wbMDrows: info dict parsed from MD wB files
    :param file: file to print the index rule to
    """
    inputFiles = []
    for r in wbRRows:
        #ignore if the file is script or noindex
        if getYamlParam(r, 'type') == 'script' or getYamlParam(r, 'type') == 'noindex':
            continue

        inputFiles.append(r['outputFile'])

    for r in wbMDrows:
        inputFiles.append(r['outputFile'])

    conf = Config()
    htmlOutputPath = conf.get("htmlOutputPath")

    file.write('\n')
    file.write('rule Index:\n')
    file.write('    input: \n        "' + '",\n        "'.join(inputFiles) + '"\n')
    file.write('    output: "' + htmlOutputPath + '/index.html"\n')
    # file.write('    script: ".wBuild/createIndex.py"\n')
    file.write('    run:\n')
    file.write('        import wbuild.createIndex\n')
    file.write('        wbuild.createIndex.ci()\n')

    file.write('\n')


if __name__ == "__main__":
    writeDependencyFile()
