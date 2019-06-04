from django.shortcuts import render
from django.views.generic import TemplateView
from home.forms import *
from sympy import *
from home.functions import *


# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name)


class ProbabilidadConjuntaView(TemplateView):
    template = 'probabilidad.conjunta.html'

    def get(self, request):

        ecuacion = EcuacionForm()
        limiteSuperiorX = LimiteSuperiorXForm()
        limiteInferiorX = LimiteInferiorXForm()
        limiteSuperiorY = LimiteSuperiorYForm()
        limiteInferiorY = LimiteInferiorYForm()

        return render(request, self.template, {'ecuacion': ecuacion,
                                               'limiteInferiorX': limiteInferiorX,
                                               'limiteSuperiorX': limiteSuperiorX,
                                               'limiteInferiorY': limiteInferiorY,
                                               'limiteSuperiorY': limiteSuperiorY})

    def post(self, request):

        stringFuncionMarginalX = ""
        stringFuncionMarginalY = ""
        stringCovarianza = ""
        stringValorEsperadoX = ""
        stringValorEsperadoY = ""

        msgMarginalX = ""
        msgMarginalY = ""
        msgValorX = ""
        msgValorY = ""
        msgCovarianza = ""

        try:
            x = symbols('x')
            y = symbols('y')

            ecuacion = (EcuacionForm(request.POST))['ecuacion'].value()
            limiteInferiorX = sympify((LimiteInferiorXForm(request.POST))['limiteInferiorX'].value())
            limiteSuperiorX = sympify((LimiteSuperiorXForm(request.POST))['limiteSuperiorX'].value())
            limiteInferiorY = sympify((LimiteInferiorYForm(request.POST))['limiteInferiorY'].value())
            limiteSuperiorY = sympify((LimiteSuperiorYForm(request.POST))['limiteSuperiorY'].value())

            # Funcion ingresada

            stringIntegral, valorIntegral = getDoubleIntegral(ecuacion, x, limiteInferiorX, limiteSuperiorX,
                                                              y, limiteInferiorY, limiteSuperiorY)

            errorMessage = 1
            # Evaluacion de el limite inferior y superior
            if (N(limiteInferiorX, 3) <= N(limiteSuperiorX, 3) and
                    (N(limiteInferiorY, 3) <= N(limiteSuperiorY, 3))):

                errorMessage += 1
                # Evaluacion de una funcion de probabilidad
                if (N(valorIntegral, 2) > 0.99 and N(valorIntegral, 4) < 1.01):
                    msgMarginalX = "Distribución marginal g(x)"
                    msgMarginalY = "Distribución marginal h(y)"
                    msgValorX = "Valor Esperado E(X)"
                    msgValorY = "Valor Esperado E(Y)"
                    msgCovarianza = "Covarianza"

                    errorMessage = 0

                    # Funcion marginal g(x)
                    stringFuncionMarginalX, valorFuncionMarginalX = getSimpleIntegral(ecuacion, y,
                                                                                      limiteInferiorY,
                                                                                      limiteSuperiorY,
                                                                                      "g(x) = ")

                    # Funcion marginal h(y)
                    stringFuncionMarginalY, valorFuncionMarginalY = getSimpleIntegral(ecuacion, x,
                                                                                      limiteInferiorX,
                                                                                      limiteSuperiorX,
                                                                                      "h(y) = ")

                    # Valor esperado E(X)
                    funcionValorEsperadoX = latex(
                        Integral(x * valorFuncionMarginalX, (x, limiteInferiorX, limiteSuperiorX)))

                    valorEsperadoX = integrate("x * " + ecuacion, (x, limiteInferiorX, limiteSuperiorX),
                                               (y, limiteInferiorY, limiteSuperiorY))

                    stringValorEsperadoX = "E(X) = " + funcionValorEsperadoX + "=" + latex(valorEsperadoX) + \
                                           "=" + latex(N(valorEsperadoX, 4))

                    # Valor esperado E(y)
                    funcionValorEsperadoY = latex(Integral(y * valorFuncionMarginalY,
                                                           (y, limiteInferiorY, limiteSuperiorY)))

                    valorEsperadoY = integrate("y * " + ecuacion, (x, limiteInferiorX, limiteSuperiorX),
                                               (y, limiteInferiorY, limiteSuperiorY))

                    stringValorEsperadoY = "E(Y) = " + funcionValorEsperadoY + "=" + latex(valorEsperadoY) + \
                                           "=" + latex(N(valorEsperadoY, 4))

                    # Valor esperado E(xy)
                    valorEsperadoXY = integrate(" x * y *" + ecuacion,
                                                (x, limiteInferiorX, limiteSuperiorX),
                                                (y, limiteInferiorY, limiteSuperiorY))

                    valorCovarianza = valorEsperadoXY - (valorEsperadoX * valorEsperadoY)

                    stringCovarianza = "{\delta}_{XY} = E(XY) - \delta_X \delta_Y = " + latex(
                        valorEsperadoXY) + "-" + latex(
                        valorEsperadoX) + latex(valorEsperadoY) + "=" + latex(valorCovarianza) + "=" + latex(
                        N(valorCovarianza, 5))

            return render(request, self.template, {'ecuacion': EcuacionForm(request.POST),
                                                   'limiteInferiorX': LimiteInferiorXForm(request.POST),
                                                   'limiteSuperiorX': LimiteSuperiorXForm(request.POST),
                                                   'limiteInferiorY': LimiteInferiorYForm(request.POST),
                                                   'limiteSuperiorY': LimiteSuperiorYForm(request.POST),
                                                   'stringIntegral': stringIntegral,
                                                   'stringFuncionMarginalX': stringFuncionMarginalX,
                                                   'stringValorEsperadoX': stringValorEsperadoX,
                                                   'stringFuncionMarginalY': stringFuncionMarginalY,
                                                   'stringValorEsperadoY': stringValorEsperadoY,
                                                   'stringCovarianza': stringCovarianza,
                                                   'errorMessage': getErrorMessage(errorMessage),
                                                   'msgDistribucion': "Distribución de probabilidad conjunta ",
                                                   'msgMarginalX': msgMarginalX,
                                                   'msgMarginalY': msgMarginalY,
                                                   'msgValorX': msgValorX,
                                                   'msgValorY': msgValorY,
                                                   'msgCovarianza': msgCovarianza})

        except:

            return render(request, self.template, {'ecuacion': EcuacionForm(request.POST),
                                                   'limiteInferiorX': LimiteInferiorXForm(request.POST),
                                                   'limiteSuperiorX': LimiteSuperiorXForm(request.POST),
                                                   'limiteInferiorY': LimiteInferiorYForm(request.POST),
                                                   'limiteSuperiorY': LimiteSuperiorYForm(request.POST),
                                                   'errorMessage': getErrorMessage(4)})


