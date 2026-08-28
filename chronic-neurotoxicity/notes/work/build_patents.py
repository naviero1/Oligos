#!/usr/bin/env python3
"""OligoTox-CNS — PATENTS lane extractor.

Every value emitted here is read out of a patent full-text document fetched in
this session (FreePatentsOnline mirrors of the USPTO grant text, saved under
sources/cns/fpo/).  No value is recalled from memory.

Sequence safety (kidney-round hazards a & b):
  * sequences are read from structured HTML table cells, never from a PDF text
    layer, and never by a bare [acgt]-run regex;
  * FPO wraps long cells across rows, which truncates sequences -- the
    reconstruction in seqbuild.py re-joins continuation rows and then REJECTS
    any sequence that disagrees with ANY length declaration printed in the same
    row (start/stop span, gapmer motif sum, chemistry-code length, linkage
    string length + 1).  Only 4-way/3-way/2-way agreeing sequences are emitted;
  * case is not judged from pixels: these Ionis/Biogen tables print sequences in
    a single case and encode chemistry in separate Motif / Linkage / Chemistry
    columns, which are recorded verbatim.
"""
import json, re, sys, collections
sys.path.insert(0, '/home/user/oligos/notes/cns/work')
from fpo_parse import load
from seqbuild import build as seqbuild, rawrows

FPO = '/home/user/oligos/sources/cns/fpo/%s.html'
ISIS = re.compile(r'^\d{6}$')

# ---------------------------------------------------------------- grading ---
def grade_fob_acute(s):
    """7-criterion rodent FOB / acute tolerability score, 0-7. Controls = 0(-1)."""
    if s < 1:   return 0
    if s < 3:   return 1
    if s < 5:   return 2
    return 3

def grade_fob_chronic(s):
    """Same 0-7 battery read at >= 8 weeks: a deficit still present then is by
    definition not transient, so the mild/transient band (grade 1) is skipped."""
    if s < 1:   return 0
    if s < 3:   return 2
    return 3

def grade_glial(fold):
    """AIF1/Iba1/GFAP level vs concurrent PBS/saline control, as fold.
    Capped at 2: a marker level alone does not establish grade-3 criteria
    (degeneration/loss, dose-limiting tox)."""
    if fold < 1.5:  return 0
    if fold < 2.0:  return 1
    return 2

def dir_glial(fold):
    if fold >= 1.15: return 'increase'
    if fold <= 0.85: return 'decrease'
    return 'no_change'

def grade_behav(val, ctrl):
    """Motor performance (rotarod latency, grip strength) vs concurrent control."""
    if ctrl in (None, 0): return 0, 'TBD'
    r = (val - ctrl) / ctrl
    d = 'no_change' if abs(r) < 0.15 else ('increase' if r > 0 else 'decrease')
    if r >= -0.15: g = 0
    elif r >= -0.30: g = 1
    else: g = 2
    return g, d

def pct(a, b):
    return '%+.0f%%_vs_control' % (100.0 * (a - b) / b)

# ------------------------------------------------------------ collectors ---
OLIGOS, MEAS = {}, []
_ocount = collections.count() if False else None

def oid(key):
    return OLIGOS[key]['oligo_id']

def add_oligo(key, **kw):
    if key in OLIGOS: return OLIGOS[key]['oligo_id']
    n = len(OLIGOS) + 1
    rec = dict(oligo_id='TMP_pat_%d' % n, oligo_name='TBD', aliases='NA',
               oligo_class='ASO_gapmer', target_gene='TBD', indication='TBD',
               developer='TBD', max_phase='research_panel', length_nt='TBD',
               backbone_chemistry='TBD', sugar_modifications='TBD',
               gapmer_design='TBD', conjugate='none', ps_count='TBD',
               sequence_5to3='TBD', design_source='TBD', notes='')
    rec.update(kw)
    OLIGOS[key] = rec
    return rec['oligo_id']

def add_meas(**kw):
    n = len(MEAS) + 1
    rec = dict(measurement_id='TMP_pat_m%d' % n, oligo_id='TBD',
               study_type='animal_invivo', species='TBD', system_model='TBD',
               cns_region='NA', delivery_method='TBD', dose_or_conc_value='TBD',
               dose_or_conc_unit='TBD', exposure_duration='TBD',
               endpoint_domain='TBD', challenge_priority='medium',
               readout_category='TBD', readout_name='TBD', readout_value='TBD',
               readout_unit='NA', effect_direction='TBD', effect_vs_control='TBD',
               neurotox_grade=0, reversibility='not_assessed', is_cns_specific='TRUE',
               source_id='TBD', source_ref='TBD', source_table='TBD',
               redistribution='public_domain', notes='grade_provisional')
    rec.update(kw)
    MEAS.append(rec)
    return rec

# --------------------------------------------------- chemistry helpers -----
def design_from_chem(chem):
    """'eeeeeddddddddddeeeee' -> ('5-10-5_MOE', "2'-MOE;DNA_gap").
       'eeeeddddddddkkeee'   -> ('4-8-5_MOE_cEt', "2'-MOE;cEt;DNA_gap")."""
    if not chem: return 'TBD', 'TBD'
    m = re.match(r'^([ek]+)(d+)([ek]+)$', chem)
    if not m: return 'TBD', 'TBD'
    w5, gap, w3 = m.groups()
    tag = 'MOE_cEt' if 'k' in w5 + w3 else 'MOE'
    sug = "2'-MOE;cEt;DNA_gap" if 'k' in w5 + w3 else "2'-MOE;DNA_gap"
    return '%d-%d-%d_%s' % (len(w5), len(gap), len(w3), tag), sug

def backbone_from_link(link):
    if not link: return 'TBD', 'TBD'
    return ('full_PS' if set(link) == {'s'} else 'PS_PO_mix'), link.count('s')

# ============================================================================
# PATENT 1 -- US 9,605,263 B2  (Ionis, "Compositions for modulating C9ORF72
#             expression").  Tables 6, 7, 8, 9, 15, 16, 17.
# ============================================================================
P1 = 'US9605263'
p1 = load(FPO % P1)
p1t = p1.find_all('table')

def rows_of(tb):
    return [[c.strip() for c in r] for r in rawrows(tb)]

# --- Table 6: the panel + sequences (4-way verified in-row) -----------------
t6 = [r for r in rows_of(p1t[18]) if len(r) == 7 and ISIS.match(r[0])]
assert len(t6) == 93, len(t6)
p1seq = {}
for isis, st, sp, seq, link, motif, sid in t6:
    L = len(seq)
    assert int(sp) - int(st) + 1 == L
    assert sum(int(x) for x in motif.split('-')) == L
    assert len(link) + 1 == L
    p1seq[isis] = dict(seq=seq, link=link, motif=motif, sid=sid, L=L)

C9_COMMON = dict(oligo_class='ASO_gapmer', target_gene='C9ORF72',
                 indication='C9orf72_ALS_FTD', developer='Ionis Pharmaceuticals',
                 max_phase='research_panel', conjugate='none',
                 sugar_modifications="2'-MOE;DNA_gap;5-methylcytosine",
                 design_source='US9605263B2 Table 6')

for isis, v in p1seq.items():
    bb, ps = backbone_from_link(v['link'])
    add_oligo(('P1', isis), oligo_name='ISIS %s' % isis, aliases='ISIS_%s' % isis,
              length_nt=v['L'], backbone_chemistry=bb, ps_count=ps,
              gapmer_design='%s_MOE' % v['motif'], sequence_5to3=v['seq'],
              notes=('C9ORF72_MOE_gapmer_panel;SEQ_ID_NO_%s;linkage=%s '
                     '(s=phosphorothioate,o=phosphodiester);'
                     'length_verified_3way(start-stop_span,motif_sum,linkage+1)'
                     % (v['sid'], v['link'])), **C9_COMMON)

# --- Table 7: acute tolerability score, mouse ICV 700 ug, 3 h --------------
t7 = [r for r in rows_of(p1t[20]) if len(r) >= 3 and ISIS.match(r[1])]
assert len(t7) == 92, len(t7)
for _, isis, sc in [(r[0], r[1], r[2]) for r in t7]:
    s = float(sc)
    add_meas(oligo_id=oid(('P1', isis)), species='mouse',
             system_model='C57BL/6_mouse_CNS_invivo', cns_region='whole_brain',
             delivery_method='intracerebroventricular', dose_or_conc_value=700,
             dose_or_conc_unit='ug', exposure_duration='3h',
             endpoint_domain='acute_neurotoxicity', challenge_priority='medium',
             readout_category='behavioral', readout_name='acute_neurotoxicity_score',
             readout_value=s, readout_unit='score_0_to_7',
             effect_direction='increase' if s > 0 else 'no_change',
             effect_vs_control='%.2f_vs_0_PBS' % s, neurotox_grade=grade_fob_acute(s),
             reversibility='not_assessed', source_id='P1', source_ref='US9605263B2',
             source_table='Table 7 (Example 2), ISIS %s' % isis,
             notes=('grade_provisional;7-criterion mouse FOB summed 0-7, group mean, '
                    'PBS controls score 0; mapping 0-<1=>0, 1-<3=>1, 3-<5=>2, >=5=>3'))

