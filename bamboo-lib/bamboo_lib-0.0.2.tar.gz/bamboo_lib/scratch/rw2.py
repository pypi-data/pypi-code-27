from gen_rca import gen_rca

global design_factor
design_factor = 1.5


def population_measures():
    pop_template = '''
        <Measure name="Total Population{0}" column="pwgtp{0}" aggregator="sum" visible="{1}"/>
    \n'''
    calc_tmp = ""
    for i in range(0, 81):
        val = "" if i == 0 else i
        calc_tmp += pop_template.format(val, "true" if i == 0 else "false")
    return calc_tmp


def population_moe():
    deltas = []
    for i in range(1, 81):
        f = 'Power([Measures].[Total Population] - [Measures].[Total Population{i}], 2)'.format(i=i)
        deltas.append(f)

    summation = "+".join(deltas)
    final_form = "1.645 * Power(.05 * ({}), 0.5)".format(summation)
    return """
    <CalculatedMember name="Total Population MOE" dimension="Measures" visible="false">
        <Annotations>
            <Annotation name="aggregation_method">MOE</Annotation>
            <Annotation name="error_for_measure">Total Population</Annotation>
        </Annotations>
    <Formula>
      <![CDATA[
        {formula}
      ]]>
    </Formula>
    </CalculatedMember>
    <CalculatedMember dimension="Measures" name="Geography Population" visible="false"> <!-- all products, current geo, current year -->
      <Formula>
        <![CDATA[(Measures.[Total Population], [Year].[Year].CurrentMember,
                 [Gender].[Gender].[All Genders],
                 [Age].[Age].[All Ages],
                 [Race].[Race].[All Races],
                 [Nativity].[Nativity].[All Nativitys],
                 [Veteran Status].[Veteran Status].[All Veteran Statuss],
                 [Wage Bin].[Wage Bin].[All Wage Bins],
                 [Weeks Worked].[Weeks Worked].[All Weeks Workeds],
                 [Employment Status].[Employment Status].[All Employment Statuss],
                 [PUMS Degree].[PUMS Degree].[All PUMS Degrees],
                 [PUMS Degree Field].[PUMS Degree Field].[All PUMS Degree Fields],
                 [PUMS Occupation].[PUMS Occupation].[All PUMS Occupations],
                 [PUMS Industry].[PUMS Industry].[All PUMS Industrys],
                 [Geography].[Geography].CurrentMember)]]>
      </Formula>
    </CalculatedMember>
    <CalculatedMember name="Total Population MOE Appx" dimension="Measures">
        <Annotations>
            <Annotation name="aggregation_method">MOE</Annotation>
            <Annotation name="error_for_measure">Total Population</Annotation>
        </Annotations>
        <Formula>
          <![CDATA[
            1.645 * {design_factor} * Power(99 * [Measures].[Total Population] *
                (1 -
                ([Measures].[Total Population]
                    / [Measures].[Geography Population])), 0.5)
          ]]>
        </Formula>
    </CalculatedMember>

    """.format(formula=final_form, design_factor=design_factor)


def gen_meas(pretty_name, col_name):
    template1 = '''
    <Measure aggregator="None" dataType="Numeric" name="Weighted {0}" visible="false">
      <MeasureExpression>
          <SQL dialect="generic">SUM(pwgtp * {1})</SQL>
      </MeasureExpression>
    </Measure>
    <Measure aggregator="None" dataType="Numeric" name="Weighted {0} SQ" visible="false">
      <MeasureExpression>
          <SQL dialect="monetdb">SUM(pwgtp * {1} * {1})</SQL>
      </MeasureExpression>
    </Measure>
    '''
    tmp1 = template1.format(pretty_name, col_name)
    template2 = '''
    <Measure aggregator="None" dataType="Numeric" name="Weighted {2}{0}" visible="{1}">
      <MeasureExpression>
          <SQL dialect="generic">SUM(pwgtp{0} * {3})</SQL>
      </MeasureExpression>
    </Measure>
    '''
    mea_tmp = ""
    for i in range(1, 81):
        val = "" if i == 0 else i
        # mea_tmp += template2.format(val, "true" if i == 0 else "false", pretty_name, col_name)
        mea_tmp += template2.format(val, "false", pretty_name, col_name)

    return tmp1 + mea_tmp


