from odoo import fields, api, models


class Project(models.Model):
    _inherit = 'project.project'

    progress = fields.Float(string='Progress')
    duration = fields.Char(string="Duration", compute='_compute_duration')

    @api.depends('date_start', 'date', 'duration')
    def _compute_duration(self):
        for i in self:
            i.duration = i.date - i.date_start
            print(i.duration, ' ini dia')

    # @api.depends('date_deadline', 'duration')
    # def _compute_duration(self):
    #     if self.start_date and self.date_deadline:
    #         self.duration = self.date_deadline - self.start_date