# --- Tables 8 & 9: WO 2014/062691 comparator ASOs (5-10-5 MOE, full PS) ----
for tix, tno in ((23, 'Table 8'), (25, 'Table 9')):
    for r in rows_of(p1t[tix]):
        if len(r) == 6 and ISIS.match(r[0]):
            isis, st, sp, seq, sc, sid = r
            L = len(seq)
            assert int(sp) - int(st) + 1 == L == 20
            add_oligo(('P1', isis), oligo_name='ISIS %s' % isis, aliases='ISIS_%s' % isis,
                      length_nt=L, backbone_chemistry='full_PS', ps_count=L - 1,
                      gapmer_design='5-10-5_MOE', sequence_5to3=seq,
                      design_source='US9605263B2 %s' % tno,
                      notes=('comparator ASO from WO 2014/062691;SEQ_ID_NO_%s;'
                             'full_PS 5-10-5 MOE gapmer per Example 3 text;'
                             'length_verified_2way(start-stop_span,declared_5-10-5_motif)' % sid),
                      **{k: v for k, v in C9_COMMON.items() if k != 'design_source'})
            s = float(sc)
            add_meas(oligo_id=oid(('P1', isis)), species='mouse',
                     system_model='C57BL/6_mouse_CNS_invivo', cns_region='whole_brain',
                     delivery_method='intracerebroventricular', dose_or_conc_value=700,
                     dose_or_conc_unit='ug', exposure_duration='3h',
                     endpoint_domain='acute_neurotoxicity', challenge_priority='medium',
                     readout_category='behavioral', readout_name='acute_neurotoxicity_score',
                     readout_value=s, readout_unit='score_0_to_7',
                     effect_direction='increase' if s > 0 else 'no_change',
                     effect_vs_control='%.2f_vs_0_PBS' % s,
                     neurotox_grade=grade_fob_acute(s), reversibility='not_assessed',
                     source_id='P1', source_ref='US9605263B2',
                     source_table='%s (Example 3), ISIS %s' % (tno, isis),
                     notes=('grade_provisional;patent states these compounds were '
                            '"poorly tolerated";7-criterion mouse FOB 0-7, group mean; '
                            'mapping 0-<1=>0, 1-<3=>1, 3-<5=>2, >=5=>3'))

# --- Table 15: mouse, 8 weeks after single ICV 700 ug ----------------------
# header (confirmed identically in US9605263 and US10138482, and cross-checked
# against the same table in US10815483):
#   ISIS No. | Score 8 weeks after injection | AIF1 (spinal cord) |
#   AIF1 (cerebellum) | GFAP (spinal cord) | GFAP (cortex) | SEQ ID NO.
t15 = [r for r in rows_of(p1t[44]) if len(r) == 7 and ISIS.match(r[0])]
assert len(t15) == 92, len(t15)
M15 = [('AIF1_mRNA', 'spinal_cord', 2), ('AIF1_mRNA', 'cerebellum', 3),
       ('GFAP', 'spinal_cord', 4), ('GFAP', 'cortex', 5)]
for r in t15:
    isis = r[0]
    s = float(r[1])
    add_meas(oligo_id=oid(('P1', isis)), species='mouse',
             system_model='C57BL/6_mouse_CNS_invivo', cns_region='whole_brain',
             delivery_method='intracerebroventricular', dose_or_conc_value=700,
             dose_or_conc_unit='ug', exposure_duration='8wk',
             endpoint_domain='chronic_neurotoxicity',
             challenge_priority='high_chronic_neurotox',
             readout_category='behavioral', readout_name='FOB_score_8wk',
             readout_value=s, readout_unit='score_0_to_7',
             effect_direction='increase' if s > 0 else 'no_change',
             effect_vs_control='%.2f_vs_0_PBS' % s, neurotox_grade=grade_fob_chronic(s),
             reversibility='irreversible' if s >= 1 else 'not_assessed',
             source_id='P1', source_ref='US9605263B2',
             source_table='Table 15 (Example 12), ISIS %s, column "Score 8 weeks after injection"' % isis,
             notes=('grade_provisional;same 7-criterion mouse FOB read at 8 weeks; '
                    'a deficit persisting to 8 wk is not transient so the mapping '
                    'skips grade 1: 0-<1=>0, 1-<3=>2, >=3=>3'))
    for name, region, col in M15:
        raw = r[col]
        if raw.upper().replace('.', '') in ('ND', ''):
            continue     # patent: "N.D." = experiment not performed; no value to record
        starred = raw.endswith('*')
        val = float(raw.rstrip('*'))
        add_meas(oligo_id=oid(('P1', isis)), species='mouse',
                 system_model='C57BL/6_mouse_CNS_invivo', cns_region=region,
                 delivery_method='intracerebroventricular', dose_or_conc_value=700,
                 dose_or_conc_unit='ug', exposure_duration='8wk',
                 endpoint_domain='neuroinflammation',
                 challenge_priority='high_chronic_neurotox',
                 readout_category='transcriptomic', readout_name=name,
                 readout_value=val, readout_unit='fold_change',
                 effect_direction=dir_glial(val), effect_vs_control='%.1fx_vs_PBS' % val,
                 neurotox_grade=grade_glial(val), reversibility='not_assessed',
                 source_id='P1', source_ref='US9605263B2',
                 source_table='Table 15 (Example 12), ISIS %s, column "%s (%s)"'
                              % (isis, name.split('_')[0], region.replace('_', ' ')),
                 notes=('grade_provisional;RT-PCR normalised to Gapdh, expressed '
                        'relative to PBS control = 1.0; mapping <1.5x=>0, '
                        '1.5-<2.0x=>1, >=2.0x=>2 (marker level alone cannot '
                        'establish grade 3)'
                        + (';value is the average of 1-3 mice (patent asterisk)' if starred else '')))

# --- Table 16: rat, single 3 mg intrathecal, 3 h and 8 weeks --------------
t16 = [r for r in rows_of(p1t[47]) if len(r) == 8 and ISIS.match(r[0])]
assert len(t16) == 8, len(t16)
M16 = [('AIF1_mRNA', 'spinal_cord', 3), ('AIF1_mRNA', 'cortex', 4),
       ('GFAP', 'spinal_cord', 5), ('GFAP', 'cortex', 6)]
for r in t16:
    isis = r[0]
    s3, s8 = float(r[1]), float(r[2])
    rev = 'reversible' if (s3 >= 1 and s8 < 1) else \
          ('partially_reversible' if 0 < s8 < s3 else 'not_assessed')
    add_meas(oligo_id=oid(('P1', isis)), species='rat',
             system_model='Sprague_Dawley_rat_CNS_invivo', cns_region='spinal_cord',
             delivery_method='intrathecal', dose_or_conc_value=3,
             dose_or_conc_unit='mg', exposure_duration='3h',
             endpoint_domain='acute_neurotoxicity', challenge_priority='medium',
             readout_category='behavioral', readout_name='acute_neurotoxicity_score',
             readout_value=s3, readout_unit='score_0_to_7',
             effect_direction='increase' if s3 > 0 else 'no_change',
             effect_vs_control='%.1f_vs_0_saline' % s3,
             neurotox_grade=grade_fob_acute(s3), reversibility=rev,
             source_id='P1', source_ref='US9605263B2',
             source_table='Table 16 (Example 13), ISIS %s, column "Score 3 hours after injection"' % isis,
             notes=('grade_provisional;rat 7-body-part paralysis score 0-7 '
                    '(0=moving, 1=paralysed, summed, group mean; saline rats score 0); '
                    'mapping 0-<1=>0, 1-<3=>1, 3-<5=>2, >=5=>3; reversibility set '
                    'from the paired 8-week score in the same table'))
    add_meas(oligo_id=oid(('P1', isis)), species='rat',
             system_model='Sprague_Dawley_rat_CNS_invivo', cns_region='spinal_cord',
             delivery_method='intrathecal', dose_or_conc_value=3,
             dose_or_conc_unit='mg', exposure_duration='8wk',
             endpoint_domain='chronic_neurotoxicity',
             challenge_priority='high_chronic_neurotox',
             readout_category='behavioral', readout_name='FOB_score_8wk',
             readout_value=s8, readout_unit='score_0_to_7',
             effect_direction='increase' if s8 > 0 else 'no_change',
             effect_vs_control='%.1f_vs_0_saline' % s8,
             neurotox_grade=grade_fob_chronic(s8),
             reversibility='irreversible' if s8 >= 1 else 'reversible',
             source_id='P1', source_ref='US9605263B2',
             source_table='Table 16 (Example 13), ISIS %s, column "Score 8 weeks after injection"' % isis,
             notes=('grade_provisional;rat 7-body-part paralysis score read at 8 weeks; '
                    'persisting deficit so mapping skips grade 1: 0-<1=>0, 1-<3=>2, >=3=>3'))
    for name, region, col in M16:
        raw = r[col]; starred = raw.endswith('*'); val = float(raw.rstrip('*'))
        add_meas(oligo_id=oid(('P1', isis)), species='rat',
                 system_model='Sprague_Dawley_rat_CNS_invivo', cns_region=region,
                 delivery_method='intrathecal', dose_or_conc_value=3,
                 dose_or_conc_unit='mg', exposure_duration='8wk',
                 endpoint_domain='neuroinflammation',
                 challenge_priority='high_chronic_neurotox',
                 readout_category='transcriptomic', readout_name=name,
                 readout_value=val, readout_unit='fold_change',
                 effect_direction=dir_glial(val), effect_vs_control='%.1fx_vs_PBS' % val,
                 neurotox_grade=grade_glial(val), reversibility='not_assessed',
                 source_id='P1', source_ref='US9605263B2',
                 source_table='Table 16 (Example 13), ISIS %s, column "%s (%s)"'
                              % (isis, name.split('_')[0], region),
                 notes=('grade_provisional;RT-PCR normalised to Gapdh, relative to '
                        'PBS control = 1.0; mapping <1.5x=>0, 1.5-<2.0x=>1, >=2.0x=>2'
                        + (';value is the average of 2-3 animals (patent asterisk)' if starred else '')))

