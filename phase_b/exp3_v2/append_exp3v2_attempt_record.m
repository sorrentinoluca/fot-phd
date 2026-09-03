function append_exp3v2_attempt_record(path, log, record)
%APPEND_EXP3V2_ATTEMPT_RECORD Append while forcing JSON-array serialization.

if isempty(log.attempts)
    records = record;
else
    records = log.attempts;
    records(end + 1) = record;
end
encodedRecords = arrayfun(@(item) jsonencode(item, ...
    'ConvertInfAndNaN', true), records, 'UniformOutput', false);
payload = sprintf(['{\n  "schema_version": %s,\n' ...
    '  "experiment": %s,\n  "attempts": [\n    %s\n  ]\n}\n'], ...
    jsonencode(log.schema_version), jsonencode(log.experiment), ...
    strjoin(encodedRecords, sprintf(',\n    ')));

parent = fileparts(path);
if ~isfolder(parent)
    mkdir(parent);
end
temporaryPath = [path '.tmp'];
assert(~isfile(temporaryPath), 'EXP3V2:AttemptLogTempExists', ...
    'Refusing to overwrite a stale attempt-log temporary file.');
fid = fopen(temporaryPath, 'w');
assert(fid ~= -1, 'EXP3V2:AttemptLogOpen', ...
    'Could not open the attempt-log temporary file.');
cleanupFile = onCleanup(@() fclose_if_open(fid));
fprintf(fid, '%s', payload);
fclose(fid);
clear cleanupFile;
movefile(temporaryPath, path, 'f');
end

function fclose_if_open(fid)
try
    fclose(fid);
catch
end
end
