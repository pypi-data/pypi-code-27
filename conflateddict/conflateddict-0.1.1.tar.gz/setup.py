import setuptools

setuptools.setup(
    name="conflateddict",
    version="0.1.1",
    url="https://github.com/christianreimer/conflateddict",
    author="Christian Reimer",
    author_email="christian.reimer@gmail.com",
    description="Classes to help conflate streaming data.",
    long_description="""This module contains classes to assist with conflating streaming data. This can be used to manage the load on consuming tasks, and is especially useful if the consumers only need the current value and can thus safely discard intermediate updates.
        
    Example:
        >>> from conflateddict import ConflatedDict
        >>> import random
        >>>
        >>> keys = ['red', 'green', 'blue', 'orange']
        >>> con = ConflatedDict()
        >>> for _ in range(100):
        ...    con[random.choice(keys)] = random.randint(0, 100)
        ...
        >>> print(list(con.items())
        [('orange', 32), ('green', 71), ('red', 71), ('blue', 80)]
        >>> print(len(con))
        4
        >>> # After a reset, there will be no dirty values
        >>> con.reset()
        >>> print(list(con.items())
        []
        >>> print(len(con))
        0
        >>> # After another update, any new dirty values will be returned
        >>> con[random.choice(keys)] = random.randint(0, 100)
        >>> print(list(con.items())
        [('orange', 58)]
        >>>
        >>> # We still have access to all the values through data()
        >>> print(list(con.data().items()))
        [('blue', 80), ('red', 71), ('green', 71), ('orange', 58)]
        >>> print(len(con.data()))
        4
        >>>
        """,
    packages=setuptools.find_packages(exclude=["tests"]),
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
    ],
)
