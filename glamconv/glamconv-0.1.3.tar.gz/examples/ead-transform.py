# -*- coding: utf-8 -*-
"""
Script running the process for transforming EAD-2002 into Ape-EAD onto the
XML files found inside a hierarchy of directories.
"""

from os import path as osp
import argparse as argp
from glamconv.cli.commands import register_actions, transform_files_from_dir


HERE = osp.abspath(osp.dirname(__file__))

PROCESS_FILENAME = osp.join(HERE, "generic-ead-transformation.json")

COUNTRY_CODES = (
    u"AF AX AL DZ AS AD AO AI AQ AG AR AM AW AU AT AZ BS BH BD BB "
    u"BY BE BZ BJ BM BT BO BA BW BV BR IO BN BG BF BI KH CM CA CV "
    u"KY CF TD CL CN CX CC CO KM CG CD CK CR CI HR CU CY CZ DK DJ "
    u"DM DO EC EG SV GQ ER EE ET FK FO FJ FI FR GF PF TF GA GM GE "
    u"DE GH GI GR GL GD GP GU GT GN GW GY HT HM VA HN HK HU IS IN "
    u"ID IR IQ IE IL IT JM JP JO KZ KE KI KP KR KW KG LA LV LB LS "
    u"LR LY LI LT LU MO MK MG MW MY MV ML MT MH MQ MR MU YT MX FM "
    u"MD MC MN MS MA MZ MM NA NR NP NL AN NC NZ NI NE NG NU NF MP "
    u"NO OM PK PW PS PA PG PY PE PH PN PL PT PR QA RE RO RU RW SH "
    u"KN LC PM VC WS SM ST SA SN CS SC SL SG SK SI SB SO ZA GS ES "
    u"LK SD SR SJ SZ SE CH SY TW TJ TZ TH TL TG TK TO TT TN TR TM "
    u"TC TV UG UA AE GB US UM UY UZ VU VE VN VG VI WF EH YE ZM ZW "
    u"RS ME EU"
).split()

DEFAULT_COUNTRY = u"FR"


def id_params_setter(process, filename):
    identifiers_step = None
    for step in process.steps:
        if step.action.uid == u"identifiers-definer":
            identifiers_step = step
            break
    if identifiers_step is not None:
        # Setting agency code and country code
        code = osp.splitext(filename)[0].split("_")[0].upper()
        country = DEFAULT_COUNTRY
        if len(code) > 2:
            if code[:2] in COUNTRY_CODES:
                country = code[:2]
                code = code[2:]
        code = country + u"-" + code
        identifiers_step.params[u"agency_code"] = code
        identifiers_step.params[u"country_code"] = country
        identifiers_step.params[u"document_id"] = filename
        identifiers_step.params[u"favour_xml_document_id"] = True


def run(input_dir, output_dir):
    register_actions()
    input_dir = osp.normpath(osp.abspath(input_dir))
    output_dir = osp.normpath(osp.abspath(output_dir))
    transform_files_from_dir(
        PROCESS_FILENAME, input_dir, output_dir, recursive=True,
        adapt_process_params=id_params_setter)


if __name__ == "__main__":
    parser = argp.ArgumentParser(
        description=u"Transform the XML files in a directory tree from "
        u"EAD-2002 standard to Ape-EAD standard.")
    parser.add_argument(
        u"input_dir", metavar=u"input_directory", type=str,
        help=u"name of the directory where the XML files are "
        u"read from.")
    parser.add_argument(
        u"output_dir", metavar=u"output_directory", type=str,
        help=u"name of the directory where the transformed XML "
        u"files are written to. Should be different from the "
        u"input directory to avoid overwriting the input "
        u"files.")
    args = parser.parse_args()
    run(args.input_dir, args.output_dir)
