from home.forms import *
from sympy import *

def getSimpleIntegral(ecuacion, variable, limiteInferior, limiteSuperior, string = ""):

    integralEcuacion = latex(Integral(ecuacion, (variable, limiteInferior, limiteSuperior)))

    valorIntegral = integrate(ecuacion, (variable, limiteInferior, limiteSuperior))

    stringIntegral = string + integralEcuacion + "=" + latex(valorIntegral)

    if ( N((N(valorIntegral.evalf(), 4) % 1), 4) != 0 ):
        stringIntegral = stringIntegral + "=" + latex(N(valorIntegral.evalf(), 4))

    return stringIntegral, valorIntegral


def getDoubleIntegral(ecuacion, x, limiteInferiorX, limiteSuperiorX, y, limiteInferiorY, limiteSuperiorY, string = ""):

    integralEcuacion = latex(Integral(ecuacion, (x, limiteInferiorX, limiteSuperiorX), (y, limiteInferiorY, limiteSuperiorY)))

    valorIntegral = integrate(ecuacion, (x, limiteInferiorX, limiteSuperiorX), (y, limiteInferiorY, limiteSuperiorY))

    stringIntegral = string + integralEcuacion + "=" + latex(valorIntegral)

    if ( N((N(valorIntegral.evalf(), 4) % 1), 4) != 0 ):
        stringIntegral = stringIntegral + "=" + latex(N(valorIntegral.evalf(), 4))

    return stringIntegral, valorIntegral


def getErrorMessage(errorMessage):

    messages = {
        0: '',
        1: 'Porfavor revisar los limites de integración, recuerda que el limite inferior '
           'debe ser menor al limite superior de la variable.',
        2: 'La función ingresada no es una distribución de probabilidad!',
        3: 'Error! Porfavor revise los intervalos para calcular la probabilidad. '
           'Recuerde que deben estar entre los intervalos de la distribución de probabilidad.',
        4: 'Error! Existe un error en los datos ingresados, porfavor revisar las instrucciones'
    }

    return messages.get(errorMessage)