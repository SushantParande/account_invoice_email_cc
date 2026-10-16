# Invoice Email CC — Odoo 17 Community

Adds an optional per-send **CC** field to the standard invoice **Send & Print** dialog.

## Install

1. Back up the `buildleads_odoo` database and take a VPS snapshot/backup.
2. Copy this module folder into `/home/administrator/odoo-projects/buildleads/addons/`.
3. Ensure the service user can read the files, for example:
   `sudo chown -R administrator:administrator /home/administrator/odoo-projects/buildleads/addons/account_invoice_email_cc`
4. Restart the Odoo service, then update the Apps list in developer mode.
5. Search for **Invoice Email CC** and install it.
6. Test with a draft/test invoice and two controlled email inboxes before production use.

## Notes

- CC is transient wizard data; it is not saved as a customer default.
- Accepts comma- or semicolon-separated addresses.
- Does not modify Odoo core files.
- This is a custom integration against Odoo 17's notification hooks. Test in a staging database first, particularly invoices with multiple recipients or followers, because Odoo may split notifications by language and recipient batch. Verify the outgoing `mail.mail` record and received message headers before production use.
