from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
import datetime
from datetime import date




class SubTaskInherit(models.Model):
    _name = "project.sub.task"

    sub_id = fields.Many2one('project.task', string="Sub Task")
    date = fields.Date(string="Date")
    employee = fields.Many2one('res.users', string="Employee", index=True)
    description = fields.Char(string="Description")
    duration = fields.Float(string="Duration")
    done = fields.Boolean(string="Done")

