from goal_optimasier import generateGrid, calculateTransitionPropabilities, calculateValues
import pytest


def test_should_generateGrid_without_cashflows():
    W0 = 100
    T = 11
    iMax = 476
    minMean = 0.0526
    minStd = 0.0374
    maxMean = 0.0886
    maxStd = 0.1954
    grid = generateGrid(W0, T, iMax, minMean, minStd, maxMean, maxStd)

    assert grid.shape == (T,iMax)
    assert pytest.approx(1834,abs=0.5)  == grid[T-1, iMax-1] 



def test_should_calclulate_transition_propabilities_for_every_value():
    W1 = [50.58320071, 57.97023288, 66.43604702, 76.13818548, 87.25719769, 100.0, 114.60372628, 131.34014078, 150.52069544, 172.50232581]
    W0 = 100
    mean = 0.0526
    std = 0.0374
    h = 1

    result = calculateTransitionPropabilities(W0, W1, mean,std,h)

    assert len(result) == len(W1)
    assert pytest.approx(1,0.001) == result.sum() 

def test_should_choose_values():
    W1 = [50.58320071, 57.97023288, 66.43604702, 76.13818548, 87.25719769, 100.0, 114.60372628, 131.34014078, 150.52069544, 172.50232581]
    W0 = 100
    meanMin = 0.0526
    stdMin = 0.0374
    meanMax = 0.0886
    stdMax = 0.1954

    portfolios = [[meanMin,stdMin],[meanMax, stdMax]]
    h = 1

    result = choose_portfolio(portfolios,calculateTransitionPropabilities(W0, W1, mean,std,h))

    assert 1 == result.index
    assert pytest.approx(109.26, 0.01) == result.value 




