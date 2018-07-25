#!/usr/bin/env python
from pathlib import Path
from ftplib import FTP
from dateutil.parser import parse
from urllib.parse import urlparse
from datetime import date, datetime, timedelta
from typing import Union
import zipfile
import numpy as np
import pandas as pd

URL = 'ftp://mussel.srl.caltech.edu/pub/ace/browse/MAG16sec/'
EPOCH = datetime(1996, 1, 1)


def download(dt: Union[str, date, datetime], odir: Path):

    odir = Path(odir).expanduser()

    if isinstance(dt, str):
        dt = parse(dt).date()
    elif isinstance(dt, (tuple, list, np.ndarray)):
        for d in dt:
            download(d, odir)

    assert isinstance(dt, (date, datetime))

    p = urlparse(URL)
    host = p[1]
    rpath = p[2] + str(dt.year)

    stem = date2filename(dt)
    fn = odir / stem

    if zipfile.is_zipfile(fn):
        print('SKIP:', fn)
        return

    print(fn)
    with FTP(host, 'anonymous', 'guest', timeout=10) as F, fn.open('wb') as f:
        F.cwd(rpath)
        F.retrbinary(f'RETR {stem}', f.write)


def date2filename(dt: Union[date, datetime]) -> str:
    if isinstance(dt, str):
        dt = parse(dt).date()

    doy = dt.strftime('%j')
    return f'ACE_MAG16_{dt.year}-{doy}_V3-3.zip'


def load(dt: date, path: Path) -> pd.DataFrame:
    path = Path(path).expanduser()

    stem = date2filename(dt)
    fn = path / stem

    with zipfile.ZipFile(fn).open(fn.stem) as f:
        dat = pd.read_csv(f, sep='\s+', comment='#', header=None, index_col=False,
                          usecols=[1, 3, 4, 5, 6, 7, 8, 9, 10],
                          names=['time', 'Br', 'Bt', 'Bn', 'Bx', 'By', 'Bz', 'Btotal', 'dBrms'])

    dat.index = [EPOCH + timedelta(seconds=t) for t in dat['time']]

    dat.drop(columns='time', inplace=True)

    return dat
