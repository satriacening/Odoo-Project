from odoo import fields, api, models

from datetime import date
import datetime


class Project(models.Model):
    _inherit = 'project.project'

    progress = fields.Float(string='Progress', compute='_compute_progress')
    duration = fields.Char(string="Duration", compute='_compute_duration')

    @api.depends('date_start', 'date', 'duration')
    def _compute_duration(self):
        for i in self:
            i.duration = i.date - i.date_start

    def _compute_progress(self):
        # (total progress task in project) : (total task)
        for sheet in self:
            if sheet.env['project.task'].search_count([('project_id', '=', sheet.id)]) == 0:
                sheet.progress = 0
            else:
                sheet.progress = (sum(sheet.tasks.mapped('progress'))) / (sheet.env['project.task'].search_count([('project_id', '=', sheet.id)]))