# --- Table 17: cynomolgus monkey, 3 x 35 mg IT, sacrifice +2 wk -----------
t17 = rows_of(p1t[50])
hdr = t17[0]
assert hdr[0] == 'Brain Region' and hdr[1:] == ['801287', '802459', '806679'] * 1 + \
       ['801287', '802459', '806679'], hdr
REGION = {'Cervical spinal': ('cervical_spinal_cord', 'spinal_cord'),
          'Thoracic spinal': ('thoracic_spinal_cord', 'spinal_cord'),
          'Temporal': ('temporal_cortex', 'cortex'),
          'Motor cortex': ('motor_cortex', 'cortex'),
          'Lumbar spinal': ('lumbar_spinal_cord', 'spinal_cord'),
          'Hippocampus': ('hippocampus', 'hippocampus'),
          'Frontal cortex': ('frontal_cortex', 'cortex')}
n17 = 0
for r in t17[1:]:
    if len(r) != 7 or r[0] not in REGION: continue
    label, enum = REGION[r[0]]
    for k, isis in enumerate(['801287', '802459', '806679']):
        for name, off in (('AIF1_mRNA', 1), ('GFAP', 4)):
            val = float(r[off + k])
            add_meas(oligo_id=oid(('P1', isis)), species='monkey',
                     system_model='cynomolgus_monkey_CNS_invivo', cns_region=enum,
                     delivery_method='intrathecal', dose_or_conc_value=35,
                     dose_or_conc_unit='mg', exposure_duration='3_doses_d1_d14_d28_sacrifice_2wk_after',
                     endpoint_domain='neuroinflammation',
                     challenge_priority='high_chronic_neurotox',
                     readout_category='transcriptomic', readout_name=name,
                     readout_value=val, readout_unit='fold_change',
                     effect_direction=dir_glial(val), effect_vs_control='%.1fx_vs_PBS' % val,
                     neurotox_grade=grade_glial(val), reversibility='not_assessed',
                     source_id='P1', source_ref='US9605263B2',
                     source_table='Table 17 (Example 14), ISIS %s, %s, %s column'
                                  % (isis, label, name.split('_')[0]),
                     notes=('grade_provisional;female cynomolgus monkeys 2-6 kg, '
                            '3 x 35 mg intrathecal bolus on days 1/14/28, n=4 per group, '
                            'sacrificed 2 weeks after the last dose; RT-PCR normalised to '
                            'GAPDH, relative to PBS control = 1.0; mapping <1.5x=>0, '
                            '1.5-<2.0x=>1, >=2.0x=>2'))
            n17 += 1
assert n17 == 42, n17

# ============================================================================
# PATENT 2 -- US 10,968,453 B2  (Biogen MA, "Compositions for modulating SOD-1
#             expression").  Tables 64, 65, 67, 69, 70.  ISIS 666853 = tofersen.
# ============================================================================
P2 = 'US10968453'
p2 = load(FPO % P2)
p2t = p2.find_all('table')
p2seq, _ = seqbuild(FPO % P2)

SOD_COMMON = dict(oligo_class='ASO_gapmer', target_gene='SOD1',
                  indication='SOD1_ALS', developer='Ionis/Biogen',
                  conjugate='none', design_source='US10968453B2')

CLINICAL = {'666853': dict(oligo_name='tofersen', aliases='BIIB067;ISIS_666853;ISIS-SOD1Rx',
                           max_phase='approved'),
            '333611': dict(oligo_name='ISIS 333611', aliases='ISIS_333611',
                           max_phase='phase_1')}

def add_sod(isis):
    key = ('P2', isis)
    if key in OLIGOS: return OLIGOS[key]['oligo_id']
    v = p2seq.get(isis)
    extra = dict(CLINICAL.get(isis, {}))
    if v:
        gd, sug = design_from_chem(v['chem'])
        bb, ps = backbone_from_link(v['link'])
        note = ('SEQ_ID_NO_from_US10968453B2;chemistry_code=%s (e=2\'-MOE, d=DNA, k=cEt)'
                ';length_verified_%dway(%s)'
                % (v['chem'], len(v['decls']), ','.join(sorted(v['decls']))))
        if v['link']: note += ';linkage=%s (s=phosphorothioate,o=phosphodiester)' % v['link']
        rec = dict(length_nt=v['len'], sequence_5to3=v['seq'], gapmer_design=gd,
                   sugar_modifications=sug + ';5-methylcytosine',
                   backbone_chemistry=bb, ps_count=ps, notes=note)
    else:
        rec = dict(notes=('sequence not disclosed anywhere in the US10968453B2 / '
                          'US10385341B2 / US10669546B2 texts for this ISIS number '
                          '- left TBD rather than inferred'))
    rec.setdefault('oligo_name', 'ISIS %s' % isis)
    rec.setdefault('aliases', 'ISIS_%s' % isis)
    rec.setdefault('max_phase', 'research_panel')
    d = dict(SOD_COMMON); d.update(rec); d.update(extra)
    return add_oligo(key, **d)

# --- Table 64: rat, single 3 mg IT, 3 h FOB -------------------------------
t64 = [r for r in rows_of(p2t[185]) if len(r) >= 5 and ISIS.match(r[1])]
assert len(t64) == 124, len(t64)
for r in t64:
    isis, start, chem, sc = r[1], r[2], r[3], r[4]
    s = float(sc)
    o = add_sod(isis)
    add_meas(oligo_id=o, species='rat', system_model='Sprague_Dawley_rat_CNS_invivo',
             cns_region='spinal_cord', delivery_method='intrathecal',
             dose_or_conc_value=3, dose_or_conc_unit='mg', exposure_duration='3h',
             endpoint_domain='acute_neurotoxicity', challenge_priority='medium',
             readout_category='behavioral', readout_name='acute_neurotoxicity_score',
             readout_value=s, readout_unit='score_0_to_7',
             effect_direction='increase' if s > 0 else 'no_change',
             effect_vs_control='%.0f_vs_0_or_1_PBS' % s,
             neurotox_grade=grade_fob_acute(s), reversibility='not_assessed',
             source_id='P2', source_ref='US10968453B2',
             source_table='Table 64 (Example 14), ISIS %s' % isis,
             notes=('grade_provisional;rat functional observational battery, 7 regions '
                    '(tail, hind paws, hind legs, hind end, front posture, fore paws, head), '
                    '0/1 each, summed 0-7; patent states control animals usually score 0 or 1; '
                    'mapping 0-<1=>0, 1-<3=>1, 3-<5=>2, >=5=>3;'
                    'patent chemistry class="%s";target start site %s on SEQ ID NO: 1'
                    % (chem, start)))

# --- Table 65: rat lumbar spinal cord IBA1/GFAP, 8 wk post 3 mg IT --------
t65 = [r for r in rows_of(p2t[188]) if len(r) >= 3 and ISIS.match(r[0])]
assert len(t65) == 79, len(t65)
for isis, iba, gfap in [(r[0], r[1], r[2]) for r in t65]:
    o = add_sod(isis)
    for name, raw in (('IBA1', iba), ('GFAP', gfap)):
        v = float(raw); fold = v / 100.0
        add_meas(oligo_id=o, species='rat', system_model='Sprague_Dawley_rat_CNS_invivo',
                 cns_region='spinal_cord', delivery_method='intrathecal',
                 dose_or_conc_value=3, dose_or_conc_unit='mg', exposure_duration='8wk',
                 endpoint_domain='neuroinflammation',
                 challenge_priority='high_chronic_neurotox',
                 readout_category='transcriptomic',
                 readout_name='AIF1_mRNA' if name == 'IBA1' else 'GFAP',
                 readout_value=v, readout_unit='% of control',
                 effect_direction=dir_glial(fold), effect_vs_control='%.0fpct_of_PBS' % v,
                 neurotox_grade=grade_glial(fold), reversibility='not_assessed',
                 source_id='P2', source_ref='US10968453B2',
                 source_table='Table 65 (Example 14), ISIS %s, %s column' % (isis, name),
                 notes=('grade_provisional;lumbar spinal cord mRNA 8 weeks after a single '
                        '3 mg intrathecal dose, %% of PBS control; IBA1 recorded as AIF1_mRNA '
                        '(same gene); mapping on fold-change <1.5x=>0, 1.5-<2.0x=>1, >=2.0x=>2'))

