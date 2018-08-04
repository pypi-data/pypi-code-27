from {{ project_name }} import main


def test_main():
    assert main.hello_world()
