import re


def check_input(field_array):
    """
    Checks syntax of input(uppercase latin chars,numeric digits, underscores).
    Returns False for error or True for correct syntax.
    """
    alphanumeric_that_does_not_start_with_digit = r"^[A-Z_][0-9A-Z_]*$"

    for line in field_array:
        ret = re.match(alphanumeric_that_does_not_start_with_digit, line)

        if ret is None:
            # print("SYNTAX ERROR:WRONG SYMBOLS!")
            return False

    return True


def render_env_var_spec(env_var_name):
    env_var_name_lower = env_var_name.lower()

    ret_str = f'<label for="env_spec_{env_var_name_lower}"> {env_var_name}</label>'
    ret_str += "\n"
    ret_str += (
        f'<input id="env_spec_{env_var_name_lower}" name="{env_var_name_lower}" />'
    )

    return ret_str


def render_env_spec_to_html(field_array):
    if check_input(field_array):
        html_output = []

        for field in field_array:
            html_output.append(render_env_var_spec(field))  # create html output

        return "\n".join(html_output)
    return ""


def main():
    field_array = spec_str.split("\n")
    html_output = render_env_spec_to_html(field_array)

    return html_output


if __name__ == "__main__":
    spec_str = "DATABASE_URL\nADMIN_EMAIL\nDEBUG"
    print(main())
