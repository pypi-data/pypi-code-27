#!/usr/bin/env python
# cardinal_pythonlib/psychiatry/drugs.py

"""
===============================================================================

    Copyright (C) 2009-2018 Rudolf Cardinal (rudolf@pobox.com).

    This file is part of cardinal_pythonlib.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

===============================================================================

Translating specific to generic names.

Test within Python:

.. code-block:: python

    from cardinal_pythonlib.drugnames import drug_name_to_generic

    drug_name_to_generic("UNKNOWN")
    drug_name_to_generic("UNKNOWN", unknown_to_default=True)
    drug_names_to_generic([
        "citalopram", "Citalopram", "Cipramil", "Celexa",
        "olanzepine",  # typo
        "dextroamphetamine",
        "amitryptyline",
    ])

Test within R:

.. code-block:: r

    # -------------------------------------------------------------------------
    # Load libraries
    # -------------------------------------------------------------------------

    library(data.table)
    library(reticulate)

    # -------------------------------------------------------------------------
    # Struggle with reticulate bugs to import a module
    # -------------------------------------------------------------------------

    VENV <- "~/dev/venvs/cardinal_pythonlib"
    PYTHON_VERSION <- "python3.5"

    reticulate::use_virtualenv(VENV, required=TRUE)
    # ... it is CRITICAL to use required=TRUE, or it might fail silently

    # WORKS:
    cardinal_pythonlib <- reticulate::import("cardinal_pythonlib")  # works
    drugnames <- reticulate::import("cardinal_pythonlib.drugnames")  # FAILS
    fileops <- reticulate::import("cardinal_pythonlib.fileops")  # FAILS
    # ... despite "import cardinal_pythonlib.fileops" working fine in Python

    # So, nasty hack:
    fileops <- reticulate::import_from_path(
        "fileops",
        file.path(VENV, "lib", PYTHON_VERSION,
                  "site-packages/cardinal_pythonlib")
    )

    # And the module we care about now:
    drugs <- reticulate::import_from_path(
        "drugs",
        file.path(VENV, "lib", PYTHON_VERSION,
                  "site-packages/cardinal_pythonlib/psychiatry")
    )
    # or under Windows, drop the PYTHON_VERSION part

    # Or, for development:
    drugs <- reticulate::import_from_path(
        "drugs",
        "~/Documents/code/cardinal_pythonlib/cardinal_pythonlib/psychiatry"
    )

    # -------------------------------------------------------------------------
    # Do something useful
    # -------------------------------------------------------------------------

    testnames <- c("citalopram", "Cipramil", "Prozac", "fluoxetine")
    # Works for simple variables:
    drugs$drug_names_to_generic(testnames)

    # Also works for data table replacements:
    dt <- data.table(
        subject = c("Alice", "Bob", "Charles", "Dawn"),
        drug = c("citalopram", "Cipramil", "Prozac", "fluoxetine")
    )
    dt[, drug_generic := drugs$drug_names_to_generic(drug)]
    dt[, is_antidepressant := drugs$drug_names_match_criteria(
            drug_generic, names_are_generic=TRUE,
            antidepressant=TRUE)]
    dt[, is_antidepressant_not_ssri := drugs$drug_names_match_criteria(
            drug_generic, names_are_generic=TRUE,
            antidepressant=TRUE, ssri=FALSE)]

"""

import re
from typing import Dict, List, Optional, Union


# =============================================================================
# Class to capture drug information
# =============================================================================

