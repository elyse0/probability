from django import forms
from django.forms.widgets import NumberInput


class EcuacionForm (forms.Form):

    ecuacion = forms.CharField(label='Función f(x,y)')

class EcuacionSimpleForm (forms.Form):

    ecuacion = forms.CharField(label='Función f(x)')

class LimiteSuperiorXForm (forms.Form):

    limiteSuperiorX = forms.CharField(label='Limite superior de x')

class LimiteInferiorXForm (forms.Form):

    limiteInferiorX = forms.CharField(label='Limite inferior de x')

class LimiteSuperiorYForm (forms.Form):

    limiteSuperiorY = forms.CharField(label='Limite superior de y')

class LimiteInferiorYForm (forms.Form):

    limiteInferiorY = forms.CharField(label='Limite inferior de y')

class ProbabilidadInferiorXForm(forms.Form):

    probabilidadInferiorX = forms.CharField(label='a')

class ProbabilidadSuperiorXForm(forms.Form):

    probabilidadSuperiorX = forms.CharField(label='b')

class ProbabilidadInferiorYForm(forms.Form):
    probabilidadInferiorY = forms.CharField(label='c')


class ProbabilidadSuperiorYForm(forms.Form):
    probabilidadSuperiorY = forms.CharField(label='d')

class LimiteSuperiorForm (forms.Form):

    limiteSuperior = forms.CharField(label='Limite superior:')

class LimiteInferiorForm (forms.Form):

    limiteInferior = forms.CharField(label='Limite inferior:')

class ProbabilidadInferiorForm(forms.Form):

    probabilidadInferior = forms.CharField(label='a')

class ProbabilidadSuperiorForm(forms.Form):

    probabilidadSuperior = forms.CharField(label='b')

class IntegracionForm (forms.Form):

    tipoIntegracion = forms.ChoiceField(label='Integrar respecto a', choices=[('dx', 'dx'), ('dy', 'dy')])