class ProbabilidadDensidadConjuntaView(TemplateView):

    template = 'valor.probabilidad.html'

    def get(self, request):

        ecuacion = EcuacionForm()
        limiteSuperiorX = LimiteSuperiorXForm()
        limiteInferiorX = LimiteInferiorXForm()
        limiteSuperiorY = LimiteSuperiorYForm()
        limiteInferiorY = LimiteInferiorYForm()
        probabilidadInferiorX = ProbabilidadInferiorXForm()
        probabilidadSuperiorX = ProbabilidadSuperiorXForm()
        probabilidadInferiorY = ProbabilidadInferiorYForm()
        probabilidadSuperiorY = ProbabilidadSuperiorYForm()

        return render(request, self.template, {'ecuacion': ecuacion,
                                               'limiteInferiorX': limiteInferiorX,
                                               'limiteSuperiorX': limiteSuperiorX,
                                               'limiteInferiorY': limiteInferiorY,
                                               'limiteSuperiorY': limiteSuperiorY,
                                               'probabilidadInferiorX': probabilidadInferiorX,
                                               'probabilidadSuperiorX': probabilidadSuperiorX,
                                               'probabilidadInferiorY': probabilidadInferiorY,
                                               'probabilidadSuperiorY': probabilidadSuperiorY})

    def post(self, request):

        msgDistribucion = "Distribución de probabilidad conjunta "
        msgProbabilidad = ""
        stringProbabilidad = ""

        try:

            x = symbols('x')
            y = symbols('y')

            ecuacion = (EcuacionForm(request.POST))['ecuacion'].value()
            limiteInferiorX = sympify((LimiteInferiorXForm(request.POST))['limiteInferiorX'].value())
            limiteSuperiorX = sympify((LimiteSuperiorXForm(request.POST))['limiteSuperiorX'].value())
            limiteInferiorY = sympify((LimiteInferiorYForm(request.POST))['limiteInferiorY'].value())
            limiteSuperiorY = sympify((LimiteSuperiorYForm(request.POST))['limiteSuperiorY'].value())
            probabilidadInferiorX = sympify((ProbabilidadInferiorXForm(request.POST))['probabilidadInferiorX'].value())
            probabilidadSuperiorX = sympify((ProbabilidadSuperiorXForm(request.POST))['probabilidadSuperiorX'].value())
            probabilidadInferiorY = sympify((ProbabilidadInferiorYForm(request.POST))['probabilidadInferiorY'].value())
            probabilidadSuperiorY = sympify((ProbabilidadSuperiorYForm(request.POST))['probabilidadSuperiorY'].value())

            # Funcion ingresada
            stringIntegral, valorIntegral = getDoubleIntegral(ecuacion, x, limiteInferiorX, limiteSuperiorX,
                                                              y, limiteInferiorY, limiteSuperiorY)
            errorMessage = 1

            if (N(limiteInferiorX, 3) <= N(limiteSuperiorX, 3) and
                    (N(limiteInferiorY, 3) <= N(limiteSuperiorY, 3))):

                errorMessage += 1

                if (N(valorIntegral, 2) > 0.99 and N(valorIntegral, 4) < 1.01):

                    errorMessage += 1

                    if (N(probabilidadInferiorX, 3) >= N(limiteInferiorX, 3) and
                            N(probabilidadInferiorX, 3) <= N(probabilidadSuperiorX, 3) and
                            N(probabilidadSuperiorX, 3) <= N(limiteSuperiorX, 3) and
                            N(probabilidadSuperiorX, 3) >= N(probabilidadInferiorX, 3) and
                            N(probabilidadInferiorY, 3) >= N(limiteInferiorY, 3) and
                            N(probabilidadInferiorY, 3) <= N(probabilidadSuperiorY, 3) and
                            N(probabilidadSuperiorY, 3) <= N(limiteSuperiorY, 2) and
                            N(probabilidadSuperiorY, 3) >= N(probabilidadInferiorY, 2)):

                        errorMessage = 0
                        msgProbabilidad = "Probabilidad"

                        text = "P(" + latex(probabilidadInferiorX) + " < X < " \
                                             + latex(probabilidadSuperiorX) + ", " \
                                             + latex(probabilidadInferiorY) + " < Y < " \
                                             + latex(probabilidadSuperiorY) + ") = "

                        stringProbabilidad, valorProbabilidad = getDoubleIntegral(ecuacion, x,
                                                                                  limiteInferiorX, limiteSuperiorX, y,
                                                                                  limiteInferiorY, limiteSuperiorY, text)

            return render(request, self.template, {'ecuacion': EcuacionForm(request.POST),
                                                   'limiteInferiorX': LimiteInferiorXForm(request.POST),
                                                   'limiteSuperiorX': LimiteSuperiorXForm(request.POST),
                                                   'limiteInferiorY': LimiteInferiorYForm(request.POST),
                                                   'limiteSuperiorY': LimiteSuperiorYForm(request.POST),
                                                   'probabilidadInferiorX': ProbabilidadInferiorXForm(request.POST),
                                                   'probabilidadSuperiorX': ProbabilidadSuperiorXForm(request.POST),
                                                   'probabilidadInferiorY': ProbabilidadInferiorYForm(request.POST),
                                                   'probabilidadSuperiorY': ProbabilidadSuperiorYForm(request.POST),
                                                   'stringIntegral': stringIntegral,
                                                   'stringProbabilidad': stringProbabilidad,
                                                   'msgProbabilidad': msgProbabilidad,
                                                   'msgDistribucion': msgDistribucion,
                                                   'errorMessage': getErrorMessage(errorMessage)})

        except:

            return render(request, self.template, {'ecuacion': EcuacionForm(request.POST),
                                                   'limiteInferiorX': LimiteInferiorXForm(request.POST),
                                                   'limiteSuperiorX': LimiteSuperiorXForm(request.POST),
                                                   'limiteInferiorY': LimiteInferiorYForm(request.POST),
                                                   'limiteSuperiorY': LimiteSuperiorYForm(request.POST),
                                                   'probabilidadInferiorX': ProbabilidadInferiorXForm(request.POST),
                                                   'probabilidadSuperiorX': ProbabilidadSuperiorXForm(request.POST),
                                                   'probabilidadInferiorY': ProbabilidadInferiorYForm(request.POST),
                                                   'probabilidadSuperiorY': ProbabilidadSuperiorYForm(request.POST),
                                                   'msgDistribucion': msgDistribucion,
                                                   'errorMessage': getErrorMessage(4)})


