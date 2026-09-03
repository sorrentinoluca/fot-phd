function result = test_exp3v2_attempt_policy()
%TEST_EXP3V2_ATTEMPT_POLICY Exercise attempt policy without calling sim.

entry = struct('physical_case_id', 'EXP3V2-N-001', ...
    'primary_seed', 320001, 'replacement_seed', 1320001);
emptyLog = struct('attempts', []);
assert_attempt_allowed(emptyLog, entry, 0, 320001);
assert_identifier(@() assert_attempt_allowed(emptyLog, entry, 1, 1320001), ...
    'EXP3V2:ReplacementWithoutPrimary');
failed = struct('physical_case_id', 'EXP3V2-N-001', 'attempt', 0, ...
    'structural_valid', false, 'technical_failure_reason', 'technical');
failedLog = struct('attempts', failed);
assert_attempt_allowed(failedLog, entry, 1, 1320001);
valid = failed;
valid.structural_valid = true;
valid.technical_failure_reason = '';
assert_identifier(@() assert_attempt_allowed( ...
    struct('attempts', valid), entry, 1, 1320001), ...
    'EXP3V2:UnauthorizedReplacement');
assert_identifier(@() assert_attempt_allowed(failedLog, entry, 0, 320001), ...
    'EXP3V2:DuplicateAttempt');
testArraySerialization();
result = true;
fprintf('PASS: V2 attempt 0/1 policy is fail-closed; sim not called.\n');
end

function testArraySerialization()
path = [tempname '.json'];
cleanup = onCleanup(@() delete_if_present(path));
log = struct('schema_version', '1.0', ...
    'experiment', 'Experiment 3 V2 — Prospective Fresh-Run Held-Out', ...
    'attempts', []);
record = struct('physical_case_id', 'EXP3V2-N-001', 'attempt', 0);
append_exp3v2_attempt_record(path, log, record);
source = fileread(path);
assert(~isempty(regexp(source, '"attempts"\s*:\s*\[', 'once')), ...
    'EXP3V2:AttemptArraySerialization', ...
    'A single attempt must serialize as a JSON array.');
jsondecode(source);
clear cleanup;
delete_if_present(path);
end

function delete_if_present(path)
if isfile(path)
    delete(path);
end
end

function assert_attempt_allowed(log, entry, attempt, seed)
attempts = log.attempts;
if isempty(attempts)
    prior = struct('attempt', {}, 'structural_valid', {}, ...
        'technical_failure_reason', {});
else
    prior = attempts(strcmp({attempts.physical_case_id}, ...
        entry.physical_case_id));
end
assert(~any([prior.attempt] == attempt), 'EXP3V2:DuplicateAttempt', ...
    'Duplicate attempt.');
if attempt == 0
    assert(seed == entry.primary_seed, 'EXP3V2:PrimarySeedMismatch', ...
        'Primary seed mismatch.');
else
    assert(attempt == 1 && seed == entry.replacement_seed, ...
        'EXP3V2:ReplacementSeedMismatch', 'Replacement seed mismatch.');
    primary = prior([prior.attempt] == 0);
    assert(isscalar(primary), 'EXP3V2:ReplacementWithoutPrimary', ...
        'Replacement requires attempt 0.');
    assert(~primary.structural_valid && ...
        strlength(string(primary.technical_failure_reason)) > 0, ...
        'EXP3V2:UnauthorizedReplacement', ...
        'Replacement requires a technical failure.');
end
assert(numel(prior) < 2, 'EXP3V2:AttemptLimit', 'Attempt limit exceeded.');
end

function assert_identifier(operation, expected)
observed = '';
try
    operation();
catch exception
    observed = exception.identifier;
end
assert(strcmp(observed, expected), 'EXP3V2:RegressionIdentifier', ...
    'Expected %s, observed %s.', expected, observed);
end
