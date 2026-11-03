"""台股：載入資料、算條件層，回傳 (Mkt, Layers, 診斷)。"""
from __future__ import annotations

import numpy as np

from . import signals as sg
from . import tw_data as td


def prepare_tw(anomaly=True):
    m = td.load_prices(anomaly=anomaly)
    dec = sg.decision_days(m.dates)
    dec_dates = m.dates[dec]
    rev = td.load_revenue(m.codes)
    l2, y0, y3 = sg.revenue_layer(rev, dec_dates)
    eps_ff, have_cols = td.load_eps(m.codes, m.dates)
    l3, eps_r, eps_have = sg.eps_layer(eps_ff, m.codes, dec_dates)
    L = sg.build_layers(m, l2, l3, dec)
    diag = dict(yoy=y0, yoy3=y3, eps_ratio=eps_r, eps_have=eps_have, eps_cols=have_cols)
    return m, L, diag
