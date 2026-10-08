"""網頁數字格式：精度一致、指數不重複基期、景氣燈號轉燈色。"""
from macro_db import render as R

IDX = {"display": "level", "unit": "指數(105=100)"}
SCORE = {"display": "level", "unit": "分"}
LIGHT = {"display": "level", "unit": "燈號序數（1藍、2黃藍、3綠、4黃紅、5紅）"}


def test_integer_values_have_no_decimals():
    assert R.vtxt(41.0, SCORE) == "41 分"
    assert R.change_txt(41.0, 41.0, SCORE).startswith("0 分")


def test_change_precision_follows_displayed_value():
    assert R.vtxt(143.8, IDX) == "143.8"
    assert R.change_txt(143.8, 145.47, IDX).startswith("−1.7")
    assert "指數" not in R.change_txt(143.8, 145.47, IDX)


def test_signal_light_shows_color():
    assert R.vtxt(5.0, LIGHT) == "紅燈"
    assert R.change_txt(5.0, 5.0, LIGHT) == "持平"
    assert R.change_txt(5.0, 4.0, LIGHT) == "由黃紅燈轉紅燈"


def test_unit_based_precision():
    spread = {"display": "level", "unit": "百分點"}
    diffusion = {"display": "level", "unit": "擴散指數"}
    assert R.vtxt(0.5, spread) == "0.50 百分點"
    assert R.vtxt(-0.2, diffusion) == "−0.2 擴散指數"
    assert R.vtxt(18.1, diffusion) == "18.1 擴散指數"
