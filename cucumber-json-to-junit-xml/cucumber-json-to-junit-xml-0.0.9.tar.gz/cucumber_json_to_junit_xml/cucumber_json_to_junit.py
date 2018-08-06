#!/usr/bin/env python3
'''
Utility to convert from Cucumber JSON output to JUnit XML output
'''

import sys
import json

def main():
    '''
    Main function
    '''
    if len(sys.argv) < 2 or not sys.argv[1].endswith(".json"):
        print("No JSON file path received. Usage:")
        print("\tpython cucumber-json-to-junit.py source-report.json target-report.xml")
        sys.exit()
    if len(sys.argv) < 3 or not sys.argv[2].endswith(".xml"):
        print("No XML file path received. Usage:")
        print("\tpython cucumber-json-to-junit.py source-report.json target-report.xml")
        sys.exit()

    with open(sys.argv[1], "r") as json_file:
        print("Opening file " + sys.argv[1] + " in read-only")
        json_data = json.load(json_file)

    test_cases = ""
    header = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n"

    test_suite_time = 0.0
    failure_count = 0
    scenario_count = 0

    for feature in json_data:

        feature_name = sanitize(feature["name"])
        scenarios = feature["elements"]
        feature_time = 0.0


        for scenario in scenarios:

            scenario_count += 1

            scenario_name = sanitize(scenario["name"])
            steps_blob = "<![CDATA["
            err_blob = ""
            scenario_status = "passed"
            scenario_time = 0.0

            for step in scenario["steps"]:

                description = sanitize(step["name"])
                results = step["result"]
                status = sanitize(results["status"])
                keyword = sanitize(step["keyword"])

                if status != "skipped":
                    scenario_time += float(results["duration"]) / 1000000000

                num_dots = 83 - len(keyword) - len(description) - len(status)
                if num_dots <= 0:
                    num_dots = 1

                steps_blob += keyword + description
                for i in range(num_dots):
                    steps_blob += "."
                steps_blob += status + "\n"
                if status == "failed":
                    err_blob = sanitize(results["error_message"])
                    scenario_status = "failed"
                    failure_count += 1

            feature_time += scenario_time

            steps_blob += "]]>"

            test_case = "<testcase "
            test_case += "classname=\"" + feature_name + "\" "
            test_case += "name=\"" + scenario_name + "\" "
            test_case += "time=\"" + str(scenario_time) + "\">"
            if scenario_status == "passed":
                test_case += "<system-out>" + steps_blob + "</system-out>\n"
            else:
                test_case += "<failure message=\"" + err_blob + "\">"
                test_case += steps_blob + "</failure>\n"
            test_case += "</testcase>\n"

        test_cases += test_case
        test_suite_time += feature_time

    test_suite = "<testsuite "
    test_suite += "failures=\"" + str(failure_count) + "\" "
    test_suite += "name=\"Cucumber JSON to JUnit\" "
    test_suite += "skipped=\"0\" "
    test_suite += "tests=\"" + str(scenario_count) + "\" "
    test_suite += "time=\"" + str(test_suite_time) + "\">\n"
    for test_case in test_cases:
        test_suite += test_case
    test_suite += "</testsuite>"


    with open(sys.argv[2], "w") as junit_file:
        print("Writing to file " + sys.argv[2] + "...")
        junit_file.write(header)
        junit_file.write(test_suite)

    print("Done.")

def sanitize(input):
    input = input.replace("&","&amp;").replace("\"","&quot;")
    input = input.replace("<","&lt;").replace(">","&gt;")
    return input

if __name__ == "__main__":
    # execute only if run as a script
    main()
