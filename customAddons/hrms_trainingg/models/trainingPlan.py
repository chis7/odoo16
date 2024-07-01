# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError


class TrainingPlan(models.Model):
    _name = "training.plan"
    _inherit = ["mail.thread"]
    _description = "training plan"
    ministry = fields.Char(string="Ministry", required=True)
    province = fields.Char(string="Province", required=True)
    institution = fields.Char(string="Institution", required=True)
    yearOfPlan = fields.Char(string="Year", required=True)
    reference = fields.Char(
        string="Reference",
        required=True, copy=False, readonly=True,
        default=lambda self: _('New'))

    training_plan_line_ids = fields.One2many('training.plan.lines', 'training_plan_id', string="Training Plan Lines")
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("hrdc", "HRDC"),
            ("ps", "PS"),
            ("psmd", "PSMD"),
            ("approved", "Approved"),
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

class TrainingPlanLines(models.Model):
    _name = "training.plan.lines"
    _description = "training plan lines"
    _rec_name = "candidateName"
    priorityRanking = fields.Integer(string="Priority Ranking", required=True)
    priorityArea = fields.Char(string="Priority Area", required=True)
    department = fields.Char(string="Department", required=True)
    candidateName = fields.Many2one('hr.employee', string="Candidate Name", required=True)
    nrcNumber = fields.Char(string="NRC Number", required=True)
    pmecNumber = fields.Char(string="PMEC Number", required=True)
    gender = fields.Selection(
        selection=[
            ("male", "Male"),
            ("female", "Female"),
        ],
        default='female',
        string="Gender",
        required=True
    )
    position = fields.Char(string="Position", required=True)
    job_description = fields.Text(string="Job Description", required=True)
    age = fields.Integer(string="Age (years)", required=True)
    candidate_level_of_training = fields.Char(string="Candidate's Level of Training", required=True)
    training_proposed = fields.Char(string="Training Proposed", required=True)
    level_of_training_proposed = fields.Char(string="Level of Training Proposed", required=True)
    location_of_programme_proposed = fields.Char(string="Location of Programme Proposed", required=True)
    proposed_date_of_programme = fields.Date(string="Proposed Date of Programme", required=True)
    sponsor = fields.Many2one('hr.employee', string="Sponsor", required=True)
    justification_of_training = fields.Text(string="Justification of Training", required=True)
    estimated_cost_per_year = fields.Integer(string="Estimated Cost per Year", required=True)

    training_plan_id = fields.Many2one('training.plan', string="Training Plan", required=True)

