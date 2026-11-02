# IMPERIA COLD WAR — Isolated Israel V2 native budget and debt integration.
"""Fresh-read, minimal marked patches. The root compiler writes returned files."""
from pathlib import Path
import base64
import hashlib
import re
from runtime_bilateral import PARTNERS

ROOT = Path(__file__).resolve().parents[2]
HEADER = '# IMPERIA COLD WAR — Israel V2 native budget and protected bilateral principal integration.\n'
PREFIX = '# IMPERIA COLD WAR — Israel V2 money '
PATHS = ('common/scripted_effects/00_money_system.txt',
         'common/scripted_effects/00_budget_effects.txt',
         'common/scripted_effects/00_economic_system_utilities.txt',
         'common/on_actions/MD_on_actions.txt')


def region(key, body, restore=None):
    receipt=('# ISR2_NATIVE_RESTORE '+base64.b64encode(restore.encode('utf-8')).decode('ascii')+'\n') if restore is not None else ''
    return PREFIX+'['+key+'] BEGIN\n'+receipt+body.strip()+'\n'+PREFIX+'['+key+'] END\n'


def clean(text):
    if text.startswith(HEADER): text=text[len(HEADER):]
    def restore(match):
        receipt=re.search(r'^# ISR2_NATIVE_RESTORE ([A-Za-z0-9+/=]+)$',match[0],re.M)
        return base64.b64decode(receipt[1]).decode('utf-8') if receipt else ''
    return re.sub(r'(?ms)^'+re.escape(PREFIX)+r'\[([^\]]+)\] BEGIN\n.*?^'+re.escape(PREFIX)+r'\[\1\] END\n?', restore, text)


def bounds(text,name):
    match=re.search(r'^'+re.escape(name)+r'\s*=\s*\{',text,re.M)
    if not match: raise ValueError('Native provider missing: '+name)
    opening=text.index('{',match.start()); depth=0; quoted=False; comment=False; escaped=False
    for i in range(opening,len(text)):
        char=text[i]
        if comment:
            if char=='\n': comment=False
            continue
        if quoted:
            if char=='"' and not escaped: quoted=False
            escaped=char=='\\' and not escaped
            continue
        if char=='#': comment=True
        elif char=='"': quoted=True
        elif char=='{': depth+=1
        elif char=='}':
            depth-=1
            if depth==0: return opening+1,i
    raise ValueError('Unclosed native provider: '+name)


def transform(text,name,fn):
    start,end=bounds(text,name)
    return text[:start]+fn(text[start:end])+text[end:]


def before_once(body,needle,section):
    if body.count(needle)!=1: raise ValueError(('Native integration anchor changed',needle,body.count(needle)))
    return body.replace(needle,section+needle,1)


def streams(kind):
    output='ISR2_money_weekly_'+kind
    destination='additional_income_rate' if kind=='income' else 'additional_expenses_rate'
    return '\n'.join([
        'if = { limit = { ISR2_is_scenario = yes } ISR2_refresh = yes }',
        'set_variable = { '+output+' = 0 }',
        *['if = { limit = { ISR2_is_scenario = yes has_variable = ISR2_'+part+'_weekly_'+kind+' } add_to_variable = { '+output+' = ISR2_'+part+'_weekly_'+kind+' } }'
          for part in ('core','domestic','territories')],
        'if = { limit = { IMP_is_1970_scenario = yes has_variable = ISR2_bilateral_weekly_'+kind+' OR = { ISR2_is_scenario = yes '+
            ' '.join('tag = '+tag for tag in PARTNERS)+' } } add_to_variable = { '+output+' = ISR2_bilateral_weekly_'+kind+' } }',
        'add_to_variable = { '+destination+' = '+output+' }'])


def helpers():
    return '''
ISR2_money_has_protected_loan = {
 ISR2_is_scenario = yes
 has_variable = ISR2_bilateral_loan_outstanding
 check_variable = { ISR2_bilateral_loan_outstanding > 0 }
}
'''


