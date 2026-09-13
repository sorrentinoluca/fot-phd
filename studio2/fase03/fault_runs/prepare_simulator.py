#!/usr/bin/env python3
"""Create a reproducible, read-only-instrumented copy; never change Phase 02."""
import hashlib
from pathlib import Path
from build_generation_plan import HERE, ROOT

BASE = ROOT / 'studio2/fase02/simulator/source/temexd_philox.c'
BASE_SHA = '230086e7712e753bf48f3e9108cd0ce2f68aba97d9590ebb3c7593a47f8b6d25'
BEGIN = '/* FOT_FAULT_DIAGNOSTICS_BEGIN */\n'
END = '/* FOT_FAULT_DIAGNOSTICS_END */\n'


def add_after(text, anchor, extra):
    if text.count(anchor) != 1:
        raise ValueError(f'non-unique source anchor: {anchor}')
    return text.replace(anchor, anchor + BEGIN + extra + '\n' + END)


def instrument(source):
    if hashlib.sha256(source).hexdigest() != BASE_SHA:
        raise ValueError('unqualified base source')
    text = source.decode()
    text = text.replace('#define S_FUNCTION_NAME  temexd_philox',
                        '#define S_FUNCTION_NAME  temexd_fault_philox')
    text = add_after(text, '  doublereal tlastcomp;\n  integer MSFlag;\n',
                     '  doublereal fot_diag_last_t;\n  unsigned int fot_last_idv_mask;')
    text = add_after(text, '  (*ModelData).code_sd = (float)0.;\n',
                     '  (*ModelData).fot_diag_last_t = -1.;\n  (*ModelData).fot_last_idv_mask = 0;')
    text = add_after(text, '  tefunc(ModelData, &NX, &rt, rx, dx, 1);\n', r'''
  /* Diagnostics only: no model, random state or solver writes. */
  if (ssIsMajorTimeStep(S)) {
    unsigned int mask = 0;
    int j;
    for (j = 0; j < 28; ++j) {
      if ((*ModelData).dvec_.idv[j] >= 0.5) mask |= (1U << j);
    }
    if (mask != (*ModelData).fot_last_idv_mask) {
      mexPrintf("FOT_IDV,%.17g,%u\n", rt, mask);
      (*ModelData).fot_last_idv_mask = mask;
    }
    if (fabs(rt * 60. - floor(rt * 60. + 0.5)) < 1e-7 &&
        rt > (*ModelData).fot_diag_last_t + 1e-10) {
      mexPrintf("FOT_DIAG,%.17g,%u", rt, mask);
      for (j = 0; j < 9; ++j) mexPrintf(",%.17g", (*ModelData).pv_.xmeasdist[j]);
      mexPrintf(",%.17g,%.17g,%.17g,%.17g\n",
        (*ModelData).teproc_.vcv[9], (*ModelData).teproc_.vcv[10], rx[47], rx[48]);
      (*ModelData).fot_diag_last_t = rt;
    }
  }''')
    text = add_after(text, '\t(*ModelData).code_sd = (*ModelData).dvec_.idv[28];\n',
                     '    mexPrintf("FOT_TRIP,%.17g,%d\\n", rt, (int)(*ModelData).code_sd);')
    return text.encode()


def strip_instrumentation(source):
    import re
    text = re.sub(re.escape(BEGIN) + '.*?' + re.escape(END), '', source.decode(), flags=re.S)
    return text.replace('#define S_FUNCTION_NAME  temexd_fault_philox',
                        '#define S_FUNCTION_NAME  temexd_philox').encode()


def main():
    dest = HERE / 'runtime/source'
    dest.mkdir(parents=True, exist_ok=True)
    data = instrument(BASE.read_bytes())
    assert strip_instrumentation(data) == BASE.read_bytes()
    for name, content in [('temexd_fault_philox.c', data)] + [
        (n, (BASE.parent/n).read_bytes()) for n in ('teprob_mod.h', 'philox4x32.h')]:
        p = dest/name
        if p.exists():
            if p.read_bytes() != content:
                raise ValueError(f'refusing overwrite: {p}')
        else:
            with p.open('xb') as f:
                f.write(content)
    print('source_sha256=' + hashlib.sha256(data).hexdigest())

if __name__ == '__main__':
    main()
