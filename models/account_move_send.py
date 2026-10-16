import re

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import email_normalize


class AccountMoveSend(models.TransientModel):
    _inherit = "account.move.send"

    mail_cc = fields.Char(
        string="CC",
        help="Optional CC email addresses, separated by commas or semicolons. "
             "These addresses are used only for this send operation.",
    )

    @api.constrains("mail_cc")
    def _check_mail_cc(self):
        for wizard in self:
            wizard._validate_mail_cc(wizard.mail_cc)

    @api.model
    def _validate_mail_cc(self, value):
        if not value or not value.strip():
            return
        addresses = [part.strip() for part in re.split(r"[,;\n]+", value) if part.strip()]
        if not addresses:
            return
        invalid = [address for address in addresses if not email_normalize(address)]
        if invalid:
            raise ValidationError(_("Invalid CC email address(es): %s", ", ".join(invalid)))

    def _get_mail_move_values(self, move, wizard=None):
        values = super()._get_mail_move_values(move, wizard=wizard)
        values["mail_cc"] = (wizard.mail_cc or "").strip() if wizard else ""
        self._validate_mail_cc(values["mail_cc"])
        return values

    def _get_mail_params(self, move, move_data):
        values = super()._get_mail_params(move, move_data)
        values["email_cc"] = (move_data.get("mail_cc") or "").strip()
        return values

    def _send_mail(self, move, mail_template, **kwargs):
        # Remove the custom parameter before calling core code. It is passed via
        # context to the notification-mail hook for this invoice message only.
        cc = (kwargs.pop("email_cc", "") or "").strip()
        if cc:
            self._validate_mail_cc(cc)
            move = move.with_context(invoice_send_email_cc=cc)
        return super()._send_mail(move, mail_template, **kwargs)