class ProbabilidadContinuaView(TemplateView):
    template = 'probabilidad.continua.html'

    def get(self, request):

        ecuacion = EcuacionSimpleForm()
        limiteInferior = LimiteInferiorForm()
        limiteSuperior = LimiteSuperiorForm()
        probabilidadInferior = ProbabilidadInferiorForm()
        probabilidadSuperior = ProbabilidadSuperiorForm()

        return render(request, self.template, {'ecuacion': ecuacion,
                                               'limiteInferior': limiteInferior,
                                               'limiteSuperior': limiteSuperior,
                                               'probabilidadInferior': probabilidadInferior,
                                               'probabilidadSuperior': probabilidadSuperior})

    def post(self, request):

        msgDistribucion = "Distribución de probabilidad continua"
        msgProbabilidad = ""
        stringIntegral = ""

        try:

            x = symbols('x')
            y = symbols('y')

            # Obteniendo string de los cuadros de informacion
            ecuacion = (EcuacionSimpleForm(request.POST))['ecuacion'].value()
            limiteInferior = sympify((LimiteInferiorForm(request.POST))['limiteInferior'].value())
            limiteSuperior = sympify((LimiteSuperiorForm(request.POST))['limiteSuperior'].value())
            probabilidadSuperior = sympify((ProbabilidadSuperiorForm(request.POST))['probabilidadSuperior'].value())
            probabilidadInferior = sympify((ProbabilidadInferiorForm(request.POST))['probabilidadInferior'].value())

            stringProbabilidad = ""

            # String y valor de la funcion ingresada
            stringIntegral, valorIntegral = getSimpleIntegral(ecuacion, x,
                                                              limiteInferior,
                                                              limiteSuperior)
            # Evaluación de limite inferior menor que limite superior
            errorMessage = 1

            if (N(limiteInferior, 3) <= N(limiteSuperior, 3)):

                errorMessage += 1

                if (N(valorIntegral, 2) > 0.99 and N(valorIntegral, 4) < 1.01):

                    errorMessage += 1

                    if (N(probabilidadInferior, 3) >= N(limiteInferior, 3) and
                            N(probabilidadInferior, 3) <= N(probabilidadSuperior, 3) and
                            N(probabilidadSuperior, 3) <= N(limiteSuperior, 3) and
                            N(probabilidadSuperior, 3) >= N(probabilidadInferior, 3)):
                        msgProbabilidad = "Probabilidad"
                        errorMessage = 0

                        stringProbabilidad, valorProbabilidad = getSimpleIntegral(ecuacion, x,
                                                                                  probabilidadInferior,
                                                                                  probabilidadSuperior)

                        stringProbabilidad = "P(" + latex(probabilidadInferior) + " < X < " \
                                             + latex(probabilidadSuperior) + ") =" + stringProbabilidad

            return render(request, self.template, {'ecuacion': EcuacionSimpleForm(request.POST),
                                                   'limiteInferior': LimiteInferiorForm(request.POST),
                                                   'limiteSuperior': LimiteSuperiorForm(request.POST),
                                                   'probabilidadInferior': ProbabilidadInferiorForm(request.POST),
                                                   'probabilidadSuperior': ProbabilidadSuperiorForm(request.POST),
                                                   'stringIntegral': stringIntegral,
                                                   'stringProbabilidad': stringProbabilidad,
                                                   'msgDistribucion': msgDistribucion,
                                                   'msgProbabilidad': msgProbabilidad,
                                                   'errorMessage': getErrorMessage(errorMessage)})

        except:

            return render(request, self.template, {'ecuacion': EcuacionSimpleForm(request.POST),
                                                   'limiteInferior': LimiteInferiorForm(request.POST),
                                                   'limiteSuperior': LimiteSuperiorForm(request.POST),
                                                   'probabilidadInferior': ProbabilidadInferiorForm(request.POST),
                                                   'probabilidadSuperior': ProbabilidadSuperiorForm(request.POST),
                                                   'stringIntegral': stringIntegral,
                                                   'msgDistribucion': msgDistribucion,
                                                   'errorMessage': getErrorMessage(4)})