def integrate():
    """Return complete current shared files with isolated, removable sections.

    Human automatic repayment is a direct on_action consumer, so its two-line
    debit must be clamped there as well as in the ordinary utility providers.
    """
    original={p:(ROOT/p).read_text(encoding='utf-8-sig') for p in PATHS}
    source={p:clean(text) for p,text in original.items()}
    money,budget,utility,onactions=(source[p] for p in PATHS)
    for name,kind in (('calculate_additional_income_rate','income'),('calculate_additional_expense_rate','expense')):
        money=transform(money,name,lambda body,kind=kind:body+region(kind+' streams',streams(kind)))
    # Floor restoration covers native write-offs without ever refunding cash.
    money=transform(money,'calculate_interest_rate',lambda body:body[:1]+region('principal floor before interest','ISR2_money_preserve_principal = yes')+body[1:]+region('exclude contracted interest','''
if = { limit = { ISR2_money_has_protected_loan = yes }
 set_temp_variable = { ISR2_money_interest_exclusion = { value = ISR2_bilateral_loan_outstanding multiply = 0.00019 multiply = interest_rate multiply = debt_fx_factor } }
 if = { limit = { check_variable = { ISR2_money_interest_exclusion > debt_rate } } set_temp_variable = { ISR2_money_interest_exclusion = debt_rate } }
 subtract_from_variable = { debt_rate = ISR2_money_interest_exclusion }
 clamp_variable = { var = debt_rate min = 0 }
}'''))
    money=transform(money,'restructure_debt_after_financial_collapse',lambda body:before_once(body,'\tingame_update_setup = yes',region('restructuring preserves principal','ISR2_money_preserve_principal = yes')))
    budget=transform(budget,'modify_debt_effect',lambda body:body[:1]+region('guard anonymous writeoff','''
if = { limit = { ISR2_money_has_protected_loan = yes NOT = { has_country_flag = ISR2_bilateral_authorized_principal } check_variable = { debt_change < 0 } }
 ISR2_money_quote_unprotected_debt = yes
 set_temp_variable = { ISR2_money_lowest_debt_change = { value = ISR2_money_unprotected_debt multiply = -1 } }
 if = { limit = { check_variable = { debt_change < ISR2_money_lowest_debt_change } } set_temp_variable = { debt_change = ISR2_money_lowest_debt_change } }
}''')+body[1:])
    # The protected borrower must use the existing gradual AI branch; the
    # original full-clear branch remains byte-for-byte for every other nation.
    utility=transform(utility,'ai_repay_debt',lambda body:before_once(body,'\t\t\t\tcheck_variable = { treasury > debt }',region('AI full clear guard','NOT = { ISR2_money_has_protected_loan = yes }')))
    def ai_patch(body):
        body=before_once(body,'\t\t\t\tif = {\n\t\t\t\t\tlimit = { check_variable = { var = ai_debt_payment',region('AI gradual payment clamp','''
set_temp_variable = { ISR2_money_repayment_request = ai_debt_payment }
ISR2_money_clamp_repayment = yes
set_temp_variable = { ai_debt_payment = ISR2_money_repayment_allowed }
if = { limit = { ISR2_money_has_protected_loan = yes check_variable = { ai_debt_payment_min > ISR2_money_unprotected_debt } }
 set_temp_variable = { ai_debt_payment_min = ISR2_money_unprotected_debt }
}
'''))
        # Protect tiny outstanding principal from the native zero-remainder cleanup.
        original='\t\t\t\t\tif = { limit = { check_variable = { debt < 0.001 } }\n'
        replacement='if = { limit = { check_variable = { debt < 0.001 } NOT = { ISR2_money_has_protected_loan = yes } }'
        if body.count(original)!=1: raise ValueError('Native AI cleanup anchor changed')
        body=body.replace(original,region('AI zero cleanup guard',replacement,original),1)
        return body+region('AI debt recalculation','if = { limit = { ISR2_money_has_protected_loan = yes } calculate_interest_rate = yes }')
    utility=transform(utility,'ai_repay_debt',ai_patch)
    utility=transform(utility,'repay_manual_debt_effect',lambda body:before_once(body,'\tif = {\n\t\tlimit = { check_variable = { repay_temp > 0 } }',region('manual payment clamp','''
set_temp_variable = { ISR2_money_repayment_request = repay_temp }
ISR2_money_clamp_repayment = yes
set_temp_variable = { repay_temp = ISR2_money_repayment_allowed }
''')))
    # These new helpers are effects. The protected-loan predicate is inlined
    # through one scripted trigger emitted alongside the shared patch files.
    utility+=region('native helper providers','''
ISR2_money_quote_unprotected_debt = {
 set_temp_variable = { ISR2_money_unprotected_debt = debt }
 if = { limit = { ISR2_money_has_protected_loan = yes }
  subtract_from_temp_variable = { ISR2_money_unprotected_debt = ISR2_bilateral_loan_outstanding }
 }
 clamp_temp_variable = { var = ISR2_money_unprotected_debt min = 0 }
}
ISR2_money_clamp_repayment = {
 ISR2_money_quote_unprotected_debt = yes
 set_temp_variable = { ISR2_money_repayment_allowed = ISR2_money_repayment_request }
 clamp_temp_variable = { var = ISR2_money_repayment_allowed min = 0 }
 if = { limit = { check_variable = { ISR2_money_repayment_allowed > ISR2_money_unprotected_debt } }
  set_temp_variable = { ISR2_money_repayment_allowed = ISR2_money_unprotected_debt }
 }
}
ISR2_money_preserve_principal = {
 if = { limit = { ISR2_money_has_protected_loan = yes NOT = { has_country_flag = ISR2_bilateral_authorized_principal } check_variable = { debt < ISR2_bilateral_loan_outstanding } }
  set_variable = { debt = ISR2_bilateral_loan_outstanding }
 }
}
''')
    # The human automatic-payment code lives outside the utility providers.
    onactions=before_once(onactions,'\t\t\t\t\tsubtract_from_variable = { debt = treasury_rate_debt_payment }',region('automatic weekly payment clamp','''
set_temp_variable = { ISR2_money_repayment_request = treasury_rate_debt_payment }
ISR2_money_clamp_repayment = yes
set_temp_variable = { treasury_rate_debt_payment = ISR2_money_repayment_allowed }
'''))
    original_cleanup='\t\t\t\t\t\tlimit = { check_variable = { debt < 0.001 } }\n'
    replacement='limit = { check_variable = { debt < 0.001 } NOT = { ISR2_money_has_protected_loan = yes } }'
    if onactions.count(original_cleanup)!=1: raise ValueError('Native automatic cleanup anchor changed')
    onactions=onactions.replace(original_cleanup,region('automatic zero cleanup guard',replacement,original_cleanup),1)
    files=dict(zip(PATHS,(money,budget,utility,onactions)))
    files={p:HEADER+text for p,text in files.items()}
    files['common/scripted_triggers/ISR2_money_triggers.txt']='# IMPERIA COLD WAR — Israel V2 protected bilateral loan predicate.\n'+helpers()
    return dict(files=files,source_sha256={p:hashlib.sha256(t.encode('utf-8')).hexdigest() for p,t in original.items()})