# --- Table 67: rat, 1 mg and 3 mg IT, FOB at 3 h and 8 wk ----------------
t67 = [r for r in rows_of(p2t[196]) if len(r) == 5 and ISIS.match(r[0])]
assert len(t67) == 5, len(t67)
for isis, f3_1, f3_3, f8_1, f8_3 in [tuple(r) for r in t67]:
    o = add_sod(isis)
    for dose, s3raw, s8raw in ((1, f3_1, f8_1), (3, f3_3, f8_3)):
        s3, s8 = float(s3raw), float(s8raw)
        rev = 'reversible' if (s3 >= 1 and s8 < 1) else \
              ('partially_reversible' if 0 < s8 < s3 else 'not_assessed')
        add_meas(oligo_id=o, species='rat', system_model='Sprague_Dawley_rat_CNS_invivo',
                 cns_region='spinal_cord', delivery_method='intrathecal',
                 dose_or_conc_value=dose, dose_or_conc_unit='mg', exposure_duration='3h',
                 endpoint_domain='acute_neurotoxicity', challenge_priority='medium',
                 readout_category='behavioral', readout_name='acute_neurotoxicity_score',
                 readout_value=s3, readout_unit='score_0_to_7',
                 effect_direction='increase' if s3 > 0 else 'no_change',
                 effect_vs_control='%.1f_vs_0_or_1_PBS' % s3,
                 neurotox_grade=grade_fob_acute(s3), reversibility=rev,
                 source_id='P2', source_ref='US10968453B2',
                 source_table='Table 67 (Example 16), ISIS %s, "3 hour FOB / %d mg" column' % (isis, dose),
                 notes=('grade_provisional;rat 7-region FOB 0-7; mapping 0-<1=>0, '
                        '1-<3=>1, 3-<5=>2, >=5=>3; reversibility from the paired '
                        '8-week score in the same table'))
        add_meas(oligo_id=o, species='rat', system_model='Sprague_Dawley_rat_CNS_invivo',
                 cns_region='spinal_cord', delivery_method='intrathecal',
                 dose_or_conc_value=dose, dose_or_conc_unit='mg', exposure_duration='8wk',
                 endpoint_domain='chronic_neurotoxicity',
                 challenge_priority='high_chronic_neurotox',
                 readout_category='behavioral', readout_name='FOB_score_8wk',
                 readout_value=s8, readout_unit='score_0_to_7',
                 effect_direction='increase' if s8 > 0 else 'no_change',
                 effect_vs_control='%.1f_vs_0_or_1_PBS' % s8,
                 neurotox_grade=grade_fob_chronic(s8),
                 reversibility='reversible' if s8 < 1 else 'irreversible',
                 source_id='P2', source_ref='US10968453B2',
                 source_table='Table 67 (Example 16), ISIS %s, "8 week FOB / %d mg" column' % (isis, dose),
                 notes=('grade_provisional;same rat FOB read at 8 weeks; persisting '
                        'deficit so mapping skips grade 1: 0-<1=>0, 1-<3=>2, >=3=>3'))

# --- Table 69: mouse, single ICV 700 ug, 3 h FOB -------------------------
t69 = [r for r in rows_of(p2t[202]) if len(r) == 3 and ISIS.match(r[0])]
assert len(t69) == 5, len(t69)
for isis, f3, bw in [tuple(r) for r in t69]:
    o = add_sod(isis); s = float(f3)
    add_meas(oligo_id=o, species='mouse', system_model='C57BL/6_mouse_CNS_invivo',
             cns_region='whole_brain', delivery_method='intracerebroventricular',
             dose_or_conc_value=700, dose_or_conc_unit='ug', exposure_duration='3h',
             endpoint_domain='acute_neurotoxicity', challenge_priority='medium',
             readout_category='behavioral', readout_name='acute_neurotoxicity_score',
             readout_value=s, readout_unit='score_0_to_7',
             effect_direction='increase' if s > 0 else 'no_change',
             effect_vs_control='%.2f_vs_0_PBS' % s, neurotox_grade=grade_fob_acute(s),
             reversibility='not_assessed', source_id='P2', source_ref='US10968453B2',
             source_table='Table 69 (Example 18), ISIS %s, "3 hour FOB" column' % isis,
             notes=('grade_provisional;7-criterion mouse FOB 0-7 (different battery from '
                    'the rat one), group mean, saline mice score 0; mapping 0-<1=>0, '
                    '1-<3=>1, 3-<5=>2, >=5=>3; body weight change at 8 wk in the same '
                    'table row was %s%% and is not recorded as a CNS row' % bw))

# --- Table 70: mouse IBA1/GFAP, 8 wk post ICV 700 ug --------------------
t70 = [r for r in rows_of(p2t[206]) if len(r) == 5 and ISIS.match(r[0])]
assert len(t70) == 5, len(t70)
for r in t70:
    isis = r[0]; o = add_sod(isis)
    for name, region, col in (('IBA1', 'spinal_cord', 1), ('IBA1', 'cortex', 2),
                              ('GFAP', 'spinal_cord', 3), ('GFAP', 'cortex', 4)):
        v = float(r[col]); fold = v / 100.0
        add_meas(oligo_id=o, species='mouse', system_model='C57BL/6_mouse_CNS_invivo',
                 cns_region=region, delivery_method='intracerebroventricular',
                 dose_or_conc_value=700, dose_or_conc_unit='ug', exposure_duration='8wk',
                 endpoint_domain='neuroinflammation',
                 challenge_priority='high_chronic_neurotox',
                 readout_category='transcriptomic',
                 readout_name='AIF1_mRNA' if name == 'IBA1' else 'GFAP',
                 readout_value=v, readout_unit='% of control',
                 effect_direction=dir_glial(fold), effect_vs_control='%.1fpct_of_PBS' % v,
                 neurotox_grade=grade_glial(fold), reversibility='not_assessed',
                 source_id='P2', source_ref='US10968453B2',
                 source_table='Table 70 (Example 18), ISIS %s, "%s (%% PBS) / %s" column'
                              % (isis, name, 'Lumbar' if region == 'spinal_cord' else 'Cortex'),
                 notes=('grade_provisional;mouse tissue mRNA 8 weeks after a single 700 ug '
                        'ICV dose, %% of PBS control ("Lumbar" column recorded as spinal_cord); '
                        'IBA1 recorded as AIF1_mRNA; mapping on fold-change <1.5x=>0, '
                        '1.5-<2.0x=>1, >=2.0x=>2'))

# ============================================================================
# PATENT 3 -- US 9,683,235 B2 (Ionis, "Compositions for modulating Tau
#             expression").  Tables 67 (mouse ICV) and 68 (rat IT).
# ============================================================================
P3 = 'US9683235'
p3 = load(FPO % P3)
p3t = p3.find_all('table')
p3seq, _ = seqbuild(FPO % P3)
TAU = ['613099', '613361', '613370', '623782', '623996', '424880', '603054']

for isis in TAU:
    v = p3seq[isis]
    bb, ps = backbone_from_link(v['link'])
    motif = v['motif'] or ('5-10-5' if v['len'] == 20 else 'TBD')
    add_oligo(('P3', isis), oligo_name='ISIS %s' % isis, aliases='ISIS_%s' % isis,
              oligo_class='ASO_gapmer', target_gene='MAPT', indication='tauopathy',
              developer='Ionis Pharmaceuticals', max_phase='research_panel',
              length_nt=v['len'], backbone_chemistry=bb, ps_count=ps,
              sugar_modifications="2'-MOE;DNA_gap;5-methylcytosine",
              gapmer_design='%s_MOE' % motif, conjugate='none',
              sequence_5to3=v['seq'], design_source='US9683235B2',
              notes=('tau MOE gapmer panel;length_verified_%dway(%s)%s'
                     % (len(v['decls']), ','.join(sorted(v['decls'])),
                        (';linkage=%s (s=phosphorothioate,o=phosphodiester)' % v['link'])
                        if v['link'] else '')))

# Table 67 -- mouse ICV. Columns: hTau 300 ug | hTau 200 ug | WT C57Bl6 300 ug
t67tau = [r for r in rows_of(p3t[168]) if len(r) == 4 and ISIS.match(r[0])]
assert len(t67tau) == 7, len(t67tau)
COLS = [('hTau_transgenic_mouse', 300), ('hTau_transgenic_mouse', 200),
        ('WT_C57BL6_mouse_CNS_invivo', 300)]