class Drug(object):
    def __init__(
            self,
            # Names
            generic: Union[str, List[str]],
            alternatives: List[str] = None,
            # Psychiatry
            antidepressant: bool = False,
            conventional_antidepressant: bool = False,
            ssri: bool = False,
            non_ssri_modern_antidepressant: bool = False,
            tricyclic_antidepressant: bool = False,
            tetracyclic_and_related_antidepressant: bool = False,
            monoamine_oxidase_inhibitor: bool = False,
            antipsychotic: bool = False,
            first_generation_antipsychotic: bool = False,
            second_generation_antipsychotic: bool = False,
            stimulant: bool = False,
            anticholinergic: bool = False,
            benzodiazepine: bool = False,
            z_drug: bool = False,
            non_benzodiazepine_anxiolytic: bool = False,
            mood_stabilizer: bool = False,
            # Endocrinology
            antidiabetic: bool = False,
            sulfonylurea: bool = False,
            biguanide: bool = False,
            glifozin: bool = False,
            glp1_agonist: bool = False,
            dpp4_inhibitor: bool = False,
            meglitinide: bool = False,
            thiazolidinedione: bool = False,
            # Cardiovascular
            cardiovascular: bool = False,
            beta_blocker: bool = False,
            ace_inhibitor: bool = False,
            statin: bool = False,
            # Respiratory
            respiratory: bool = False,
            beta_agonist: bool = False,
            # Gastrointestinal
            gastrointestinal: bool = False,
            proton_pump_inhibitor: bool = False,
            nonsteroidal_anti_inflammatory: bool = False,
            # Nutritional
            vitamin: bool = False) -> None:
        """
        Initialize and determine/store category knowledge.

        "alternatives" can include regexes (as text).
        """
        # Name handling
        if isinstance(generic, list):
            self.mixture = True
            self.all_generics = [x.lower().strip() for x in generic]
            self.generic_name = "_with_".join(self.all_generics)
        elif isinstance(generic, str):
            self.mixture = False
            self.generic_name = generic.lower().strip()
            self.all_generics = [self.generic_name]
        else:
            raise ValueError("Bad generic_name: {!r}".format(generic))
        self.alternatives = alternatives or []  # type: List[str]
        possibilities = list(set(self.all_generics + self.alternatives))
        regex_text = "|".join("(?:" + x + ")" for x in possibilities)
        self.regex = re.compile(regex_text, re.IGNORECASE | re.VERBOSE)

        # Things we know about drugs

        if (ssri or non_ssri_modern_antidepressant or
                tricyclic_antidepressant or
                tetracyclic_and_related_antidepressant or
                monoamine_oxidase_inhibitor):
            conventional_antidepressant = True

        if conventional_antidepressant:
            antidepressant = True

        if first_generation_antipsychotic or second_generation_antipsychotic:
            antipsychotic = True

        if (sulfonylurea or biguanide or glifozin or glp1_agonist or
                dpp4_inhibitor or meglitinide or thiazolidinedione):
            antidiabetic = True

        if beta_blocker or ace_inhibitor:
            cardiovascular = True

        # Store category knowledge

        self.antidepressant = antidepressant
        self.conventional_antidepressant = conventional_antidepressant
        self.ssri = ssri
        self.non_ssri_modern_antidepressant = non_ssri_modern_antidepressant
        self.tricyclic = tricyclic_antidepressant
        self.tetracyclic_and_related_antidepressant = tetracyclic_and_related_antidepressant  # noqa
        self.monoamine_oxidase_inhibitor = monoamine_oxidase_inhibitor

        self.antipsychotic = antipsychotic
        self.first_generation_antipsychotic = first_generation_antipsychotic
        self.second_generation_antipsychotic = second_generation_antipsychotic

        self.stimulant = stimulant

        self.anticholinergic = anticholinergic

        self.benzodiazepine = benzodiazepine
        self.z_drug = z_drug
        self.non_benzodiazepine_anxiolytic = non_benzodiazepine_anxiolytic

        self.mood_stabilizer = mood_stabilizer

        self.antidiabetic = antidiabetic
        self.sulfonylurea = sulfonylurea
        self.biguanide = biguanide
        self.cardiovascular = cardiovascular
        self.beta_blocker = beta_blocker
        self.ace_inhibitor = ace_inhibitor
        self.statin = statin
        self.respiratory = respiratory
        self.beta_agonist = beta_agonist
        self.gastrointestinal = gastrointestinal
        self.proton_pump_inhibitor = proton_pump_inhibitor
        self.nonsteroidal_anti_inflammatory = nonsteroidal_anti_inflammatory
        self.vitamin = vitamin

    def name_matches(self, name: str) -> bool:
        """
        The parameter should be pre-stripped of edge whitespace.
        """
        return bool(self.regex.match(name))


