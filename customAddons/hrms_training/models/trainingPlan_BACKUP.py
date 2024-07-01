# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError


class TrainingPlan(models.Model):
    _name = "training.plan"
    _inherit = ["mail.thread"]
    _description = "training plan"
    name = fields.Char(string="Name", required=True)
    reference = fields.Char(
        string="Reference",
        required=True, copy=False, readonly=True,
        default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string="Employee ID", required=True)
    field_of_study = fields.Many2one('field.of.study', string="Field of Study", required=True)
    level_of_study = fields.Many2one('level.of.study', string="Level of Study", required=True)
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("hrdc", "HRDC"),
            ("ps", "PS"),
            ("psmd", "PSMD"),
            ("done", "Done"),
        ],
        default='draft',
        string="Status",
        required=True
    )

    def action_hrdc_approve_training_plan(self):
        self.write({'state': 'ps'})

    def action_hrdc_send_back_training_plan(self):
        self.write({'state': 'draft'})

    def action_ps_approve_training_plan(self):
        self.write({'state': 'psmd'})

    def action_ps_send_back_training_plan(self):
        self.write({'state': 'hrdc'})

    def action_psmd_approve_training_plan(self):
        self.write({'state': 'done'})

    def action_psmd_send_back_training_plan(self):
        self.write({'state': 'ps'})

    @api.model
    def create(self, vals):
        if vals.get('reference', _('Invalid')) == _('Invalid'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('training.plan') or _('Invalid')
        res = super(TrainingPlan, self).create(vals)
        return res