for r in t67tau:
    isis = r[0]
    for k, (model, dose) in enumerate(COLS):
        raw = r[1 + k]
        if raw == 'ND': continue
        s = float(raw)
        add_meas(oligo_id=oid(('P3', isis)), species='mouse', system_model=model,
                 cns_region='whole_brain', delivery_method='intracerebroventricular',
                 dose_or_conc_value=dose, dose_or_conc_unit='ug', exposure_duration='3h',
                 endpoint_domain='acute_neurotoxicity', challenge_priority='medium',
                 readout_category='behavioral', readout_name='acute_neurotoxicity_score',
                 readout_value=s, readout_unit='score_0_to_7',
                 effect_direction='increase' if s > 0 else 'no_change',
                 effect_vs_control='%.2f_vs_0_saline' % s,
                 neurotox_grade=grade_fob_acute(s), reversibility='not_assessed',
                 source_id='P3', source_ref='US9683235B2',
                 source_table='Table 67 (Example 20), ISIS %s, "%s / %d ug" column'
                              % (isis, 'hTau' if k < 2 else 'WT C57Bl6', dose),
                 notes=('grade_provisional;7-criterion mouse FOB 0-7 at 3 h after a single '
                        'ICV dose, group mean of 3-4 mice, saline mice score 0; '
                        'mapping 0-<1=>0, 1-<3=>1, 3-<5=>2, >=5=>3'))

# Table 68 -- rat, 1 mg and 3 mg IT bolus, 3 h
t68 = [r for r in rows_of(p3t[172]) if len(r) == 3 and ISIS.match(r[0])]
assert len(t68) == 7, len(t68)
for isis, d1, d3 in [tuple(r) for r in t68]:
    for dose, raw in ((1, d1), (3, d3)):
        s = float(raw)
        add_meas(oligo_id=oid(('P3', isis)), species='rat',
                 system_model='Sprague_Dawley_rat_CNS_invivo', cns_region='spinal_cord',
                 delivery_method='intrathecal', dose_or_conc_value=dose,
                 dose_or_conc_unit='mg', exposure_duration='3h',
                 endpoint_domain='acute_neurotoxicity', challenge_priority='medium',
                 readout_category='behavioral', readout_name='acute_neurotoxicity_score',
                 readout_value=s, readout_unit='score_0_to_7',
                 effect_direction='increase' if s > 0 else 'no_change',
                 effect_vs_control='%.2f_vs_0_saline' % s,
                 neurotox_grade=grade_fob_acute(s), reversibility='not_assessed',
                 source_id='P3', source_ref='US9683235B2',
                 source_table='Table 68 (Example 20), ISIS %s, "%d mg" column' % (isis, dose),
                 notes=('grade_provisional;rat 7-body-part paralysis score 0-7 at 3 h '
                        'after a single intrathecal bolus, group mean of 4 rats, saline '
                        'rats score 0; mapping 0-<1=>0, 1-<3=>1, 3-<5=>2, >=5=>3'))

# ============================================================================
# PATENT 4 -- US 11,834,660 B2 (Ionis, "Compositions for modulating Ataxin 2
#             expression").  Table 7 (Iba1) and Table 10 (rotarod).
# ============================================================================
P4 = 'US11834660'
p4 = load(FPO % P4)
p4t = p4.find_all('table')
p4seq, _ = seqbuild(FPO % P4)
ATX = ['564133', '564127', '564216', '564210']
for isis in ATX:
    v = p4seq[isis]
    add_oligo(('P4', isis), oligo_name='ISIS %s' % isis, aliases='ISIS_%s' % isis,
              oligo_class='ASO_gapmer', target_gene='ATXN2',
              indication='SCA2_ALS', developer='Ionis Pharmaceuticals',
              max_phase='research_panel', length_nt=v['len'],
              backbone_chemistry='full_PS', ps_count=v['len'] - 1,
              sugar_modifications="2'-MOE;DNA_gap;5-methylcytosine",
              gapmer_design='5-10-5_MOE', conjugate='none', sequence_5to3=v['seq'],
              design_source='US11834660B2',
              notes=('ataxin-2 5-10-5 MOE gapmer, full PS per Example 1 text;'
                     'length_verified_2way(mRNA_start-stop_span,genomic_start-stop_span)'
                     ' and against the uniform declared 20-nucleoside design'))

# Table 7 -- percent Iba1 mRNA level INCREASE vs saline, ATXN2-Q127 mice, ICV 250 ug
t7atx = [r for r in rows_of(p4t[20]) if len(r) >= 3 and ISIS.match(r[1])]
assert len(t7atx) == 4, len(t7atx)
for r in t7atx:
    isis = r[1]; inc = float(r[2]); fold = 1.0 + inc / 100.0
    add_meas(oligo_id=oid(('P4', isis)), species='mouse',
             system_model='ATXN2-Q127_transgenic_mouse', cns_region='cerebellum',
             delivery_method='intracerebroventricular', dose_or_conc_value=250,
             dose_or_conc_unit='ug', exposure_duration='7d',
             endpoint_domain='neuroinflammation', challenge_priority='medium',
             readout_category='transcriptomic', readout_name='Iba1',
             readout_value=inc, readout_unit='pct_increase_vs_control',
             effect_direction=dir_glial(fold), effect_vs_control='+%.0f%%_vs_saline' % inc,
             neurotox_grade=grade_glial(fold), reversibility='not_assessed',
             source_id='P4', source_ref='US11834660B2',
             source_table='Table 7 (Example 2), ISIS %s' % isis,
             notes=('grade_provisional;single 250 ug ICV dose in ATXN2-Q127 mice, brain '
                    'harvested after 7 days; value is percent Iba1 mRNA INCREASE over the '
                    '0.9%% saline control, converted to fold = 1 + pct/100 before grading; '
                    'mapping <1.5x=>0, 1.5-<2.0x=>1, >=2.0x=>2'))

# Table 10 -- rotarod latency to fall; the WT arm is the tolerability comparison
t10 = rows_of(p4t[28])
# reconstruct: (strain, n, treatment, latency)
recs, strain = [], None
for r in t10:
    c = [x for x in r]
    if len(c) >= 5 and c[4]:
        if c[1]: strain = c[1]
        recs.append((strain, c[2], c[3], float(c[4])))
assert len(recs) >= 6, recs
ctrl = {s: v for s, n, t, v in recs if 'saline' in t}
for strain, n, treat, val in recs:
    if 'saline' in treat: continue
    m = re.search(r'ISIS (\d{6}) \((\d+)', treat)
    if not m: continue
    isis, dose = m.group(1), int(m.group(2))
    base = ctrl[strain]
    g, d = grade_behav(val, base)
    wt = strain.upper().startswith('WT')
    add_meas(oligo_id=oid(('P4', isis)), species='mouse',
             system_model=('WT_mouse_CNS_invivo' if wt else 'ATXN2-Q127_transgenic_mouse'),
             cns_region='cerebellum', delivery_method='intracerebroventricular',
             dose_or_conc_value=dose, dose_or_conc_unit='ug', exposure_duration='chronic',
             endpoint_domain='neurobehavioral',
             challenge_priority='high_chronic_neurotox' if wt else 'medium',
             readout_category='functional', readout_name='rotarod_latency',
             readout_value=val, readout_unit='sec', effect_direction=d,
             effect_vs_control=pct(val, base), neurotox_grade=g,
             reversibility='not_assessed', source_id='P4', source_ref='US11834660B2',
             source_table='Table 10 (Example 2), %s mice, %s' % (strain, treat.replace('\n', ' ')),
             notes=('grade_provisional;rotarod mean latency to fall vs the concurrent '
                    '0.9%% saline arm of the SAME strain (%.0f s, n as printed); mapping '
                    'within -15%%=>0, -15 to -30%%=>1, worse than -30%%=>2; '
                    'in the ATXN2-Q127 disease strain a LONGER latency is efficacy, not '
                    'toxicity, so only a shortfall vs the strain-matched saline arm is '
                    'graded as a CNS signal' % base))

# ============================================================================
# PATENT 5 -- US 11,339,393 B2 (Ionis, "Compositions for modulating C9ORF72
#             expression").  Example 7 dose-response AIF-1 / rotarod / grip
#             strength (mouse, ISIS 571883) and rat AIF-1 (ISIS 603538).
# ============================================================================
P5 = 'US11339393'
p5 = load(FPO % P5)
p5t = p5.find_all('table')
p5text = p5.get_text('\n')

# ISIS 603538 sequence is printed in Example 7 as an annotated linkage string.
m = re.search(r'ISIS 603538[^.]*?\(([^)]*?wherein[^)]*?)\)', p5text, re.S)
lk = re.search(r'\(\s*((?:[ACGT][so]?\s*)+);\s*wherein', p5text)
assert lk, 'ISIS 603538 linkage string not found'
tok = re.findall(r'([ACGT])([so])?', lk.group(1))
seq603538 = ''.join(t[0] for t in tok)
link603538 = ''.join(t[1] for t in tok if t[1])
assert len(seq603538) == 20 and len(link603538) == 19, (seq603538, link603538)
assert 'ISIS 603538 was designed as a 5-10-5 MOE gapmer, 20 nucleosides in length' \
       in re.sub(r'\s+', ' ', p5text)

