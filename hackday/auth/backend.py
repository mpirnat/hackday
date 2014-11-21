# ----------------------------------------
#          ActiveDirectoryBackend
# ----------------------------------------
#
# Created new snippet:
#       http://www.djangosnippets.org/snippets/edit/1397/
# based on:
#       http://www.djangosnippets.org/snippets/501/
# similar snippet (ldaps:// - secured) is on:
#       http://www.djangosnippets.org/snippets/901/
#
# ---------- settings.py -------------------
#
#     # Active directory auth backend setup
#     # on win32 check env.vars:
#     #   USERDNSDOMAIN=EXAMPLE.COM
#     #   USERDOMAIN=EXAMPLE
#     AD_DNS_NAME = 'domaindnsname.local'
#     AD_NT4_DOMAIN = 'DOMAINNAME' # This is the NT4/Samba domain name
#     AD_SEARCH_DN = 'dc=domaindnsname,dc=local'
#     AD_LDAP_PORT = 389
#
#     AUTHENTICATION_BACKENDS = (
#                               'company.django.auth.ActiveDirectoryBackend',
#                               # if you want to have default django backend too
#                               'django.contrib.auth.backends.ModelBackend',
#                               )
#
import ldap
import logging
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.conf import settings

logger = logging.getLogger()

ldap.set_option(ldap.OPT_REFERRALS, 0)
ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, settings.AD_CERT_FILE)

# -------------------------------------------

# general function - belongs to utils
def get_exc_str(bClear=False):
   import sys, traceback
   x=sys.exc_info()
   if not x[0]:
      return "No py exception"
   out="%s/%s/%s" % (str(x[0]), str(traceback.extract_tb(x[2])), str(x[1]))
   if bClear:
      sys.exc_clear()
   return out

# --------------------------------------------

class ADUser(object):

    # class level, makes "operational error" problem by search occurs less
    ldap_connection = None
    AD_SEARCH_FIELDS = ['mail','givenName','sn','sAMAccountName', 'proxyAddresses']

    @classmethod
    def get_ldap_url(cls):
        return 'ldaps://%s:%s' % (settings.AD_DNS_NAME, settings.AD_LDAP_PORT)

    def __init__(self, username, domain, search):
        self.search = search
        self.username = username
        self.user_bind_name = "%s\\%s" % (domain, self.username)
        self.is_bound = False
        self.has_data = False

        self.first_name = None
        self.last_name = None
        self.email = None

    def connect(self, password):
        had_connection = ADUser.ldap_connection is not None
        ret = self._connect(password)
        # WORKAROUND: for invalid connection
        if not ret and had_connection and ADUser.ldap_connection is None:
            logger.warning("AD reset connection - invalid connection, try again with new connection")
            ret = self._connect(password)
        return ret

    def _connect(self, password):
        if not password:
            return False # Disallowing null or blank string as password
        try:
            if ADUser.ldap_connection is None:
                logger.info("AD auth backend ldap connecting")
                ADUser.ldap_connection = ldap.initialize(self.get_ldap_url())
                assert self.ldap_connection==ADUser.ldap_connection # python won't do that ;)
            self.ldap_connection.simple_bind_s(self.user_bind_name,password)
            self.is_bound = True
        except Exception, e:
            if str(e.message).find("connection invalid")>=0:
                logger.warning("AD reset connection - it looks like invalid: %s (%s)" % (str(e),  get_exc_str()))
                ADUser.ldap_connection = None
            else:
                logger.error("AD auth backend ldap - probably bad credentials: %s (%s)" % (str(e),  get_exc_str()))
            return False
        return True

    def disconnect(self):
        if self.is_bound:
            logger.info("AD auth backend ldap unbind")
            self.ldap_connection.unbind_s()
            self.is_bound=False

    def get_data(self):
        try:
            assert self.ldap_connection
            # NOTE: Something goes wrong in my case - ignoring this until solved :(
            #       {'info': '00000000: LdapErr: DSID-0C090627, comment: In order to perform this operation a successful bind must be completed on the connection., data 0, vece', 'desc': 'Operations error'}
            res = self.ldap_connection.search_ext_s(self.search,
                                 ldap.SCOPE_SUBTREE,
                                 "sAMAccountName=%s" % self.username,
                                 self.AD_SEARCH_FIELDS)
            self.disconnect()
            if not res:
                logger.error("AD auth ldap backend error by searching %s. No result." % self.search)
                return False
            assert len(res)>=1, "Result should contain at least one element: %s" % res
            result = res[0][1]
        except Exception, e:
            self.disconnect()
            logger.error("AD auth backend error by fetching ldap data: %s (%s)" % (str(e),  get_exc_str()))
            return False

        try:
            logger.error("AD auth user data: %s" % result)

            self.first_name = None
            if result.has_key('givenName'):
                self.first_name = result['givenName'][0]

            self.last_name = None
            if result.has_key('sn'):
                self.last_name = result['sn'][0]

            self.email = None
            if result.has_key('mail'):
                self.email = result['mail'][0]
            self.has_data = True
        except Exception, e:
            logger.error("AD auth backend error by reading fetched data: %s (%s)" % (str(e),  get_exc_str()))
            return False

        return True

    def __del__(self):
        try:
            self.disconnect()
        except Exception, e:
            logger.error("AD auth backend error when disconnecting: %s (%s)" % (str(e),  get_exc_str()))
            return False

    def __str__(self):
        return "AdUser(<%s>, connected=%s, is_bound=%s, has_data=%s)" % (self.username, self.ldap_connection is not None, self.is_bound, self.has_data)

# -------------------------------------------

class ActiveDirectoryBackend(ModelBackend):

    def authenticate(self,username=None,password=None):
#        logger.info("AD auth backend for %s" % username)

        for domain, search in settings.AD_DOMAIN_MAP:
            logger.info("AD auth backend for %s\\%s" % (domain, username))
            aduser = ADUser(username, domain, search)

            connection = aduser.connect(password)

            if connection:
                break

        if not connection:
            return None

        user = None
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User(username=username, is_staff = False, is_superuser = False)

        if not aduser.get_data():
            logger.warning("AD auth backend failed when reading data for %s. User detail data won't be updated in User model." % username)
        else:
            # NOTE: update user data exchange to User model
            assert user.username.lower()==aduser.username.lower()
            user.first_name=aduser.first_name
            user.last_name=aduser.last_name
            user.email=aduser.email
            #user.set_password(password)
            logger.warning("AD auth backend overwriting auth.User data with data from ldap for %s." % username)
        user.save()
        logger.info("AD auth backend check passed for %s" % username)
        return user

    # NOTE: no need to implement get_user - ModelBackend.get_user is all I need
