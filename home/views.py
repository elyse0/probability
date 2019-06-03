from django.shortcuts import render
from django.views.generic import TemplateView
from home.forms import *
from sympy import *
from sympy.parsing.sympy_parser import parse_expr


# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name)


class ProbabilidadConjuntaView(TemplateView):
    getTemplate = 'probabilidad.conjunta.get.html'
    postTemplate = 'probabilidad.conjunta.post.html'
    errorTemplate = 'probabilidad.conjunta.error.html'

    def get(self, request):

        ecuacion = EcuacionForm()
        limiteSuperiorX = LimiteSuperiorXForm()
        limiteInferiorX = LimiteInferiorXForm()
        limiteSuperiorY = LimiteSuperiorYForm()
        limiteInferiorY = LimiteInferiorYForm()

        return render(request, self.getTemplate, {'ecuacion': ecuacion,
                                                  'limiteInferiorX': limiteInferiorX,
                                                  'limiteSuperiorX': limiteSuperiorX,
                                                  'limiteInferiorY': limiteInferiorY,
                                                  'limiteSuperiorY': limiteSuperiorY})

    def post(self, request):

        ecuacion = EcuacionForm(request.POST)
        limiteInferiorX = LimiteInferiorXForm(request.POST)
        limiteSuperiorX = LimiteSuperiorXForm(request.POST)
        limiteInferiorY = LimiteInferiorYForm(request.POST)
        limiteSuperiorY = LimiteSuperiorYForm(request.POST)

        try:
            x = symbols('x')
            y = symbols('y')

            valorEcuacion = ecuacion['ecuacion'].value()
            valorLimiteInferiorX = sympify(limiteInferiorX['limiteInferiorX'].value())
            valorLimiteSuperiorX = sympify(limiteSuperiorX['limiteSuperiorX'].value())
            valorLimiteInferiorY = sympify(limiteInferiorY['limiteInferiorY'].value())
            valorLimiteSuperiorY = sympify(limiteSuperiorY['limiteSuperiorY'].value())

            # Funcion ingresada
            integralEcuacion = latex(Integral(valorEcuacion, (x, valorLimiteInferiorX, valorLimiteSuperiorX),
                                              (y, valorLimiteInferiorY, valorLimiteSuperiorY)))

            valorIntegral = integrate(valorEcuacion, (x, valorLimiteInferiorX, valorLimiteSuperiorX),
                                      (y, valorLimiteInferiorY, valorLimiteSuperiorY))

            print(valorIntegral)

            stringIntegral = integralEcuacion + "=" + latex(valorIntegral)

            print(stringIntegral)
            print(N(valorIntegral, 2))

            errorMessage = "Porfavor revisar los limites de integración, " \
                           "recuerda que el limite inferior debe ser menor al limite superior de la variable."

            if (N(valorLimiteInferiorX, 3) <= N(valorLimiteSuperiorX, 3) and
                    (N(valorLimiteInferiorY, 3) <= N(valorLimiteSuperiorY, 3))):

                errorMessage = "La función ingresada no es una distribución de probabilidad!"
                # Evaluacion de una funcion de probabilidad
                if (N(valorIntegral, 2) > 0.99 and N(valorIntegral, 4) < 1.01):
                    # Funcion marginal g(x)
                    funcionMarginalX = latex(Integral(valorEcuacion, (y, valorLimiteInferiorY, valorLimiteSuperiorY)))

                    valorFuncionMarginalX = integrate(valorEcuacion, (y, valorLimiteInferiorY, valorLimiteSuperiorY))

                    stringFuncionMarginalX = "g(x) = " + funcionMarginalX + "=" + latex(valorFuncionMarginalX)

                    # Funcion marginal h(y)
                    funcionMarginalY = latex(Integral(valorEcuacion, (x, valorLimiteInferiorX, valorLimiteSuperiorX)))

                    valorFuncionMarginalY = integrate(valorEcuacion, (x, valorLimiteInferiorX, valorLimiteSuperiorX))

                    stringFuncionMarginalY = "h(y) = " + funcionMarginalY + "=" + latex(valorFuncionMarginalY)

                    # Valor esperado E(X)
                    print("OK4")
                    funcionValorEsperadoX = latex(
                        Integral(x * valorFuncionMarginalX, (x, valorLimiteInferiorX, valorLimiteSuperiorX)))

                    print(funcionValorEsperadoX)

                    valorEsperadoX = integrate("x * " + valorEcuacion, (x, valorLimiteInferiorX, valorLimiteSuperiorX),
                                               (y, valorLimiteInferiorY, valorLimiteSuperiorY))

                    print("OK5")

                    stringValorEsperadoX = "E(x) = " + funcionValorEsperadoX + "=" + latex(
                        valorEsperadoX) + "=" + latex(
                        N(valorEsperadoX, 5))

                    print("OK6")

                    # Valor esperado E(y)
                    funcionValorEsperadoY = latex(
                        Integral(y * valorFuncionMarginalY, (y, valorLimiteInferiorY, valorLimiteSuperiorY)))

                    valorEsperadoY = integrate("y * " + valorEcuacion, (x, valorLimiteInferiorX, valorLimiteSuperiorX),
                                               (y, valorLimiteInferiorY, valorLimiteSuperiorY))

                    stringValorEsperadoY = "E(y) = " + funcionValorEsperadoY + "=" + latex(
                        valorEsperadoY) + "=" + latex(
                        N(valorEsperadoY, 5))

                    # Valor esperado E(xy)
                    valorEsperadoXY = integrate(" x * y *" + valorEcuacion,
                                                (x, valorLimiteInferiorX, valorLimiteSuperiorX),
                                                (y, valorLimiteInferiorY, valorLimiteSuperiorY))

                    valorCovarianza = valorEsperadoXY - (valorEsperadoX * valorEsperadoY)

                    stringCovarianza = "Cov = E(XY) - E(X)E(Y) = " + latex(valorEsperadoXY) + "-" + latex(
                        valorEsperadoX) + latex(valorEsperadoY) + "=" + latex(valorCovarianza) + "=" + latex(
                        N(valorCovarianza, 5))

                    return render(request, self.postTemplate, {'ecuacion': ecuacion,
                                                               'limiteInferiorX': limiteInferiorX,
                                                               'limiteSuperiorX': limiteSuperiorX,
                                                               'limiteInferiorY': limiteInferiorY,
                                                               'limiteSuperiorY': limiteSuperiorY,
                                                               'stringIntegral': integralEcuacion,
                                                               'stringValorIntegral': valorIntegral,
                                                               'stringIntegralCompleta': stringIntegral,
                                                               'stringFuncionMarginalX': stringFuncionMarginalX,
                                                               'stringValorEsperadoX': stringValorEsperadoX,
                                                               'stringFuncionMarginalY': stringFuncionMarginalY,
                                                               'stringValorEsperadoY': stringValorEsperadoY,
                                                               'stringCovarianza': stringCovarianza})

            return render(request, self.errorTemplate, {'ecuacion': ecuacion,
                                                        'limiteInferiorX': limiteInferiorX,
                                                        'limiteSuperiorX': limiteSuperiorX,
                                                        'limiteInferiorY': limiteInferiorY,
                                                        'limiteSuperiorY': limiteSuperiorY,
                                                        'stringIntegral': integralEcuacion,
                                                        'stringValorIntegral': valorIntegral,
                                                        'stringIntegralCompleta': stringIntegral,
                                                        'errorMessage': errorMessage})

        except:

            return render(request, self.errorTemplate, {'ecuacion': ecuacion,
                                                        'limiteInferiorX': limiteInferiorX,
                                                        'limiteSuperiorX': limiteSuperiorX,
                                                        'limiteInferiorY': limiteInferiorY,
                                                        'limiteSuperiorY': limiteSuperiorY,
                                                        'errorMessage': "Error! Existe un error en los datos ingresados, porfavor revisar las instrucciones"})