add_oligo(('P5', '603538'), oligo_name='ISIS 603538', aliases='ISIS_603538',
          oligo_class='ASO_gapmer', target_gene='C9ORF72',
          indication='C9orf72_ALS_FTD_rodent_surrogate',
          developer='Ionis Pharmaceuticals', max_phase='research_panel',
          length_nt=20, backbone_chemistry='PS_PO_mix', ps_count=link603538.count('s'),
          sugar_modifications="2'-MOE;DNA_gap;5-methylcytosine",
          gapmer_design='5-10-5_MOE', conjugate='none', sequence_5to3=seq603538,
          design_source='US11339393B2 Example 7',
          notes=('rat-C9ORF72-targeted surrogate;sequence read from the annotated '
                 'linkage string printed in Example 7 (Gs Ao Co Co Gs ...);'
                 'linkage=%s;length_verified_2way(20 nucleoside letters vs the text\'s '
                 'declared "20 nucleosides in length"; 19 linkages = 20-1)' % link603538))

add_oligo(('P5', '571883'), oligo_name='ISIS 571883', aliases='ISIS_571883',
          oligo_class='ASO_gapmer', target_gene='C9ORF72',
          indication='C9orf72_ALS_FTD_rodent_surrogate',
          developer='Ionis Pharmaceuticals', max_phase='research_panel',
          length_nt=20, backbone_chemistry='full_PS', ps_count=19,
          sugar_modifications="2'-MOE;DNA_gap;5-methylcytosine",
          gapmer_design='5-10-5_MOE', conjugate='none', sequence_5to3='TBD',
          design_source='US11339393B2 Example 7',
          notes=('mouse-C9ORF72-targeted surrogate;Example 7 declares a 20-nucleoside '
                 '5-10-5 MOE gapmer, full phosphorothioate, target start site 33704 on '
                 'SEQ ID NO: 11, but does NOT print the nucleobase sequence - '
                 'sequence_5to3 left TBD rather than inferred'))

# Table 32 -- AIF-1 % of PBS, mouse ICV dose response, 14 d
t32 = [r for r in rows_of(p5t[95]) if len(r) == 3 and r[0].isdigit()]
assert len(t32) == 5, len(t32)
for dose, pb, sc in [tuple(r) for r in t32]:
    for region, label, raw in (('whole_brain', 'Posterior brain', pb),
                               ('spinal_cord', 'Spinal cord', sc)):
        v = float(raw); fold = v / 100.0
        add_meas(oligo_id=oid(('P5', '571883')), species='mouse',
                 system_model='C57BL/6_mouse_CNS_invivo', cns_region=region,
                 delivery_method='intracerebroventricular', dose_or_conc_value=int(dose),
                 dose_or_conc_unit='ug', exposure_duration='14d',
                 endpoint_domain='neuroinflammation', challenge_priority='medium',
                 readout_category='transcriptomic', readout_name='AIF1_mRNA',
                 readout_value=v, readout_unit='% of control',
                 effect_direction=dir_glial(fold), effect_vs_control='%.0fpct_of_PBS' % v,
                 neurotox_grade=grade_glial(fold), reversibility='not_assessed',
                 source_id='P5', source_ref='US11339393B2',
                 source_table='Table 32 (Example 7, Mouse Experiment 1), %d ug, "%s" column'
                              % (int(dose), label),
                 notes=('grade_provisional;groups of 4 C57BL/6 mice, single ICV bolus, '
                        'tissue taken 14 days later; AIF-1 mRNA as %% of PBS control; '
                        'mapping on fold-change <1.5x=>0, 1.5-<2.0x=>1, >=2.0x=>2'))

# Table 33 -- rotarod latency, PBS vs ISIS 571883
t33 = [r for r in rows_of(p5t[97]) if len(r) == 3 and r[0].isdigit()]
assert len(t33) == 3, len(t33)
for wk, pbs, aso in [tuple(r) for r in t33]:
    if int(wk) == 0: continue          # pre-dose baseline
    g, d = grade_behav(float(aso), float(pbs))
    add_meas(oligo_id=oid(('P5', '571883')), species='mouse',
             system_model='C57BL/6_mouse_CNS_invivo', cns_region='whole_brain',
             delivery_method='intracerebroventricular', dose_or_conc_value='TBD',
             dose_or_conc_unit='TBD', exposure_duration='%swk' % wk,
             endpoint_domain='neurobehavioral',
             challenge_priority='high_chronic_neurotox',
             readout_category='functional', readout_name='rotarod_latency',
             readout_value=float(aso), readout_unit='sec', effect_direction=d,
             effect_vs_control=pct(float(aso), float(pbs)), neurotox_grade=g,
             reversibility='not_assessed', source_id='P5', source_ref='US11339393B2',
             source_table='Table 33 (Example 7), week %s, "ISIS 571883" column vs "PBS" column' % wk,
             notes=('grade_provisional;latency to fall vs the concurrent PBS column of '
                    'the same row; mapping within -15%%=>0, -15 to -30%%=>1, worse than '
                    '-30%%=>2; dose not stated for this sub-experiment in the patent text'))

# Table 34 -- hindlimb grip strength, PBS vs ISIS 571883
t34 = [r for r in rows_of(p5t[100]) if len(r) == 3 and r[0].isdigit()]
assert len(t34) == 11, len(t34)
for wk, pbs, aso in [tuple(r) for r in t34]:
    if int(wk) == 0: continue
    g, d = grade_behav(float(aso), float(pbs))
    add_meas(oligo_id=oid(('P5', '571883')), species='mouse',
             system_model='C57BL/6_mouse_CNS_invivo', cns_region='whole_brain',
             delivery_method='intracerebroventricular', dose_or_conc_value='TBD',
             dose_or_conc_unit='TBD', exposure_duration='%swk' % wk,
             endpoint_domain='neurobehavioral',
             challenge_priority='high_chronic_neurotox',
             readout_category='functional', readout_name='grip_strength',
             readout_value=float(aso), readout_unit='g', effect_direction=d,
             effect_vs_control=pct(float(aso), float(pbs)), neurotox_grade=g,
             reversibility='not_assessed', source_id='P5', source_ref='US11339393B2',
             source_table='Table 34 (Example 7), week %s, "ISIS 571883" column vs "PBS" column' % wk,
             notes=('grade_provisional;mean hindlimb grip strength vs the concurrent PBS '
                    'column of the same row; mapping within -15%%=>0, -15 to -30%%=>1, '
                    'worse than -30%%=>2'))

# Table 36 -- AIF-1 % of PBS, rat IT dose response (ISIS 603538)
t36 = [r for r in rows_of(p5t[106]) if len(r) == 6 and r[1].isdigit()]
assert len(t36) == 3, len(t36)
R36 = [('whole_brain', 'Brain (1 mm section)', 2), ('cortex', 'Cortex', 3),
       ('spinal_cord', 'Spinal cord (lumbar)', 4), ('spinal_cord', 'Spinal cord (cervical)', 5)]
for r in t36:
    dose = int(r[1])
    for region, label, col in R36:
        v = float(r[col]); fold = v / 100.0
        add_meas(oligo_id=oid(('P5', '603538')), species='rat',
                 system_model='Sprague_Dawley_rat_CNS_invivo', cns_region=region,
                 delivery_method='intrathecal', dose_or_conc_value=dose,
                 dose_or_conc_unit='ug', exposure_duration='TBD',
                 endpoint_domain='neuroinflammation', challenge_priority='medium',
                 readout_category='transcriptomic', readout_name='AIF1_mRNA',
                 readout_value=v, readout_unit='% of control',
                 effect_direction=dir_glial(fold), effect_vs_control='%.0fpct_of_PBS' % v,
                 neurotox_grade=grade_glial(fold), reversibility='not_assessed',
                 source_id='P5', source_ref='US11339393B2',
                 source_table='Table 36 (Example 7, rat experiment), %d ug, "%s" column' % (dose, label),
                 notes=('grade_provisional;AIF-1 mRNA as %% of PBS control after '
                        'intrathecal dosing of the rat-targeted surrogate ISIS 603538; '
                        'mapping on fold-change <1.5x=>0, 1.5-<2.0x=>1, >=2.0x=>2'))

# ============================================================================
# PATENT 6 -- US 12,241,065 B2 (Bristol-Myers Squibb, "Antisense oligonucleotides
#             targeting alpha-synuclein and uses thereof").  Tables 5-7.
#             Different sponsor, different chemistry (LNA), different scale.
# ============================================================================
P6 = 'US12241065'
p6 = load(FPO % P6)
p6t = p6.find_all('table')
p6T = re.sub(r'\s+', ' ', p6.get_text(' '))

# Sequence of ASO-005459: printed verbatim in the description, with the case
# carrying the chemistry, and corroborated three further ways in the same text.
assert 'AtTcctttacaccACAC (SEQ ID NO: 15) has 17 nucleotides' in p6T
assert 'DES-005459 refers to an ASO sequence of AtTcctttacaccACAC (SEQ ID NO: 15) ' \
       'with an ASO design of LDLDDDDDDDDDDLLLL' in p6T
