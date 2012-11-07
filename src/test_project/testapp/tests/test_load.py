# -*- coding: utf-8 -*-

from unittest import TestCase
from template_preprocessor.core import compile
from template_preprocessor.core.context import Context

class TestTemplateLoad(TestCase):

	def test_load_url_from_future(self):
		compiled, context = compile('{% load url from future %}')
		compiled = compiled.strip()
		self.assertEqual(compiled, '{% load url from future%}')
