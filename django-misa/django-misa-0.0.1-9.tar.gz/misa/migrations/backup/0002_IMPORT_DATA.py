# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from misa.utils.ontology_utils import check_and_create_ontology
from misa.utils.sample_batch_create import check_and_create_model

def save_model_list_migration(l,db_alias):
    [i.save(using=db_alias) for i in l]

def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    db_alias = schema_editor.connection.alias

    Organism = apps.get_model("misa", "Organism")
    OrganismPart = apps.get_model("misa", "OrganismPart")
    SampleType = apps.get_model("misa", "SampleType")
    MeasurementTechnique = apps.get_model("misa", "MeasurementTechnique")
    PolarityType = apps.get_model("misa", "PolarityType")
    ExtractionType = apps.get_model("misa", "ExtractionType")
    SpeType = apps.get_model("misa", "SpeType")
    ChromatographyType = apps.get_model("misa", "ChromatographyType")

    SampleCollectionProtocol = apps.get_model("misa", "SampleCollectionProtocol")
    ExtractionProtocol = apps.get_model("misa", "ExtractionProtocol")
    SpeProtocol = apps.get_model("misa", "SpeProtocol")
    ChromatographyProtocol = apps.get_model("misa", "ChromatographyProtocol")
    MeasurementProtocol = apps.get_model("misa", "MeasurementProtocol")

    OntologyTerm = apps.get_model("misa", "OntologyTerm")

    Investigation = apps.get_model("misa", "Investigation")
    Study = apps.get_model("misa", "Study")
    Assay = apps.get_model("misa", "Assay")

    # Polarity types
    p_input = ['POSITIVE', 'NEGATIVE', 'NA']
    polaritietypes = [PolarityType.objects.create(type=i) for i in p_input]

    #######################################################################################################
    # Setup ontologies
    #######################################################################################################
    # print('###ontologies')
    terms = ['NCIT_C49019', 'NCIT_C61575', 'SIO_001046', 'SIO_001047', 'CHEMINF_000070', 'CHMO_0002302',
             'CHMO_0002262', 'CHMO_0002269', 'CO_356:3000142', 'CHMO_0002658', 'CHMO_0002804', 'NCIT_C16631',
             'NCIT_C43366', 'NCIT_C14182', 'NCIT_C62195', 'NCIT_C25360', 'NCIT_C61299', 'NCIT_C25301', 'NCIT_C25207',
             'NCBITaxon_35128',  'NCIT_C13413', 'NCBITaxon_35525', 'NCBITaxon_6669', 'SIO_001047']


    [check_and_create_ontology(term, db_alias, False) for term in terms]


    #######################################################################################################
    # Setup ISA backbone
    #######################################################################################################
    # print('###ISA backbone')
    investigation = Investigation(name='Example Investigation', description='Example investigation for MOGI tutorial. '
                                                            'Use data derived from the MetaboLights study '
                                                            'MTBLS144. https://www.ebi.ac.uk/metabolights/MTBLS144')
    investigation.save(using=db_alias)

    study = Study(investigation=investigation, name='MTBLS144-TEST-CASE', dmastudy=False,
                  description='Phytoplankton are significant producers of '
                      'dissolved organic matter (DOM) in marine ecosystems but '
                      'the identity and dynamics of this DOM remain poorly constrained. '
                      'Knowledge on the identity and dynamics of DOM are crucial for understanding '
                      'the molecular-level reactions at the base of the global carbon cycle. '
                      'Here we apply emerging analytical and computational tools from metabolomics '
                      'to investigate the composition of DOM produced by the centric diatom '
                      'Thalassiosira pseudonana. We assessed both intracellular metabolites within T. pseudonana '
                      '(the endo-metabolome) and extracellular metabolites released by T. pseudonana '
                      '(the exo-metabolome). The intracellular metabolites had a more variable composition than '
                      'the extracellular metabolites. We putatively identified novel compounds not previously '
                      'associated with T. pseudonana as well as compounds that have previously been identified '
                      'within T. pseudonana’s metabolic capacity (e.g. dimethylsulfoniopropionate and degradation '
                      'products of chitin). The resulting information will provide the basis for '
                      'future experiments to assess the impact of T. pseudonana on the composition of '
                      'dissolved organic matter in marine environments.')
    study.save()

    assay_pos = Assay(name='Positive metabolic profiling (FT-ICR)', study=study)
    assay_pos.save(using=db_alias)
    assay_neg = Assay(name='Negative metabolic profiling (FT-ICR)', study=study)
    assay_neg.save(using=db_alias)

    #######################################################################################################
    # Protocols
    #######################################################################################################
    #============================================
    # Sample collection
    #============================================
    # print('###Sample collection protocol')
    sc_protocol = SampleCollectionProtocol(name="Diatom culturing",
                             description="The diatom Thalassiosira pseudonana (CCMP 1335) was cultured "
                                         "axenically in a modified version of L1 media with Turks Island Salts. "
                                         "The cultures were incubated under a 12 h:12 h light:dark cycle. Cells were "
                                         "collected 6 h into the light cycle on days 0, 1, 3, 7, 8, and 10.",
                             version=1,
                             code_field="DIATOM")
    sc_protocol.save(using=db_alias)
    #============================================
    # Liquid Phase extraction
    #============================================
    # print('###LPE')
    # Liquid Phase Extraction types
    lpe_type1 = ExtractionType(type="Apolar", description="Apolar (non-polar)")
    lpe_type1.save(using=db_alias)
    lpe_type1.ontologyterm.add(OntologyTerm.objects.filter(name='non-polar')[0])
    lpe_type1.ontologyterm.add(OntologyTerm.objects.filter(name='Extraction')[0])

    lpe_type2 = ExtractionType(type="Polar", description="Polar")
    lpe_type2.save(using=db_alias)
    lpe_type2.ontologyterm.add(OntologyTerm.objects.filter(name='polar')[0])
    lpe_type2.ontologyterm.add(OntologyTerm.objects.filter(name='Extraction')[0])

    # Liquid Phase Extraction protocol
    lpe_protocol = ExtractionProtocol(name="DOM-acetonitrile",
                                      description="""The intracellular metabolites were extracted using a previously described method [1]. Briefly, 1.5 ml samples were centrifuged at 16,000 x g at 4 ºC for 30 minutes and the supernatant discarded. The resulting cell pellet was extracted three times with ice-cold extraction solvent (acetonitrile:methanol:water with 0.1 M formic acid, 40:40:20). The combined extracts were neutralized with 0.1 M ammonium hydroxide, dried in a vacufuge, and then re-dissolved in 1 ml of 90:10 (v/v) water:acetonitrile for analysis on the mass spectrometer. 
                                                     Prior to sampling the extracellular metabolites, the cells were removed by gentle vacuum filtration through 0.2 µm Omnipore filters (hydrophilic PTFE membranes, Millipore). [2] have observed filtration may release intracellular metabolites into the exometabolome, and this potential bias must be considered in the discussion of our results. 
                                                    Ref:
                                                    [1] Rabinowitz JD, Kimball E. Acidic acetonitrile for cellular metabolome extraction from Escherichia coli. Anal Chem. 2007 Aug 15;79(16):6167-73. PMID: 17630720.
                                                    [2] Barofsky A, Vidoudez C, Pohnert G. Metabolic profiling reveals growth stage variability in diatom exudates. Limnology and Oceanography: Methods. June 2009, 7(6), 382–390.
                                                  """,
                                      version=1,
                                      code_field="DOM",
                                      extractiontype=lpe_type2,
                                      postextraction="90:10 (v/v) water:acetonitrile"
                                      )
    lpe_protocol.save(using=db_alias)

    #============================================
    # Sold phase extraction
    #============================================
    # print('###SPE')
    # SPE types
    spe_type1 = SpeType(type="PPL", description="Polymer type sorbents")
    spe_type1.save(using=db_alias)
    spe_type1.ontologyterm.add(OntologyTerm.objects.filter(name='SPE')[0])

    spe_type2 = SpeType(type="Weak anion-exchange", description="Weak anion-exchange solid phase extraction")
    spe_type2.save(using=db_alias)
    spe_type2.ontologyterm.add(OntologyTerm.objects.filter(name='SPE')[0])
    spe_type2.ontologyterm.add(OntologyTerm.objects.filter(name='weak anion-exchange column')[0])

    spe_protocol = SpeProtocol(name="SPE-DOM (PPL)",
                                      description="The acidified filtrate was extracted using solid phase extraction with PPL cartridges (Varian Bond Elut PPL cartridges) as previously described [3]. After eluting with methanol, the extracts were dried in a vacufuge, and then re-dissolved in 1 ml 90:10 water:acetonitrile prior to analysis. [1] Dittmar T, Koch B, Hertkorn N, Kattner G. A simple and efficient method for the solid-phase extraction of dissolved organic matter (SPE-DOM) from seawater. Limnology and Oceanography: Methods. June 2008, 6(6), 230–235",
                                      version=1,
                                      code_field="DOM",
                                      spetype=spe_type2
                                      )
    spe_protocol.save(using=db_alias)


    #============================================
    # Chromatography
    #============================================
    # print('###Chroma')
    # Chromatography types
    lc_type1 = ChromatographyType(type="Reversed phase chromatography", description="Reversed phase chromatography")
    lc_type1.save(using=db_alias)
    lc_type1.ontologyterm.add(OntologyTerm.objects.filter(name='reversed-phase chromatography')[0])

    lc_type2 = ChromatographyType(type="HILIC", description="Hydrophilic interaction chromatography")
    lc_type2.save(using=db_alias)
    lc_type2.ontologyterm.add(OntologyTerm.objects.filter(name='hydrophilic interaction chromatography')[0])

    lc_protocol = ChromatographyProtocol(name="Synergi Fusion RP",
                                      description="LC separation was performed on a Synergi Fusion reversed-phase column using a binary gradient with solvent A being water with 0.1% formic acid and solvent B being acetonitrile with 0.1% formic acid. Samples were eluted at 250 µl/min with the following gradient: hold at 5% B for 0-2 min, ramp from 5 to 65% B between 2 and 20 min, ramp from 65 to 100% B between 20 and 25 min, hold at 100% B from 25-32 min, and then ramp back to 5% B between 32 and 32.5 min for re-equilibration (32.5-40 min).",
                                      version=1,
                                      code_field="SFRP",
                                      chromatographytype=lc_type1
                                      )
    lc_protocol.save(using=db_alias)


    #============================================
    # Measurements
    #============================================
    # print('###Meas')
    # Measurement types
    m_type1 = MeasurementTechnique(type="FT-ICR", description="Fourier Tranform Ion Cyclon Resonance Mass Spectrometry")
    m_type1.save()
    m_type1.ontologyterm.add(OntologyTerm.objects.filter(name='linear quadrupole ion trap Fourier transform ion cyclotron resonance mass spectrometer')[0])

    m_protocol = MeasurementProtocol(name="FT-ICR",
                                     description="All metabolomics analyses were conducted using liquid chromatography (LC) coupled by electrospray ionization to a hybrid linear ion trap - Fourier-transform ion cyclotron resonance (FT-ICR) mass spectrometer (7T LTQ FT Ultra, Thermo Scientific) Both full MS and MS/MS data were collected. The MS scan was performed in the FT-ICR cell from m/z 100-1000 at 100,000 resolving power (defined at 400 m/z). In parallel to the FT acquisition, MS/MS scans were collected at nominal mass resolution in the ion trap from the two features with the highest peak intensities in each scan. Separate autosampler injections were made for analysis in positive and negative ion modes.",
                                     version=1,
                                     code_field="FT-ICR",
                                     measurementtechnique=m_type1
                                     )
    m_protocol.save(using=db_alias)

    #######################################################################################################
    # Organisms
    #######################################################################################################
    # print('###Orgs')
    check_and_create_model('Thalassiosira pseudonana', Organism, db_alias)
    check_and_create_model('Daphnia magna', Organism, db_alias)
    check_and_create_model('Daphnia pulex', Organism, db_alias)
    check_and_create_model('Homo sapiens', Organism, db_alias)
    check_and_create_model('Mus musculus', Organism, db_alias)

    check_and_create_model('Whole Organism', OrganismPart, db_alias)
    check_and_create_model('exometabolome', OrganismPart, db_alias)
    check_and_create_model('endometabolome', OrganismPart, db_alias)

    #######################################################################################################
    # Sample types
    #######################################################################################################
    # print('###Sample Types')
    st1 = SampleType(type='ANIMAL', ontologyterm=OntologyTerm.objects.filter(name='Animal')[0])
    st2 = SampleType(type='COMPOUND', ontologyterm=OntologyTerm.objects.filter(name='Compound')[0])
    st3 = SampleType(type='BLANK', ontologyterm=OntologyTerm.objects.filter(name='blank value')[0])

    st1.save()
    st2.save()
    st3.save()


def reverse_func(apps, schema_editor):
    ##########################
    # Reverse func not currently implemented
    ############################

    # forwards_func() creates two instances
    # so reverse_func() should delete them.
    SampleType = apps.get_model("misa", "SampleType")
    MeasurementTechnique = apps.get_model("misa", "MeasurementTechnique")
    PolarityType = apps.get_model("misa", "PolarityType")
    ExtractionType = apps.get_model("misa", "ExtractionType")
    SpeType = apps.get_model("misa", "SpeType")
    ChromatographyType = apps.get_model("misa", "ChromatographyType")


class Migration(migrations.Migration):
    dependencies = [
        ('misa', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]