assert 'each of the first nucleotide, the third nucleotide, and the 14 th -17 th ' \
       'nucleotides from the 5′ end is a modified nucleotide' in p6T
SEQ5459 = 'AtTcctttacaccACAC'
assert len(SEQ5459) == 17 and [i + 1 for i, c in enumerate(SEQ5459) if c.isupper()] == [1, 3, 14, 15, 16, 17]

def grade_bms(total):
    """BMS 5-category x 0-4 tolerability score, max 20 (Table 5 footnote).
    Same proportional band edges as the 0-7 rodent FOB scale."""
    if total < 1:  return 0
    if total < 9:  return 1
    if total < 15: return 2
    return 3

add_oligo(('P6', 'ASO-005459'), oligo_name='ASO-005459', aliases='DES-005459;SEQ_ID_NO_15',
          oligo_class='ASO_gapmer', target_gene='SNCA',
          indication='Parkinson_disease_multiple_system_atrophy',
          developer='Bristol-Myers Squibb', max_phase='preclinical', length_nt=17,
          backbone_chemistry='full_PS', ps_count='TBD',
          sugar_modifications='LNA;DNA_gap', gapmer_design='1-1-1-10-4_LNA_mixed_wing',
          conjugate='none', sequence_5to3=SEQ5459, design_source='US12241065B2',
          notes=('17-mer beta-D-oxy-LNA/DNA ASO targeting the SNCA intron1/exon2 boundary; '
                 'CASE IS CHEMISTRY and was resolved from the text layer, not from a render: '
                 'upper = LNA, lower = DNA, corroborated by the printed design string '
                 'LDLDDDDDDDDDDLLLL and by the text "the first, the third, and the 14th-17th '
                 'nucleotides from the 5-prime end is a modified nucleotide"; length '
                 'corroborated by the printed statement "has 17 nucleotides"; '
                 'the design is not a classic symmetric gapmer (LNA at 1,3,14-17); '
                 'ps_count not stated in the text'))

# Table 6 -- A53T-PAC mice, 100 ug ICV, tolerability at 3 days
t6bms = [r for r in rows_of(p6t[16]) if len(r) == 7 and r[0].isdigit()]
mean6 = [r for r in rows_of(p6t[16]) if r and r[0] == 'mean']
assert len(t6bms) == 5 and mean6 and mean6[0][-1] == '1.00'
add_meas(oligo_id=oid(('P6', 'ASO-005459')), species='mouse',
         system_model='A53T-PAC_transgenic_mouse', cns_region='whole_brain',
         delivery_method='intracerebroventricular', dose_or_conc_value=100,
         dose_or_conc_unit='ug', exposure_duration='3d',
         endpoint_domain='acute_neurotoxicity', challenge_priority='medium',
         readout_category='behavioral', readout_name='tolerability_score_total',
         readout_value=1.00, readout_unit='score_0_to_20', effect_direction='increase',
         effect_vs_control='1.00_group_mean_max_20', neurotox_grade=grade_bms(1.00),
         reversibility='not_assessed', source_id='P6', source_ref='US12241065B2',
         source_table='Table 6 (Example 5), group mean row',
         notes=('grade_provisional;Table 5 scoring system: 5 categories (hyperactivity/'
                'stereotypies, decreased vigilance, motor coordination and strength, '
                'posture/appearance/breathing, tremor/convulsion) each scored 0-4, summed, '
                'max 20; individual animal totals were 5, 0, 0, 0, 0 (n=5), group mean 1.00; '
                'mapping to our 0-3 uses the same proportional band edges as the 0-7 rodent '
                'FOB scale: 0-<1=>0, 1-<9=>1, 9-<15=>2, >=15=>3'))

# Table 7 -- 28-day study, per-animal scores at day 1 and day 28, all zero
t7bms = [r for r in rows_of(p6t[19]) if len(r) == 8 and r[0].isdigit()]
assert len(t7bms) == 10, len(t7bms)
for day in ('1', '28'):
    sub = [r for r in t7bms if r[1] == day]
    assert len(sub) == 5 and all(r[-1] == '0' for r in sub)
    add_meas(oligo_id=oid(('P6', 'ASO-005459')), species='mouse',
             system_model='mouse_CNS_invivo', cns_region='whole_brain',
             delivery_method='intracerebroventricular', dose_or_conc_value='TBD',
             dose_or_conc_unit='TBD', exposure_duration='%sd' % day,
             endpoint_domain='chronic_neurotoxicity' if day == '28' else 'acute_neurotoxicity',
             challenge_priority='high_chronic_neurotox' if day == '28' else 'medium',
             readout_category='behavioral', readout_name='tolerability_score_total',
             readout_value=0, readout_unit='score_0_to_20', effect_direction='no_change',
             effect_vs_control='0_in_all_5_animals', neurotox_grade=0,
             reversibility='not_assessed', source_id='P6', source_ref='US12241065B2',
             source_table='Table 7 (Example 5), day %s rows (animals 26-30)' % day,
             notes=('grade_provisional;all 5 animals scored 0 in every category at this '
                    'timepoint on the Table 5 0-20 scale; NEGATIVE CONTROL row. '
                    'DOSE AND STRAIN NOT ATTRIBUTABLE: the surrounding text describes both '
                    'a 3.13-50 ug ICV dose-response in A53T-PAC mice and a separate 100 ug '
                    'ICV study in wild-type C57BL/6 mice monitored over 4 weeks, and the '
                    'patent does not say which one Table 7 reports - left TBD, not guessed'))

# ============================================================================
# PATENT 7 -- US 11,851,654 B2 (National University Corporation Tokyo Medical
#             and Dental University, "Nucleic acid with reduced toxicity").
#             A category-1 patent: a METHOD OF REDUCING the CNS toxicity of an
#             oligonucleotide, with per-agent mouse ICV tolerability data.
# ============================================================================
sys.path.insert(0, '/home/user/oligos/notes/cns/work')
from tmdu_parse import parse_seq_table, decode

P7 = 'US11851654'
p7 = load(FPO % P7)
p7t = p7.find_all('table')
p7T = re.sub(r'\s+', ' ', p7.get_text(' '))
assert 'the acute tolerability score' in p7T
assert 'administered into the left lateral ventricle' in p7T

def tmdu_seqs(ti):
    out = {}
    for rec in parse_seq_table(p7t[ti]):
        res, seq = decode(rec['raw'])
        m = re.search(r'(\d+)mer', rec['name'])
        if m: assert int(m.group(1)) == len(seq), (rec['name'], seq)
        out[rec['name']] = dict(seq=seq, sid=rec['sid'], raw=rec['raw'].replace(CARET := '{circumflex over ( )}', '^'),
                                ps=rec['raw'].count('{circumflex over ( )}'), decl=int(m.group(1)) if m else None)
    return out

# (example, seq-table idx, score tbl, rate tbl, death tbl, dose, target, agents)
TMDU = [
    dict(ex=1, st=3,  sc=6,  rt=9,  dt=11, dose=12,
         target='BACE1', aso='ASO (BACE1) 13mer',
         pairs=[('ASO', None),
                ('HDO cRNA all PO', 'cRNA (BACE1) all PO'),
                ('HDO cRNA all PS', 'cRNA (BACE1) all PS'),
                ('HDO cDNA all PO', 'cDNA (BACE1) all PO'),
                ('HDO cDNA all PS', 'cDNA (BACE1) all PS')]),
    dict(ex=2, st=13, sc=16, rt=19, dt=21, dose=12,
         target='BACE1', aso='ASO (BACE1) 13mer',
         pairs=[('ASO', None),
                ('HDO 13mer', 'cRNA (BACE1) 13mer'), ('HDO 12mer', 'cRNA (BACE1) 12mer'),
                ('HDO 11mer', 'cRNA (BACE1) 11mer'), ('HDO 10mer', 'cRNA (BACE1) 10mer')]),
    dict(ex=4, st=23, sc=26, rt=29, dt=31, dose=12,
         target='BACE1', aso='ASO (BACE1) 13mer',
         pairs=[('ASO', None),
                ('OH 26mer', 'overhanging cRNA (BACE1)Gapmer 26mer'),
                ('OH 26mer PS-4', 'overhanging cRNA (BACE1)Gapmer 26mer PS-4'),
                ('OH 26mer PS-8', 'overhanging cRNA (BACE1)Gapmer 26mer PS-8'),
                ('OH 30mer', 'overhanging cRNA (BACE1)Gapmer 30mer'),
                ('OH 22mer', 'overhanging cRNA (BACE1)Gapmer 22mer'),
                ('OH 18mer', 'overhanging cRNA (BACE1)Gapmer 18mer')]),
    dict(ex=5, st=33, sc=36, rt=39, dt=41, dose=6,
         target='MAPT', aso='ASO (Tau) 16mer',
         pairs=[('ASO', None), ('HDO', 'HDO cRNA (Tau) 16mer'),
                ('OH', 'overhanging cRNA (Tau) DNA 29mer')]),
]
TP = {1: '1h', 3: '3h', 6: '6h'}

