function result = test_exp3v2_python_runtime_preflight()
%TEST_EXP3V2_PYTHON_RUNTIME_PREFLIGHT Exercise Python checks without sim/RNG.

expectedInput = '/opt/anaconda3/bin/python3';
runtime = validate_exp3v2_python_runtime(expectedInput);
assert(strcmp(runtime.executable_path, ...
    char(java.io.File(expectedInput).getCanonicalPath())));
assert(strcmp(runtime.python_version, '3.13.9'));
assert(strcmp(runtime.jsonschema_version, '4.25.0'));
assert(strcmp(runtime.openpyxl_version, '3.1.5'));

assert_failure(@() validate_exp3v2_python_runtime( ...
    '/definitely/missing/exp3v2/python3'), ...
    'EXP3V2:PythonExecutableNotRegular');
assert_failure(@() validate_exp3v2_python_runtime( ...
    'relative/python3'), 'EXP3V2:PythonExecutableNotAbsolute');
assert_failure(@() validate_exp3v2_python_runtime([mfilename('fullpath') '.m']), ...
    'EXP3V2:PythonExecutableNotExecutable');

shimPath = [tempname '.sh'];
fid = fopen(shimPath, 'w');
assert(fid ~= -1, 'EXP3V2:PythonShimOpen', ...
    'Cannot create dependency-incomplete Python shim.');
fprintf(fid, '#!/bin/sh\nexec /opt/anaconda3/bin/python3 -S "$@"\n');
fclose(fid);
shimCleanup = onCleanup(@() delete_if_present(shimPath));
[status, output] = system(sprintf('chmod u+x %s', ...
    exp3v2_shell_quote(shimPath)));
assert(status == 0, 'EXP3V2:PythonShimChmod', ...
    'Cannot mark test shim executable: %s', output);
assert_failure(@() validate_exp3v2_python_runtime(shimPath), ...
    'EXP3V2:PythonRuntimeProbeFailed');

result = true;
fprintf(['PASS: explicit Python runtime rejects missing, relative, ' ...
    'non-executable, and dependency-incomplete interpreters; sim/RNG not called.\n']);
clear shimCleanup;
end

function assert_failure(callback, expectedIdentifier)
failed = false;
try
    callback();
catch exception
    failed = strcmp(exception.identifier, expectedIdentifier);
end
assert(failed, 'EXP3V2:PythonPreflightTest', ...
    'Expected failure identifier: %s', expectedIdentifier);
end

function delete_if_present(path)
if isfile(path)
    delete(path);
end
end
