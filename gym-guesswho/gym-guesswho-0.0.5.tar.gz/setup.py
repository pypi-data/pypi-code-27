import setuptools

setuptools.setup(
    name='gym-guesswho',
    version='0.0.5',
    author="Charles Rule, William (Alex) Fallin",
    author_email="alexfallin@gmail.com",
    description="An OpenAI Gym framework for machine learning with the game \"Guess Who?\"",
    #long_description=long_description,
    #long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://github.com/cerule7/Guess-Who",
    packages=setuptools.find_packages(),
    install_requires=['gym', 'numpy', 'torch'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Natural Language :: English",
        "License :: Other/Proprietary License",
    ),
)