# Source data.
DRUGS = [
    # In comments below: (*) misspelling, capitalized for brand name, (~)
    # hybrid generic/brand name, (+) old name.

    # -------------------------------------------------------------------------
    # SSRIs
    # -------------------------------------------------------------------------
    Drug("citalopram", ["Cipramil", "Celexa"], ssri=True),
    Drug("escitalopram", ["Cipralex", "Lexapro"], ssri=True),
    Drug(
        "fluoxetine",
        [
            "Prozac", "Bellzac", "Oxactin", "Prozep",
            "fluox.*",  # CPFT 2013: "fluoxetine  Dec"
        ],
        ssri=True
    ),
    Drug(
        "fluvoxamine",
        [
            "Luvox", "Faverin",
            "fluvoxamine.*",  # e.g. "fluvoxamine maleate"
        ],
        ssri=True
    ),
    Drug(
        "paroxetine",
        ["Seroxat", "Paxil"],  # there are other brands elsewhere...
        ssri=True
    ),
    Drug(
        "sertraline",
        ["Lustral", "Zoloft", "Bellsert"],
        # NOT Seretra (cf. SLAM code, see email to self 2016-12-02); Seretra =
        # seratrodast = for asthma
        ssri=True
    ),

    # -------------------------------------------------------------------------
    # FIRST-GENERATION ANTIPSYCHOTICS
    # -------------------------------------------------------------------------
    Drug("benperidol", ["Anquil"], first_generation_antipsychotic=True),
    Drug("chlorpromazine", ["Largactil"], first_generation_antipsychotic=True),
    Drug(
        "flupentixol",
        [
            "Depixol", "Fluanxol",
            "flupent.*", "Depixol.*",
            # e.g. flupenthixol, flupenthixol decanoate, flupentixol decanoate
        ],
        first_generation_antipsychotic=True
    ),
    Drug(
        "fluphenazine",
        [
            "Modecate",
            "fluphen.*", "Modecate.*",
        ],
        first_generation_antipsychotic=True
    ),
    Drug(
        "haloperidol",
        [
            "Haldol", "Serenase",
            "halop.*", "Dozi.*", "Hald.*", "Serena.*",
            # NB Serenase, Serenace.
            #  CPFT 2013: haloperidol, haloperidol decanoate, Haldol, Haldol
            #  decanoate, Serenase.
        ],
        first_generation_antipsychotic=True
    ),
    Drug("levomepromazine", ["Nozinan"], first_generation_antipsychotic=True),
    Drug("pericyazine", first_generation_antipsychotic=True),
    Drug("perphenazine", ["Fentazin"], first_generation_antipsychotic=True),
    Drug(
        ["amitriptyline", "perphenazine"],
        ["Triptafen"],  # special
        first_generation_antipsychotic=True,
        tricyclic_antidepressant=True,
    ),
    Drug("pimozide", ["Orap"], first_generation_antipsychotic=True),
    Drug(
        "pipotiazine",
        [
            "pipot.*", "Piport.*",
            # ... actually (CPFT 2013): pipotiazine, Piportil
        ],
        first_generation_antipsychotic=True
    ),
    Drug("prochlorperazine", ["Stemetil"],
         first_generation_antipsychotic=True),
    Drug("promazine", first_generation_antipsychotic=True),
    Drug("sulpiride", ["Dolmatil", "Sulpor"],
         first_generation_antipsychotic=True),
    Drug("trifluoperazine", ["Stelazine"],
         first_generation_antipsychotic=True),
    Drug(
        "zuclopenthixol",
        [
            "zuclop.*", "Clopix.*", "Acc?uphase",
            # ... actually (CPFT 2013): zuclopenthixol, zuclopenthixol acetate,
            # zuclopenthixol decanoate, Clopixol, Clopixol Decanoate, Acuphase
        ],
        first_generation_antipsychotic=True
    ),

    # -------------------------------------------------------------------------
    # SECOND-GENERATION ANTIPSYCHOTICS
    # -------------------------------------------------------------------------
    Drug(
        "amisulpride",
        [
            "amisulp.*", "Solian",
            # ... actually (CPFT 2013): amisulpiride(*), amisulpride, Solian
        ],
        second_generation_antipsychotic=True
    ),
    Drug("aripiprazole", ["Abilify"], second_generation_antipsychotic=True),
    Drug("asenapine", ["Saphris", "Sycrest"],
         second_generation_antipsychotic=True),
    Drug(
        "clozapine",
        ["cloz.*", "Denz.*", "Zapon.*"],
        # ... actually (CPFT 2013): clozapine, Clozaril, clozepine(*)
        second_generation_antipsychotic=True
    ),
    Drug("iloperidone", ["Fanapt", "Fanapta", "Zomaril"],
         second_generation_antipsychotic=True),
    Drug("lurasidone", ["Latuda"], second_generation_antipsychotic=True),
    Drug(
        "olanzapine",
        [
            "olanz.*", "Zalast.*", "Zyprex.*", "Zypad.*"
            # ... actually (CPFT 2013): olanzapine, olanzapine embonate,
            # olanz(*), olanzepine(*), olanzapin(*), Zyprexa
        ],
        second_generation_antipsychotic=True
    ),
    Drug("paliperidone", ["Invega", "Xeplion"],
         second_generation_antipsychotic=True),
    Drug(
        "quetiapine",
        ["quet.*", "Seroquel"],
        # ... actually (CPFT 2013): quetiapine, quetiepine(*), Seroquel
        second_generation_antipsychotic=True
    ),
    Drug(
        "risperidone",
        ["risp.*"],
        # ... actually (CPFT 2013): risperidone, risperadone(*), Risperidone
        # Consta (~), Risperdal, Risperdal Consta
        second_generation_antipsychotic=True
    ),
    Drug("sertindole", ["Serdolect", "Serlect"],
         second_generation_antipsychotic=True),
    Drug("ziprasidone", second_generation_antipsychotic=True),
    Drug(
        "zotepine",  # not in UK
        ["Nipolept", "Losizopilon", "Lodopin", "Setous"],
        second_generation_antipsychotic=True
    ),

    # -------------------------------------------------------------------------
    # STIMULANTS
    # -------------------------------------------------------------------------
    Drug(
        "amfetamine",
        [".*am[ph|f]etamine.*", "Adderall"],
        # ... actually (CPFT 2013): dextroamphetamine(+), dexamfetamine
        stimulant=True
    ),
    Drug(
        "methylphenidate",
        ["Ritalin", "Concerta.*", "Equasym.*", "Medikinet.*"],
        # ... actually (CPFT 2013): methylphenidate, Ritalin, Concerta
        stimulant=True
    ),
    Drug("modafinil", ["Provigil"], stimulant=True),

    # -------------------------------------------------------------------------
    # ANTICHOLINERGICS
    # -------------------------------------------------------------------------
    Drug("benztropine", ["benzatropine"], anticholinergic=True),
    Drug("orphenadrine", ["Biorphen", "Disipal"], anticholinergic=True),
    Drug("procyclidine", ["Arpicolin", "Kemadrin"], anticholinergic=True),
    Drug("trihexyphenidyl", ["Broflex"], anticholinergic=True),

    # -------------------------------------------------------------------------
    # OTHER MODERN ANTIDEPRESSANTS
    # -------------------------------------------------------------------------
    Drug("agomelatine", ["Valdoxan"], non_ssri_modern_antidepressant=True),
    Drug(
        "bupropion", ["Zyban"], non_ssri_modern_antidepressant=True
        # antidepressant license in US, smoking cessation in UK
    ),
    Drug("duloxetine", ["Cymbalta", "Yentreve"],
         non_ssri_modern_antidepressant=True),
    Drug(
        "mirtazapine",
        ["mirtaz.*", "mirtazepine", "Zispin", "Mirza"],
        # ... actually (CPFT 2013): mirtazapine, mirtazepine(*), "mirtazapine
        # Dec" (?)
        non_ssri_modern_antidepressant=True
    ),
    Drug("reboxetine", ["Edronax"], non_ssri_modern_antidepressant=True),
    Drug("tryptophan", ["Optimax"], non_ssri_modern_antidepressant=True),
    Drug(
        "venlafaxine",
        ["venla.*", "Eff?exor.*"],
        # ... actually (CPFT 2013): venlafaxine, venlafaxine XL,
        non_ssri_modern_antidepressant=True  # though obviously an SSRI too...
    ),

    # -------------------------------------------------------------------------
    # TRICYCLIC AND RELATED ANTIDEPRESSANTS
    # -------------------------------------------------------------------------
    Drug(
        "amitriptyline",
        ["amitr[i|y]pt[i|y]l[i|y]n.*", "Vanatrip", "Elavil", "Endep"],
        tricyclic_antidepressant=True
        # ... actually (CPFT 2013): amitriptyline, amitriptiline(*),
        # amitryptyline(*)
        # Triptafen = amitriptyline + perphenazine; see above.
    ),
    Drug("clomipramine", ["Anafranil.*"], tricyclic_antidepressant=True),
    Drug(
        "dosulepin", ["dothiepin", "Prothiaden"],
        tricyclic_antidepressant=True
        # ... actually (CPFT 2013): dosulepin, dothiepin(+)
    ),
    Drug(
        "doxepin",
        ["Sinepin", "Sinequan", "Sinepin", "Xepin"],
        # Xepin is cream only
        tricyclic_antidepressant=True
    ),
    Drug("imipramine", ["Tofranil"], tricyclic_antidepressant=True),
    Drug("lofepramine", ["Lomont"], tricyclic_antidepressant=True),
    Drug(
        "nortriptyline",
        ["nortr.*", "Allegron", "Pamelor", "Aventyl"],
        # ... actually (CPFT 2013): nortriptyline, nortryptiline(*)
        tricyclic_antidepressant=True
    ),
    Drug("trimipramine", ["Surmontil"], tricyclic_antidepressant=True),

    # -------------------------------------------------------------------------
    # TETRACYCLIC-RELATED ANTIDEPRESSANTS
    # -------------------------------------------------------------------------
    Drug("mianserin", tetracyclic_and_related_antidepressant=True),
    Drug("trazodone", ["Molipaxin"],
         tetracyclic_and_related_antidepressant=True),
    Drug(
        "nefazodone",
        # discontinued for hepatotoxicity? But apparently still used in 2014
        # in the UK: http://www.bbc.co.uk/news/uk-25745824
        ["Dutonin", "Nefadar", "Serzone"],
        tetracyclic_and_related_antidepressant=True
        # brand names from https://en.wikipedia.org/wiki/Nefazodone
        # ... yup, still a trickle, mostly from Islington:
        # https://openprescribing.net/chemical/0403040T0/
    ),

    # -------------------------------------------------------------------------
    # MAOIs
    # -------------------------------------------------------------------------
    Drug(
        "phenelzine", ["Nardil"], monoamine_oxidase_inhibitor=True
        # SLAM code (see e-mail to self 2016-12-02) also has %Alazin%; not sure
        # that's right; see also
        # http://www.druglib.com/activeingredient/phenelzine/
    ),
    # not included: pheniprazine
    Drug("isocarboxazid", monoamine_oxidase_inhibitor=True),
    Drug("moclobemide", monoamine_oxidase_inhibitor=True),
    Drug("tranylcypromine", ["Parnate"], monoamine_oxidase_inhibitor=True),

    # -------------------------------------------------------------------------
    # BENZODIAZEPINES
    # -------------------------------------------------------------------------
    Drug("alprazolam", benzodiazepine=True),
    Drug("chlordiazepoxide", benzodiazepine=True),
    Drug("clobazam", benzodiazepine=True),
    Drug("clonazepam", ["Rivotril"], benzodiazepine=True),
    Drug(
        "diazepam", ["diaz.*", "Valium"], benzodiazepine=True
        # ... actually (CPFT 2013): diazepam, diazapam(*), diazapem(*), Valium
    ),
    Drug("flurazepam", ["Dalmane"], benzodiazepine=True),
    Drug("loprazolam", benzodiazepine=True),
    Drug("lorazepam", ["Ativan"], benzodiazepine=True),
    Drug("lormetazepam", benzodiazepine=True),
    Drug("midazolam", ["Hypnovel"], benzodiazepine=True),
    Drug("nitrazepam", benzodiazepine=True),
    Drug("oxazepam", benzodiazepine=True),
    Drug("temazepam", benzodiazepine=True),

    # -------------------------------------------------------------------------
    # Z-DRUGS
    # -------------------------------------------------------------------------
    Drug("zaleplon", ["Sonata"], z_drug=True),
    Drug(
        "zolpidem", ["zolpidem.*", "Stilnoct"], z_drug=True
        # ... actually (CPFT 2013): zolpidem, zolpidem tartrate
    ),
    Drug("zopiclone", ["Zimovane"], z_drug=True),

    # -------------------------------------------------------------------------
    # OTHER ANXIOLYTICS
    # -------------------------------------------------------------------------
    Drug("buspirone", ["Buspar"], non_benzodiazepine_anxiolytic=True),

    # -------------------------------------------------------------------------
    # OTHER ANTIMANIC
    # -------------------------------------------------------------------------
    Drug(
        "carbamazepine",
        ["Carbagen.*", "Tegretol.*"],
        # also Tegretol Prolonged Release (formerly Tegretol Retard)
        # ... actually (CPFT 2013): carbamazepine, Tegretol
        mood_stabilizer=True
    ),
    Drug(
        "valproate",
        [".*valp.*", "Epilim.*", "Episenta", "Epival", "Convulex", "Depakote"],
        # ... also semisodium valproate
        # ... actually (CPFT 2013): sodium valproate [chrono], valproic acid,
        # valproate, sodium valproate, sodium valporate(*), sodium valporate(*)
        # chrono, Depakote
        mood_stabilizer=True
    ),
    Drug(
        "lithium",
        ["lithium.*", "Camcolit", "Liskonum", "Priadel", "Li-Liquid"],
        # ... actually (CPFT 2013): lithium, lithium carbonate, lithium citrate
        # (curious: Priadel must be being changed to lithium...)
        antidepressant=True,
        mood_stabilizer=True
    ),

    # -------------------------------------------------------------------------
    # Other for bipolar/unipolar depression
    # -------------------------------------------------------------------------
    Drug(
        "lamotrigine",
        ["lamotrigine.*", "Lamictal"],
        mood_stabilizer=True, antidepressant=True,
    ),
    Drug(
        "triiodothyronine",
        ["tri-iodothyronine", "liothyronine", "Cytomel"],
        antidepressant=True,
    ),

    # -------------------------------------------------------------------------
    # GENERAL MEDICINE: DIABETES
    # -------------------------------------------------------------------------
    Drug("glibenclamide", sulfonylurea=True),
    Drug(
        "gliclazide",
        ["Zicron", "Diamicron.*", "Dacadis.*", "Vitile.*"],
        sulfonylurea=True
    ),
    Drug("glimepiride", ["Amaryl"], sulfonylurea=True),
    Drug("glipizide", ["Minodiab"], sulfonylurea=True),
    Drug("tolbutamide", sulfonylurea=True),
    Drug("metformin", ["metformin.*", "Glucophage.*"], biguanide=True),
    Drug("acarbose", ["Glucobay"], antidiabetic=True),
    Drug("dapagliflozin", ["Forxiga"], glifozin=True),
    Drug("exenatide", ["Byetta", "Bydureon"], glp1_agonist=True),
    Drug("linagliptin", ["Trajenta"], dpp4_inhibitor=True),
    Drug(["linagliptin", "metformin"], ["Jentadueto"],
         biguanide=True, dpp4_inhibitor=True),
    Drug("liraglutide", ["Victoza"], glp1_agonist=True),
    Drug("lixisenatide", ["Lyxumia"], glp1_agonist=True),
    Drug("nateglinide", ["Starlix"], meglitinide=True),
    Drug("pioglitazone", ["Actos"], thiazolidinedione=True),
    Drug(["pioglitazone", "metformin"], ["Competact"],
         thiazolidinedione=True, biguanide=True),
    Drug("repaglinide", ["Prandin"], meglitinide=True),
    Drug("saxagliptin", ["Onglyza"], dpp4_inhibitor=True),
    Drug(["saxagliptin", "metformin"], ["Komboglyze"],
         dpp4_inhibitor=True, biguanide=True),
    Drug("sitagliptin", ["Januvia"], dpp4_inhibitor=True),
    Drug(["sitagliptin", "metformin"], ["Janumet"],
         dpp4_inhibitor=True, biguanide=True),
    Drug("vildagliptin", ["Galvus"], dpp4_inhibitor=True),
    Drug(["vildagliptin", "metformin"], ["Eucreas"], 
         dpp4_inhibitor=True, biguanide=True),
    Drug(
        "insulin",
        # Insulin. Covering the BNF categories:
        # INSULIN
        # INSULIN ASPART
        # INSULIN GLULISINE
        # INSULIN LISPRO
        # INSULIN DEGLUDEC
        # INSULIN DETEMIR
        # INSULIN GLARGINE
        # INSULIN ZINC SUSPENSION
        # ISOPHANE INSULIN
        # PROTAMINE ZINC INSULIN
        # BIPHASIC INSULIN ASPART
        # BIPHASIC INSULIN LISPRO
        # BIPHASIC ISOPHANE INSULIN
        [
            ".*insulin.*", ".*aspart.*", ".*glulisine.*", ".*lispro.*",
            ".*degludec.*", ".*detemir.*", ".*glargine.*", ".*Hypurin.*",
            ".*Actrapid.*", ".*Humulin.*", ".*Insuman.*", ".*Novorapid.*",
            ".*Apidra.*", ".*Humalog.*", ".*Tresiba.*", ".*Levemir.*",
            ".*Lantus.*", ".*Insulatard.*", ".*NovoMix.*",
        ], 
        antidiabetic=True
    ),

    # -------------------------------------------------------------------------
    # GENERAL MEDICINE: CARDIOVASCULAR
    # -------------------------------------------------------------------------
    Drug("aspirin", cardiovascular=True),
    Drug("atenolol", beta_blocker=True),
    # ACE inhibitors (selected)
    Drug("lisinopril", ace_inhibitor=True),
    Drug("ramipril", ace_inhibitor=True),
    # Statins
    Drug("atorvastatin", ["Lipitor"], statin=True),
    Drug("fluvastatin", ["Lescol.*"], statin=True),
    Drug("pravastatin", ["Lipostat"], statin=True),
    Drug("rosuvastatin", ["Crestor"], statin=True),
    Drug("simvastatin", ["Zocor"], statin=True),
    Drug(["simvastatin", "ezetimibe"], ["Inegy"], statin=True),

    # -------------------------------------------------------------------------
    # GENERAL MEDICINE: RESPIRATORY
    # -------------------------------------------------------------------------
    Drug(
        "salbutamol",
        ["salbut.*", "vent.*"],
        # ... actually (CPFT 2013): salbutamol
        respiratory=True, beta_agonist=True
    ),

    # -------------------------------------------------------------------------
    # GENERAL MEDICINE: GASTROINTESTINAL
    # -------------------------------------------------------------------------
    Drug(
        "lactulose",
        ["lactul.*", "Duphal.*", "Lactug.*", "laevol.*"],
        # ... actually (CPFT 2013): lactulose
        gastrointestinal=True
    ),
    Drug("lansoprazole", proton_pump_inhibitor=True),
    Drug("omeprazole", proton_pump_inhibitor=True),
    Drug("senna", gastrointestinal=True),

    # -------------------------------------------------------------------------
    # GENERAL MEDICINE: OTHER
    # -------------------------------------------------------------------------
    Drug("ibuprofen", nonsteroidal_anti_inflammatory=True),
    Drug("levothyroxine"),
    Drug("paracetamol"),
    Drug("thiamine", vitamin=True),

]  # type: List[Drug]