def gen_calcs(pretty_name, col_name):
    template2 = '''
    <CalculatedMember name="Average {0}" dimension="Measures" visible="true">
      <Annotations>
        <Annotation name="aggregation_method">AVERAGE</Annotation>
      </Annotations>
      <Formula>[Measures].[Weighted {0}] / [Measures].[Total Population]</Formula>
    </CalculatedMember>
    <CalculatedMember name="Weighted {0} Squared" dimension="Measures" visible="false">
      <Formula>Power([Measures].[Weighted {0}], 2)</Formula>
    </CalculatedMember>
    <CalculatedMember name="SSquared EST {0}" dimension="Measures" visible="false">
          <Formula>
          ([Measures].[Weighted {0} SQ] - (Power([Measures].[Weighted {0}], 2) /
                                          [Measures].[Total Population])) /
            ([Measures].[Total Population] - 1)
          </Formula>
    </CalculatedMember>
    <CalculatedMember name="Average {0} Appx MOE" dimension="Measures">
      <Annotations>
        <Annotation name="aggregation_method">MOE</Annotation>
        <Annotation name="error_for_measure">Average {0}</Annotation>
      </Annotations>
      <Formula>
          1.645 * {2} * Power([Measures].[SSquared EST {0}] * (99 / [Measures].[Total Population]), 0.5)
      </Formula>
    </CalculatedMember>
    '''

    simple_part1 = template2.format(pretty_name, col_name, design_factor)

    template_rw = '''
    <CalculatedMember name="Average {2}{0}" dimension="Measures" visible="{1}">
        <Annotations>
            <Annotation name="aggregation_method">AVERAGE</Annotation>
        </Annotations>
      <Formula>[Measures].[Weighted {2}{0}] / [Measures].[Total Population{0}]</Formula>
    </CalculatedMember>\n
    '''

    calc_tmp = ""

    for i in range(1, 81):
        val = "" if i == 0 else i
        calc_tmp += template_rw.format(val, "true" if i == 0 else "false", pretty_name, col_name)

    deltas = []
    for i in range(1, 81):
        f = 'Power([Measures].[Average {pretty_name}] - [Measures].[Average {pretty_name}{i}], 2)'.format(i=i, pretty_name=pretty_name)
        deltas.append(f)
    summation = "+".join(deltas)
    final_form = "1.645 * Power(.05 * ({}), 0.5)".format(summation)
    wagp_moe = """
    <CalculatedMember name="Average {pretty_name} MOE" dimension="Measures" visible="false">
        <Annotations>
            <Annotation name="aggregation_method">MOE</Annotation>
            <Annotation name="error_for_measure">Average {pretty_name}</Annotation>
        </Annotations>
    <Formula>
      <![CDATA[
        {formula}
      ]]>
    </Formula>
    </CalculatedMember>
    """.format(formula=final_form, pretty_name=pretty_name)
    return simple_part1 + calc_tmp + wagp_moe


def gen_all():
    tmp = population_measures()
    metrics = [("Wage", "wagp")]
    metrics += [("Age", "agep")]
    metrics += [("Income", "pincp")]
    metrics += [("Usual Hours Worked Per Week", "wkhp")]

    for metric, col in metrics:
        tmp += gen_meas(metric, col)

    for metric, col in metrics:
        tmp += gen_calcs(metric, col)
    tmp += population_moe()

    tmp += gen_rca("ygopop", "PUMS Occupation", ["Year", "Geography"], ["Employment Status"])
    tmp += gen_rca("ygipop", "PUMS Industry", ["Year", "Geography"], ["Employment Status"])
    tmp += gen_rca("yocpop", "PUMS Degree Field", ["Year", "PUMS Occupation"], ["Employment Status"])
    tmp += gen_rca("yiopop", "PUMS Occupation", ["Year", "PUMS Industry"], ["Employment Status"])
    to_hide = ["ygopop RCA", "ygipop RCA", "yocpop RCA", "yiopop RCA"]
    return tmp, to_hide
