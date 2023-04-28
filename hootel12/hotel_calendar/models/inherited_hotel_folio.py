# Copyright 2018-2019 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, api, _


class HotelFolio(models.Model):
    _inherit = 'hotel.folio'

    @api.multi
    def write(self, vals):
        ret = super(HotelFolio, self).write(vals)
        fields_to_check = ('room_lines', 'service_lines', 'pending_amount')
        fields_checked = [elm for elm in fields_to_check if elm in vals]
        if any(fields_checked):
            for record in self:
                record.room_lines.send_bus_notification('write', 'noshow')
        return ret

    @api.multi
    def unlink(self):
        for record in self:
            record.room_lines.send_bus_notification('unlink',
                                   'warn',
                                   _("Folio Deleted"))
        return super(HotelFolio, self).unlink()

    @api.multi
    def compute_amount(self):
        ret = super(HotelFolio, self).compute_amount()
        with self.env.norecompute():
            for record in self:
                record.room_lines.send_bus_notification('write', 'noshow')
        return ret
