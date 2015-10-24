# -*- coding: utf-8 -*-
import openerp
UID = openerp.SUPERUSER_ID
modules = ['l10n_syscohada', 'auth_crypt', 'crm', 'stock', 'purchase', 'sale', 'account_voucher',
           'account_accountant', 'hr', 'hr_payroll', 'hr_payroll_account']


def install_accounting(session, logger):
    """ Install accounting on a new Odoo base.

    This function must not be executed many time but can be. The action is totally like
    a men would made on webclient.
    """
    acc_set = session.registry('account.config.settings')
    chart_template = session.registry('account.chart.template')
    # TODO: use odoo config file to have options configurable with the buildout
    chart_syscohada = chart_template.search(
        session.cr, UID, [('name', '=', u'SYSCOHADA - Plan de compte')])[0]
    wiz_field = acc_set.default_get(session.cr, UID, [])
    wiz_field.update(dict(chart_template_id=chart_syscohada))
    onchange_value = acc_set.onchange_chart_template_id(session.cr, UID, [], chart_syscohada)
    wiz_field.update(onchange_value['value'])
    wiz_field.update(dict(date_start="2015-01-01", date_stop="2015-12-31", period="month"))
    wiz_id = acc_set.create(session.cr, UID, wiz_field)
    acc_set.execute(session.cr, UID, [wiz_id])
    logger.info("Accounting installed (l10n_syscohada)")


def uninstall_im_module(session, logger):
    m = session.registry('ir.module.module')
    m_ids = m.search(session.cr, session.uid, [('name', 'in', ('im_chat', 'im_odoo_support'))])
    m.module_uninstall(session.cr, session.uid, m_ids)
    logger.info("Remove im modules:")


def run(session, logger):
    """Update all modules."""
    if session.is_initialization:
        session.install_modules(modules)
        uninstall_im_module(session, logger)
        install_accounting(session, logger)
        logger.info("Fresh database with accounting! Installing modules: %r", modules)
        return
    logger.info("Default upgrade procedure : updating all modules.")
    session.update_modules(['hotelsahel'])
