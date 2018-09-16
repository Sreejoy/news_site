'''
    it parses the setting.conf file
'''
import ConfigParser, os

file_name = 'settings.conf'


def get_config_value(section, key, location=False):
    """
    gets a value from settings.conf file
    :param section: name of section
    :param key: name of key
    :param location: location of settings.conf file
    :return: value of the key in that section
    """
    try:
        config = ConfigParser.SafeConfigParser()
        if not location:
            _file_name = os.getcwd() + os.sep + file_name
        else:
            _file_name = location
        config.read(_file_name)
        return config.get(section, key)
    except ConfigParser.NoSectionError:
        print "No section in that name: %s" % section
        return ""
    except ConfigParser.NoOptionError:
        print "No option in that name: %s" % key
        return ""
