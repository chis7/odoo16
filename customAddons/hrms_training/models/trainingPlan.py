# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class TrainingPlan(models.Model):
    _name = "training.plan"
    _inherit = ["mail.thread"]
    _description = "training plan"
    name = fields.Char(string="Ministry", required=True)
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
    hrdcComment = fields.Text(string="HRDC Comment")
    psComment = fields.Text(string="PS Comment")
    psmdComment = fields.Text(string="PSMD Comment")

    def action_save_training_plan_as_draft(self):
        self.write({'state': 'draft'})

    def action_submit_training_plan_to_hrdc(self):
        self.write({'state': 'hrdc'})

    def action_hrdc_approve_training_plan(self):
        self.write({'state': 'ps'})

    def action_hrdc_send_back_training_plan(self):
        self.write({'state': 'draft'})

    def action_ps_approve_training_plan(self):
        self.write({'state': 'psmd'})

    def action_ps_send_back_training_plan(self):
        self.write({'state': 'hrdc'})

    def action_psmd_approve_training_plan(self):
        self.write({'state': 'approved'})

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
    employee_id = fields.Many2one('hr.employee', string="Candidate Name", required=True, store=True)
    priorityRanking = fields.Integer(string="Priority Ranking", required=True, store=True)
    priorityArea = fields.Char(string="Priority Area", required=True, store=True)
    department = fields.Char(string="Department", required=True, store=True)
    nrcNumber = fields.Char(string="NRC Number", required=True, store=True)
    pmecNumber = fields.Char(string="PMEC Number", required=True, store=True)
    gender = fields.Selection(
        selection=[
            ("male", "Male"),
            ("female", "Female"),
        ],
        default='female',
        string="Gender",
        required=True,
        store=True
    )
    position = fields.Char(string="Position", required=True, store=True)
    job_description = fields.Text(string="Job Description", required=True, store=True)
    age = fields.Integer(string="Age (years)", required=True, store=True)
    candidate_level_of_training = fields.Char(string="Candidate's Level of Training", required=True, store=True)
    name = fields.Char(string="Training Proposed", required=True, store=True)
    level_of_training_proposed = fields.Char(string="Level of Training Proposed", required=True, store=True)
    location_of_programme_proposed = fields.Many2one("res.country", "Location of Programme Proposed", required=True,
                                                     store=True)
    proposed_date_of_programme = fields.Date(string="Proposed Date of Programme", required=True, store=True)
    sponsor = fields.Many2one('hr.employee', string="Sponsor", required=True, store=True)
    justification_of_training = fields.Text(string="Justification of Training", required=True, store=True)
    estimated_cost_per_year = fields.Integer(string="Estimated Cost per Year", required=True, store=True)
    training_plan_id = fields.Many2one('training.plan', string="Training Plan", required=True, store=True)