class AcomulativaContinuaView(TemplateView):
    template = 'funcion.acumulativa.html'

    def get(self, request):

        ecuacion = EcuacionSimpleForm()
        limiteInferior = LimiteInferiorForm()
        limiteSuperior = LimiteSuperiorForm()
        probabilidadInferior = ProbabilidadInferiorForm()

        return render(request, self.template, {'ecuacion': ecuacion,
                                               'limiteInferior': limiteInferior,
                                               'limiteSuperior': limiteSuperior,
                                               'probabilidadInferior': probabilidadInferior})

    def post(self, request):

        msgDistribucion = "Distribución de probabilidad"
        msgProbabilidad = ""
        stringIntegral = ""
        stringProbabilidad = ""

        try:

            x = symbols('x')

            # Obteniendo string de los cuadros de informacion
            ecuacion = (EcuacionSimpleForm(request.POST))['ecuacion'].value()
            limiteInferior = sympify((LimiteInferiorForm(request.POST))['limiteInferior'].value())
            limiteSuperior = sympify((LimiteSuperiorForm(request.POST))['limiteSuperior'].value())
            probabilidadInferior = sympify((ProbabilidadInferiorForm(request.POST))['probabilidadInferior'].value())

            # String y valor de la funcion ingresada
            stringIntegral, valorIntegral = getSimpleIntegral(ecuacion, x, limiteInferior, limiteSuperior)

            # Evaluación de limite inferior menor que limite superior
            errorMessage = 1

            if (N(limiteInferior, 3) <= N(limiteSuperior, 3)):

                # Evaluación de distribución de probabilidad
                errorMessage += 1

                if (N(valorIntegral, 2) > 0.99 and N(valorIntegral, 4) < 1.01):

                    # Evaluacion de los limites de probabilidad
                    errorMessage += 1

                    if (N(probabilidadInferior, 3) >= N(limiteInferior, 3) and
                            N(probabilidadInferior, 3) <= N(limiteSuperior, 3)):
                        msgProbabilidad = "Función de distribución acumulativa "
                        errorMessage = 0

                        stringProbabilidad, valorProbabilidad = getSimpleIntegral(ecuacion, x,
                                                                                  limiteInferior,
                                                                                  probabilidadInferior)

                        stringProbabilidad = r"P\left(X \leq" + latex(probabilidadInferior) + r"\right) =" + \
                                             stringProbabilidad

            return render(request, self.template, {'ecuacion': EcuacionSimpleForm(request.POST),
                                                   'limiteInferior': LimiteInferiorForm(request.POST),
                                                   'limiteSuperior': LimiteSuperiorForm(request.POST),
                                                   'probabilidadInferior': ProbabilidadInferiorForm(request.POST),
                                                   'stringIntegral': stringIntegral,
                                                   'stringProbabilidad': stringProbabilidad,
                                                   'msgDistribucion': msgDistribucion,
                                                   'msgProbabilidad': msgProbabilidad,
                                                   'errorMessage': getErrorMessage(errorMessage)})

        except:
            return render(request, self.template, {'ecuacion': EcuacionSimpleForm(request.POST),
                                                   'limiteInferior': LimiteInferiorForm(request.POST),
                                                   'limiteSuperior': LimiteSuperiorForm(request.POST),
                                                   'probabilidadInferior': ProbabilidadInferiorForm(request.POST),
                                                   'stringIntegral': stringIntegral,
                                                   'msgDistribucion': msgDistribucion,
                                                   'errorMessage': getErrorMessage(4)})