# =============================================================================
# High-speed lookup versions of the original constants
# =============================================================================

DRUGS_BY_GENERIC_NAME = {d.generic_name: d for d in DRUGS}


# =============================================================================
# Get drug object by name
# =============================================================================

def get_drug(drug_name: str, name_is_generic: bool = False) -> Optional[Drug]:
    """
    Converts a drug name to a Drug class.
    If you already have the generic name, you can get the Drug more
    efficiently.
    """
    drug_name = drug_name.strip().lower()
    if name_is_generic:
        return DRUGS_BY_GENERIC_NAME.get(drug_name)
    for d in DRUGS:
        if d.name_matches(drug_name):
            return d
    return None


# =============================================================================
# Convert drug names to generic equivalents
# =============================================================================

def drug_name_to_generic(drug_name: str, unknown_to_default: bool = False,
                         default: str = None) -> str:
    """
    Converts a drug name to a generic equivalent.
    """
    drug = get_drug(drug_name)
    if drug is not None:
        return drug.generic_name
    return default if unknown_to_default else drug_name


def drug_names_to_generic(drugs: List[str], unknown_to_default: bool = False,
                          default: str = None) -> List[str]:
    """
    Converts a list of drug names to their generics equivalents.
    """
    return [
        drug_name_to_generic(drug, unknown_to_default=unknown_to_default,
                             default=default)
        for drug in drugs
    ]


