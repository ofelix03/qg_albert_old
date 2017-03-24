import xmlrpclib

METHOD_READ = 'read'
METHOD_SEARCH_READ = 'search_read'
METHOD_CREATE = 'create'
METHOD_WRITE = 'write'
METHOD_SEARCH = 'search'

class OdooAdapter:

    ADMIN_ID = 1
    def setUsername(self, username):
        if username:
            self.username = username

        return self

    def getUsername(self):
        return self.username

    def setPassword(self, password):
        if password:
            self.password = password

        return self

    def getPassword(self):
        return self.password

    def setDatabase(self, database):
        if database:
            self.database = database

        return self

    def getDatabase(self):
        return self.database

    def setUrl(self, url):
        if url:
            self.url = url.rstrip("/")

        return self

    def getUrl(self):
        return self.url

    def setModel(self, model):
        self.model = model

        return self

    def getModel(self):
        return self.model

    def setUserId(self, userId):
        self.userId = userId

        return self

    def getUserId(self):
        return self.userId


    def setServerConfig(self, config):
        if 'database' in config:
            self.setDatabase(config['database'])

        if 'username' in config:
            self.setUsername(config['username'])

        if 'password' in config:
            self.setPassword(config['password'])

        if 'url' in config:
            self.setUrl(config['url'])

        return self


    def getCommonPostfixUrl(self):
        return "{}/xmlrpc/2/common"

    def getObjectPostfixUrl(self):
        return "{}/xmlrpc/2/object"


    def setUpCommon(self):
        if hasattr(self, "url") and not self.url:
            raise Exception("You need to set a URL to  your odoo server instance, using self::setServerUrl()")

        self.common = xmlrpclib.ServerProxy(self.getCommonPostfixUrl().format(self.url))


    def getCommon(self):
        if not hasattr(self, 'common'):
            self.setUpCommon()

        return self.common

    def getVersion(self):
         if not hasattr(self, 'common'):
            self.setUpCommon()

         return self.getCommon().version()

    def setUpModels(self):
        if hasattr(self, 'url') and not self.url:
            raise Exception("You  need to set a URL to your odoo server instance, using self::setServerUrl()")

        self.models = xmlrpclib.ServerProxy(self.getObjectPostfixUrl().format(self.getUrl()))
        return self.models

    def getModels(self):
        if not hasattr(self, 'models'):
            self.setUpModels()

        return self.models


    def authenticate(self, username = None, password = None, database = None):
        if username:
            self.setUsername(username)

        if password:
            self.setPassword(password)

        if database:
            self.setDatabase(database)

        uid = self.getCommon().authenticate(self.getDatabase(), self.getUsername(), self.getPassword(), {})
        if uid:
            self.setUserId(uid)
            return self

        raise Exception("Authentication failed. Check your login details and try again")


    def getRecords(self):
        return self.getModels().execute_kw(self.getDatabase(), self.getUserId(), self.getPassword(),
                          self.getModel(), 'check_access_rights',
                          ['read'], {'raise_exception': False})

    def getRecordsWithIds(self, ids, fields=None):
        if not fields:
            fields = []

        if not isinstance(ids, list):
           ids = [ids]

        return self.getModels().execute_kw(self.getDatabase(), self.getUserId(), self.getPassword(), self.getModel(), METHOD_READ, [ids], {'fields': fields})

    def searchForRecordIdsWhere(self, filter=None, limit=None):
        optionalArgs = {}

        if not filter:
            filter = []

        if limit:
            optionalArgs['limit'] = limit

        return self.getModels().execute_kw(self.getDatabase(), self.getUserId(), self.getPassword(), self.getModel(), METHOD_SEARCH, [filter], optionalArgs)


    def recordsExistsForFilter(self, filter=None):
         ids = self.searchForRecordIdsWhere(filter)

         if len(ids) > 0:
             return False

         return True

    def getRecordsWhere(self, filter=None, fields=None, limit=None):
        # Returns an array of the record found

        if not filter:
            filter = []

        optionalArgs = {}
        if not fields:
            optionalArgs['fields'] = []
        else:
            optionalArgs['fields'] = fields


        if limit:
            optionalArgs['limit'] = limit


        return self.getModels().execute_kw(self.getDatabase(), self.getUserId(), self.getPassword(), self.getModel(), METHOD_SEARCH_READ, [filter], optionalArgs)

    def createRecord(self, record=None):
        # Returns the PRIMARY KEY of the newly created record

        if not record:
            raise Exception("You have no record to save. Give us some record to create for you!")

        return self.getModels().execute_kw(self.getDatabase(), self.getUserId(), self.getPassword(), self.getModel(), METHOD_CREATE, [record])


    def updateRecord(self, ids=None, record=None):

        if not record:
            return False

        if not isinstance(ids, list):
            ids = [ids]


        result = self.getModels().execute_kw(self.getDatabase(), self.getUserId(), self.getPassword(), self.getModel(), METHOD_WRITE, [ids, record])
       
        return result