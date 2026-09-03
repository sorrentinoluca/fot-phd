function quoted = exp3v2_shell_quote(value)
%EXP3V2_SHELL_QUOTE Quote one POSIX shell argument without interpolation.

assert((ischar(value) && isrow(value)) || ...
    (isstring(value) && isscalar(value)), ...
    'EXP3V2:ShellArgumentType', ...
    'Shell arguments must be character vectors or string scalars.');
value = char(value);
assert(~contains(value, char(0)), 'EXP3V2:ShellArgumentNul', ...
    'Shell arguments must not contain NUL bytes.');
singleQuote = char(39);
escapedQuote = char([39 34 39 34 39]);
quoted = [singleQuote strrep(value, singleQuote, escapedQuote) singleQuote];
end
