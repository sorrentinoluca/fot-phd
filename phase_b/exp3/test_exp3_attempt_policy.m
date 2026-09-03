function result = test_exp3_attempt_policy()
%TEST_EXP3_ATTEMPT_POLICY Regression test for pre-simulation attempt policy.
%
% This test calls policy logic only. It does not invoke the generator, consume
% a simulator seed, create an output directory, or write an attempt log.

caseId = 'EXP3-N-001';
caseEntry = struct('primary_seed', 310001, 'replacement_seed', 1310001);

emptyLog = struct('attempts', []);
assert_attempt_allowed(emptyLog, caseId, 0, 310001, caseEntry);

validPrimary = struct( ...
    'physical_case_id', caseId, ...
    'attempt', 0, ...
    'structural_valid', true, ...
    'technical_failure_reason', '');
duplicateLog = struct('attempts', validPrimary);
assert_identifier(@() assert_attempt_allowed( ...
    duplicateLog, caseId, 0, 310001, caseEntry), 'EXP3:DuplicateAttempt');

assert_identifier(@() assert_attempt_allowed( ...
    emptyLog, caseId, 1, 1310001, caseEntry), ...
    'EXP3:ReplacementWithoutPrimary');

failedPrimary = validPrimary;
failedPrimary.structural_valid = false;
failedPrimary.technical_failure_reason = 'EXP3:StructuralInvalid';
replacementLog = struct('attempts', failedPrimary);
assert_attempt_allowed(replacementLog, caseId, 1, 1310001, caseEntry);

scriptDir = fileparts([mfilename('fullpath') '.m']);
repoRoot = fileparts(fileparts(scriptDir));
realLogPath = fullfile(repoRoot, 'tep_exp3_heldout', 'exp3_attempt_log.json');
if isfile(realLogPath)
    realLog = jsondecode(fileread(realLogPath));
    realPrimary = realLog.attempts;
    assert(strcmp(realPrimary.physical_case_id, caseId) && ...
        realPrimary.attempt == 0 && realPrimary.seed == 310001 && ...
        ~realPrimary.structural_valid && ...
        contains(realPrimary.technical_failure_reason, ...
        'Simulink:Engine:CallbackEvalErr'), ...
        'EXP3:RealAttemptLogMismatch', ...
        'The real attempt-0 technical-failure record is not as expected.');
    assert_identifier(@() assert_attempt_allowed( ...
        realLog, caseId, 0, 310001, caseEntry), 'EXP3:DuplicateAttempt');
    assert_attempt_allowed(realLog, caseId, 1, 1310001, caseEntry);
end

result = true;
fprintf(['PASS: empty, duplicate, unauthorized replacement, valid replacement; ' ...
    'real attempt 0 rejected and attempt 1 authorized when log is present.\n']);
end

function assert_identifier(operation, expectedIdentifier)
observed = '';
try
    operation();
catch exception
    observed = exception.identifier;
end
assert(strcmp(observed, expectedIdentifier), 'EXP3:RegressionIdentifier', ...
    'Expected %s, observed %s.', expectedIdentifier, observed);
end

function assert_attempt_allowed(log, caseId, attempt, seed, caseEntry)
attempts = log.attempts;
if isempty(attempts)
    prior = struct('attempt', {}, 'structural_valid', {}, ...
        'technical_failure_reason', {});
else
    prior = attempts(strcmp({attempts.physical_case_id}, caseId));
end
assert(~any([prior.attempt] == attempt), 'EXP3:DuplicateAttempt', ...
    'This case/attempt is already present in the attempt log.');
if attempt == 0
    assert(seed == caseEntry.primary_seed, 'EXP3:PrimarySeedMismatch', ...
        'Attempt 0 must use the primary seed.');
else
    assert(seed == caseEntry.replacement_seed, 'EXP3:ReplacementSeedMismatch', ...
        'Attempt 1 must use the replacement seed.');
    primary = prior([prior.attempt] == 0);
    assert(isscalar(primary), 'EXP3:ReplacementWithoutPrimary', ...
        'Attempt 1 requires exactly one logged attempt 0.');
    assert(~primary.structural_valid && ...
        strlength(string(primary.technical_failure_reason)) > 0, ...
        'EXP3:UnauthorizedReplacement', ...
        'Attempt 1 requires a technical failure on attempt 0.');
end
assert(numel(prior) < 2, 'EXP3:AttemptLimit', ...
    'Maximum two total attempts per intended case.');
end
