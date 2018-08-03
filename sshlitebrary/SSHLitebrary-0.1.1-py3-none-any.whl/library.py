from .abstractclient import SSHClientException
from .pythonclient import PythonSSHClient as SSHClient
from .config import (Configuration, IntegerEntry, LogLevelEntry, NewlineEntry,
                     StringEntry, TimeEntry)
from .utils import ConnectionCache, is_string, is_truthy, plural_or_not

class SSHLibrary(object):    
    DEFAULT_TIMEOUT = '3 seconds'
    DEFAULT_NEWLINE = 'LF'
    DEFAULT_PROMPT = None
    DEFAULT_LOGLEVEL = 'INFO'
    DEFAULT_TERM_TYPE = 'vt100'
    DEFAULT_TERM_WIDTH = 80
    DEFAULT_TERM_HEIGHT = 24
    DEFAULT_PATH_SEPARATOR = '/'
    DEFAULT_ENCODING = 'UTF-8'

    def __init__(self,
                 timeout=DEFAULT_TIMEOUT,
                 newline=DEFAULT_NEWLINE,
                 prompt=DEFAULT_PROMPT,
                 loglevel=DEFAULT_LOGLEVEL,
                 term_type=DEFAULT_TERM_TYPE,
                 width=DEFAULT_TERM_WIDTH,
                 height=DEFAULT_TERM_HEIGHT,
                 path_separator=DEFAULT_PATH_SEPARATOR,
                 encoding=DEFAULT_ENCODING):
        self._connections = ConnectionCache()
        self._config = _DefaultConfiguration(
            timeout or self.DEFAULT_TIMEOUT,
            newline or self.DEFAULT_NEWLINE,
            prompt or self.DEFAULT_PROMPT,
            loglevel or self.DEFAULT_LOGLEVEL,
            term_type or self.DEFAULT_TERM_TYPE,
            width or self.DEFAULT_TERM_WIDTH,
            height or self.DEFAULT_TERM_HEIGHT,
            path_separator or self.DEFAULT_PATH_SEPARATOR,
            encoding or self.DEFAULT_ENCODING
        )

    @property
    def current(self):
        return self._connections.current

    def set_default_configuration(self, timeout=None, newline=None, prompt=None,
                                  loglevel=None, term_type=None, width=None,
                                  height=None, path_separator=None,
                                  encoding=None):        
        self._config.update(timeout=timeout, newline=newline, prompt=prompt,
                            loglevel=loglevel, term_type=term_type, width=width,
                            height=height, path_separator=path_separator,
                            encoding=encoding)

    def set_client_configuration(self, timeout=None, newline=None, prompt=None,
                                 term_type=None, width=None, height=None,
                                 path_separator=None, encoding=None):       
        self.current.config.update(timeout=timeout, newline=newline,
                                   prompt=prompt, term_type=term_type,
                                   width=width, height=height,
                                   path_separator=path_separator,
                                   encoding=encoding)

    def enable_ssh_logging(self, logfile):       
        if SSHClient.enable_logging(logfile):
            self._log('SSH log is written to <a href="%s">file</a>.' % logfile,
                      'HTML')

    def open_connection(self, host, alias=None, port=22, timeout=None,
                        newline=None, prompt=None, term_type=None, width=None,
                        height=None, path_separator=None, encoding=None):       
        timeout = timeout or self._config.timeout
        newline = newline or self._config.newline
        prompt = prompt or self._config.prompt
        term_type = term_type or self._config.term_type
        width = width or self._config.width
        height = height or self._config.height
        path_separator = path_separator or self._config.path_separator
        encoding = encoding or self._config.encoding
        client = SSHClient(host, alias, port, timeout, newline, prompt,
                           term_type, width, height, path_separator, encoding)
        connection_index = self._connections.register(client, alias)
        client.config.update(index=connection_index)
        return connection_index

    def switch_connection(self, index_or_alias):        
        old_index = self._connections.current_index
        if index_or_alias is None:
            self.close_connection()
        else:
            self._connections.switch(index_or_alias)
        return old_index

    def close_connection(self):       
        self.current.close()
        self._connections.current = self._connections._no_current

    def close_all_connections(self):      
        self._connections.close_all()

    def get_connection(self, index_or_alias=None, index=False, host=False,
                       alias=False, port=False, timeout=False, newline=False,
                       prompt=False, term_type=False, width=False, height=False,
                       encoding=False):        
        if not index_or_alias:
            index_or_alias = self._connections.current_index
        try:
            config = self._connections.get_connection(index_or_alias).config
        except RuntimeError:
            config = SSHClient(None).config
        self._log(str(config), self._config.loglevel)
        return_values = tuple(self._get_config_values(config, index, host,
                                                      alias, port, timeout,
                                                      newline, prompt,
                                                      term_type, width, height,
                                                      encoding))
        if not return_values:
            return config
        if len(return_values) == 1:
            return return_values[0]
        return return_values

    def _log(self, msg, level='INFO'):
        level = self._active_loglevel(level)
        if level != 'NONE':
            msg = msg.strip()
            if not msg:
                return
            print(f"*{level}* {msg}")

    def _active_loglevel(self, level):
        if level is None:
            return self._config.loglevel
        if is_string(level) and \
                level.upper() in ['TRACE', 'DEBUG', 'INFO', 'WARN', 'HTML', 'NONE']:
            return level.upper()
        raise AssertionError("Invalid log level '%s'." % level)

    def _get_config_values(self, config, index, host, alias, port, timeout,
                           newline, prompt, term_type, width, height, encoding):
        if is_truthy(index):
            yield config.index
        if is_truthy(host):
            yield config.host
        if is_truthy(alias):
            yield config.alias
        if is_truthy(port):
            yield config.port
        if is_truthy(timeout):
            yield config.timeout
        if is_truthy(newline):
            yield config.newline
        if is_truthy(prompt):
            yield config.prompt
        if is_truthy(term_type):
            yield config.term_type
        if is_truthy(width):
            yield config.width
        if is_truthy(height):
            yield config.height
        if is_truthy(encoding):
            yield config.encoding

    def get_connections(self):        
        configs = [c.config for c in self._connections._connections]
        for c in configs:
            self._log(str(c), self._config.loglevel)
        return configs

    def login(self, username, password, delay='0.5 seconds'):       
        return self._login(self.current.login, username, password, delay)

    def login_with_public_key(self, username, keyfile, password='',
                              allow_agent=False, look_for_keys=False,
                              delay='0.5 seconds'):        
        return self._login(self.current.login_with_public_key, username,
                           keyfile, password, is_truthy(allow_agent),
                           is_truthy(look_for_keys), delay)

    def _login(self, login_method, username, *args):
        self._log("Logging into '%s:%s' as '%s'."
                   % (self.current.config.host, self.current.config.port,
                      username), self._config.loglevel)
        try:
            login_output = login_method(username, *args)
            self._log('Read output: %s' % login_output, self._config.loglevel)
            return login_output
        except SSHClientException as e:
            raise RuntimeError(e)

    def get_pre_login_banner(self, host=None, port=22):        
        if host:
            banner = SSHClient.get_banner_without_login(host, port)
        elif self.current:
            banner = self.current.get_banner()
        else:
            raise RuntimeError("'host' argument is mandatory if there is no open connection.")
        return banner.decode(self.DEFAULT_ENCODING)

    def execute_command(self, command, return_stdout=True, return_stderr=False,
                        return_rc=False, sudo=False,  sudo_password=None):        
        if not is_truthy(sudo):
            self._log("Executing command '%s'." % command, self._config.loglevel)
        else:
            self._log("Executing command 'sudo %s'." % command, self._config.loglevel)
        opts = self._legacy_output_options(return_stdout, return_stderr,
                                           return_rc)
        stdout, stderr, rc = self.current.execute_command(command, sudo, sudo_password)
        return self._return_command_output(stdout, stderr, rc, *opts)

    def start_command(self, command, sudo=False,  sudo_password=None):       
        if not is_truthy(sudo):
            self._log("Starting command '%s'." % command, self._config.loglevel)
        else:
            self._log("Starting command 'sudo %s'." % command, self._config.loglevel)
        self._last_command = command
        self.current.start_command(command, sudo, sudo_password)

    def read_command_output(self, return_stdout=True, return_stderr=False,
                            return_rc=False):        
        self._log("Reading output of command '%s'." % self._last_command, self._config.loglevel)
        opts = self._legacy_output_options(return_stdout, return_stderr,
                                           return_rc)
        try:
            stdout, stderr, rc = self.current.read_command_output()
        except SSHClientException as msg:
            raise RuntimeError(msg)
        return self._return_command_output(stdout, stderr, rc, *opts)

    def create_local_ssh_tunnel(self, local_port, remote_host, remote_port):       
        self.current.create_local_ssh_tunnel(local_port, remote_host, remote_port)

    def _legacy_output_options(self, stdout, stderr, rc):
        if not is_string(stdout):
            return stdout, stderr, rc
        stdout = stdout.lower()
        if stdout == 'stderr':
            return False, True, rc
        if stdout == 'both':
            return True, True, rc
        return stdout, stderr, rc

    def _return_command_output(self, stdout, stderr, rc, return_stdout,
                               return_stderr, return_rc):
        self._log("Command exited with return code %d." % rc, self._config.loglevel)
        ret = []
        if is_truthy(return_stdout):
            ret.append(stdout.rstrip('\n'))
        if is_truthy(return_stderr):
            ret.append(stderr.rstrip('\n'))
        if is_truthy(return_rc):
            ret.append(rc)
        if len(ret) == 1:
            return ret[0]
        return ret

    def write(self, text, loglevel=None):        
        self._write(text, add_newline=True)
        return self._read_and_log(loglevel, self.current.read_until_newline)

    def write_bare(self, text):        
        self._write(text)

    def _write(self, text, add_newline=False):
        try:
            self.current.write(text, is_truthy(add_newline))
        except SSHClientException as e:
            raise RuntimeError(e)

    def write_until_expected_output(self, text, expected, timeout,
                                    retry_interval, loglevel=None):        
        self._read_and_log(loglevel, self.current.write_until_expected, text,
                           expected, timeout, retry_interval)

    def read(self, loglevel=None, delay=None):       
        return self._read_and_log(loglevel, self.current.read, delay)

    def read_until(self, expected, loglevel=None):        
        return self._read_and_log(loglevel, self.current.read_until, expected)

    def read_until_prompt(self, loglevel=None):        
        return self._read_and_log(loglevel, self.current.read_until_prompt)

    def read_until_regexp(self, regexp, loglevel=None):        
        return self._read_and_log(loglevel, self.current.read_until_regexp,
                                  regexp)

    def _read_and_log(self, loglevel, reader, *args):
        try:
            output = reader(*args)
        except SSHClientException as e:
            raise RuntimeError(e)
        self._log(output, loglevel)
        return output

    def get_file(self, source, destination='.'):        
        return self._run_sftp_command(self.current.get_file, source,
                                      destination)

    def get_directory(self, source, destination='.', recursive=False):
        return self._run_sftp_command(self.current.get_directory, source,
                                      destination, is_truthy(recursive))

    def put_file(self, source, destination='.', mode='0744', newline=''):
        return self._run_sftp_command(self.current.put_file, source,
                                      destination, mode, newline)

    def put_directory(self, source, destination='.', mode='0744', newline='',
                      recursive=False):
        return self._run_sftp_command(self.current.put_directory, source,
                                      destination, mode, newline, is_truthy(recursive))

    def _run_sftp_command(self, command, *args):
        try:
            files = command(*args)
        except SSHClientException as e:
            raise RuntimeError(e)
        for src, dst in files:
            self._log("'%s' -> '%s'" % (src, dst), self._config.loglevel)

    def file_should_exist(self, path):        
        if not self.current.is_file(path):
            raise AssertionError("File '%s' does not exist." % path)

    def file_should_not_exist(self, path):
        if self.current.is_file(path):
            raise AssertionError("File '%s' exists." % path)

    def directory_should_exist(self, path):
        if not self.current.is_dir(path):
            raise AssertionError("Directory '%s' does not exist." % path)

    def directory_should_not_exist(self, path):
        if self.current.is_dir(path):
            raise AssertionError("Directory '%s' exists." % path)

    def list_directory(self, path, pattern=None, absolute=False):
        try:
            items = self.current.list_dir(path, pattern, is_truthy(absolute))
        except SSHClientException as msg:
            raise RuntimeError(msg)
        self._log('%d item%s:\n%s' % (len(items), plural_or_not(items),
                                       '\n'.join(items)), self._config.loglevel)
        return items

    def list_files_in_directory(self, path, pattern=None, absolute=False):
        absolute = is_truthy(absolute)
        try:
            files = self.current.list_files_in_dir(path, pattern, absolute)
        except SSHClientException as msg:
            raise RuntimeError(msg)
        files = self.current.list_files_in_dir(path, pattern, absolute)
        self._log('%d file%s:\n%s' % (len(files), plural_or_not(files),
                                       '\n'.join(files)), self._config.loglevel)
        return files

    def list_directories_in_directory(self, path, pattern=None, absolute=False):
        try:
            dirs = self.current.list_dirs_in_dir(path, pattern, is_truthy(absolute))
        except SSHClientException as msg:
            raise RuntimeError(msg)
        self._log('%d director%s:\n%s' % (len(dirs),
                                           'y' if len(dirs) == 1 else 'ies',
                                           '\n'.join(dirs)), self._config.loglevel)
        return dirs


class _DefaultConfiguration(Configuration):

    def __init__(self, timeout, newline, prompt, loglevel, term_type, width,
                 height, path_separator, encoding):
        super(_DefaultConfiguration, self).__init__(
            timeout=TimeEntry(timeout),
            newline=NewlineEntry(newline),
            prompt=StringEntry(prompt),
            loglevel=LogLevelEntry(loglevel),
            term_type=StringEntry(term_type),
            width=IntegerEntry(width),
            height=IntegerEntry(height),
            path_separator=StringEntry(path_separator),
            encoding=StringEntry(encoding)
        )