def grade_tmdu(s):
    """11-item mouse ICV acute tolerability score, 0-11 (PBS controls score 0).
    Same proportional band edges as the 0-7 Ionis FOB scale."""
    if s < 1: return 0
    if s < 5: return 1
    if s < 8: return 2
    return 3

for blk in TMDU:
    seqs = tmdu_seqs(blk['st'])
    aso = seqs[blk['aso']]
    scores = {r[1]: r[2:5] for r in rows_of(p7t[blk['sc']]) if len(r) >= 5 and r[1]}
    rates  = {r[1]: r[2:5] for r in rows_of(p7t[blk['rt']]) if len(r) >= 5 and r[1]}
    deaths = {r[1]: r[2]   for r in rows_of(p7t[blk['dt']]) if len(r) >= 3 and r[1]}
    assert scores['PBS'] == ['0 ± 0'] * 3, scores['PBS']
    for label, comp in blk['pairs']:
        key = ('P7', blk['ex'], label)
        cs = seqs[comp] if comp else None
        if comp:
            note = ('heteroduplex: the same LNA/DNA gapmer annealed to the complementary '
                    'strand "%s" (%s, SEQ ID NO %s, %d phosphorothioate bonds), printed as: %s; '
                    % (comp, 'RNA' if 'cRNA' in comp else 'DNA', cs['sid'], cs['ps'], cs['raw']))
            klass, nm = 'other', '%s + %s' % (blk['aso'], comp)
        else:
            note, klass, nm = '', 'ASO_gapmer', blk['aso']
        w5 = len(re.match(r'^[A-Z]*', aso['seq']).group(0))
        w3 = len(re.search(r'[A-Z]*$', aso['seq']).group(0))
        add_oligo(key, oligo_name=nm, aliases='%s (US11851654B2 Example %d)' % (label, blk['ex']),
                  oligo_class=klass, target_gene=blk['target'],
                  indication='Alzheimer_disease' if blk['target'] == 'BACE1' else 'tauopathy',
                  developer='Tokyo Medical and Dental University', max_phase='research_panel',
                  length_nt=aso['decl'], backbone_chemistry='full_PS', ps_count=aso['ps'],
                  sugar_modifications='LNA;DNA_gap',
                  gapmer_design='%d-%d-%d_LNA' % (w5, aso['decl'] - w5 - w3, w3),
                  conjugate='none', sequence_5to3=aso['seq'],
                  design_source='US11851654B2 Example %d' % blk['ex'],
                  notes=(note + 'antisense strand printed as %s; CASE IS CHEMISTRY and was '
                         'resolved from the text layer via the explicit "(L)" LNA markers '
                         '(upper+(L)=LNA, lower=DNA, upper=RNA), not from a render; length '
                         'verified against the "%dmer" declared in the compound name'
                         % (aso['raw'], aso['decl'])))
        for k, (hr, tp) in enumerate(sorted(TP.items())):
            raw = scores[label][k]
            mean = float(raw.split('±')[0].strip())
            s1 = float(scores[label][0].split('±')[0].strip())
            s6 = float(scores[label][2].split('±')[0].strip())
            rev = 'reversible' if (s1 >= 1 and s6 < 1) else \
                  ('partially_reversible' if 0 < s6 < s1 else 'not_assessed')
            g = grade_tmdu(mean)
            add_meas(oligo_id=oid(key), species='mouse', system_model='ICR_mouse_CNS_invivo',
                     cns_region='whole_brain', delivery_method='intracerebroventricular',
                     dose_or_conc_value=blk['dose'], dose_or_conc_unit='TBD',
                     exposure_duration=tp, endpoint_domain='acute_neurotoxicity',
                     challenge_priority='medium', readout_category='behavioral',
                     readout_name='acute_neurotoxicity_score', readout_value=mean,
                     readout_unit='score_0_to_11',
                     effect_direction='increase' if mean > 0 else 'no_change',
                     effect_vs_control='%s_vs_0_PBS' % raw.replace(' ', ''),
                     neurotox_grade=g, reversibility=rev, source_id='P7',
                     source_ref='US11851654B2',
                     source_table='Table %d "Acute tolerability score" (Example %d), row "%s", %s column'
                                  % ({1: 2, 2: 6, 4: 10, 5: 14}[blk['ex']], blk['ex'], label, tp),
                     notes=('grade_provisional;7-week-old female ICR mice, single injection into '
                            'the left lateral ventricle; 11-item behavioural battery scored '
                            '0=normal / 1=abnormal per item, summed 0-11, PBS controls 0+/-0; '
                            'value is mean +/- SD (%s), n=4-7; mapping uses the same proportional '
                            'band edges as the 0-7 FOB scale: 0-<1=>0, 1-<5=>1, 5-<8=>2, >=8=>3; '
                            'DOSE printed as "%d umol/mouse" - reproduced as printed, and the '
                            'unit left TBD because the schema dose-unit enum has no molar-amount '
                            'unit (the figure is very likely a nmol/umol typo in the patent, '
                            'so it was NOT converted)' % (raw, blk['dose'])))
            rr = float(rates[label][k])
            add_meas(oligo_id=oid(key), species='mouse', system_model='ICR_mouse_CNS_invivo',
                     cns_region='whole_brain', delivery_method='intracerebroventricular',
                     dose_or_conc_value=blk['dose'], dose_or_conc_unit='TBD',
                     exposure_duration=tp, endpoint_domain='acute_neurotoxicity',
                     challenge_priority='medium', readout_category='behavioral',
                     readout_name='side_effect_event_rate', readout_value=rr,
                     readout_unit='pct_incidence',
                     effect_direction='increase' if rr > 0 else 'no_change',
                     effect_vs_control='%.0fpct_vs_0pct_PBS' % rr, neurotox_grade=g,
                     reversibility=rev, source_id='P7', source_ref='US11851654B2',
                     source_table='Table %d "Side-effect event rate (%%)" (Example %d), row "%s", %s column'
                                  % ({1: 3, 2: 7, 4: 11, 5: 15}[blk['ex']], blk['ex'], label, tp),
                     notes=('grade_provisional;percentage of mice showing an abnormality in any '
                            'one of the 11 behavioural items at this timepoint (PBS = 0%%); this '
                            'is the incidence expression of the SAME observation graded in the '
                            'paired acute_neurotoxicity_score row, so it carries that row\'s grade'))
        dn = deaths[label]
        ndead = int(dn.split('/')[0])
        add_meas(oligo_id=oid(key), species='mouse', system_model='ICR_mouse_CNS_invivo',
                 cns_region='whole_brain', delivery_method='intracerebroventricular',
                 dose_or_conc_value=blk['dose'], dose_or_conc_unit='TBD',
                 exposure_duration='24h', endpoint_domain='acute_neurotoxicity',
                 challenge_priority='medium', readout_category='clinical_neuro_outcome',
                 readout_name='mortality', readout_value=dn, readout_unit='n_of_N',
                 effect_direction='increase' if ndead > 0 else 'no_change',
                 effect_vs_control='%s_vs_%s_PBS' % (dn, deaths['PBS']),
                 neurotox_grade=3 if ndead > 0 else 0, reversibility='irreversible' if ndead else 'not_assessed',
                 source_id='P7', source_ref='US11851654B2',
                 source_table='Table %d "Number of deaths/number of doses" (Example %d), row "%s"'
                              % ({1: 4, 2: 8, 4: 12, 5: 16}[blk['ex']], blk['ex'], label),
                 notes=('grade_provisional;number of mice that died within one day of the ICV '
                        'dose over the number dosed; concurrent PBS control was %s; any '
                        'treatment-emergent death after CNS dosing is graded 3 per the rubric '
                        '("moribundity/death"), 0/N is graded 0' % deaths['PBS']))

# ---------------------------------------------------------------- output ---
used = {m['oligo_id'] for m in MEAS}
dropped = [k for k in OLIGOS if OLIGOS[k]['oligo_id'] not in used]
for k in dropped: del OLIGOS[k]
print('dropped %d oligo(s) with no measurement' % len(dropped))

OUT = {
    'lane': 'patents',
    'oligos': [OLIGOS[k] for k in OLIGOS],
    'measurements': MEAS,
    'extraction_notes': open('/home/user/oligos/notes/cns/work/extraction_notes.txt').read().strip(),
}
path = '/home/user/oligos/notes/cns/extractions/patents.json'
with open(path, 'w') as f:
    json.dump(OUT, f, indent=1)
print('oligos', len(OUT['oligos']), 'measurements', len(OUT['measurements']))
seqfilled = sum(1 for o in OUT['oligos'] if o['sequence_5to3'] != 'TBD')
print('sequences filled', seqfilled, '/', len(OUT['oligos']))
print('grades', collections.Counter(m['neurotox_grade'] for m in MEAS))
print('priority', collections.Counter(m['challenge_priority'] for m in MEAS))
print('domain', collections.Counter(m['endpoint_domain'] for m in MEAS))
print('species', collections.Counter(m['species'] for m in MEAS))
