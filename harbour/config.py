# encoding: utf-8
ADS_CLASSIC_URL = 'http://{mirror}'
ADS_CLASSIC_LIBRARIES_URL = 'http://{mirror}/cookie={cookie}'
ADS_CLASSIC_MIRROR_LIST = [
    'adstrio.cfa.harvard.edu',
    'adsnun.cfa.harvard.edu',
    'adsate.cfa.harvard.edu',
    'astrobib.u-strasbg.fr',
    'ads.nao.ac.jp',
    'ads.astro.puc.cl',
    'esoads.eso.org',
    'ukads.nottingham.ac.uk',
    'ads.iucaa.ernet.in',
    'ads.inasan.ru',
    'ads.bao.ac.cn',
    'ads.mao.kiev.ua',
    'ads.ari.uni-heidelberg.de',
    'ads.arsip.lipi.go.id',
    'ads.on.br',
    'saaoads.chpc.ac.za',
    'adsabs.harvard.edu'
]
ADS_TWO_POINT_OH_S3_MONGO_BUCKET = 'adsabs-mongogut'
ADS_TWO_POINT_OH_LOADED_USERS = False
ADS_TWO_POINT_OH_USERS = {}
ADS_TWO_POINT_OH_MIRROR = 'adsabs.harvard.edu'

SQLALCHEMY_BINDS = {'harbour': ''}

HARBOUR_SERVICE_ADSWS_API_TOKEN = ''
HARBOUR_EXPORT_SERVICE_URL = 'http://fakeapi.adsabs.harvard.edu/v1/export'
HARBOUR_EXPORT_TYPES = ['zotero']

HARBOUR_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(levelname)s\t%(process)d '
                      '[%(asctime)s]:\t%(message)s',
            'datefmt': '%m/%d/%Y %H:%M:%S',
        }
    },
    'handlers': {
        'console': {
            'formatter': 'default',
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

