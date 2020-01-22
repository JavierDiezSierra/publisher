import os
import netCDF4
import numpy as np
import sys

def get_adapter(project):
	p = project.lower()

	if p == 'cmip6':
		return Cmip6Adapter()
	elif p == 'cmip5':
		return Cmip5Adapter()
	elif p == 'cordex':
		return CordexAdapter()
	elif p == 'cordex_providers':
		return CordexProvidersAdapter()
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
		return self.facets[:10]

	def get_fx_dict(self, d):
		d.pop('frequency')
		return d

class CordexProvidersAdapter(object):

	fx = ['areacella', 'areacellr', 'orog', 'sftlf', 'sftgif', 'mrsofc', 'rootd', 'zfull']
	variable_options = ['aclwdnt', 'alb', 'areacella', 'clfr1000', 'clfr200', 'clfr300', 'clfr400', 'clfr500', 'clfr600', 'clfr700', 'clfr850', 'clfr875',\
						'clfr900', 'clfr925', 'clfr950', 'clfr975', 'clh', 'clice1000', 'clice200', 'clice300', 'clice400', 'clice500', 'clice600',\
						'clice700', 'clice850','clice875', 'clice900', 'clice925', 'clice950', 'clice975', 'clivi', 'cll', 'clm', 'clt', 'clwmr1000',
						'clwmr200', 'clwmr300', 'clwmr400', 'clwmr500','clwmr600', 'clwmr700', 'clwmr850', 'clwmr875', 'clwmr900', 'clwmr925', 'clwmr950',\
						'clwmr975', 'clwvi', 'evspsbl', 'evspsblpot', 'hfls', 'hfss', 'hufs', 'hur1000', 'hur200', 'hur300', 'hur400', 'hur500', 'hur600',\
						'hur700', 'hur850', 'hur875', 'hur900', 'hur925', 'hur950', 'hur975', 'hurs','hus1000', 'hus200', 'hus300', 'hus400', 'hus500',\
						'hus600', 'hus700', 'hus850', 'hus875', 'hus900', 'hus925', 'hus950', 'hus975', 'huss', 'mrfso','mross', 'mrro', 'mrros', 'mrso',\
						'mrsofc', 'mrsos', 'mrsosat', 'mrsosd', 'mrsowp', 'orog', 'pr', 'prc', 'prhmax', 'prls', 'prsn', 'prw', 'ps', 'psl','rlds', 'rlus',\
						'rlut', 'rootd', 'rsds', 'rsdt', 'rsus', 'rsut', 'sfcWind', 'sfcWindmax', 'sfcWindmaxmax', 'sftgif', 'sftlf', 'sic', 'slev', 'slw',\
						'snc', 'snd', 'snm', 'snownc', 'snw', 'sst', 'sund', 'ta1000', 'ta200', 'ta300', 'ta400', 'ta500', 'ta600', 'ta700', 'ta850', 'ta875',\
						'ta900', 'ta925','ta950', 'ta975', 'tas', 'tasmax', 'tasmaxts', 'tasmin', 'tasmints', 'tauu', 'tauv', 'ts', 'tsmax', 'tsmin', 'tsos',\
						'u200', 'u500', 'u850', 'ua1000','ua200', 'ua300', 'ua400', 'ua500', 'ua600', 'ua700', 'ua850', 'ua875', 'ua900', 'ua925', 'ua950',\
						'ua975', 'uas', 'ustar', 'v200', 'v500', 'v850','va1000', 'va200', 'va300', 'va400', 'va500', 'va600', 'va700', 'va850', 'va875',\
						'va900', 'va925', 'va950', 'va975', 'vas', 'wsgsmax', 'zg1000','zg200', 'zg300', 'zg350', 'zg400', 'zg450', 'zg500', 'zg550', 'zg600',\
						'zg650', 'zg700', 'zg750', 'zg800', 'zg850', 'zg875', 'zg900', 'zg925','zg950', 'zg975', 'zmla']
	drs = 'activity/product/domain/institution/gcmmodelname/cmip5experimentname/cmip5ensemblemenber/rcmmodelname/rcmversionid/frequency/variable/version'

	def __init__(self, template='cordex.ncml.j2'):
		self.template = template
		self.facets = CordexProvidersAdapter.drs.split('/')
		self.variable_options = CordexProvidersAdapter.variable_options

	def drs_to_var(self, drs):
		root_grp = netCDF4.Dataset(drs)
		nc_variables = [var for var in root_grp.variables]
		variable = np.intersect1d(self.variable_options, nc_variables)[0]
		root_grp.close()
		return variable

	def drs_to_rcmversionid(self, drs):
		root_grp = netCDF4.Dataset(drs)
		rcmversionid = root_grp.rcm_version_id
		root_grp.close()
		return rcmversionid

	def drs_to_version(self, drs):
		version = 'v20200101'
		return version

	def drs_to_ncml(self, drs):
		root_grp = netCDF4.Dataset(drs)
		version = 'v20200101'
		ncml = '_'.join(['cordex', 'output', root_grp.CORDEX_domain, root_grp.institute_id, root_grp.driving_model_id,\
						 root_grp.experiment_id, root_grp.driving_model_ensemble_member, root_grp.model_id,\
						 root_grp.rcm_version_id, root_grp.frequency])
		root_grp.close()
		return ncml

	def ncml_facets(self, drs):
		root_grp = netCDF4.Dataset(drs)
		nc_variables = [var for var in root_grp.variables]
		variable = np.intersect1d(self.variable_options, nc_variables)[0]
		version = 'v20200101'
		ncml = '/'.join(['cordex', 'output', root_grp.CORDEX_domain, root_grp.institute_id, root_grp.driving_model_id,\
						 root_grp.experiment_id, root_grp.driving_model_ensemble_member, root_grp.model_id,\
						 root_grp.rcm_version_id, root_grp.frequency, variable, version])
		root_grp.close()
		return ncml

	def ncml_facets2(self):
		return self.facets[:10]

	def get_fx_dict(self, d):
		d.pop('frequency')
		return d