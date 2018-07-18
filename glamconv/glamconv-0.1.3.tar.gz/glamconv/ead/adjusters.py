# -*- coding: utf-8 -*-
"""
Module containing actions for changing the values of the vocabulary-controlled
attributes in order to have a legit value.
"""

import re
from glamconv.ead.utils import log_element, add_text_around_element
from glamconv.ead.formats import EAD_2002
from glamconv.transformer.actions import TransformAction


OTHLEV_REGEXP = re.compile(r"^([A-Za-z]|:|_)([0-9A-Za-z]|:|_|-|\.)*$")


class ArchdescLevelAttribAdjuster(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"archdesc-level-adjuster"
    name = u"Adjusting the value of level attribute in <archdesc>"
    category = u"Cleansing"
    desc = (u"In the 'level' attribute of <archdesc> elements the only "
            u"possible legit value is \"fonds\". This action sets 'level' "
            u"to its legit value and puts its previous value in the "
            u"'otherlevel' attribute of <archsdesc> if it is empty.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        for arch in xml_root.xpath(
                u'.//archdesc[not(@level) or @level!="fonds"]'):
            msg = u""
            value = arch.get(u"level", u"")
            if value not in [u"", u"otherlevel"] \
               and arch.get(u"otherlevel", u"") != u"" \
               and OTHLEV_REGEXP.match(value) is not None:
                arch.set(u"otherlevel", value)
            else:
                msg = (u"    Old value: {0}".format(value))
            arch.set(u"level", u"fonds")
            count += 1
            if log_details:
                log_data.append(log_element(arch, msg=msg))
        if count > 0:
            logger.warning(
                u"The 'level' attribute in the <archdesc> element can only "
                u"have one value: \"fonds\". {0:d} elements have been "
                u"corrected.".format(count))
            if log_details:
                logger.warning(u"The following elements have been corrected:",
                               u"\n".join(log_data))
        return xml_root


class DscTypeAttribAdjuster(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"dsc-type-adjuster"
    name = u"Adjusting the value of type attribute in <dsc>"
    category = u"Cleansing"
    desc = (u"In the 'type' attribute of <dsc> elements the only possible "
            u"legit value is \"othertype\". This action sets 'type' "
            u"to its legit value.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        for dsc in xml_root.xpath(u'.//dsc[@type!="othertype"]'):
            if log_details:
                msg = u"    Old value: {0}".format(dsc.get("type"))
                log_data.append(log_element(dsc, msg=msg))
            dsc.attrib['type'] = 'othertype'
            count += 1
        if count > 0:
            logger.warning(
                u"The 'type' attribute in the <dsc> element can only have "
                u"one value: \"othertype\". {0:d} elements have been "
                u"corrected.".format(count))
            if log_details:
                logger.warning(u"The following elements have been corrected:",
                               u"\n".join(log_data))
        return xml_root


class EmphRenderAttribAdjuster(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"emph-render-adjuster"
    name = u"Adjusting the value of render attribute in <emph>"
    category = u"Cleansing"
    desc = (u"In the 'render' attribute of <emph> elements the only possible "
            u"legit values are \"bold\" and \"italic\". If the value contains "
            u"\"bold\", sets the value to \"bold\", else if the value "
            u"contains \"italic\", sets the value to \"italic\", else deletes "
            u"the value. If the value contains the mention of quotes (single "
            u"or double), adds them to the text before and after the <emph> "
            u"element.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        for emph in xml_root.xpath(
                u'.//emph[@render!="bold" and @render!="italic"]'):
            value = emph.attrib.pop("render", u"")
            if value == u"":
                continue
            if u"bold" in value:
                emph.set(u"render", u"bold")
            elif u"italic" in value:
                emph.set(u"render", u"italic")
            if u"doublequote" in value:
                add_text_around_element(emph, u"« ", u" »")
            elif u"singlequote" in value:
                add_text_around_element(emph, u"\u2018", u"\u2019")
            if log_details:
                msg = u"    Old value: {0}".format(value)
                log_data.append(log_element(emph, msg=msg, text_content=True))
            count += 1
        if count > 0:
            logger.warning(
                u"The render attribute in the <emph> element can only have "
                u"the values \"bold\" or \"italic\". {0:d} elements have been "
                u"corrected.".format(count))
            if log_details:
                logger.warning(u"The following elements have been corrected:"
                               u"\n".join(log_data))
        return xml_root


LNGS = (u"roh sco scn rom ron alg oss ale alb scc mni nld mno osa mnc scr oci "
        u"mwr crp lua jav hrv lub lun twi aus roa ven uga mwl ger mga hit fas "
        u"ssw lug luo fat fan fao lui tgl ita geo him hin mlg din mun hye gba "
        u"guj cmc slk bad nep iba ban ady div bam bak shn bai arp tel tem arw "
        u"nwc ara tkl arc nbl ter sel tet arm arn ave lus mus sun kut suk kur "
        u"wol kum sus iro new oji kua sux mlt iku hai tup tur men tut mic grc "
        u"tuk tum mul lez nav cop cos cor gla bos gwi gle eka glg akk und dra "
        u"aka tlh bod glv jrb vie ipk por uzb pon pol sah sgn sga tgk bre apa "
        u"wak bra aym cha chb che fre chg swa chi chk fro chm chn cho chp cpf "
        u"chr xal chu chv chy fry dut hat msa gay oto ota hmn hmo ice niu myv "
        u"iii gaa fur ndo ibo ina car slv xho deu cau cat cai slo del fil den "
        u"ilo inh ful sla cad tat jpn vol myn vot ind dzo spa tam jpr tah tai "
        u"bis cze pap afh pau eng afa ewe csb phi paa nyn nyo nym bnt nya sio "
        u"sin afr map mas mar lah phn sna may kir yao snk dgr syr mac mad mag "
        u"mai mah lav mal mao man egy pag znd sit gmh epo jbo tiv tha dum fon "
        u"zen kbd enm kha sam tsn tso dsb cus ell fiu ssa wen wel byn elx gem "
        u"uig ada fij tli fin hau eus haw bin amh non ceb bih mos dan nog bat "
        u"nob dak moh ces mon dar mol son day nor bas cel pal baq pam hil kpe "
        u"dua sot lad lam mdf snd tvl lao abk mdr ijo gon goh sms per smo smn "
        u"peo smj smi pan tmh got sme bla sma gor hsb nic nia run ast mkd sag "
        u"cre fra bik orm que ori rus crh asm pus kik gez srd ltz ach nde sqi "
        u"ath kru srr ido srp nub kro wln isl ava krc nds zun zul kin umb sog "
        u"nso swe som yap lat frm art mak zap yid kok vai kom her kon ukr lol "
        u"mkh ton heb loz kos kor was tog ira pli sid bur hun hup bul wal bua "
        u"bug cym udm bej gil ben bel bem tsi aze war zha ace rum aar ber nzi "
        u"zho nno sai ang pra san bho sal pro arg raj sad khi rar khm rap kho "
        u"sas ine sem sat min lim lin nai tir nah lit efi nap gre grb btk nau "
        u"grn ypk mis tig yor tib kac kab kaa ile kan kam kal kas kar mya est "
        u"kaw kau kat kaz tyv awa kmb urd doi ewo cpe tpi mri dyu cpp bal inc")
LNGS = tuple(LNGS.split(" "))


class LanguageLangcodeAttribAdjuster(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"language-langcode-adjuster"
    name = u"Adjusting the value of langcode attribute in <language>"
    category = u"Cleansing"
    desc = (
        u"The 'langcode' attribute of <language> elements can only take "
        u"a definite set of values. This action erases the attributes that "
        u"don't have a legit value.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        for elt in xml_root.xpath(u'.//language[@langcode]'):
            value = elt.attrib.pop(u"langcode", u"").lower()
            if value in LNGS:
                elt.set(u"langcode", value)
            else:
                if log_details:
                    msg = u"    Deleted value: {0}".format(value)
                    log_data.append(log_element(elt, msg=msg))
                count += 1
        if count > 0:
            logger.warning(
                u"The 'langcode' attribute in the <language> element can only "
                u"have a value taken from a fixed vocabulary. {0:d} elements "
                u"have had their 'langcode' attribute deleted because of a "
                u"non-legit value.".format(count))
            if log_details:
                logger.warning(u"The following elements have been corrected:"
                               u"\n".join(log_data))
        return xml_root


SCRS = (u"Tfng Shaw Cirt Guru Hebr Geor Zzzz Phnx Hrkt Plrd Ogam Telu Bopo "
        u"Dsrt Xsux Visp Hmng Hano Bali Gujr Hang Thaa Sinh Hans Hant Talu "
        u"Mong Deva Sara Qabx Tagb Inds Xpeo Geok Tale Mymr Mand Perm Bugi "
        u"Phag Brai Brah Mlym Tibt Kali Batk Vaii Sylo Lina Teng Mero Limb "
        u"Kana Yiii Roro Java Taml Orya Laoo Ugar Cyrl Nkoo Armn Cyrs Latg "
        u"Latf Khmr Khar Egyh Latn Maya Ethi Goth Ital Arab Zxxx Buhd Copt "
        u"Thai Cprt Linb Lepc Osma Runr Glag Hira Syre Hani Orkh Hung Grek "
        u"Qaaa Egyd Cher Zyyy Cham Syrc Blis Cans Beng Egyp Syrj Tglg Syrn "
        u"Knda")
SCRS = tuple(SCRS.split(" "))


class LanguageScriptcodeAttribAdjuster(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"language-scriptcode-adjuster"
    name = u"Adjusting the value of scriptcode attribute in <language>"
    category = u"Cleansing"
    desc = (
        u"The 'scriptcode' attribute of <language> elements can only take "
        u"a definite set of values. This action erases the attributes that "
        u"don't have a legit value.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        for elt in xml_root.xpath(u'.//language[@scriptcode]'):
            value = elt.attrib.pop(u"scriptcode", u"").capitalize()
            if value in SCRS:
                elt.set(u"scriptcode", value)
            else:
                if log_details:
                    msg = u"    Deleted value: {0}".format(value)
                    log_data.append(log_element(elt, msg=msg))
                count += 1
        if count > 0:
            logger.warning(
                u"The 'scriptcode' attribute in the <language> element can "
                u"only have a value taken from a fixed vocabulary. {0:d} "
                u"elements have had their 'scriptcode' attribute deleted "
                u"because of a non-legit value.".format(count))
            if log_details:
                logger.warning(u"The following elements have been corrected:"
                               u"\n".join(log_data))
        # Return the cleaned EAD tree
        return xml_root


class ListAttribsAdjuster(TransformAction):
    applicable_for = (EAD_2002,)
    uid = u"list-attribs-adjuster"
    name = u"Adjusting the value of attributes in <list>"
    category = u"Cleansing"
    desc = (u"The 'numeration' and the 'type' attributes of <list> elements "
            u"can only have a few legit value. This action erases the "
            u"attributes whose value is not legit.")

    def _execute(self, xml_root, logger, log_details):
        count = 0
        if log_details:
            log_data = []
        for list_elt in xml_root.xpath(u'.//list[@numeration or @type]'):
            msg = u""
            if list_elt.get(u"numeration") not in [None, u"arabic"]:
                val = list_elt.pop(u"numeration")
                msg += u" numeration= \"{0}\"".format(val)
            if list_elt.get(u"type") not in [None, u"ordered", u"marked"]:
                val = list_elt.pop(u"type")
                msg += u" type= \"{0}\"".format(val)
            if msg != "":
                if log_details:
                    log_data.append(
                        log_element(list_elt,
                                    msg=(u"    Deleted attributes:"+msg)))
                count += 1
        if count > 0:
            logger.warning(
                u"The attributes of <list> elements can only have specific "
                u"values. {0:d} elements have had their attributes deleted "
                u"because of a non-legit value:".format(count)),
            if log_details:
                logger.warning(u"The following elements have been corrected:"
                               u"\n".join(log_data))
        return xml_root