class EsperadoContinuaView(TemplateView):
    template = 'esperado.html'

    def get(self, request):

        ecuacion = EcuacionSimpleForm()
        limiteInferior = LimiteInferiorForm()
        limiteSuperior = LimiteSuperiorForm()

        return render(request, self.template, {'ecuacion': ecuacion,
                                               'limiteInferior': limiteInferior,
                                               'limiteSuperior': limiteSuperior})

    def post(self, request):

        ecuacion = EcuacionSimpleForm(request.POST)
        limiteInferior = LimiteInferiorForm(request.POST)
        limiteSuperior = LimiteSuperiorForm(request.POST)

        try:

            x = symbols('x')

            # Obteniendo string de los cuadros de informacion
            valorEcuacion = ecuacion['ecuacion'].value()
            valorLimiteInferior = sympify(limiteInferior['limiteInferior'].value())
            valorLimiteSuperior = sympify(limiteSuperior['limiteSuperior'].value())

            msgValorEsperado = ""
            msgDistribucion = ""
            stringValorEsperado = ""

            # String y valor de la funcion ingresada
            stringIntegral, valorIntegral = getSimpleIntegral(valorEcuacion, x,
                                                              valorLimiteInferior,
                                                              valorLimiteSuperior)

            # Evaluación de limite inferior menor que limite superior
            errorMessage = 1

            if (N(valorLimiteInferior, 3) <= N(valorLimiteSuperior, 3)):

                # Evaluación de distribución de probabilidad
                errorMessage += 1

                if (N(valorIntegral, 2) > 0.99 and N(valorIntegral, 4) < 1.01):
                    errorMessage = 0
                    msgValorEsperado = "Valor Esperado E(X)"
                    msgDistribucion = "Distribución de probabilidad"

                    stringValorEsperado, valorEsperado = getSimpleIntegral("x * " + valorEcuacion,
                                                                           x, valorLimiteInferior,
                                                                           valorLimiteSuperior)

            return render(request, self.template, {'ecuacion': ecuacion,
                                                   'limiteInferior': limiteInferior,
                                                   'limiteSuperior': limiteSuperior,
                                                   'stringIntegral': stringIntegral,
                                                   'stringValorEsperado': stringValorEsperado,
                                                   'msgDistribucion': msgDistribucion,
                                                   'msgValorEsperado': msgValorEsperado,
                                                   'errorMessage': getErrorMessage(errorMessage)})

        except:

            return render(request, self.template, {'ecuacion': ecuacion,
                                                   'limiteInferior': limiteInferior,
                                                   'limiteSuperior': limiteSuperior,
                                                   'stringIntegral': stringIntegral,
                                                   'msgDistribucion': msgDistribucion,
                                                   'errorMessage': getErrorMessage(4)})