class ProbabilidadDensidadConjuntaView(TemplateView):
    getTemplate = 'valor.probabilidad.get.html'
    postTemplate = 'valor.probabilidad.post.html'
    errorTemplate = 'valor.probabilidad.error.html'

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

        return render(request, self.getTemplate, {'ecuacion': ecuacion,
                                                  'limiteInferiorX': limiteInferiorX,
                                                  'limiteSuperiorX': limiteSuperiorX,
                                                  'limiteInferiorY': limiteInferiorY,
                                                  'limiteSuperiorY': limiteSuperiorY,
                                                  'probabilidadInferiorX': probabilidadInferiorX,
                                                  'probabilidadSuperiorX': probabilidadSuperiorX,
                                                  'probabilidadInferiorY': probabilidadInferiorY,
                                                  'probabilidadSuperiorY': probabilidadSuperiorY})

    def post(self, request):

        ecuacion = EcuacionForm(request.POST)
        limiteInferiorX = LimiteInferiorXForm(request.POST)
        limiteSuperiorX = LimiteSuperiorXForm(request.POST)
        limiteInferiorY = LimiteInferiorYForm(request.POST)
        limiteSuperiorY = LimiteSuperiorYForm(request.POST)
        probabilidadInferiorX = ProbabilidadInferiorXForm(request.POST)
        probabilidadSuperiorX = ProbabilidadSuperiorXForm(request.POST)
        probabilidadInferiorY = ProbabilidadInferiorYForm(request.POST)
        probabilidadSuperiorY = ProbabilidadSuperiorYForm(request.POST)

        errorMessage = "Porfavor revisar los limites de integración, " \
                       "recuerda que el limite inferior debe ser menor al limite superior de la variable."

        try:

            x = symbols('x')
            y = symbols('y')

            valorEcuacion = ecuacion['ecuacion'].value()
            valorLimiteInferiorX = sympify(limiteInferiorX['limiteInferiorX'].value())
            valorLimiteSuperiorX = sympify(limiteSuperiorX['limiteSuperiorX'].value())
            valorLimiteInferiorY = sympify(limiteInferiorY['limiteInferiorY'].value())
            valorLimiteSuperiorY = sympify(limiteSuperiorY['limiteSuperiorY'].value())
            valorProbabilidadInferiorX = sympify(probabilidadInferiorX['probabilidadInferiorX'].value())
            valorProbabilidadSuperiorX = sympify(probabilidadSuperiorX['probabilidadSuperiorX'].value())
            valorProbabilidadInferiorY = sympify(probabilidadInferiorY['probabilidadInferiorY'].value())
            valorProbabilidadSuperiorY = sympify(probabilidadSuperiorY['probabilidadSuperiorY'].value())

            # Funcion ingresada
            integralEcuacion = latex(Integral(valorEcuacion, (x, valorLimiteInferiorX, valorLimiteSuperiorX),
                                              (y, valorLimiteInferiorY, valorLimiteSuperiorY)))

            valorIntegral = integrate(valorEcuacion, (x, valorLimiteInferiorX, valorLimiteSuperiorX),
                                      (y, valorLimiteInferiorY, valorLimiteSuperiorY))

            stringIntegral = integralEcuacion + "=" + latex(valorIntegral)

            if (N(valorLimiteInferiorX, 3) <= N(valorLimiteSuperiorX, 3) and
                    (N(valorLimiteInferiorY, 3) <= N(valorLimiteSuperiorY, 3))):

                # print(valorIntegral)
                # print(stringIntegral)
                # print(N(valorIntegral, 2))

                # Evaluacion de una funcion de probabilidad

                errorMessage = "La función ingresada no es una distribución de probabilidad!"

                if (N(valorIntegral, 2) > 0.99 and N(valorIntegral, 4) < 1.01):
                    errorMessage = "Error! Porfavor revise los intervalos para calcular la probabilidad. " \
                                   "Recuerde que deben estar entre los intervalos de la distribución de probabilidad."
                    print("OK 1")

                    print("Pi: " + latex(N(valorProbabilidadSuperiorX, 5)))

                    if (N(valorProbabilidadInferiorX, 3) >= N(valorLimiteInferiorX, 3) and
                            N(valorProbabilidadInferiorX, 3) <= N(valorProbabilidadSuperiorX, 3) and
                            N(valorProbabilidadSuperiorX, 3) <= N(valorLimiteSuperiorX, 3) and
                            N(valorProbabilidadSuperiorX, 3) >= N(valorProbabilidadInferiorX, 3) and
                            N(valorProbabilidadInferiorY, 3) >= N(valorLimiteInferiorY, 3) and
                            N(valorProbabilidadInferiorY, 3) <= N(valorProbabilidadSuperiorY, 3) and
                            N(valorProbabilidadSuperiorY, 3) <= N(valorLimiteSuperiorY, 2) and
                            N(valorProbabilidadSuperiorY, 3) >= N(valorProbabilidadInferiorY, 2)):
                        probabilidadEcuacion = latex(Integral(valorEcuacion,
                                                              (x, valorProbabilidadInferiorX,
                                                               valorProbabilidadSuperiorX),
                                                              (y, valorProbabilidadInferiorY,
                                                               valorProbabilidadSuperiorY)))

                        valorProbabilidad = integrate(valorEcuacion,
                                                      (x, valorProbabilidadInferiorX, valorProbabilidadSuperiorX),
                                                      (y, valorProbabilidadInferiorY, valorProbabilidadSuperiorY))

                        print("Valor Probabilidad:" + latex(N(valorProbabilidad.evalf(), 3)))

                        stringProbabilidadCompleta = probabilidadEcuacion + "=" + latex(
                            valorProbabilidad) + "=" + latex(
                            N(valorProbabilidad.evalf(), 3))

                        stringProbabilidad = "P(" + latex(valorProbabilidadInferiorX) + " < X < " \
                                             + latex(valorProbabilidadSuperiorX) + ", " \
                                             + latex(valorProbabilidadInferiorY) + " < Y < " \
                                             + latex(valorProbabilidadSuperiorY) + ")"

                        return render(request, self.postTemplate, {'ecuacion': ecuacion,
                                                                   'limiteInferiorX': limiteInferiorX,
                                                                   'limiteSuperiorX': limiteSuperiorX,
                                                                   'limiteInferiorY': limiteInferiorY,
                                                                   'limiteSuperiorY': limiteSuperiorY,
                                                                   'probabilidadInferiorX': probabilidadInferiorX,
                                                                   'probabilidadSuperiorX': probabilidadSuperiorX,
                                                                   'probabilidadInferiorY': probabilidadInferiorY,
                                                                   'probabilidadSuperiorY': probabilidadSuperiorY,
                                                                   'stringIntegral': integralEcuacion,
                                                                   'stringValorIntegral': valorIntegral,
                                                                   'stringIntegralCompleta': stringIntegral,
                                                                   'stringProbabilidadCompleta': stringProbabilidadCompleta,
                                                                   'stringProbabilidad': stringProbabilidad})

            return render(request, self.errorTemplate, {'ecuacion': ecuacion,
                                                        'limiteInferiorX': limiteInferiorX,
                                                        'limiteSuperiorX': limiteSuperiorX,
                                                        'limiteInferiorY': limiteInferiorY,
                                                        'limiteSuperiorY': limiteSuperiorY,
                                                        'probabilidadInferiorX': probabilidadInferiorX,
                                                        'probabilidadSuperiorX': probabilidadSuperiorX,
                                                        'probabilidadInferiorY': probabilidadInferiorY,
                                                        'probabilidadSuperiorY': probabilidadSuperiorY,
                                                        'stringIntegral': integralEcuacion,
                                                        'stringValorIntegral': valorIntegral,
                                                        'stringIntegralCompleta': stringIntegral,
                                                        'errorMessage': errorMessage})

        except:

            return render(request, self.errorTemplate, {'ecuacion': ecuacion,
                                                        'limiteInferiorX': limiteInferiorX,
                                                        'limiteSuperiorX': limiteSuperiorX,
                                                        'limiteInferiorY': limiteInferiorY,
                                                        'limiteSuperiorY': limiteSuperiorY,
                                                        'probabilidadInferiorX': probabilidadInferiorX,
                                                        'probabilidadSuperiorX': probabilidadSuperiorX,
                                                        'probabilidadInferiorY': probabilidadInferiorY,
                                                        'probabilidadSuperiorY': probabilidadSuperiorY,
                                                        'errorMessage': "Error! Existe un error en los datos ingresados, porfavor revisar las instrucciones"})