# =============================================================================
# Check drugs against criteria
# =============================================================================

def drug_matches_criteria(drug: Drug, **criteria: Dict[str, bool]) -> bool:
    for attribute, value in criteria.items():
        if getattr(drug, attribute) != value:
            return False
    return True


def all_drugs_where(sort=True, **criteria: Dict[str, bool]) -> List[Drug]:
    """
    Pass keyword arguments such as

    .. code-block:: python

        from cardinal_pythonlib.psychiatry.drugs import *
        mydrugs = all_drugs_where(antidepressant=True, ssri=False)
        print([d.generic_name for d in mydrugs])
    """
    matching_drugs = []  # type: List[Drug]
    for drug in DRUGS:
        if drug_matches_criteria(drug, **criteria):
            matching_drugs.append(drug)
    if sort:
        matching_drugs.sort(key=lambda d: d.generic_name)
    return matching_drugs


def drug_name_matches_criteria(drug_name: str, name_is_generic: bool = False,
                               **criteria: Dict[str, bool]) -> bool:
    drug = get_drug(drug_name, name_is_generic)
    if drug is None:
        return False
    return drug_matches_criteria(drug, **criteria)


def drug_names_match_criteria(drug_names: List[str],
                              names_are_generic: bool = False,
                              **criteria: Dict[str, bool]) -> List[bool]:
    return [drug_name_matches_criteria(dn, names_are_generic, **criteria)
            for dn in drug_names]
