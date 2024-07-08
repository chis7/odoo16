# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import fields, models, _, api


class CreateTrainingPlanWizard(models.TransientModel):
    _name = "create.training.plan.wizard"
    _description = "create training plan wizard"
    name = fields.Char(string="Ministry", required=True)
    province = fields.Char(string="Province", required=True)
    institution = fields.Char(string="Institution", required=True)
    yearOfPlan = fields.Char(string="Year", required=True)
    supervisor_id = fields.Many2one("hr.employee", string="Supervisor")
    reference = fields.Char(
        string="Reference",
        required=True, copy=False, readonly=True,
        default=lambda self: _('New'))
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
    create_training_plan_wizard_line_ids = fields.One2many('create.training.plan.wizard.lines',
                                                           'create_training_plan_wizard_id',
                                                           string="Training Plan Wizard Lines")

    def action_save_training_plan_as_draft(self):
        vals = {
            'name': self.name,
            'province': self.province,
            'institution': self.institution,
            'yearOfPlan': self.yearOfPlan,
            'state': 'draft'
        }
        training_plan_record = self.env['training.plan'].create(vals)
        record_id = training_plan_record.id
        lines_to_create = []
        for line in self.create_training_plan_wizard_line_ids:
            vals_lines = {
                'training_plan_id': record_id,
                'name': line.create_training_plan_wizard_line_ids.name,
                'employee_id': line.create_training_plan_wizard_line_ids.employee_id.id,
                'nrcNumber': line.create_training_plan_wizard_line_ids.nrcNumber,
                'pmecNumber': line.create_training_plan_wizard_line_ids.pmecNumber,
                'gender': line.create_training_plan_wizard_line_ids.gender,
                'position': line.create_training_plan_wizard_line_ids.position,
                'age': line.create_training_plan_wizard_line_ids.age,
                'job_description': line.create_training_plan_wizard_line_ids.job_description,
                'department': line.create_training_plan_wizard_line_ids.department,
                'priorityArea': line.create_training_plan_wizard_line_ids.priorityArea,
                'priorityRanking': line.create_training_plan_wizard_line_ids.priorityRanking,
                'candidate_level_of_training': line.create_training_plan_wizard_line_ids.candidate_level_of_training,
                'level_of_training_proposed': line.create_training_plan_wizard_line_ids.level_of_training_proposed,
                'location_of_programme_proposed': line.create_training_plan_wizard_line_ids.location_of_programme_proposed.id,
                'proposed_date_of_programme': line.create_training_plan_wizard_line_ids.proposed_date_of_programme,
                'sponsor': line.create_training_plan_wizard_line_ids.sponsor.id,
                'justification_of_training': line.create_training_plan_wizard_line_ids.justification_of_training,
                'estimated_cost_per_year': line.create_training_plan_wizard_line_ids.estimated_cost_per_year,

            }
            lines_to_create.append(vals_lines)
        if lines_to_create:
            self.env['training.plan.lines'].create(lines_to_create)


    def action_submit_training_plan_to_hrdc(self):

        self.write({'state': 'hrdc'})


    @api.model
    def create(self, vals):
        current_year_month = datetime.now().strftime('%Y%m')
        sequence_code = self.env['ir.sequence'].next_by_code('training.plan') or _('Invalid')
        vals['reference'] = f"{current_year_month}-{sequence_code}"
        res = super(CreateTrainingPlanWizard, self).create(vals)
        return res


class CreateTrainingPlanWizardLines(models.TransientModel):
    _name = "create.training.plan.wizard.lines"
    _description = "create training plan wizard lines"
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
    create_training_plan_wizard_id = fields.Many2one('create.training.plan.wizard', string="Training Plan",
                                                     required=True, store=True)