class ProbabilidadContinuaView(TemplateView):
    getTemplate = 'probabilidad.continua.get.html'
    postTemplate = 'probabilidad.continua.post.html'
    errorTemplate = 'probabilidad.continua.error.html'

    def get(self, request):

        ecuacion = EcuacionSimpleForm()
        limiteInferior = LimiteInferiorForm()
        limiteSuperior = LimiteSuperiorForm()
        probabilidadInferior = ProbabilidadInferiorForm()
        probabilidadSuperior = ProbabilidadSuperiorForm()

        return render(request, self.getTemplate, {'ecuacion': ecuacion,
                                                  'limiteInferiorX': limiteInferior,
                                                  'limiteSuperiorX': limiteSuperior,
                                                  'probabilidadInferior': probabilidadInferior,
                                                  'probabilidadSuperior': probabilidadSuperior})

    def post(self, request):

        ecuacion = EcuacionSimpleForm(request.POST)
        limiteInferior = LimiteInferiorForm(request.POST)
        limiteSuperior = LimiteSuperiorForm(request.POST)
        probabilidadInferior = ProbabilidadInferiorForm(request.POST)
        probabilidadSuperior = ProbabilidadSuperiorForm(request.POST)

        errorMessage = "Porfavor revisar los limites de integración, " \
                       "recuerda que el limite inferior debe ser menor al limite superior de la variable."

        try:

            x = symbols('x')
            y = symbols('y')

            valorEcuacion = ecuacion['ecuacion'].value()
            valorLimiteInferior = sympify(limiteInferior['limiteInferior'].value())
            valorLimiteSuperior = sympify(limiteSuperior['limiteSuperior'].value())
            valorProbabilidadSuperior = sympify(probabilidadSuperior['probabilidadSuperior'].value())
            valorProbabilidadInferior = sympify(probabilidadInferior['probabilidadInferior'].value())

            # Funcion ingresada
            integralEcuacion = latex(Integral(valorEcuacion, (x, valorLimiteInferior, valorLimiteSuperior)))

            valorIntegral = integrate(valorEcuacion, (x, valorLimiteInferior, valorLimiteSuperior))

            stringIntegral = integralEcuacion + "=" + latex(valorIntegral)

            if (N(valorLimiteInferior, 3) <= N(valorLimiteSuperior, 3)):

                errorMessage = "La función ingresada no es una distribución de probabilidad!"

                if (N(valorIntegral, 2) > 0.99 and N(valorIntegral, 4) < 1.01):
                    errorMessage = "Error! Porfavor revise los intervalos para calcular la probabilidad. " \
                                   "Recuerde que deben estar entre los intervalos de la distribución de probabilidad."

                    print("OK 1")

                    if (N(valorProbabilidadInferior, 3) >= N(valorLimiteInferior, 3) and
                            N(valorProbabilidadInferior, 3) <= N(valorProbabilidadSuperior, 3) and
                            N(valorProbabilidadSuperior, 3) <= N(valorLimiteSuperior, 3) and
                            N(valorProbabilidadSuperior, 3) >= N(valorProbabilidadInferior, 3)):
                        probabilidadEcuacion = latex(Integral(valorEcuacion,
                                                              (x, valorProbabilidadInferior,
                                                               valorProbabilidadSuperior), ))

                        valorProbabilidad = integrate(valorEcuacion,
                                                      (x, valorProbabilidadInferior, valorProbabilidadSuperior))

                        print("Valor Probabilidad:" + latex(N(valorProbabilidad.evalf(), 3)))

                        stringProbabilidadCompleta = probabilidadEcuacion + "=" + latex(
                            valorProbabilidad) + "=" + latex(N(valorProbabilidad.evalf(), 3))

                        stringProbabilidad = "P(" + latex(valorProbabilidadInferior) + " < X < " \
                                             + latex(valorProbabilidadSuperior) + ")"

                        return render(request, self.postTemplate, {'ecuacion': ecuacion,
                                                                   'limiteInferior': limiteInferior,
                                                                   'limiteSuperior': limiteSuperior,
                                                                   'probabilidadInferior': probabilidadInferior,
                                                                   'probabilidadSuperior': probabilidadSuperior,
                                                                   'stringIntegral': integralEcuacion,
                                                                   'stringValorIntegral': valorIntegral,
                                                                   'stringIntegralCompleta': stringIntegral,
                                                                   'stringProbabilidadCompleta': stringProbabilidadCompleta,
                                                                   'stringProbabilidad': stringProbabilidad})

            return render(request, self.errorTemplate, {'ecuacion': ecuacion,
                                                        'limiteInferior': limiteInferior,
                                                        'limiteSuperior': limiteSuperior,
                                                        'probabilidadInferior': probabilidadInferior,
                                                        'probabilidadSuperior': probabilidadSuperior,
                                                        'stringIntegralCompleta': stringIntegral,
                                                        'errorMessage': errorMessage})

        except:

            return render(request, self.errorTemplate, {'ecuacion': ecuacion,
                                                        'limiteInferior': limiteInferior,
                                                        'limiteSuperior': limiteSuperior,
                                                        'probabilidadInferior': probabilidadInferior,
                                                        'probabilidadSuperior': probabilidadSuperior,
                                                        'stringIntegralCompleta': stringIntegral,
                                                        'errorMessage': "Error! Existe un error en los datos ingresados, porfavor revisar las instrucciones"})


