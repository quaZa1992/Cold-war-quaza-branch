# IMPERIA COLD WAR — Bounded national news archive.
"""Only disposable bulletin pointers expire; mission receipts remain permanent."""
REGULAR_DAYS = 180
MAJOR_DAYS = 365
MAJOR_STAGES = (8, 11)


def stamp(c, n, stage):
    sv, av, var = (c[k] for k in ['sv', 'av', 'var'])
    return (sv(var(n, 'last_report'), stage)
            + sv(var(n, 'report_expires'), 'global.num_days')
            + av(var(n, 'report_expires'), MAJOR_DAYS if stage in MAJOR_STAGES else REGULAR_DAYS)
            + sv('cw_sr_news_next_cleanup', 'global.num_days'))


def build(c):
    sv, av, cv, block_if, effect, var = (c[k] for k in ['sv', 'av', 'cv', 'block_if', 'effect', 'var'])
    # The next scan runs in at most seven days, or on the earliest expiry.
    # The ordinary daily refresh otherwise performs only the due-date check.
    body = sv('cw_sr_news_count', 0) + sv('cw_sr_news_next_cleanup', 'global.num_days') + av('cw_sr_news_next_cleanup', 7)
    for n, _ in enumerate(c['PROGRAMMES'], 1):
        report, expires = var(n, 'last_report'), var(n, 'report_expires')
        major = 'OR = { ' + ' '.join(cv(report, '=', stage) for stage in MAJOR_STAGES) + ' }'
        # Existing saves have no timestamp. Give their current reports one
        # bounded retention period, once; rereading never renews this date.
        migrate = sv(expires, 'global.num_days') + block_if(major, av(expires, MAJOR_DAYS), av(expires, REGULAR_DAYS))
        keep = av('cw_sr_news_count', 1) + block_if(cv(expires, '<', 'cw_sr_news_next_cleanup'), sv('cw_sr_news_next_cleanup', expires))
        live = block_if(cv(expires, '=', 0), migrate)
        live += block_if(cv(expires, '<=', 'global.num_days'), f'clear_variable = {report}\nclear_variable = {expires}\n', keep)
        body += block_if(cv(report, '>', 0), live, block_if(cv(expires, '>', 0), f'clear_variable = {expires}\n'))
    body += 'set_country_flag = cw_sr_news_retention_initialized\n'
    due = 'OR = { NOT = { has_country_flag = cw_sr_news_retention_initialized } ' + cv('global.num_days', '>=', 'cw_sr_news_next_cleanup') + ' }'
    c['write']('common/scripted_effects/COLDWAR_space_race_news.txt', effect('cw_sr_news_cleanup', block_if(c['guard']() + ' ' + due, body)))
