#!/usr/bin/env python
import views

def medieval():
    import argparse
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    with start_view():
        pass
