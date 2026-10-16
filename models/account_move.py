from odoo import models
from odoo.tools import email_normalize


class AccountMove(models.Model):
    _inherit = "account.move"

    def _notify_by_email_get_final_mail_values(self, recipient_ids, mail_values, additional_values=None):
        values = super()._notify_by_email_get_final_mail_values(
            recipient_ids, mail_values, additional_values=additional_values
        )
        cc = (self.env.context.get("invoice_send_email_cc") or "").strip()
        if not cc:
            return values

        # In this invoice-send context, use a normal To header plus a real Cc
        # header. Odoo's mail.mail parser treats email_cc without email_to as a
        # separate CC-only message, so convert this recipient chunk to explicit
        # To addresses and clear recipient_ids for the outgoing mail object.
        partners = self.env["res.partner"].browse(recipient_ids).exists()
        to_addresses = []
        seen = set()
        for partner in partners:
            normalized = email_normalize(partner.email)
            if normalized and normalized not in seen:
                seen.add(normalized)
                to_addresses.append(partner.email.strip())

        if to_addresses:
            values.update({
                "email_to": ", ".join(to_addresses),
                "email_cc": cc,
                "recipient_ids": [],
            })
        return values