class VarianzaContinuaView(TemplateView):
    template = 'varianza.html'

    def get(self, request):

        ecuacion = EcuacionSimpleForm()
        limiteInferior = LimiteInferiorForm()
        limiteSuperior = LimiteSuperiorForm()

        return render(request, self.template, {'ecuacion': ecuacion,
                                               'limiteInferior': limiteInferior,
                                               'limiteSuperior': limiteSuperior, })

    def post(self, request):

        msgDistribucion = "Distribución de probabilidad"
        msgProbabilidad = ""
        stringIntegral = ""
        stringProbabilidad = ""

        try:

            x = symbols('x')

            # Obteniendo string de los cuadros de informacion
            ecuacion = (EcuacionSimpleForm(request.POST))['ecuacion'].value()
            limiteInferior = sympify((LimiteInferiorForm(request.POST))['limiteInferior'].value())
            limiteSuperior = sympify((LimiteSuperiorForm(request.POST))['limiteSuperior'].value())

            # Funcion ingresada
            stringIntegral, valorIntegral = getSimpleIntegral(ecuacion, x,
                                                              limiteInferior,
                                                              limiteSuperior)
            errorMessage = 1

            if (N(limiteInferior, 3) <= N(limiteSuperior, 3)):

                errorMessage += 1

                if (N(valorIntegral, 2) > 0.99 and N(valorIntegral, 4) < 1.01):
                    msgProbabilidad = "Varianza"
                    valorEsperadoX = integrate("x * " + ecuacion,
                                               (x, limiteInferior, limiteSuperior))

                    valorEsperadoX2 = integrate("x**2 * " + ecuacion,
                                                (x, limiteInferior, limiteSuperior))

                    stringProbabilidad = r"{\delta}^{2} = E(X^2) - " + r"{\mu}^{2} =" + latex(valorEsperadoX2) \
                                         + " - " + r"{\left(" + latex(valorEsperadoX) + r"\right)}^{2}" + "=" + \
                                         latex(N(valorEsperadoX2.evalf(), 5) - pow(N(valorEsperadoX.evalf(), 5), 2))

            return render(request, self.template, {'ecuacion': EcuacionSimpleForm(request.POST),
                                                   'limiteInferior': LimiteInferiorForm(request.POST),
                                                   'limiteSuperior': LimiteSuperiorForm(request.POST),
                                                   'stringIntegral': stringIntegral,
                                                   'stringProbabilidad': stringProbabilidad,
                                                   'msgDistribucion': msgDistribucion,
                                                   'msgProbabilidad': msgProbabilidad,
                                                   'errorMessage': getErrorMessage(errorMessage)})

        except:

            return render(request, self.template, {'ecuacion': EcuacionSimpleForm(request.POST),
                                                   'limiteInferior': LimiteInferiorForm(request.POST),
                                                   'limiteSuperior': LimiteSuperiorForm(request.POST),
                                                   'stringIntegral': stringIntegral,
                                                   'msgDistribucion': msgDistribucion,
                                                   'errorMessage': getErrorMessage(4)})
