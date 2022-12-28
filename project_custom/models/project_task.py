from odoo import api, fields, models, _
import datetime
from odoo.exceptions import UserError, ValidationError, Warning
from datetime import datetime, date


class Task(models.Model):
    _inherit = 'project.task'

    @api.depends('check_user')
    def _compute_check(self):
        user_id = self.env.user
        if user_id.has_group('project.group_project_manager'):
            self.check_user = True
        else:
            self.check_user = False
            if self.create_uid == self.env.user:
                self.write({'user_ids': [(4, self.env.user.id)]})

    def create(self, vals_list):
        if not self.check_user:
            self.write({'user_ids': [(4, self.env.user.id)]})
        return super(Task, self).create(vals_list)

    start_date = fields.Date(string="Start Date")
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
        ('3', 'Urgent'),
    ], default='0', index=True, string="Priority", tracking=True)
    duration = fields.Char(string="Duration", compute='_compute_duration')
    planned_hours = fields.Float(string="Planned Hours")
    real_planned = fields.Float(string="Real Planned Hours", compute='_compute_real_planned')
    progress = fields.Float(string="Progress", compute='_compute_progress')
    sub_tasks = fields.One2many('project.sub.task', 'sub_id', string='Sub Tasks')
    reviewer = fields.Many2one('res.users', string="Reviewer")
    check_user = fields.Boolean(compute='_compute_check')

    def _compute_bridge(self):
        self.bridge = self.progress

    @api.depends('sub_tasks.duration')
    def _compute_real_planned(self):
        for sheet in self:
            sheet.real_planned = sum(sheet.sub_tasks.mapped('duration'))

    @api.depends('date_deadline', 'duration')
    def _compute_duration(self):
        if self.start_date and self.date_deadline:
            self.duration = self.date_deadline - self.start_date
        if self.duration:
            if self.duration.find(",") == -1:
                self.duration = "0"
            else:
                day = self.duration
                x = day.index(",")
                self.duration = day[0:x]

    def _compute_progress(self):
        # this is the finishedcode
        for i in self:
            query = """
            SELECT sum(duration) FROM project_sub_task where done = TRUE and sub_id = (%s)
            """ % i.id
            i.env.cr.execute(query)
            val = i.env.cr.fetchone()

            if val[0] != None:
                result = (val[0] / i.real_planned) * 100
                i.progress = result
            else:
                i.progress = 0

    @api.onchange('date_deadline')
    def _onchange_deadline(self):
        if self.date_deadline and not self.start_date:
            self.start_date = date.today()
            return {
                'warning': {
                    'title': _('Notice'),
                    'message': _('You have not specified "Start Date", "Start Date" will be filled with the current Date'),
                },
            }

    # ===== uncomment this code if you activate this feature
    # ===== the feature gives a popup warning when user doesn't have access
    # @api.onchange('stage_id')
    # def _onchange_deadline(self):
    #     for rec in self:
    #         if rec.stage_id:
    #             if not rec.check_user:
    #                 raise UserError('you do not have access to change the stage')