class AcomulativaContinuaView(TemplateView):
    getTemplate = 'funcion.acumulativa.get.html'
    postTemplate = 'funcion.acumulativa.post.html'
    errorTemplate = 'funcion.acumulativa.error.html'

    def get(self, request):

        ecuacion = EcuacionSimpleForm()
        limiteInferior = LimiteInferiorForm()
        limiteSuperior = LimiteSuperiorForm()
        probabilidadInferior = ProbabilidadInferiorForm()

        return render(request, self.getTemplate, {'ecuacion': ecuacion,
                                                  'limiteInferiorX': limiteInferior,
                                                  'limiteSuperiorX': limiteSuperior,
                                                  'probabilidadInferior': probabilidadInferior})

    def post(self, request):

        ecuacion = EcuacionSimpleForm(request.POST)
        limiteInferior = LimiteInferiorForm(request.POST)
        limiteSuperior = LimiteSuperiorForm(request.POST)
        probabilidadInferior = ProbabilidadInferiorForm(request.POST)

        errorMessage = "Porfavor revisar los limites de integración, " \
                       "recuerda que el limite inferior debe ser menor al limite superior de la variable."

        try:

            x = symbols('x')
            y = symbols('y')

            valorEcuacion = ecuacion['ecuacion'].value()
            valorLimiteInferior = sympify(limiteInferior['limiteInferior'].value())
            valorLimiteSuperior = sympify(limiteSuperior['limiteSuperior'].value())
            valorProbabilidadInferior = sympify(probabilidadInferior['probabilidadInferior'].value())

            # Funcion ingresada
            integralEcuacion = latex(Integral(valorEcuacion, (x, valorLimiteInferior, valorLimiteSuperior)))

            valorIntegral = integrate(valorEcuacion, (x, valorLimiteInferior, valorLimiteSuperior))

            stringIntegral = integralEcuacion + "=" + latex(valorIntegral)

            if (N(valorLimiteInferior, 3) <= N(valorLimiteSuperior, 3)):

                errorMessage = "La función ingresada no es una distribución de probabilidad!"

                if (N(valorIntegral, 2) > 0.99 and N(valorIntegral, 4) < 1.01):
                    errorMessage = "Error! Porfavor revise los intervalos para calcular la probabilidad. " \
                                   "Recuerde que deben estar entre los intervalos de la distribución de probabilidad."

                    print("OK 1")

                    if (N(valorProbabilidadInferior, 3) >= N(valorLimiteInferior, 3) and
                            N(valorProbabilidadInferior, 3) <= N(valorLimiteSuperior, 3)):
                        probabilidadEcuacion = latex(Integral(valorEcuacion,
                                                              (x, valorLimiteInferior,
                                                               valorProbabilidadInferior), ))

                        valorProbabilidad = integrate(valorEcuacion,
                                                      (x, valorLimiteInferior, valorProbabilidadInferior))

                        print("Valor Probabilidad:" + latex(N(valorProbabilidad.evalf(), 3)))

                        stringProbabilidadCompleta = probabilidadEcuacion + "=" + latex(
                            valorProbabilidad) + "=" + latex(N(valorProbabilidad.evalf(), 3))

                        stringProbabilidad = "P( X <=" + latex(valorProbabilidadInferior) + ")"

                        return render(request, self.postTemplate, {'ecuacion': ecuacion,
                                                                   'limiteInferior': limiteInferior,
                                                                   'limiteSuperior': limiteSuperior,
                                                                   'probabilidadInferior': probabilidadInferior,
                                                                   'stringIntegral': integralEcuacion,
                                                                   'stringValorIntegral': valorIntegral,
                                                                   'stringIntegralCompleta': stringIntegral,
                                                                   'stringProbabilidadCompleta': stringProbabilidadCompleta,
                                                                   'stringProbabilidad': stringProbabilidad})

            return render(request, self.errorTemplate, {'ecuacion': ecuacion,
                                                        'limiteInferior': limiteInferior,
                                                        'limiteSuperior': limiteSuperior,
                                                        'probabilidadInferior': probabilidadInferior,
                                                        'stringIntegralCompleta': stringIntegral,
                                                        'errorMessage': errorMessage})

        except:

            return render(request, self.errorTemplate, {'ecuacion': ecuacion,
                                                        'limiteInferior': limiteInferior,
                                                        'limiteSuperior': limiteSuperior,
                                                        'probabilidadInferior': probabilidadInferior,
                                                        'stringIntegralCompleta': stringIntegral,
                                                        'errorMessage': "Error! Existe un error en los datos ingresados, porfavor revisar las instrucciones"})


