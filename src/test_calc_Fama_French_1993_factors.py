import pandas as pd
from pandas.testing import assert_frame_equal

import load_CRSP_Compustat
from calc_Fama_French_1993_factors import (
    calc_book_equity_and_years_in_compustat,
    subset_CRSP_to_common_stock_and_exchanges,
    calculate_market_equity,
    use_dec_market_equity,
    merge_CRSP_and_Compustat,
    assign_size_and_bm_portfolios,
    create_fama_french_portfolios,
    create_factors_from_portfolios,
    create_Fama_French_factors,
)


import config

DATA_DIR = config.DATA_DIR


comp = load_CRSP_Compustat.load_compustat(data_dir=DATA_DIR)
crsp = load_CRSP_Compustat.load_CRSP_stock_ciz(data_dir=DATA_DIR)
ccm = load_CRSP_Compustat.load_CRSP_Comp_Link_Table(data_dir=DATA_DIR)


def test_calc_book_equity_and_years_in_compustat():
    
    comp = load_CRSP_Compustat.load_compustat(data_dir=DATA_DIR)
    comp = calc_book_equity_and_years_in_compustat(comp)
    
    expected = """
        gvkey   datadate    be
        001000 1961-12-31   NaN
        001000 1962-12-31   NaN
        001000 1963-12-31 0.561
        001000 1964-12-31 0.627
        001000 1965-12-31 0.491
    """
    output = comp[["gvkey", "datadate", "be"]].head().to_string(index=False)
    # print(output)
    assert output.replace(" ", "").replace("\n", "") == expected.replace(" ", "").replace("\n", "")

def test_subset_CRSP_to_common_stock_and_exchanges():
    crsp = load_CRSP_Compustat.load_CRSP_stock_ciz(data_dir=DATA_DIR)
    crsp = subset_CRSP_to_common_stock_and_exchanges(crsp)
    
    output = crsp.loc[crsp["jdate"] <= "2022", :].shape
    expected = (3348395, 16)
    
    assert output== expected

def test_calculate_market_equity():
    crsp = load_CRSP_Compustat.load_CRSP_stock_ciz(data_dir=DATA_DIR)
    crsp = subset_CRSP_to_common_stock_and_exchanges(crsp)
    crsp2 = calculate_market_equity(crsp)
    output = crsp2[["permco", "mthcaldt", "me"]].head().to_string(index=False)
    # print(output)
    expected = """
    permco   mthcaldt         me
    7952 1986-01-31 16100.0000
    7952 1986-02-28 11960.0000
    7952 1986-03-31 16330.0000
    7952 1986-04-30 15172.0000
    7952 1986-05-30 11793.9542
    """
    assert output.replace(" ", "").replace("\n", "") == expected.replace(" ", "").replace("\n", "")

def test_factors():
    vwret, vwret_n, ff_factors, ff_nfirms = create_Fama_French_factors(data_dir=DATA_DIR)
    expected = """
        date        BH        BL        BM
    2022-08-31 -0.014792 -0.046368 -0.018841
    2022-09-30 -0.087951 -0.088352 -0.094143
    2022-10-31  0.147658  0.059447  0.110792
    2022-11-30  0.049565  0.048842  0.055844
    2022-12-31 -0.049520 -0.067278 -0.043296
    """.replace(" ", "").replace("\n", "")
    output = ff_factors[['date', 'BH', 'BL', 'BM']].tail().to_string(index=False)
    # print(output)
    assert expected == output.replace(" ", "").replace("\n", "")

    