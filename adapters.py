import os

def get_adapter(project):
	p = project.lower()

	if p == 'cmip6':
		return Cmip6Adapter()
	elif p == 'cmip5':
		return Cmip5Adapter()
	elif p == 'cordex':
		return CordexAdapter()
	else:
		return None

class Cmip6Adapter(object):
	fx = ['areacella', 'areacellr', 'orog', 'sftlf', 'sftgif', 'mrsofc', 'rootd', 'zfull']
	drs = 'project/product/institution/model/experiment/ensemble/frequency/variable/grid/version'

	def __init__(self, template='cmip.ncml.j2'):
		self.template = template
		self.facets = Cmip6Adapter.drs.split('/')

	def drs_to_var(self, drs):
		facets = os.path.dirname(drs).split('/')
		return facets[7]

	def drs_to_version(self, drs):
		facets = os.path.dirname(drs).split('/')
		return facets[9][1:]

	def drs_to_ncml(self, drs):
		facets = os.path.dirname(drs).split('/')
		ncml = '_'.join(facets[:7] + facets[8:-1])
		return ncml

	def ncml_facets(self):
		return self.facets[:7] + self.facets[8:]

	def get_fx_dict(self, d):
		d.pop('frequency')
		return d

class Cmip5Adapter(object):
	fx = ['areacella', 'areacellr', 'orog', 'sftlf', 'sftgif', 'mrsofc', 'rootd', 'zfull']
	drs = 'project/product/institution/model/experiment/frequency/realm/table/ensemble/version/variable'

	def __init__(self, template='cmip.ncml.j2'):
		self.template = template
		self.facets = Cmip5Adapter.drs.split('/')

	def ncml_facets(self):
		return self.facets[:-1]

	def get_fx_dict(self, d):
		d.pop('frequency')
		d.pop('ensemble')
		return d

class CordexAdapter(object):
	fx = ['areacella', 'areacellr', 'orog', 'sftlf', 'sftgif', 'mrsofc', 'rootd', 'zfull']
	drs = 'activity/product/domain/institution/gcmmodelname/cmip5experimentname/cmip5ensemblemenber/rcmmodelname/rcmversionid/frequency/variable/version'

	def __init__(self, template='cordex.ncml.j2'):
		self.template = template
		self.facets = CordexAdapter.drs.split('/')

	def drs_to_var(self, drs):
		facets = os.path.dirname(drs).split('/')
		return facets[10]

	def drs_to_rcmversionid(self, drs):
		facets = os.path.dirname(drs).split('/')
		return facets[8]

	def drs_to_version(self, drs):
		facets = os.path.dirname(drs).split('/')
		return facets[11]

	def drs_to_ncml(self, drs):
		facets = os.path.dirname(drs).split('/')
		ncml = '_'.join(facets[:10])
		return ncml

	def ncml_facets(self):
		return self.facets[:11]

	def get_fx_dict(self, d):
		d.pop('frequency')
		return d