class EsperadoContinuaView(TemplateView):
    getTemplate = 'esperado.get.html'
    postTemplate = 'esperado.post.html'
    errorTemplate = 'esperado.error.html'

    def get(self, request):

        ecuacion = EcuacionSimpleForm()
        limiteInferior = LimiteInferiorForm()
        limiteSuperior = LimiteSuperiorForm()

        return render(request, self.getTemplate, {'ecuacion': ecuacion,
                                                  'limiteInferiorX': limiteInferior,
                                                  'limiteSuperiorX': limiteSuperior})

    def post(self, request):

        ecuacion = EcuacionSimpleForm(request.POST)
        limiteInferior = LimiteInferiorForm(request.POST)
        limiteSuperior = LimiteSuperiorForm(request.POST)

        errorMessage = "Porfavor revisar los limites de integración, " \
                       "recuerda que el limite inferior debe ser menor al limite superior de la variable."

        try:

            x = symbols('x')
            y = symbols('y')

            valorEcuacion = ecuacion['ecuacion'].value()
            valorLimiteInferior = sympify(limiteInferior['limiteInferior'].value())
            valorLimiteSuperior = sympify(limiteSuperior['limiteSuperior'].value())

            # Funcion ingresada
            integralEcuacion = latex(Integral(valorEcuacion, (x, valorLimiteInferior, valorLimiteSuperior)))

            valorIntegral = integrate(valorEcuacion, (x, valorLimiteInferior, valorLimiteSuperior))

            stringIntegral = integralEcuacion + "=" + latex(valorIntegral)

            if (N(valorLimiteInferior, 3) <= N(valorLimiteSuperior, 3)):

                errorMessage = "La función ingresada no es una distribución de probabilidad!"

                if (N(valorIntegral, 2) > 0.99 and N(valorIntegral, 4) < 1.01):
                    errorMessage = "Error! Porfavor revise los intervalos para calcular la probabilidad. " \
                                   "Recuerde que deben estar entre los intervalos de la distribución de probabilidad."

                    print("OK 1")

                    probabilidadEcuacion = latex(Integral("x * " + valorEcuacion,
                                                          (x, valorLimiteInferior, valorLimiteSuperior)))
                    print(probabilidadEcuacion)

                    valorProbabilidad = integrate("x * " + valorEcuacion,
                                                  (x, valorLimiteInferior, valorLimiteSuperior))

                    print("Valor Probabilidad:" + latex(N(valorProbabilidad.evalf(), 3)))

                    stringProbabilidadCompleta = probabilidadEcuacion + "=" + latex(
                        valorProbabilidad) + "=" + latex(N(valorProbabilidad.evalf(), 3))

                    return render(request, self.postTemplate, {'ecuacion': ecuacion,
                                                               'limiteInferior': limiteInferior,
                                                               'limiteSuperior': limiteSuperior,
                                                               'stringIntegral': integralEcuacion,
                                                               'stringValorIntegral': valorIntegral,
                                                               'stringIntegralCompleta': stringIntegral,
                                                               'stringProbabilidadCompleta': stringProbabilidadCompleta})

            return render(request, self.errorTemplate, {'ecuacion': ecuacion,
                                                        'limiteInferior': limiteInferior,
                                                        'limiteSuperior': limiteSuperior,
                                                        'stringIntegralCompleta': stringIntegral,
                                                        'errorMessage': errorMessage})

        except:

            return render(request, self.errorTemplate, {'ecuacion': ecuacion,
                                                        'limiteInferior': limiteInferior,
                                                        'limiteSuperior': limiteSuperior,
                                                        'stringIntegralCompleta': stringIntegral,
                                                        'errorMessage': "Error! Existe un error en los datos ingresados, porfavor revisar las instrucciones"})


class VarianzaContinuaView(TemplateView):
    getTemplate = 'varianza.get.html'
    postTemplate = 'varianza.post.html'
    errorTemplate = 'varianza.error.html'

    def get(self, request):

        ecuacion = EcuacionSimpleForm()
        limiteInferior = LimiteInferiorForm()
        limiteSuperior = LimiteSuperiorForm()

        return render(request, self.getTemplate, {'ecuacion': ecuacion,
                                                  'limiteInferiorX': limiteInferior,
                                                  'limiteSuperiorX': limiteSuperior, })

    def post(self, request):

        ecuacion = EcuacionSimpleForm(request.POST)
        limiteInferior = LimiteInferiorForm(request.POST)
        limiteSuperior = LimiteSuperiorForm(request.POST)

        errorMessage = "Porfavor revisar los limites de integración, " \
                       "recuerda que el limite inferior debe ser menor al limite superior de la variable."

        try:

            x = symbols('x')
            y = symbols('y')

            valorEcuacion = ecuacion['ecuacion'].value()
            valorLimiteInferior = sympify(limiteInferior['limiteInferior'].value())
            valorLimiteSuperior = sympify(limiteSuperior['limiteSuperior'].value())

            # Funcion ingresada
            integralEcuacion = latex(Integral(valorEcuacion, (x, valorLimiteInferior, valorLimiteSuperior)))

            valorIntegral = integrate(valorEcuacion, (x, valorLimiteInferior, valorLimiteSuperior))

            stringIntegral = integralEcuacion + "=" + latex(valorIntegral)

            if (N(valorLimiteInferior, 3) <= N(valorLimiteSuperior, 3)):

                errorMessage = "La función ingresada no es una distribución de probabilidad!"

                if (N(valorIntegral, 2) > 0.99 and N(valorIntegral, 4) < 1.01):
                    errorMessage = "Error! Porfavor revise los intervalos para calcular la probabilidad. " \
                                   "Recuerde que deben estar entre los intervalos de la distribución de probabilidad."

                    valorEsperadoX = integrate("x * " + valorEcuacion,
                                                  (x, valorLimiteInferior, valorLimiteSuperior))

                    print(latex(valorEsperadoX))

                    valorEsperadoX2 = integrate("x**2 * " + valorEcuacion,
                                                  (x, valorLimiteInferior, valorLimiteSuperior))

                    print(latex(valorEsperadoX2))

                    print("OK 1")

                    stringProbabilidadCompleta = r"{\delta}^{2} = E(X^2) - " + r"{\mu}^{2} =" + latex(valorEsperadoX2) \
                                                 + " - " + r"{\left(" + latex(valorEsperadoX) + r"\right)}^{2}" +  \
                                                 "=" + latex(N(valorEsperadoX2.evalf(), 5) - pow(N(valorEsperadoX.evalf(), 5), 2))

                    return render(request, self.postTemplate, {'ecuacion': ecuacion,
                                                               'limiteInferior': limiteInferior,
                                                               'limiteSuperior': limiteSuperior,
                                                               'stringIntegral': integralEcuacion,
                                                               'stringValorIntegral': valorIntegral,
                                                               'stringIntegralCompleta': stringIntegral,
                                                               'stringProbabilidadCompleta': stringProbabilidadCompleta})

            return render(request, self.errorTemplate, {'ecuacion': ecuacion,
                                                        'limiteInferior': limiteInferior,
                                                        'limiteSuperior': limiteSuperior,
                                                        'stringIntegralCompleta': stringIntegral,
                                                        'errorMessage': errorMessage})

        except:

            return render(request, self.errorTemplate, {'ecuacion': ecuacion,
                                                        'limiteInferior': limiteInferior,
                                                        'limiteSuperior': limiteSuperior,
                                                        'stringIntegralCompleta': stringIntegral,
                                                        'errorMessage': "Error! Existe un error en los datos ingresados, porfavor revisar las instrucciones"})
